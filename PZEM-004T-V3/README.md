# Introduction

## ZEM-004T Version 3.0 TTL Modbus RTU

It is a single-phase AC power meter, which through a TTL interface allows the reading of:
- Consumption (A)
- Voltage (V)
- Frequency (Hz)
- Power factor

It also allows to set an alarm when a certain demand is reached, as well as to store the demand (Wh) and to reset it.

There are two variants: 
- PZEM-004T-10A: measuring range 10A 
- PZEM-004T-100A: measuring range 100 A 


# Usage

This python class allow to control the device. It was tested with Python 3.7.4 64 bits (windows 10)

Find the COM port where your PZEM-004T v3 device is connected

Create an instance and test it by calling the test function.

    mydev = PZEM004TV3('COM7', 1, False)
    mydev.test()

The console will print out standard readings every 5 seconds: 

    get_voltage_wu() [238.4, 'V']
    get_current_wu() [0.165, 'A']
    gett_power_wu() [10.6, 'W']
    get_energy_wu() [33, 'Wh']
    get_frequency_wu() [50.0, 'Hz']
    get_power_wu_factor() [0.27, '']
    get_alarm_status() False


