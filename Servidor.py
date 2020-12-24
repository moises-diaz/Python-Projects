#######################################################################
##                                                                   ##
##                    UNIVERSIDAD SIMON BOLIVAR                      ##
##                     REDES DE COMPUTADORAS                         ##
##                                                                   ##
## PROGRAMMER: Moises DIaz                                           ##
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


Features:

ini () - Asks the user for the host and port.

createSocket () - Returns a new socket following the scheme of the
                 TCP protocol

bindSocket (s, host, port) - Attempts to bind a socket to the parameters
                              host and port

connection (s) - Wait for the connection of external clients. Returns
                 the customer's address in a tuple

send (conn) - Send an encrypted message to the address of client 1

send2 (conn) - Send an encrypted message to the address of client 2

receive (conn) - Manages the messages received from the different clients.
                 Calls the send function once it receives messages

sendSpecial (conn) - The server assigns a number and sends it to the client
                        respective

"""

#######################################################################
##                            LIBRARIES                              ##
#######################################################################

from socket import *
from _thread import *
import time
import sys

#######################################################################
##                            FUNCTIONS                              ##
#######################################################################

def ini():
    host = input("Host: ")
    port = int(input("Port: "))
    return host, port

def crearSocket():
    s = socket(AF_INET, SOCK_STREAM)
    return s

def ligarSocket(s, host, port):
    while True:
        try:
            s.bind((host, port))
            break

        except error as e:
            print("ERROR:", e)

def conexiones(s):

    conn, addr = s.accept()
    print("\nEstablished Connection.\nThe client is:", addr[0] + ":" + str(addr[1])+"\n")
    return conn, addr

def enviar(conn):

        msg = input("")
        msg = "Server: " + msg
        try:

            conn.send(msg.encode("UTF-8"))

        except:
            print("\nSomething happened")
            print("Try in 5 seg\n")
            time.sleep(5)

def enviar2(conn):

        msg = input("")
        msg = "Servidor: " + msg
        try:

            conn.send(msg.encode("UTF-8"))

        except:
            print("\nSomething happened")
            print("Try in 5 seg\n")
            time.sleep(5)

def recibir(conn):
    while True:
        global bandera
        try:
            reply = conn.recv(2048)
            reply = reply.decode("UTF-8")

            if reply[0] == "1":
                print("Client", reply)
                start_new_thread(enviar, (conn,))

            elif reply[0] == "2":
                print("Client", reply)
                start_new_thread(enviar2, (conn,))

            else:
                lista_de_clientes.append(reply[4])
                print("\nThe client "+reply[4]+" is gone")
                bandera = True
                break



        except:
            print("\nCant recieve response")
            print("Trying in 5 seg\n")
            time.sleep(5)


def enviarEspecial(conn):
    global lista_de_clientes,client
    client = lista_de_clientes.pop()
    conn.send(client.encode("UTF-8"))

#######################################################################
##                          GLOBAL VARIABLES                         ##
#######################################################################

bandera = False      # Used in disconnecting / connecting clients

lista_de_clientes = ["2","1"]  # The server assigns a number to the
                                 # clients according to this list

client = ""     # Number of client


#######################################################################
##                                MAIN                               ##
#######################################################################

def main():

    global bandera
    host,port = ini()
    s = crearSocket()
    ligarSocket(s, host,port)
    s.listen(2)     # Listening / awaiting for 2 clients

    print("\nW A R N I N G : THE SERVER IS A SLAVE. DON'T "
          "WRITE IF THE SERVER DOESN'T HAVE ANY MESSAGE TO RESPONSE")
    print("\nWaiting for clients")

    conn,addr = conexiones(s)
    enviarEspecial(conn)               # Waiting connection of the client
    start_new_thread(recibir,(conn,))

    conn2,addr2 = conexiones(s)
    enviarEspecial(conn2)              # WAITING connection of the second client
    start_new_thread(recibir,(conn2,))

    while True: # This is necessary so the threads dont die

        if bandera != True:    # In case a client disconnects,
                                 # wait for another to connect again
            conn3,addr3 = conexiones(s)
            enviarEspecial(conn3)
            start_new_thread(recibir,(conn3,))
            bandera = False


main()
