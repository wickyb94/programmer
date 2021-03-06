
from BluenetLib.lib.util.Conversion import Conversion


from enum import IntEnum
class UserLevel(IntEnum):
    admin   = 0
    member  = 1
    basic   = 2
    setup   = 100
    unknown = 255


class BluenetSettings:
    
    def __init__(self):
        self.adminKey = None
        self.memberKey = None
        self.basicKey = None
        self.setupKey = None
        self.serviceDataKey = None
        self.localizationKey = None
        self.meshApplicationKey = None
        self.meshNetworkKey = None

        self.referenceId = None
        self.sessionNonce = None
        self.initializedKeys = False
        self.temporaryDisable = False
        self.userLevel = UserLevel.unknown


    def loadKeys(self, adminKey, memberKey, basicKey, serviceDataKey, localizationKey, meshApplicationKey, meshNetworkKey, referenceId):
        self.adminKey  = Conversion.ascii_or_hex_string_to_16_byte_array(adminKey)
        self.memberKey = Conversion.ascii_or_hex_string_to_16_byte_array(memberKey)
        self.basicKey  = Conversion.ascii_or_hex_string_to_16_byte_array(basicKey)
        self.serviceDataKey  = Conversion.ascii_or_hex_string_to_16_byte_array(serviceDataKey)
        self.localizationKey  = Conversion.ascii_or_hex_string_to_16_byte_array(localizationKey)
        self.meshApplicationKey = Conversion.ascii_or_hex_string_to_16_byte_array(meshApplicationKey)
        self.meshNetworkKey  = Conversion.ascii_or_hex_string_to_16_byte_array(meshNetworkKey)

        self.referenceId = referenceId
        
        self.initializedKeys = True
        self.determineUserLevel()
        

    def determineUserLevel(self):
        if   len(self.adminKey)  == 16:
            self.userLevel = UserLevel.admin
        elif len(self.memberKey) == 16:
            self.userLevel = UserLevel.member
        elif len(self.basicKey)  == 16:
            self.userLevel = UserLevel.basic
        else:
            self.userLevel = UserLevel.unknown
            self.initializedKeys = False


    def invalidateSessionNonce(self):
        self.sessionNonce = None


    def setSessionNonce(self, sessionNonce):
        self.sessionNonce = sessionNonce


    def loadSetupKey(self, setupKey):
        self.setupKey  = setupKey
        self.userLevel = UserLevel.setup


    def exitSetup(self):
        self.setupKey = None
        self.determineUserLevel()


    def disableEncryptionTemporarily(self):
        self.temporaryDisable = True


    def restoreEncryption(self):
        self.temporaryDisable = False


    def isTemporarilyDisabled(self):
        return self.temporaryDisable


    def isEncryptionEnabled(self):
        if self.temporaryDisable:
            return False
        return True






