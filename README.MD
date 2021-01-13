# Blueberry Python Connect App

Connect to Blueberry brain sensing pod from Linux, MacOS, RasbperryPi, and Windows.

## Install

You should have Python 3.6/3.7/3.8 installed and the corresponding pip package installed.

Go ahead and `git clone` this repo (or your fork/copy of it): https://github.com/blueberryxtech/BlueberryPython. Move into the directory you just cloned (`cd BlueberryGlassesServer`).  

Now we need to setup a virtual environment and install dependencies.   

If in Linux/Raspberry Pi, run `sudo apt-get install libatlas-base-dev`.    

Setup and activate virtualenv:
```
pip3 install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
```

Install packages:
```
pip3 install -r requirements.txt
```

Good to go!

## Tested

Ubuntu 20, MacOS, Raspberry Pi 3B+.
Should work in Windows 10. Not tested.

## Scripts

bby_stream.py - connect, see data, and save data to a file  
bby_data_plot.py - plot data created with bby_stream.py  
list_devices.py - scan Bluetooth to find your Blueberry  
bby_details.py - see information about your Blueberry

## Getting Started

List all available Blueberry units (make sure yours is on):
```
python3 list_bbys.py
```

Now connect to the unit that you want stream from:
```
python3 bby_stream.py -a <Blueberry MAC address> -s -d -f <filename of csv>
```

Now plot the data:  
```
python3 bby_data_plot.py -f test.csv
```

## Help

Email cayden at blueberryx.com
