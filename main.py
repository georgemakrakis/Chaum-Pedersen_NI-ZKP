from hmac import digest
from Crypto.Util.number import *
from Crypto import Random
import libnum
import hashlib


def main():
    x = int.from_bytes(Random.get_random_bytes(16), "big")
    g = 5
    h = 3
    k = int.from_bytes(Random.get_random_bytes(16), "big")

    p = pow(2, 255)

    Y = pow(g, x, p)
    Z = pow(h, x, p)
    
    A = pow(g, k, p)
    B = pow(h, k, p)


    c_val = str(Y) + str(Z) + str(A) + str(B)

    hash_1 = hashlib.sha256(c_val.encode('utf-8'))  

    # print(''.join('{:02x}'.format(x) for x in hash_1.digest()))
    c = int.from_bytes(hash_1.digest(), 'little', signed='True')


    # s = (k - c * x) % p
    s = (k - c * x)

    if s < 0:
        val1 = pow(g, -s, p) 
        # val1 = libnum.invmod(pow(g, as, p),p)
        val2 = pow(h, -s,  p) 
        # val2 = libnum.invmod(pow(h, s,  p),p)

        val1 = libnum.xgcd(val1, p)  
        # TODO: DO we need that check?
        if (val1[2] < 0):
            val1 = val1[2] + p
        else:
            val1 = val1[2]
        
        val2 = libnum.xgcd(val2, p)   
        if (val2[2] < 0):
            val2 = val2[2] + p
        else:
            val2 = val2[2]

    else:
        # Modular Exponentiation
        val1 = pow(g, s, p) 
        val2 = pow(h, s,  p) 

    if c < 0:
        val3 = pow(Y, -c, p)
        # val3 = libnum.invmod(pow(Y, c, p),p)
        val4 = pow(Z, -c,  p) 
        # val4 = libnum.invmod(pow(Z, c,  p),p)

        val3 = libnum.xgcd(val3, p)[0]
        # # TODO: Do we need that check?
        if (val3 < 0):
            val3 = val3 + p

        val4 = libnum.xgcd(val4, p)[0]
        if (val4 < 0):
            val4 = val4 + p

    else:
        val3 = pow(Y, c, p) 
        val4 = pow(Z, c, p) 

    A2 = (val1 * val3) % p
    B2 = (val2 * val4) % p
    
    c_val_2 = str(Y) + str(Z) + str(A2) + str(B2)

    hash_2 = hashlib.sha256(c_val_2.encode())  

    # c_ = hash_2.digest() % p
    c2 = int.from_bytes(hash_2.digest(), 'little', signed='True')

    if c == c2:
        print("Proven!")
    else:
        print("Not Proven!")
    
    return


if __name__ == "__main__":
    main()