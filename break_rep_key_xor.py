# Break repeating-key XOR
# It is officially on, now.
# This challenge isn't conceptually hard, but it involves actual error-prone coding.
# The other challenges in this set are there to bring you up to speed.
# This one is there to qualify you. If you can do this one, you're probably just fine up to Set 6.
# There's a file (challenge6.txt). It's been base64'd after being encrypted with repeating-key XOR.
# Decrypt it.
# Here's how:
#     Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.
#     Write a function to compute the edit distance/Hamming distance between two strings.
#     The Hamming distance is just the number of differing bits. The distance between:
#     this is a test
#     and
#     wokka wokka!!!
#     is 37. Make sure your code agrees before you proceed.
#     For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second KEYSIZE worth of bytes,
#     and find the edit distance between them. Normalize this result by dividing by KEYSIZE.
#     The KEYSIZE with the smallest normalized edit distance is probably the key.
#     You could proceed perhaps with the smallest 2-3 KEYSIZE values. Or take 4 KEYSIZE blocks instead of 2 and average the distances.
#     Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.
#     Now transpose the blocks: make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.
#     Solve each block as if it was single-character XOR. You already have code to do this.
#     For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte for that block.
#     Put them together and you have the key.
#     This code is going to turn out to be surprisingly useful later on.
#     Breaking repeating-key XOR ("Vigenere") statistically is obviously an academic exercise, a "Crypto 101" thing.
#     But more people "know how" to break it than can actually break it, and a similar technique breaks something much more important.

import base64
import string
import utils

def hamming_dist(s, s2):
    to_comp = bytes(a ^ b for (a,b) in zip(s, s2))
    diff = 0
    for byte in to_comp:
        for bit in range(8):
            diff += (byte >> bit) & 1
    return diff

def key_length(s):
    with open(s, "rb") as txt:
        s = base64.b64decode(txt.read())
    distances = {}
    for k_length in range(2, 40):
        blocks = utils.get_blocks(s, k_length)
        # get the normalized hamming distance of each block with his adjacent block
        distances[k_length] = sum(hamming_dist(a, b)/k_length for
         a, b in zip(blocks, blocks[1:]))
         # get the avg of all normalized hamming distance with the current key length
        distances[k_length] /= len(blocks)
    distances = sorted(distances.items(), key=lambda x: x[1])
    #Returns the lowest distance using the greatest common divisor if the first two are a multiple of the key_length
    return distances[0][0] if utils.pgcd(distances[0][0], distances[1][0]) == 1\
     else utils.pgcd(distances[0][0], distances[1][0])

def find_key(s, key_length):
    """
    Find the key by scoring several "single byte xor" using the frequency letter.
    """
    s = base64.b64decode(s)
    transposed_blocks = utils.transpose_blocks(utils.get_blocks(s, key_length), key_length)
    letter_place = {}
    key = ""
    occurence = dict((letter, 0) for letter in string.printable)
    for i, tblock in enumerate(transposed_blocks):
        for letter in string.printable:
            occurence[letter] = 0
            xored_tblock = [byte ^ ord(letter) for byte in tblock]
            for byte in xored_tblock:
                # the 6 first most frequent letters in english plaintexts http://letterfrequency.org/#english-language-letter-frequency
                if chr(byte) in "etaoinETAOIN":
                    occurence[letter] += 1
                    letter_place[i] = occurence.copy()
    for i, value in letter_place.items(): #for each dict in letter_place returns the key that contains the greatest score
        getkey = lambda i, val: [k for k,v in value.items() if v == (max(value.values()))]
        key += max(getkey(i, value))
    return key
