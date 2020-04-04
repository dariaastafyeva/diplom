from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.topo import SingleSwitchTopo

from mininet.node import OVSSwitch
from mininet.node import Host
from functools import partial
from collections import namedtuple
from mininet.topo import Topo
from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)

Host = namedtuple('Host', 'info')
hosts = []
switches = []

class MyTopo( Topo ):

    def __init__(self):

        # Initialize topology
        Topo.__init__(self)

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        leftSwitch = self.addSwitch( 's3' )
        rightSwitch = self.addSwitch( 's4' )

        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('start.html')


@app.route('/create', methods=['GET'])
def create():
    # topos = MyTopo()
    # hosts = topos.g.node
    return render_template('create.html', hosts=hosts, switches=switches)


@app.route('/add_host', methods=['POST'])
def add_host():
    num = len(hosts)
    string = 'h' + str(num)
    h = Host(string)
    hosts.append(h)
    return redirect(url_for('create'))


@app.route('/add_switch', methods=['POST'])
def add_switch():
    num = len(switches)
    string = 's' + str(num)
    s = OVSSwitch(string)
    switches.append(s)
    return redirect(url_for('create'))
