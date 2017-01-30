#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    

    def connect(self, host, port):
        # use sockets! -me: ok
        #Ryan mentioned client lab for this part, so I used my previous lab for this

        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        print 'made a socket...'
        # AF_INET means we want an IPv4 socket
        # SOCK_STREAM means we want a TCP socket
        port = 80 #for now? Note to self, 8080 is not TCP
        clientSocket.connect( (host, port) ) #address, port
        print 'connected, returning connection...'
        return clientSocket

#---Section below are for processing the response I think -------------------------------------------------------------

    def get_code(self, data):
        print data
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

#---End of processing response section --------------------------------------------------------------------------------

    def plainifyURL(self, url):
        #remove all the junk after a slash, return the main url
        #may not work if no http:// - possible?
        plainURL = url.split('/')
        print 'plain url = ' + plainURL[2]
        return plainURL[2]


    def GET(self, url, args=None):
        #build the request to send to the url

        #host needs to be plainer! like www.tutorialspoint.com ONLY
        newURL = self.plainifyURL(url)

        #need the bit after the above
        toFetch = '/' #for now

        #Helpful information about building a request header from:
        #https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html

        header=''
        header += 'GET ' + toFetch + ' HTTP/1.1\r\n'
        header += 'Host: ' + newURL + '\r\n'
        header += 'Accept: ' + '*/*\r\n'
        #header += 'Accept-Language: en-us\r\n'
        #header += 'Accept-Encoding: *\r\n' #??
        #header += 'Connection: Keep-Alive\r\n'
        header +='\r\n'
        
        #do this when youre ready
        print 'connecting...'
        theClient = self.connect(newURL, 80) #hardcoded for now? Does it change?

        print 'Header is: ' + header
        theClient.sendall(header)
        print 'Sent header. Getting response...'
        response = self.recvall(theClient)
        print 'Got response'
        code = 500
        self.get_code(response)
        body = ""

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        #build the request to send to the url
        #POST, so use urllib.urlencode() here!

        #host needs to be plainer! like www.tutorialspoint.com ONLY

        newURL = self.plainifyURL(url)

        header=''
        header += 'POST ' + url + ' HTTP/1.1\r\n'
        header +='\r\n'
        
        #do this when youre ready
        print 'connecting...'
        theClient = self.connect(newURL, 80) #hardcoded for now? Does it change?

        print 'Connected. sending header'
        theClient.sendall(header)
        print 'Sent header. Getting response...'
        response = self.recvall(theClient)
        print 'Got response'

        code = 500
        body = ""

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )   
