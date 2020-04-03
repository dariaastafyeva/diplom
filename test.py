from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.topo import SingleSwitchTopo

from mininet.node import Host
from functools import partial

from flask import Flask
app = Flask(__name__)


# class SingleSwitchTopo(Topo):
#     "Single switch connected to n hosts."
#     def build(self, n=2):
#         switch = self.addSwitch('s1')
#         # Python's range(N) generates 0..N-1
#         for h in range(n):
#             host = self.addHost('h%s' % (h + 1))
#             self.addLink(host, switch)
#
#
# def simple_test():
#     # "Create and test a simple network"
#     topo = SingleSwitchTopo(n=2)
#     net = Mininet(topo)
#     net.start()
#     dumping = "Dumping host connections"
#     dumpNodeConnections(net.hosts)
#     print('********************')
#     print("Testing network connectivity")
#     net.pingAll()
#     # net.stop()
#     return dumping
#
#
# if __name__ == '__main__':
#     # Tell mininet to print useful information
#     setLogLevel('info')
#     simple_test()

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        leftSwitch = self.addSwitch( 's3' )
        rightSwitch = self.addSwitch( 's4' )

        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )






@app.route('/')
def hello_world():
    b = "string"
    topos = MyTopo()
    c = "++++++++++"
    return topos.g.node


@app.route('/create')
def create():
    return "Here'll be topos!"