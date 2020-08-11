# Class for connecting to and controlling the xyz table

# Need to understand when Isel sends communication and what each message means - use this to listen at the appropriate times and for reasonable lengths

# e.g. during axis movement does the table send regular updates regarding the axis still moving, or is it silent until the axis arrives
# Answer - After a movement command the table will send 'OK->' then 'Fehler->' straight away and then 'NEXTOK->' only after the axis has arrived 

# To do

# Add error checks (except statements where possible)
# Allow specifying port and IP address
# After sending commands look for the 'NEXTOK' reply before continuing (instead of timing out after so many seconds)
# If a bad command is sent we get 'ERROR: ...' - handle these as well
# Have the send method return the first string (for e.g. the GETPOSITION command)

# Add special functions for some commands
# e.g. GetPos to return three floats - Pos[0] = x, Pos[1] = y and Pos[2] = z
# For move commands add an additional check if the coordinates are legal / safe


from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import input              # Python 2 + 3 compatible method of getting user input strings
import time                             # Insert pauses due to limited data transfer speed
import sys                              # Exit command
import socket				# TCP/IP communication
import select				# For waiting until data is transmitted before calling recv


###############################################
############ Isel Class Definition ############
###############################################

# For handling all communication with Isel
class IselXYZ:

	# IP address of Isel (can be checked on Isel via cmd->ipconfig)
	TCP_IP = "169.254.160.111"
	# Port for communication
	TCP_PORT = 930
	# Buffer size for incoming messages
	BUFFER_SIZE = 1000


	# Table coordinates
	x=0; y=0;	z=0
	# Axis Limits
	xMin = 120000; xMax = 500000
	yMin = -600000; yMax = 500
	zMin = -130000; zMax = 500

	# Timeout in seconds when waiting for communication
	# No movement should take longer than this
	timeout = 60

	# Set up the connection here already
	def __init__(self):
		
		# Define the socket and make the connection
		self.s = s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.TCP_IP, self.TCP_PORT))
	
		# Make the socket non-blocking
		self.s.setblocking(0)
	
		# Wait for communication
		# Replace with self.read()
		ready = select.select([self.s], [], [], self.timeout)
		if ready[0]:
			data = self.s.recv(self.BUFFER_SIZE)
			print(data)


	# Read in buffers received from Isel
	# Keep reading and printing until no more buffers are received in $timeout seconds
	# For most commands the last signal received should be NEXTOK->
	def read(self):
		
		# Keep reading while data is being received
		while True:
			ready = select.select([self.s], [], [], self.timeout)
                	if ready[0]:
                		data = self.s.recv(self.BUFFER_SIZE)
                		print(data)
                		# If NEXTOK is received stop waiting (check if NEXTOK is attached to a previous line)
                		if (data == "NEXTOK->" or data[-8:] == "NEXTOK->"):
                			return 0
			else:
				break
		
		print("No more buffers received")
		return 1


	# Set the axis limits
	def setXLimits(self, xMin, xMax):
		self.xMin = xMin
		self.xMax = xMax
	def setYLimits(self, yMin, yMax):
		self.yMin = yMin
		self.yMax = yMax
	def setZLimits(self, zMin, zMax):
		self.zMin = zMin
		self.zMax = zMax
		
	# Return the axis limits
	def getXMin(self):
		return self.xMin
	def getXMax(self):
		return self.xMax
	def getYMin(self):
		return self.yMin
	def getYMax(self):
		return self.yMax
	def getYMin(self):
		return self.yMin
	def getYMax(self):
		return self.yMax

	# Send a command to Isel
	def send(self, command):

		self.s.send(command)
		# Read whatever comes back from Isel
		self.read()
		
	def getpos(self):
		# Send the GETPOSITION command and grab the first string returned
		# Split this into x y and z coordinates
		# Update the internal coordinates
		self.s.send("GETPOSITION->")
		# This needs to be changed
		# Maybe read could take an argument - e.g. to return 1st string received
		# Still need to receive all other strings so to avoid instant nextok on the next read
		self.read()
	
	# Move x axis only
	def moveX(self, xPos):
		# Only move if poisition is within limits, otherwise quit
		if (xPos >= self.xMin and xPos <= self.xMax):
			command = "MOVEABS X" + str(xPos)
			self.send(command)
		else:
			print("X coordinate outside allowed range:")
			print("Limit = " + str(self.xMin) + " -> " + str(self.xMax))
			print("Requested position = " + str(xPos))
			exit(0)

	# Move y axis only
	def moveY(self, yPos):
		# Only move if poisition is within limits, otherwise quit
		if (yPos >= self.yMin and yPos <= self.yMax):
			command = "MOVEABS Y" + str(yPos)
			self.send(command)
		else:
			print("Y coordinate outside allowed range:")
			print("Limit = " + str(self.yMin) + " -> " + str(self.yMax))
			print("Requested position = " + str(yPos))
			exit(0)
			
	# Move z axis only
	def moveZ(self, zPos):
		# Only move if poisition is within limits, otherwise quit
		if (zPos >= self.zMin and zPos <= self.zMax):
			command = "MOVEABS Z" + str(zPos)
			self.send(command)
		else:
			print("Z coordinate outside allowed range:")
			print("Limit = " + str(self.zMin) + " -> " + str(self.zMax))
			print("Requested position = " + str(zPos))
			exit(0)
		
		
	# Print list of commands
	def help(self):
		print("Help will eventually appear here ...")

	# Close the socket
	def close(self):
		print("Close the connection")
		self.s.close()
		
		
###############################################
#### Main definition - interactive session ####
###############################################		

# Only run main if this script is run directly (i.e. not imported as a module)
def main():
	
	isel = IselXYZ()
	
	# Enter infinite command loop
	while True:
	
		command = input('Enter command ("q" to quit, "h" for command list)->')
		assert isinstance(command, str)
		
		# quit	
		if (command=="q"):
			break
		
		# Call help printing method
		elif (command=="h"):
			isel.help()
		
		# Assume we have a valid command and send it
		else:
			isel.send(command)
	
	# Terminate the connection - should also send the exit signal to Isel
	isel.close()




# Do not execute main if this module was imported
if __name__ == "__main__":
        main()

