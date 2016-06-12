# Some useful functions for the challenge 6 of the set 1

def get_blocks(s, length):
    """Returns length-sized blocks list from s."""
    blocks = [s[start:start+length] for start in range(0, len(s), length) if start + length <= len(s)]
    return blocks

def transpose_blocks(blocks, key_length):
    """
    Returns a block list where each block contains the n position character of
    each block of the block list in parameter.
    """
    transposed = []
    for i in range(key_length):
        transposed.append([blk[i] for blk in blocks])
    return transposed

def pgcd(a,b) :
   while a%b != 0 :
      a, b = b, a%b
   return b
