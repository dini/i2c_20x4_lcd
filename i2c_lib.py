import smbus


class i2c_device:
    """"""
    def __init__(self, addr, port=1):
        """"""
        self.addr = addr
        self.bus = smbus.SMBus(port)

    def write_cmd(self, cmd):
        """Write a single command"""
        self.bus.write_byte(self.addr, cmd)

    def write_cmd_arg(self, cmd, data):
        """Write a command and argument"""
        self.bus.write_byte_data(self.addr, cmd, data)

    def write_block_data(self, cmd, data):
        """Write a block of data"""
        self.bus.write_block_data(self.addr, cmd, data)

    def read(self):
        """Read a single byte"""
        return self.bus.read_byte(self.addr)

    def read_data(self, cmd):
        """Read"""
        return self.bus.read_byte_data(self.addr, cmd)

    def read_block_data(self, cmd):
        """Read a block of data"""
        return self.bus.read_block_data(self.addr, cmd)
