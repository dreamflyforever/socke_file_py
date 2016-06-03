#!/usr/bin/python
import socket
import struct
import os
import time
import hashlib
import sys

HOST = 'localhost'
PORT = 1307
BUFFER_SIZE = 1024
# Structure of file head
HEAD_STRUCT = '128sIq32s'

def send_file(file_name):
	FILE_SIZE = os.path.getsize(file_name)
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Connect the socket to the server
	server_address = (HOST, PORT)

	#Calculate MD5
	print "Calculating MD5..."
	fr = open(file_name, 'rb')
	md5_code = hashlib.md5()
	md5_code.update(fr.read())
	fr.close()
	print "Calculating success"

	# Need open again
	fr = open(file_name, 'rb')
	# Pack file info(file name and file size)
	file_head = struct.pack(HEAD_STRUCT, file_name, len(file_name), FILE_SIZE, md5_code.hexdigest())

	try:
		# Connect
		sock.connect(server_address)
		print "Connecting to %s port %s" % server_address
		# Send file info
		sock.send(file_head)
		send_size = 0
		print "Sending data..."
		time_start = time.time()
		while(send_size < FILE_SIZE):
			if(FILE_SIZE - send_size < BUFFER_SIZE):
				file_data = fr.read(FILE_SIZE - send_size)
				send_size = FILE_SIZE
			else:
				file_data = fr.read(BUFFER_SIZE)
				send_size += BUFFER_SIZE
			sock.send(file_data)
		time_end = time.time()
		print "Send success!"
		print "MD5 : %s" % md5_code.hexdigest()
		print "Cost %f seconds" % (time_end - time_start)
		fr.close()
		sock.close()
	except socket.errno, e:
		print "Socket error: %s" % str(e)
	except Exception, e:
		print "Other exception : %s" % str(e)
	finally:
		print "Closing connect"

if __name__ == '__main__':
	argc = len(sys.argv)
	if argc< 2:
		print "argc: ", argc
	else:
		print "input argv: ", sys.argv[1]

		for i in range(1, len(sys.argv)):
			print "output argv: ", sys.argv[i]
			send_file(sys.argv[1])
