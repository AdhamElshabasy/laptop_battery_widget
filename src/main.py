#-----------------------------------------------------------------------------#
# Code Author          : Adham N. Elshabasy
# Contact me           : Email: Adhamnasser@live.com
# Created On           : Friday - September 22, 2023 / 16:21:44 UTC+2
# Operating System     : Windows 10
# Programming Language : Python (Version 3.10.1)
# File Name            : main.py
# Version              : v1.2.0
# Code Title           : Always-on-top Laptop Battery Widget
#-----------------------------------------------------------------------------#
# Temporary terminal clear command, remove when done.
# pylint: disable=wrong-import-position
from os import system
from sys import platform
if platform == 'win32':
	system('cls')
else:
	system('clear')
# pylint: enable=wrong-import-position
#-----------------------------------------------------------------------------#

# Importing modules and libraries
from battery_widget import BatteryWidget


# Main function
if __name__ == "__main__":
    # Import the UI class and run it
    widget = BatteryWidget()
    widget.mainloop()