# Computer-Security
Some practical implementations of how to break certain security mechanisms in servers and wireless protocols.


# Problem descriptions: 
# Many time pad: 
Given 11 cipher texs which are encrypted with the same key, without using cribdragging estimate what the 11th cipher text is in plain text by using the other 10. This might be used to break the wireless protocol WEP which after some time reuses keystreams. Written for Python 2.7.6
# Timing Attack:
A testserver has been configured to exit validation as soon as a wrong character is found instead of going through the entire credentials which opens up for a timing attack to figure out the credentials. The server has been taken down and cannot be tested as of this moment. This code needs renaming and refactoring. Written for Python 3.7.1
