# Script for measuring an area of the table using the sylvac indicator

# Compatability between python 2 and 3
from __future__ import absolute_import, division, print_function, unicode_literals

# Import the isel class
from IselClass import *
# Import trhe sylvac class
from SylvacClass import *

import sys
import time


# Create an indicator instance
syl = Sylvac()

# Create an Isel instance
isel = IselXYZ()

# Set the movement velocity
isel.send("MOVEVEL 10000")
isel.setZLimits(-160000,500)

# Output file
of = open("TableMeasure_finegrid.dat","w")

# Axis values to use for measurements
xMin = 134770
xMax = 400000
xDelta = 2000

yMin = -207000
yMax = -001000
yDelta = 2000
zMove = -154000
zMeasure = -157000

# Function for the segment curvature
#R = 798600
#y0 = -103700
#z0 = 798600 - 139200 # Subtract the z value for the axis when measuring the centre of the segment

# Starting positions
xPos = xMin
yPos = yMin

# Move to safe Z
# End each loop with a movement to safe z
isel.moveZ(zMove)

# Loop over x range
while ((xPos) <= (xMax + xDelta/2.0) and (xPos)>120000):

	# Set yPos to yMin at start of each loop
	yPos = yMin
	
	# Move to new x
	isel.moveX(xPos)
	
	# Loop over the range of y values
	while ((yPos) <= (yMax + yDelta/2.0)):
	
		# Move to new y
		isel.moveY(yPos)
	
		# Measure z - move to point about 2 mm above surface
		#zPos = int((z0 - (R**2 - (yPos-y0)**2)**0.5))
		zPos = zMeasure
		isel.moveZ(zPos)
	
		# Make measurement and write to file
		time.sleep(0.1)
		Value = syl.send('?')
		time.sleep(0.1)
		print(xPos, "\t", yPos, "\t", zPos, "\t", Value, file=of)
		print(xPos, "\t", yPos, "\t", zPos, "\t", Value)
	
		# Move to safe Z
		isel.moveZ(zMove)
	
		# New y
		yPos += yDelta
		
	# Update the x position	
	xPos += xDelta

# End communication with Isel and indicator
isel.close()
syl.close()	

# Close the output file
of.close()
