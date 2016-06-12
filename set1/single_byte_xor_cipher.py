# Single-byte XOR cipher
# The hex encoded string:
# 1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
# ... has been XOR'd against a single character. Find the key, decrypt the message.
# You can do this by hand. But don't: write code to do it for you.
# How? Devise some method for "scoring" a piece of English plaintext.
# Character frequency is a good metric. Evaluate each output and choose the one with the best score.

import string

def xor_single_byte(s):
    """
    Defines a set of valid characters (common in english plaintext) and return the
    xored string in which each character match with the valid characters.
    """
    s = bytes.fromhex(s)
    valids_chr = set(string.printable)-set(string.digits)-set(['/','`','@','_','#','$','%','~'])
    for letter in string.printable:
        result = "".join([chr(byte ^ ord(letter)) for byte in s])
        if all(map(lambda c: c in valids_chr, result)):
            print("KEY: %s\nMESSAGE: %s" % (letter, result))
