
from encryptdec import Security


def test_security():
    sercure = Security()
    password = "oparolaminunata"
    if ( new_pass := sercure.encryptPass(password) )!= password:
        assert sercure.decryptPass(new_pass) == password
    else:
        assert False