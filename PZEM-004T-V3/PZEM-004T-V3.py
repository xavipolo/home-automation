import minimalmodbus
import serial
import time

class PZEM004TV3( minimalmodbus.Instrument ):
    """Instrument class for PZEM-004T-V3 energy meter.

    Args:
        * portname (str): port name
        * slaveaddress (int): slave address in the range 1 to 247
        * debug

    """

    def __init__(self, portname, slaveaddress, debug = False):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress, minimalmodbus.MODE_RTU, True, debug)
        self.serial.baudrate = 9600
        self.serial.bytesize = 8
        self.serial.timeout = 0.2
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = 1

    def reset_energy(self):
        """Reset internal counter of energy.

        Message:
        * Slave address 
        * 0x42
        * CRC Check High Byte
        * CRC Check Low Byte

        """

        self._perform_command(66, '')

    def set_alarm(self, threshold: int):
        """Set the alarm threshold in Watts.
        
        Args:
        * threshold (int): Watts. Must be greater than 0.

        Message:
        * Slave address 
        * 0x06 Function code
        * 0x00 Register Address High Byte
        * 0x01 Register Address Low Byte
        * Register Value High Byte
        * Register Value Low Byte
        * CRC Check High Byte
        * CRC Check Low Byte

        """
        
        self.write_register(1, threshold, 0, 6)
        
    
    def set_slave_address(self, address: int):
        """Changes the slave address to new number (1 to 247)
        
        Args:
        * address (int): Must be between 1 and 247.

        Message:
        * Slave address 
        * 0x06 Function code
        * 0x00 Register Address High Byte
        * 0x02 Register Address Low Byte
        * Register Value High Byte
        * Register Value Low Byte
        * CRC Check High Byte
        * CRC Check Low Byte

        """
        
        self.write_register(2, address, 0, 6)

    
    def calibrate(self):
        """Calibrate.
        There is no info about process
                
        Message:
        * Slave address? 
        * 0x41 Function code
        * 0x37 Register Address High Byte
        * 0x21 Register Address Low Byte
        * CRC Check High Byte
        * CRC Check Low Byte

        """

        self._perform_command(5, '\x37\x21')


    # Composite values are reading using 2 registers
    # Register 1 -> Low 16 bits (AB -> 8 + 8 bits)
    # Register 2 -> High 16 bits (CD -> 8 + 8 bits)
    # ABCD, with BYTEORDER_LITTLE_SWAP -> CDAB 

    def get_current(self) -> float:
        """Return current in Amperes (A)"""
        value = self.read_long(1, 4, False, minimalmodbus.BYTEORDER_LITTLE_SWAP)
        return value/1000 

    def get_power(self) -> float:
        """Return power in Watts (W)"""
        value = self.read_long(3, 4, False, minimalmodbus.BYTEORDER_LITTLE_SWAP)
        return value/10

    def get_energy(self) -> int:
        """Return internal counter for energy in Watts per Hour (Wh).
        Could be reset with reset_energy() function"""
        value = self.read_long(5, 4, False, minimalmodbus.BYTEORDER_LITTLE_SWAP)
        return value 


    # Simple values are reading using 1 register

    def get_voltage(self) -> float:
        """Return the voltage in Volts (V)"""
        return self.read_register(0, 1, 4)

    def get_frequency(self) -> float:
        """Return the frequency in Herzs (Hz)"""
        return self.read_register(7, 1, 4)

    def get_power_factor(self) -> float:
        """Return the power factor"""
        return self.read_register(8, 2, 4)

    def get_alarm_status(self) -> bool:
        """Return the alarm status (True o False)"""
        return (self.read_register(9, 0, 4) != 0)

    
    # Return values with units

    def get_voltage_wu(self):
        return [self.get_voltage(), 'V']   
    
    def get_current_wu(self):
        return [self.get_current(), 'A'] 

    def get_power_wu(self):
        return [self.get_power(), 'W'] 

    def get_energy_wu(self):
        return [self.get_energy(), 'Wh'] 

    def get_frequency_wu(self):
        return [self.get_frequency(), 'Hz'] 

    def get_power_factor_wu(self):
        return [self.get_power_factor(), ''] 
    
    def test(self, wait_seconds = 5, alarm_value = None, reset_energy = False):
        
        try:
            if (alarm_value != None):
                self.set_alarm(alarm_value)
            
            if (reset_energy):
                self.reset_energy()

        except IOError:
                print("Failed to read from instrument")    
           

        while True:
            
            try:
                print("get_voltage_wu()", mydev.get_voltage_wu())
                print("get_current_wu()", mydev.get_current_wu())
                print("get_power_wu()", mydev.get_power_wu())
                print("mydev.get_energy_wu", mydev.get_energy_wu())
                print("mydev.get_frequency_wu", mydev.get_frequency_wu())
                print("mydev.get_power_factor_wu", mydev.get_power_factor_wu())
                print("get_alarm_status()", mydev.get_alarm_status())

                time.sleep(wait_seconds)

            except IOError:
                print("Failed to read from instrument")    
