from BluenetLib.lib.protocol.BluenetTypes import ControlType, OpCode
from BluenetLib.lib.util.Conversion import Conversion


class BLEPacket:

    def __init__(self, packetType):
        self.lengthAsUint8Array = [0, 0]
        self.payload = []
        self.type = packetType.value

    def loadKey(self, keyString):
        self.payload = Conversion.ascii_or_hex_string_to_16_byte_array(keyString)
        return self._process()
    
    def loadString(self, string):
        self.payload = Conversion.string_to_uint8_array(string)
        return self._process()

    def loadInteger(self, integer):
        self.payload = [Conversion.int8_to_uint8(integer)]
        return self._process()

    def loadUInt8(self, uint8):
        self.payload = [uint8]
        return self._process()

    def loadUInt16(self, uint16):
        self.payload = Conversion.uint16_to_uint8_array(uint16)
        return self._process()

    def loadUInt32(self, uint32):
        self.payload = Conversion.uint32_to_uint8_array(uint32)
        return self._process()

    def loadFloat(self, float):
        self.payload = Conversion.float_to_uint8_array(float)
        return self._process()

    def loadByteArray(self, byteArray):
        self.payload = byteArray
        return self._process()

    def appendByteArray(self, byteArray):
        self.payload += byteArray
        return self._process()

    def _process(self):
        self.length = len(self.payload)
        self.lengthAsUint8Array = Conversion.uint16_to_uint8_array(len(self.payload))
        return self

    def getPacket(self):
        packet = []
        packet += Conversion.uint16_to_uint8_array(self.type)
        packet += self.lengthAsUint8Array
        packet += self.payload

        return packet

class ControlPacket(BLEPacket):

    def __init__(self, packetType):
        super().__init__(packetType)




class FactoryResetPacket(ControlPacket):

    def __init__(self):
        super().__init__(ControlType.FACTORY_RESET)
        self.loadUInt32(0xdeadbeef)

class ControlStateGetPacket(ControlPacket):

    def __init__(self, stateType, id = 0):
        super().__init__(ControlType.GET_STATE)
        self.id = id
        self.loadUInt16(stateType)


    def getPacket(self):
        arr = []
        arr += Conversion.uint16_to_uint8_array(self.type)
        arr += Conversion.uint16_to_uint8_array(self.length + 2) # 2 for the ID size
        arr += self.payload # this is the state type
        arr += Conversion.uint16_to_uint8_array(self.id)
        return arr


class ControlStateSetPacket(ControlPacket):

    def __init__(self, stateType, id=0):
        super().__init__(ControlType.SET_STATE)
        self.stateType = stateType
        self.id = id


    def getPacket(self):
        arr = []
        arr += Conversion.uint16_to_uint8_array(self.type)
        arr += Conversion.uint16_to_uint8_array(self.length + 4) # the + 2 is for the stateType uint16 and +2 for the id
        arr += Conversion.uint16_to_uint8_array(self.stateType)
        arr += Conversion.uint16_to_uint8_array(self.id)
        arr += self.payload
        return arr

