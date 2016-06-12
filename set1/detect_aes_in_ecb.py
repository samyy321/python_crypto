# Detect AES in ECB mode
# In "challenge8.txt" are a bunch of hex-encoded ciphertexts.
# One of them has been encrypted with ECB.
# Detect it.
# Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will always produce the same 16 byte ciphertext.

def detect_aes_ecb(s):
    with open(s, "r") as s:
        s = s.read()
    block_occ = []
    i = 0
    while i < len(s) - 15:
        if s[i:].count(s[i:i + 16]) > 1:
            block_occ.append([s[i:i + 16], "index: " + str(i)])
            i += 16
        else:
            i += 1
    return block_occ
