import random
import util, keystore, bitcoin
import argparse
import sys
import threading
import os
import time
from time import sleep
from util import json_encode, print_msg
import json



MAX_THREADS=6
TARGET_ADDR="1L6rCPLm6YLfjxP3Besw49R3Qsei3Wt1DV"
MAX_ADDR_IDX=1


# Array of BIP39 words to use
with open('AZword0.txt','r') as L2:
    SEED_ARRAY = [word.strip() for word in L2]
##SEED_ARRAY=["peanut", "glow", "gravity", "gospel", "limb", "place", "early", "buzz", "pitch",
##            "payment", "view", "sleep", "pipe", "witness", "peanut", "future", "pumpkin", "matrix" ]


def my_shuffle(array):
    random.shuffle(array)
    return array
    
    
def combinations(n, list, combos=[]):
    # initialize combos during the first pass through
    if combos is None:
        combos = []

    if len(list) == n:
        # when list has been dwindeled down to size n
        # check to see if the combo has already been found
        # if not, add it to our list
        if combos.count(list) == 0:
            combos.append(list)
            combos.sort()
        return combos
    else:
        # for each item in our list, make a recursive
        # call to find all possible combos of it and
        # the remaining items
        for i in range(len(list)):
            refined_list = list[:i] + list[i+1:]
            combos = combinations(n, refined_list, combos)
        return combos
        
def deriveAddresses(line, xprv, i):
    xprv2, _xpub = bitcoin.bip32_private_derivation(xprv, "", str(i))
    btc_addr = xpub2btc(_xpub)
    print(line,'\n',btc_addr)
    if (TARGET_ADDR.lower()):
        privkey = xprv2btc(xprv2)
        if (TARGET_ADDR.lower() == btc_addr.lower()):
            print("FOUND PUZZLE PRIZE: " + privkey)
            win = open("SOLVED.txt", "a")
            win.write("WINNING SEED: "+line + "\n")
            win.write("ADDRESS: "+btc_addr + "\n")
            win.write("PRIVKEY: "+privkey + "\n")



def checkPassphrase(line):
    passw = ""

    seed = util.bh2u(keystore.bip39_to_seed(line, passw))
    seed = util.bfh(seed)
    xprv, _xpub = bitcoin.bip32_root(seed, "standard")
    xprv, _xpub = bitcoin.bip32_private_derivation(xprv, "", "44'")
    xprv, _xpub = bitcoin.bip32_private_derivation(xprv, "", "0'")
    xprv, _xpub = bitcoin.bip32_private_derivation(xprv, "", "0'")
    xprv, _xpub = bitcoin.bip32_private_derivation(xprv, "", "0")
    for i in range(MAX_ADDR_IDX):
        deriveAddresses(line, xprv, i)

def xpub2btc(xpub):
    _xtype, _depth, _fp, _cn, _c, K = bitcoin.deserialize_xpub(xpub)
    return bitcoin.pubkey_to_address("p2pkh", util.bh2u(K))

def xprv2btc(xprv):
    _xtype, _depth, _fp, _cn, _c, k = bitcoin.deserialize_xprv(xprv)
    privkey = bitcoin.serialize_privkey(k, True, "p2pkh")
    return privkey

def main():
    SEED_COUNTER=0
    VALID_SEED_COUNT=0

    TOTAL_COUNTER=0
    SEED_START_TIME=time.time()
    while True:
        # GENERATE NEW SEED PHRASE
        word=""
        WORD_COUNT=0
        SEED_TO_TEST=''
        for suit in my_shuffle(SEED_ARRAY):
            if (WORD_COUNT <= 11): 
                word=word+" "+suit
                WORD_COUNT+= 1
            if (WORD_COUNT == 12): 
                line = word
                threads = []                
                SEED_COUNTER+=1
                if (SEED_COUNTER >= 1000):
                    TOTAL_COUNTER+=SEED_COUNTER
                    SEED_COUNTER=0
                    TIME_SINCE=time.time()-SEED_START_TIME
                    print("[BRUTEFORCE] Checked "+str(TOTAL_COUNTER)+" seeds and found "+str(VALID_SEED_COUNT)+" valid seeds in "+str(TIME_SINCE)+" seconds." )
                    

         
                (checksum_ok, wordlist_ok) = keystore.bip39_is_checksum_valid(line)
                if not wordlist_ok:
                    print("       Unknown words!" + line, file=sys.stderr)
                    continue
                if not checksum_ok:
                    #print("       Checksum NOT OK!" + line, file=sys.stderr)
                    continue
                #print("       Check passed. Queued:  " + line)
                VALID_SEED_COUNT+=1

                t = threading.Thread(target=checkPassphrase, args=(line,))
                threads.append(t)
                t.start()

                if len(threads) == MAX_THREADS:
                    for t in threads:
                        t.join()

                    threads.clear()

if __name__ == "__main__":
    main()
