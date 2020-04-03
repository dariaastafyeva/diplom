from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.topo import SingleSwitchTopo

from mininet.node import Host
from functools import partial
from collections import namedtuple

from mininet.topo import Topo
from flask import Flask, request, render_template
app = Flask(__name__)

Host = namedtuple('Host', 'info')
hosts = []

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
    return render_template('start.html')


@app.route('/create')
def create():
    topos = MyTopo()
    hosts = topos.g.node
    return render_template('create.html', hosts=hosts)
