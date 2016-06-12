# Detect single-character XOR
# One of the 60-character strings in "challeng4.txt" has been encrypted by single-character XOR.
# Find it.
# (Your code from #3 should help.)

import single_byte_xor_cipher

def detect_xored_line(s):
    with open(s, "r") as txt:
        txt = txt.readlines()
    txt = [line.strip() for line in txt] # remove \n
    return [single_byte_xor_cipher.xor_single_byte(line) for line in txt]
