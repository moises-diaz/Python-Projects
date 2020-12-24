#######################################################################
##                                                                   ##
##                     Practice                                      ##
##               COMPUTER NETWORKING                                 ##
##                                                                   ##
## PROGRAMMER: Moises Diaz.                                          ##
##                                                                   ##                      
##                                                                   ##
#######################################################################


#######################################################################
##                          DESCRIPTION                              ##
#######################################################################

"""\

This project is based on the execution of a server that waits
response from a max of 2 clients. The behavior of
a chat. In its execution, the server will be the slave while with which
clients will be the masters, that is, the server will be in "waiting"
that customers "talk" to you. The server will not be able to respond to a
client if he did not speak to him first. Of having many messages,
the server will respond according to the order of the request, that is, if the
client 1 and 2 write, the server will first serve client 1
and then to 2 (tail).

The server will be running for life. Customers could get out
sending the message "exit" and they can reconnect if he does not
has shut down the server.


Functions:

ini () - Asks the user for the host and port.

createSocket () - Returns a new socket following the scheme of the
                  TCP protocol

connect (host, port, s) - Its name says it all

attemptConnection (host, port, s) - If the port is not taken and
                                   the address provided is correct
                                   will connect to the server

send (s) - Manage the messages that will be sent to the server.
              This function calls to receive once the message is
              sent to customer

receive (s) - Thread that runs once and dies. Receive the messages
               from the server

receiveSpecial (s) - Receive a number. This will be the customer's number

"""


#######################################################################
##                            LIBRARIES                              ##
#######################################################################

from socket import *
import time
from _thread import *

#######################################################################
##                            FUNCTIONS                              ##
#######################################################################

def ini():
    host = input("Server Address: ")
    port = int(input("Port: "))
    return host, port

def crearSocket():                              ## Creating socket
    s = socket(AF_INET, SOCK_STREAM)
    return s

def conectarse (host, port, s):                 ## Setting connection
    s.connect((host, port))

def intentoConexion(host, port, s):             ## Trying connection

        while True:
            print("\nTrying to connect to:", host + ":" + str(port))
            try:
                conectarse(host, port, s)
                break
            except:
                print("There is no Server at:", host + ":" + str(port))
                print("Trying again in 5 Seconds\n")
                time.sleep(5)

def enviar(s):                                  ## Sending packet and input to the server

    while True:

        global exit

        try:
            msg = input("")
            msg = client +": " + msg
            if msg == client+": salir":
                exit = True
                msg = "The "+client+" Client is gone"
                s.send(msg.encode("UTF-8"))
                s.close
                break
            else:
                s.send(msg.encode("UTF-8"))
                start_new_thread(recibir,(s,))


        except:
            print("Something happend\n")
            print("Trying in 5 seg")
            time.sleep(5)

def recibir(s):                                 ## Recieving response
    while True:

        try:
          reply = s.recv(2048)
          print(reply.decode("UTF-8"))
          break


        except:
            print("Cant recieve response\n")
            print("Trying in 5 seg")
            time.sleep(5)

def recibirEspecial(s):
    global client
    client = s.recv(2048).decode("UTF-8")

#######################################################################
##                         GLOBAL VARIABLES                          ##
#######################################################################

exit=False      # If the client sends exit, exit is set to true and the
                 # the program ends
client = ""

#######################################################################
##                                MAIN                               ##
#######################################################################

def main():

    host, port = ini()
    s = crearSocket()
    intentoConexion(host,port,s)
    recibirEspecial(s)
    print("\nConnection To Server Established!\nThe server is:", host+":"+str(port)+"\n")
    print("Write your messages\n")
    start_new_thread(enviar,(s,))

    while exit!=True:   # this is necessary so that the threads do not die basically
        pass

    print("\nSorry something went wrong! You have lost connection to the server.:(")
    print("Closing the windows in 5 seg")
    time.sleep(10)

main()


