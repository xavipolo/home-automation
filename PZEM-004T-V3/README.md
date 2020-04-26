# Introduction

## ZEM-004T Version 3.0 TTL Modbus RTU

It is a single-phase AC power meter, which through a TTL interface allows the reading of:
- Consumption (A)
- Voltage (V)
- Power (W)
- Frequency (Hz)
- Power factor
- Accumulated demand (Wh)

It also allows to set an alarm when a certain demand is reached, as well as to store the demand and to reset it.

There are two variants: 
- PZEM-004T-10A: measuring range 10A 
- PZEM-004T-100A: measuring range 100 A 


### Installation requierements

- Python (tested with Python 3.7.4 64 bits windows 10) 
- Install minimalmodbus library (tested with 1.0.2)
    
    pip3 install -U minimalmodbus

Copy PZEM004TV3.py to your python project.


### Usage

This python class allow to control the device.

Find the COM port where your PZEM-004T v3 device is connected

Create an instance specifying the port, the slave address (default 1) and whether you want to activate debugging (which will generate traces of the input/output communications)

    from PZEM004TV3 import PZEM004TV3

    mydev = PZEM004TV3('COM7', 1, False)
   
Call methods or try it calling test method.

    mydev.test()

The console will print out standard readings every 5 seconds: 

    get_voltage_wu() [238.4, 'V']
    get_current_wu() [0.165, 'A']
    gett_power_wu() [10.6, 'W']
    get_energy_wu() [33, 'Wh']
    get_frequency_wu() [50.0, 'Hz']
    get_power_wu_factor() [0.27, '']
    get_alarm_status() False

Code is commented
