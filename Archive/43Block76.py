import hashlib
import json
import mnemonic as mne
import bip32utils
import itertools
import random
import codecs
from playsound import playsound
# import sweep
import re
import time
import datetime
from numba import jit
import bitcoin
import keystore
import util
import json

c2 = 'f8e'
Win = '13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd'

with open('english.txt', 'r') as f:
    Bip39List = [word.strip() for word in f]


@jit
def EntropyToInt(x):
    xbytes = bytes.fromhex(x)
    # print(xbytes)
    xhash = hashlib.sha256(xbytes).hexdigest()
    # change back to 2 hex, so 0:2 with length 256
    return int(x + xhash[0:1], 16)


def MnemonicWordIndexes(x, Bip39List):
    word = []
    # change back to 0,24 with length 256
    for _ in range(0, 12):
        word_int = x & 2047
        x = x >> 11
        word.append(Bip39List[word_int])

    mnemonic_string = ' '.join(word[::-1])
    return (mnemonic_string)


@jit
def bip39(line, xprv, i):
    xprv2, _xpub = bitcoin.bip32_private_derivation(xprv, "", str(i))
    btc_addr = xpub2btc(_xpub)
    pvkey = xprv2btc(xprv2)
    # print(line,'\n')
    # print(btc_addr,'\n')
    # print(xprv2,'\n')
    # print(pvkey,'\n')
    return btc_addr, pvkey


def checkPassphrase(line):
    passw = ""

    seed = util.bh2u(keystore.bip39_to_seed(line, passw))
    seed = util.bfh(seed)
    xprv, _xpub = bitcoin.bip32_root(seed, "standard")
    xprv, _xpub = bitcoin.bip32_private_derivation(xprv, "", "44'")
    xprv, _xpub = bitcoin.bip32_private_derivation(xprv, "", "0'")
    xprv, _xpub = bitcoin.bip32_private_derivation(xprv, "", "0'")
    xprv, _xpub = bitcoin.bip32_private_derivation(xprv, "", "0")
    xprv2, btc_addr = bip39(seed, xprv, 0)
    return xprv2, btc_addr


def xpub2btc(xpub):
    _xtype, _depth, _fp, _cn, _c, K = bitcoin.deserialize_xpub(xpub)
    return bitcoin.pubkey_to_address("p2pkh", util.bh2u(K))


def xprv2btc(xprv):
    _xtype, _depth, _fp, _cn, _c, k = bitcoin.deserialize_xprv(xprv)
    privkey = bitcoin.serialize_privkey(k, True, "p2pkh")
    return privkey


@jit
def HashCheck(xx):
    x = hashlib.md5(xx.encode('utf-8')).hexdigest()
    # print(x)
    if x[:3] == c2:
        return True, x
    elif x[:3] != c2:
        return True, x
    return x


@jit
def TextToAddr(str):
    addr, pk = checkPassphrase(MnemonicWordIndexes(EntropyToInt(str), Bip39List))
    # print(addr)
    # 'path': "m/44'/0'/0'/" + str(i),
    # 'addr': bip32_child_key_obj.Address()
    # 'publickey': binascii.hexlify(bip32_child_key_obj.PublicKey()).decode(),
    # 'privatekey': bip32_child_key_obj.WalletImportFormat(),
    # 'coin': 'BTC'
    return addr, pk


@jit
def AddressCheck(x):
    if x == Win:
        return True


print(datetime.datetime.now())
ds = datetime.datetime.now()

# w4 = []
with open('76prayer.txt') as g:
    w4 = [lin.rstrip('\n') for lin in g]


##    for li in lit:
##        w4.append(li)

##w3 = map(str.capitalize, w4)
##w5 = map(str.lower, w4)


@jit
def chck():
    hitch = open('76next attempt43.txt', 'a')
    n = 0
    for r in w4:
        for s in w4:
            for t in w4:
                for u in w4:
                    for v in w4:
                        #if v != x:
                        # uu = '{} {}'.format(v,x)
                        # ch1 = HashCheck3(uu)
                        # ch2 = HashCheck3(w+' '+x)
                        # if ch1 == True:# and ch2 == True:
                        hs1 = 'format TOMI {} {} {} {} {}'.format(r, s, t, u, v)
                        ck, hsh = HashCheck(hs1)
                        # print(hs1)
                        n = n + 1
                        # if ck == True:
                        addr, pk = TextToAddr(hsh)
                        hitch.write('\n' + hs1 + '\n' + addr + '\n' + pk)
                        hitch.flush()
                        print('\n' + str(n) + ' - ' + hs1 + '\n' + addr + '\n', pk)
                        if AddressCheck(addr) == True:
                            print('\n' + hs1 + '\n' + 'winner : ', addr, 'PrivateKey : ', pk)
                            playsound('zen.mp3')
                            hit = open('WINNER.txt', 'a')
                            hit.write('\n' + hs1 + '\n' + 'winner' + addr + ' PrivateKey: ' + pk)
                            hit.close()
                            # sweep.sweep(pk)
                            return


##                else:
##                    pass                  


chck()
dt = datetime.datetime.now() - ds
print(dt, datetime.datetime.now())
