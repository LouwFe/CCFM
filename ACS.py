# -*- coding: utf-8 -*-

import socket
import json

class Device:
    TCP_PORT   = 9090
    is_open    = False
    request_id = 0

    def __init__(self, address):
        self.address  = address
        self.language = 0

    def __del__(self):
        self.close()

    def connect(self):
        """
            Initializes and connects the selected AMC device.

        Parameters
        ----------
        IP : str
            Address of the device to connect
        """
        if not self.is_open:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.settimeout(10)
            tcp.connect((self.address, self.TCP_PORT))
            self.tcp = tcp
            self.bufferedSocket = tcp.makefile("rwb", newline='\r\n')
            self.is_open = True
        return self.tcp

    def close(self):
        """
            Closes the connection to the device.

        Returns
        -------
        """
        if self.is_open:
            self.bufferedSocket.close()
            self.tcp.close()
            self.is_open = False

    def sendRequest(self, method, params=False):
        req = {
                "jsonrpc": "2.0",
                "method": method,
                "id": self.request_id
                }
        if params:
            req["params"] = params
        self.bufferedSocket.write(bytes(json.dumps(req), 'utf-8'))
        self.bufferedSocket.flush()
        self.request_id = self.request_id + 1

    def getResponse(self):
        response = self.bufferedSocket.readline().decode('utf-8')
        return json.loads(response)

    def request(self,method,params=False):
        """ Synchronous request.
        """
        if not self.is_open:
            raise Exception("not connected, use connect()");
        self.sendRequest(method, params)
        return self.getResponse()

    def handleError(self, response):
        if response.get('error', False):
            raise Exception("JSON error in %s" % response['error'])
        errNo = response['result'][0]
        if (errNo != 0 and errNo != 'null'):
            raise Exception(("Error! " + str(self.errorNumberToString(errNo))))
        return errNo
