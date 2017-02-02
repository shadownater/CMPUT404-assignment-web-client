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

#Here test this: http://127.0.0.1:27650/abcdef/gjkd/dsadas

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
        port = int(port)
        clientSocket.connect( (host, port) ) #address, port
        print 'connected, returning connection...'
        return clientSocket

#---Section below are for processing the response I think -------------------------------------------------------------

    def get_code(self, data):
        #print data
        myCode = data.split(' ')
        print myCode[1]
        return myCode[1]

    def get_headers(self,data):
        #where do I use this lol?
        myHead = data.split('\r\n\r\n')
        return myHead

    def get_body(self, data):
        print 'Data is:'
        print data
        myBody = data.split('\r\n\r\n')
        print 'Boy is: '
        print myBody[1]
        return myBody[1]

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
    def getPort(self, url):
        #gets the port number from the url if a : was found (besides http://)
        print 'Before: ' +url
        myPort = url.split(':')
        print myPort[1]
        finalP = myPort[1].split('/')
        print 'Final port value: ' + finalP[0]
        return finalP[0]

    def plainifyURL(self, url):
        #remove all the junk after a slash, return the main url
        #may not work if no http:// - possible?
        #looked in test, it can come in 3 parts
        #http://HOST:PORT/path
        
        plainURL = url.split('/')
        print 'plain url = ' + plainURL[0]

        if(':' in plainURL[0]):
            nonPURL = plainURL[0].split(':')
            print 'Had a port, but now its ' + nonPURL[0] 
            return nonPURL[0]

        return plainURL[0]
    
    def get_path(self, url):
        #gets the path part of the url - url in this case has no http:// on it
        
        myPath = url.split('/', 1)

        print 'myPath ='
        print myPath

        print 'Length = ', len(myPath)

        if( len(myPath) == 1):
            #no slashes detected
            myPath = '/' + myPath[0]
            return myPath
        else:
           #1 or more slashes detected
           myPath = '/' + myPath[1] 
           print 'path url = ' + myPath
           return myPath

    def get_ContentLength(self, content):
        #gets the POST's content length - already in format at this point -body?
        return str( len(content) )


    def GET(self, url, args=None):
        #build the request to send to the url

        port = 80
        #check if a port has been defined
        nonHttpUrl = url.split('http://')
        print nonHttpUrl[1]
        if(':' in nonHttpUrl[1]):
            port = self.getPort(nonHttpUrl[1])

        #host needs to be plainer! like www.tutorialspoint.com ONLY
        newURL = self.plainifyURL(nonHttpUrl[1])

        #need the bit after the above
        toFetch = self.get_path(nonHttpUrl[1])
        
        if(toFetch == ''):
            toFetch = '/'
        
        #Helpful information about building a request header from:
        #https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html

        header=''
        header += 'GET ' + toFetch + ' HTTP/1.1\r\n'
        header += 'Host: ' + newURL + '\r\n'
        header += 'Accept: ' + '*/*\r\n'
        header +='\r\n'
        
        #do this when youre ready
        print 'connecting with ' + newURL + ', ' + str(port) + '...' #adding str() may break ones with deinfed port?
        theClient = self.connect(newURL, port) 

        print 'Header is: ' + header
        theClient.sendall(header)

        response = self.recvall(theClient)

        code = self.get_code(response)
        code = int(code)
        body = self.get_body(response)
        
        return HTTPResponse(code, body)

#--POST-POST-POST-POST-POST-POST-POST-POST-POST-POST-POST-POST-POST-POST-POST-POST-POST-POST-POST-POST-POST-

    def POST(self, url, args=None):
        #build the request to send to the url
        #POST, so use urllib.urlencode() here!

        port = 80
        #check if a port has been defined
        nonHttpUrl = url.split('http://')
        print nonHttpUrl[1]
        if(':' in nonHttpUrl[1]):
            port = self.getPort(nonHttpUrl[1])
        
        #host needs to be plainer! like www.tutorialspoint.com ONLY

        newURL = self.plainifyURL(nonHttpUrl[1])

        #need the bit after the above
        toFetch = self.get_path(nonHttpUrl[1])
        if(toFetch == ''):
            toFetch = '/'

        #Credit Ryan here!
        myArgs = ''
        if(args != None):
            myArgs = urllib.urlencode(args)

        contentLength = self.get_ContentLength(myArgs)

        header=''
        header += 'POST ' + toFetch + ' HTTP/1.1\r\n'
        header += 'Host: ' + newURL + '\r\n'
        header+= 'Content-Type: ' + 'application/x-www-form-urlencoded;\r\n' 
        header += 'Content-Length: ' + contentLength + '\r\n'
        header += 'Accept: ' + '*/*\r\n'
        header +='\r\n'

        header += myArgs + '\r\n'
        
        #do this when youre ready
        print 'connecting with ' + newURL + ', ' + port + '...'
        theClient = self.connect(newURL, port) 

        print 'Header is: ' + header
        theClient.sendall(header)

        response = self.recvall(theClient)

        code = self.get_code(response)
        code = int(code)
        body = self.get_body(response)

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
