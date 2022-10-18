## DIAGNOSIS BY TOUCH
This project is made for Samsung Innovation Campus Batch 3 Stage 3. This repository was made to track the progress we make to build an IoT device.

You can see the full design here:
[Product Design](https://docs.google.com/presentation/d/1X4S7OHgEltPV4uqPD-Z991j0jWk4kUk-/edit?usp=sharing&ouid=100909576299268218717&rtpof=true&sd=true)

We are using:

 - DS18B20 Body Temperature Sensor
 - Max30102 Pulse Oximeter and Hearth Rate Sensor
 - Raspberry Pi 3 Model B Rev 1.2
 - LED light
 - LCD I2C


## Script Content
**All Files at Script Folder**

Script needed for this IoT project

|File Name|Content  |
|--|--|
| .env|Configuration file |
| LED.py|All functions for controlling LED light |
| Oksi.py|All the functions necessary to run and read Max30102 sensor |
| location.py|Get device location data |
| main.py|Main script for IoT project |
| sendDataMongoDB.py|Function to send, read, update, and delete data to MongoDB |
| sendUbidots.py|Function to send data to Ubidots |
| temperature.py |All the functions necessary to read DS18B20 temperature sensor  |

**All files at TestScript Folder**

All script to test components in this IoT project

**Unused Script**

|File Name|Content  |
|--|--|
|~~maintem.py~~|~~Function to read and some logic to determine health based on body temperature~~ *(Merged all functionality to temperature.py)*|
|~~mainLED.py~~|~~Script to control LED light. Required LED.py~~ *(Merged all functionality to LED.py)*|
|~~max30102.py~~|~~Contains a class which has some setup functions and sensor-reading functions~~ *(Moved all functionality to Oksi.py)*|
|~~hrcalc.py~~| ~~Provides a function which calcs HR and SpO2~~ *(Moved all functionality to Oksi.py)*|
|~~mainOksi.py~~|~~Run and read data from sensor, main script for Max30102~~ *(Moved all functionality to Oksi.py)*|
|~~mainOksiTem.py~~|~~Combine Max30102 and DS18B20 sensor~~ *(Moved all functionality to main.py)*|



**Logic LED and Temperature**

mainLEDtem.py and mainLEDsettem.py logic:
 - Less than or equal to 36C, show `Error: Suhu terlalu rendah`
 - Between 36C and 37,5C, show `Normal` and turn on LED Green
 - Between 37,5C and 38,5C, show `Sakit ringan` and turn on LED Red
 - Above 38,5C, show `Sakit parah` and make LED Red blink

## DS18B20 Setup
**Wiring to Raspberry Pi**

|DS18B20|Raspberry Pi  |
|--|--|
|GND (Black wire) |Raspberry Pi GND |
|DQ (Yellow wire)|Raspberry Pi GPIO17|
|VDD (Red wire)|Resistor 4,7k ohm|
|Resistor|Raspberry Pi 3v3|

See wiring diagram at Design folder or at Documentation for RL application

**Enable 1-Wire**

 - Open terminal, type `sudo raspi-config`
 - Select *Interfacing Option*
 - Enable *1-Wire*
 - Back to terminal, type `sudo modprobe w1_gpio` then `sudo modprobe w1_therm`
 - Edit config.txt file, type `sudo nano /boot/config.txt`
 - Append new line, and type `dtoverlay=w1-gpio-pullup,gpiopin=17`

**Read Temperature**

 - Change directory to /sys/bus/w1/devices, type `cd /sys/bus/w1/devices`
 - Check the directory using `ls` It should contain folder *28-xxxxxxxxxxxx*
 - Hop into that folder
 - Read the temperature using `cat w1-slave`
 - The YES in the first line indicates CRC check success (Data Valid). The number following t= is the temperature
 
**Script Read Temperature**

Here we are using Python to show the temperature. In the *Script* folder, for DS18B20 there are two Python scripts, one (temperature.py) contains all necessary functions to read temperature for the sensor, another one (maintem.py) contains function to read and some logic to determine health based on body temperature.

**How to Use**

 - Copy the script (maintem.py and temperature.py) to Raspberry Pi. *All the scripts must be put in one folder!*
 - Hold the sensor using one of your hands
 - In Raspberry Pi, run terminal, navigate to where you put the script
 - Run the script by typing `sudo python maintem.py` *Note: this script must be run by the root user*
 
 **Important Note**
 
For now, this is just proof of concept!


## LED
**Wiring to Raspberry Pi**

LED Green Wiring
|LED Green|Raspberry Pi  |
|--|--|
|Anode (longer leg)|Raspberry Pi GPIO25|
|Cathode (shorter leg) |Resistor 220 ohm|
|Resistor 220 ohm | Raspberry Pi GND|

LED Red Wiring
| LED Red | Raspberry Pi |
|--|--|
|Anode (longer leg)|Raspberry Pi GPIO8|
|Cathode (shorter leg) |Resistor 220 ohm|
|Resistor 220 ohm | Raspberry Pi GND|


See wiring diagram at Design folder or at Documentation for RL application

**Script**

Here we are using Python to change the LED state. In the *script* folder, for LED there are two Python scripts, one (LED.py) contains all necessary functions for controlling the LED, another one (mainLED.py) contains script to control the LED light.

**How to Use**

 - Copy the script (mainLED.py and LED.py) to Raspberry Pi. *All the scripts must be put in one folder!*
 - In Raspberry Pi, using terminal, run mainLED.py `python mainLED.py`
 - Enter either `Green` or `Red`
 - Then enter either `On` or `Off` to control the LED


## LCD I2C
**Wiring to Raspberry Pi**

| LCD I2C |Raspberry Pi  |
|--|--|
| GND | Raspberry Pi GND|
| VCC | Raspberry Pi 5V|
| SDA | Raspberry Pi GPIO2|
| SCL | Raspberry Pi GPIO3|


See wiring diagram at Design folder or at Documentation for RL application

**Enable I2C**

 - Open terminal, type `sudo raspi-config`
 - Select *Interfacing Option*
 - Enable *I2C*
 - Back to terminal, then reboot system `sudo reboot`
 - Open terminal again, type `i2cdetect -y 1`. The *i2cdetect* command can be used to see what is connected and what the addresses are. Most common are `27 hexadecimal`.

**Install Python Library**

 - Using terminal. type `sudo pip3 install rpi_lcd`
 - This library has the default 27 address hard-coded. If your display has a different address, you will need to change it. Find the library using `sudo find /usr/local –name rpi_lcd 2> /dev/null`
 - Find *rpi_lcd*, commonly it can be found at `/usr/local/lib/(python version)/dist-packages/rpi_lcd`
 - Get into that directory using `cd /usr/local/lib/(python version)/dist-packages/rpi_lcd`
 - Type `nano __init__.py`, locate `LCD class`, `def __init__(self, address = 27, ...)`
 - Change `address = 27` to your address that show at `i2cdetect` command

**Script**

Here we are using Python to control the LCD. In the *script* folder, there is testLCD.py. It contains a function and some information about how to control the LCD.

**How to Use**

Using terminal, run the script `sudo python testLCD.py`

## Max30102

**Wiring to Raspiberry Pi**
|Max30102|Raspberry Pi  |
|--|--|
|VIN|Raspberry Pi 3v3  |
|GND|Raspberry Pi GND|
|SCL|Raspberry Pi GPIO3|
|SDA|Raspberry Pi GPIO2|
|INT|Raspberry Pi GPIO4|


See wiring diagram at Design folder or at Documentation for RL application

**Enable I2C**

 - Open terminal, type `sudo raspi-config`
 - Select *Interfacing Option*
 - Enable *I2C*
 - Back to terminal, then reboot system `sudo reboot`

**Install Required Python Library**

 - Open terminal, type `sudo apt-get update` then `sudo apt-get install python-smbus python3-smbus python-dev python3-dev i2c-tools` This will install *smbus python library*
 - If that doesn't work, try `sudo apt-get update` then `sudo apt-get install python3-smbus python3-dev i2c-tools`
 - You also need *rpi.gpio module*, if it's not already installed, type `sudo apt-get update` then `sudo apt-get install rpi.gpio`

**Script**

Here we are using Python to read the sensor. All functions that are needed for the sensor to run are inside *Oksi.py* file. Running the file dirrectly will get and show sensor's data. You can also import this to another file to perform more complex logic.

**How to Use**

 - Run terminal and navigate to script folder, type `sudo python Oksi.py`
 - Touch Max30102 using your finger and wait until the program is complete

## How to Setup

Here's how to set up this project

- Install all the components as shown below
![Wiring diagram](https://raw.githubusercontent.com/MuhammadNauvalDwiAfandi/DiagnosisByTouch/master/Design/Schematic_bb.jpg)*You can also download wiring diagram in fritzing format [here](https://github.com/MuhammadNauvalDwiAfandi/DiagnosisByTouch/raw/master/Design/Schematic.fzz)*
- Download all the script from **Script** folder and put it into **one folder**. Download it [here](https://github.com/MuhammadNauvalDwiAfandi/DiagnosisByTouch/tree/master/Script)
- Download [requirement.txt](https://github.com/MuhammadNauvalDwiAfandi/DiagnosisByTouch/blob/master/requirement.txt)
- Install all the requirements by opening a terminal and type `pip install -r requirement.txt`
- Enable i2c and 1-wire, type `sudo raspi-config`, *Interfacing Option*, enable *I2C* and *1-Wire*
- Reboot system
- Run main script by typing `sudo python main.py`