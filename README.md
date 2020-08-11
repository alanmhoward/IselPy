# IselPy

Python class for controlling the ISEL xyz table. The class can be used as a standalone application or, more likely, imported into a python script together with other devices to permit operations to be performed using the table.

In the present form the IP address of the ISEL is hardcoded - run ipconfig from the ISEL box itself to confirm this is correct.

To enable remote access the SpeedControl GUI must be used and the relevant option selected.

An example python script is included which also uses the SylvacClass (see the sylvac-ctrl repo) in order to measure the height profile of an object placed upon the granite table.
