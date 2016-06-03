#!/usr/bin/python
import socket
import struct
import hashlib

HOST = 'localhost'
PORT = 1307
BUFFER_SIZE = 1024
HEAD_STRUCT = '128sIq32s'   # Structure of file head

def recv_file():
	# Create a TCP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Enable reuse address/port
	# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# Bind the socket to the port
	server_address = (HOST, PORT)
	# Bind server address
	sock.bind(server_address)
	print "Starting server on %s port %s" % server_address
	# Listen to clients
	sock.listen(1)
	print "Waiting to receive from client"
	client_socket, client_address = sock.accept()
	print "Socket %s:%d has connect" % client_address

	# Receive file info
	info_struct = struct.calcsize(HEAD_STRUCT)
	file_info = client_socket.recv(info_struct)
	file_name2, filename_size, file_size, md5_recv = struct.unpack(HEAD_STRUCT, file_info)
	file_name = file_name2[:filename_size]
	fw = open(file_name, 'wb')
	recv_size = 0
	print "Receiving data..."
	while (recv_size < file_size):
		if(file_size - recv_size < BUFFER_SIZE):
			file_data = client_socket.recv(file_size - recv_size)
			recv_size = file_size
		else:
			file_data = client_socket.recv(BUFFER_SIZE)
			recv_size += BUFFER_SIZE
		fw.write(file_data)
	fw.close()
	print "Accept success!"
	print "Calculating MD5..."
	fw = open(file_name, 'rb')
	md5_cal = hashlib.md5()
	md5_cal.update(fw.read())
	print "  Recevie MD5 : %s" %md5_recv
	print "Calculate MD5 : %s" % md5_cal.hexdigest()
	fw.close()

if __name__ == '__main__':
	recv_file()
