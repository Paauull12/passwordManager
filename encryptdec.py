import base64
import hashlib
from cryptography.fernet import Fernet
import base64

class Security:

    def __init__(self, key=None):
        self.__key = key or Fernet.generate_key()

        self.__fernet = Fernet(self.__key)

    def encryptPass(self, text):
        return self.__fernet.encrypt(text.encode()).decode()

    def decryptPass(self, text):
        return self.__fernet.decrypt(text.encode()).decode()

    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    @staticmethod
    def hashPass(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def check_password(stored_password, provided_password):
        return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()