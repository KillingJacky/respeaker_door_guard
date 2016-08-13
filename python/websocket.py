import threading
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class SimpleServerProc(WebSocket):

    def handleMessage(self):
        # echo message back to client
        self.sendMessage(self.data)

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'

class WebSocketServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = False
        self.server = SimpleWebSocketServer('', 20168, SimpleServerProc)

    def run(self):
        while not self.stop:
            self.server.loop_once()

    def terminate(self):
        self.stop = True
