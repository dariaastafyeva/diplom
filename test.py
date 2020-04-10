import sys
from mininet.log import info, setLogLevel
from mininet.net import Mininet, VERSION
from mininet.util import netParse, ipAdd, quietRun, buildTopo, custom, customClass, dumpNodeConnections
from mininet.term import makeTerm, cleanUpScreens
from mininet.moduledeps import moduleDeps
from mininet.topolib import TreeTopo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import Link, TCLink, Intf
from mininet.node import CPULimitedHost, Node, Host, Controller, Switch, OVSSwitch, UserSwitch, RemoteController, NOX, OVSController
from mininet.topo import Topo, SingleSwitchTopo, LinearTopo, SingleSwitchReversedTopo
from flask import Flask, request, render_template, redirect, url_for
from collections import namedtuple
import os
from functools import partial
app = Flask(__name__)

Host = namedtuple('Host', 'info')
hosts = []
switches = []
controllers = []
links = []
ping = ''


class MyTopo(Topo):

    def __init__(self):

        # Initialize topology
        Topo.__init__(self)

        # Add hosts and switches
        leftHost = self.addHost('h1')
        rightHost = self.addHost( 'h2' )
        leftSwitch = self.addSwitch( 's3' )
        rightSwitch = self.addSwitch( 's4' )

        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )


class SimplePktSwitch(Topo):
    """Simple topology example."""

    def __init__(self, **opts):
        """Create custom topo."""

        # Initialize topology
        # It uses the constructor for the Topo cloass
        super(SimplePktSwitch, self).__init__(**opts)

        # Add hosts and switches
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        # Adding switches
        s1 = self.addSwitch('s1', dpid="0000000000000001")
        s2 = self.addSwitch('s2', dpid="0000000000000002")
        s3 = self.addSwitch('s3', dpid="0000000000000003")
        s4 = self.addSwitch('s4', dpid="0000000000000004")

        # Add links
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)

        self.addLink(s1, s2)
        self.addLink(s1, s3)
        self.addLink(s1, s4)


def run():
    c = RemoteController('c', '0.0.0.0', 6633)
    net = Mininet(topo=SimplePktSwitch(), host=CPULimitedHost, controller=None)
    net.addController(c)
    net.start()

    CLI(net)
    net.stop()


# if the script is run directly (sudo custom/optical.py):
if __name__ == '__main__':
    setLogLevel('info')
    run()


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('start.html')


@app.route('/create', methods=['GET'])
def create():
    # topos = MyTopo()
    # hosts = topos.g.node
    return render_template('create.html', hosts=hosts, switches=switches, controllers=controllers, links=links, ping=ping)


@app.route('/create_net', methods=['POST'])
def create_net():
    # c = RemoteController('c', '0.0.0.0', 6633)
    # net = Mininet(topo=SimplePktSwitch(), host=CPULimitedHost, controller=None)
    # net.addController(c)
    # net.start()
    #
    # CLI(net)
    # net.stop()
    print("*******************************************************************************************")
    os.system("python /usr/lib/python2.7/dist-packages/mininet/examples/test2.py")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(sys.argv[1])
    return redirect(url_for('create'))


@app.route('/add_host', methods=['POST'])
def add_host():
    num = len(hosts)
    string_h = 'h' + str(num)
    h = Host(string_h)
    # tmp = int(num) + 1
    # ip = '10.' + str(tmp) + '/8'
    # h.setIP(ip)
    hosts.append(h)
    return redirect(url_for('create'))


@app.route('/add_switch', methods=['POST'])
def add_switch():
    num = len(switches)
    string = 's' + str(num)
    s = Switch(string, inNamespace=False)
    switches.append(s)
    return redirect(url_for('create'))


@app.route('/add_controller', methods=['POST'])
def add_controller():
    num = len(controllers)
    string = 'c' + str(num)
    c = Controller(string, inNamespace=False)
    controllers.append(c)
    return redirect(url_for('create'))


@app.route('/add_link', methods=['POST'])
def add_link():
    Link(hosts[0], switches[0])
    Link(hosts[1], switches[0])
    tmp1 = int(hosts.index('h0')) + 1
    tmp2 = int(hosts.index('h1')) + 1
    ip1 = '10.' + str(tmp1) + '/8'
    ip2 = '10.' + str(tmp2) + '/8'
    hosts[0].setIP(ip1)
    hosts[1].setIP(ip2)
    controllers[0].start()
    switches[0].start(controllers[0])
    ping = hosts[0].cmd('ping -c1', hosts[1].IP())
    switches[0].stop()
    controllers[0].stop()
    return redirect(url_for('create'))


@app.route('/form_topology', methods=['POST'])
def form_topology():
    h, s = 1, 1
    amt_h = 4
    amt_s = 4
    str_file = """from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mininet.cli import CLI


class SimplePktSwitch(Topo):

    def __init__(self, **opts):
        # Initialize topology
        # It uses the constructor for the Topo cloass
        super(SimplePktSwitch, self).__init__(**opts)\n\n"""

    while h <= amt_h:
        str_file += "        h" + str(h) + " = self.addHost('h" + str(h) + "')\n"
        h += 1
    while s <= amt_s:
        str_file += "        s" + str(s) + " = self.addSwitch('s" + str(s) + "', dpid='000000000000000" + str(s) + "')\n"
        s += 1

    # handle = open("mycode.py", "w")
    # handle.write(str_file)
    # handle.close()

    print("*******************************************************************************************")
    os.system("python ~/home/roman/PycharmProjects/test/mycode.py")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    return redirect(url_for('create'))


@app.route('/add_topology', methods=['POST'])
def add_topology():
    h, s = 1, 1
    amt_h = int(request.form['input_host'])
    amt_s = int(request.form['input_switch'])
    str_file = """from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mininet.cli import CLI


class SimplePktSwitch(Topo):

    def __init__(self, **opts):
        # Initialize topology
        # It uses the constructor for the Topo cloass
        super(SimplePktSwitch, self).__init__(**opts)\n\n"""

    while h <= amt_h:
        str_file += "        h" + str(h) + " = self.addHost('h" + str(h) + "')\n"
        h += 1
    while s <= amt_s:
        str_file += "        s" + str(s) + " = self.addSwitch('s" + str(s) + "', dpid='000000000000000" + str(s) + "')\n"
        s += 1

    handle = open("mycode.py", "w")
    handle.write(str_file)
    handle.close()

    print("*******************************************************************************************")
    # os.system("python ~/home/roman/PycharmProjects/test/mycode.py")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    return redirect(url_for('create'))



