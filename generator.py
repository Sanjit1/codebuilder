import sympy
from google.cloud import translate
import json
import random

def header(n, name):
    return {
        "timed": 0,
        "count": n,
        "questions": list(range(1,n+1)),
        "title": name,
        "useCustomHeader":False,
        "customHeader":"",
        "testtype":"cstate"
    }
    
def keyStringRandom():
    spl = lambda word: [char for char in word]
    A = spl("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    while not test1(A):
        random.shuffle(A)
    return "".join(A)

def test1(l):
    for i in range(26):
        if ord(l[i])-65==i:
            return False
    return True
    
def genRandMono(num, quote, pat, mode, hint):
    key = keyStringRandom()
    r = {}
    for i in range(0, 26):
        r[chr(i+65)] = key[i]
    x = {
        "cipherString":quote,
        "encodeType":"random",
        "offset":1,
        "shift":1,
        "offset2":1,
        "keyword":"",
        "keyword2":"",
        "alphabetSource":"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "alphabetDest":key,
        "curlang":"en",
        "replacement": r,
        "editEntry":str(num)
    }
    if pat=="1":
        x["cipherType"] = "patristocrat"
        x["question"] = "<p>Solve this patristocrat.</p>"
        x["points"] = 600
    else:
        x["cipherType"] = "aristocrat"
        x["question"] = "<p>Solve this aristocrat.</p>"
        x["points"] = 250
    return x


def genRandAffine(num, quote, enc):
    a = random.choice([3, 5, 7, 9, 11, 15, 17, 19, 21, 23])
    b = random.randint(3, 24)
    r = {}
    for i in range(0, 26):
        r[str(i+65)] = chr((i*a+b)%26+65)
    x = {
        "a":a,
        "b":b,
        "cipherString":quote,
        "cipherType":"affine",
        "solclick1":-1,
        "solclick2":-1,
        "replacement":r,
        "curlang":"en",
        "editEntry":num
    }
    if enc=="E":
        x["operation"]="encode"
        x["points"]=175
        x["question"]='<p>Encode this sentence with the Affine cipher. (a,b)=('+str(a)+','+str(b)+').</p>'
    elif enc=="D":
        x["operation"]="decode"
        x["points"]=150
        x["question"]='<p>Decode this sentence which has been encoded with an Affine cipher. (a,b)=('+str(a)+','+str(b)+').</p>'
    elif enc=="C":
        one = random.randint(0,13)
        two = random.randint(13,26)
        onemap = (one*a+b)%26
        twomap = (two*a+b)%26
        x["operation"]="crypt"
        x["points"]=200
        x["question"]="<p>Decode this sentence which has been encoded with an Affine cipher. The letters "+chr(onemap+65)+" and "+chr(twomap+65)+" map to "+chr(one+65)+" and "+chr(two+65)+".</p>"
    return x
    
def genRandCaesar(num, quote, enc):
    a = random.randint(3, 24)
    r = {}
    for i in range(0, 26):
        r[str(i+65)] = chr((i+a)%26+65)
    x = {
        "offset":a,
        "offset2":None,
        "cipherString":quote,
        "cipherType":"caesar",
        "solclick1":-1,
        "solclick2":-1,
        "replacement":r,
        "curlang":"en",
        "editEntry":num,
        "shift":None
    }
    if enc=="E":
        x["operation"]="encode"
        x["points"]=150
        x["question"]="<p>Encode this sentence with the Caesar cipher with offset "+str(a)+".</p>"
    elif enc=="D":
        x["operation"]="decode"
        x["points"]=125
        x["question"]="<p>Decode this sentence which has been encoded with an Caesar cipher.</p>"
    return x
    
def genRandVig(num, quote, enc):
    key = getRandWord(5, 8)
    x = {
    "cipherType": "vigenere",
    "keyword": key,
    "cipherString": quote,
    "findString": "",
    "blocksize": len(key),
    "curlang": "en",
    "editEntry": str(num)
    }
    if enc=="E":
        x["operation"] = "encode",
        x["question"] = "<p>Encode this sentence with the Vigenere cipher using the keyword "+key+".",
        x["points"] = "200"
    if enc=="D":
        x["operation"] = "decode",
        x["question"] = "<p>Decode this sentence with the Vigenere cipher using the keyword "+key+".",
        x["points"] = "175"
    if enc=="C":
        x["operation"] = "crypt",
        x["question"] = "<p>Decode this sentence with the Vigenere cipher. The first "+str(len(key))+" characters of the sentence is "+quote[:len(key)]+".",
        x["points"] = "175"
    return x
    

def genRand2x2Hill(num, quote, enc):
    quote = quote.split(" ")
    q = ""
    a = 0
    while len(q)<12:
        q+=quote[a]+" "
        a+=1
    q=q[:-1]
    key = get2x2Key()
    x = {
        "cipherString":q,
        "cipherType":"hill",
        "curlang":"en",
        "editEntry":num,
        "keyword": key
    }
    if enc=="C":
        x["points"]=100
        x["question"]="<p>Compute the decryption matrix of the key "+key+".</p>"
        x["cipherString"]=""
    else:
        x["offset"]=None
        x["alphabetSource"]=""
        x["alphabetDest"]=""
        x["shift"]=None
        x["offset2"]=None
    if enc=="E":
        x["operation"]="encode"
        x["points"]=225
        x["question"]="<p>Encrypt this phrase with the key "+key+" using the Hill cipher.</p>"
    if enc=="D":
        x["operation"]="decode"
        x["points"]=175
        x["question"]="<p>Decrypt this phrase with the key "+key+" using the Hill cipher.</p>"
    return x

def RSA(num, enc):
    p = sympy.randprime(200,2000)
    q = sympy.randprime(200,2000)
    n = p*q
    phi = (p-1)*(q-1)
    e = sympy.randprime(0,n)
    while sympy.gcd(e,phi)!=1:
        e = sympy.randprime(0,n)
    d = sympy.mod_inverse(e, phi)
    x = {
        "cipherString":"",
        "cipherType":"rsa",
        "curlang":"en",
        "editEntry":"1308",
        "offset":None,
        "alphabetSource":"",
        "alphabetDest":"",
        "shift":None,
        "offset2":None,
        "name1":"Allen",
        "rsa": {
            "p": p,
            "q": q,
            "n": n,
            "phi": phi,
            "e": e,
            "d": d
        }
    }
    if enc=="E":
        x["operation"]="rsa2"
        x["digitsPrime"]=4
        x["digitsCombo"]=4
        x["points"]=450
        x["combo"]=1000
        x["question"]="<p>Given primes (p,q)=("+str(p)+","+str(q)+"), compute the private key d.</p>"
    if enc=="D":
        year = random.randint(1950,2000)
        enc = pow(year,e,n)
        x["operation"]="rsa4"
        x["digitsPrime"]=4
        x["digitsCombo"]=4
        x["points"]=350
        x["year"]=year
        x["encrypted"]=enc
        x["name2"]="Jason"
        x["question"]="<p>Given (n,e,c,d)=("+str(n)+","+str(e)+","+str(enc)+","+str(d)+"), compute the original message m.</p>"
    return x

def getRandWord(min, max):
    f = open("words.txt", "r")
    for i in range(random.randint(0,9000)):
        f.readline()
    r = ''
    while len(r)<min or len(r)>max:
        r=f.readline().strip()
    return r

def genQuotes(n):
    json_file = open('quotes.json', 'r')
    l = []
    data = json.load(json_file)
    for p in data['quotes']:
        l.append(p['text'])
    random.shuffle(l)
    count = 0
    loc = 0
    r = []
    while count<n:
        if len(l[loc])>70 and len(l[loc])<160:
            r.append(l[loc])
            count+=1
        loc+=1
    return r

def getDeterminant(l):
    if len(l)==4:
        return (l[1]*l[2]-l[0]*l[3])%26
    return 0

def get2x2Key():
    determinant=0
    while (determinant%2==0 or determinant%13==0):
        l = random.sample(range(0,26),4)
        determinant=getDeterminant(l)
    return "".join(chr(i+97) for i in l)

def genTest():
    n = int(input("Number of Questions: "))
    na = input("Test Name: ")
    print("1\tAristocrat\t\tK1\t1\t\tWord Hint\t0")
    print("2\tPatristocrat\t\tK2\t2\t\tCharacter Hint\t1")
    print("3\tAffine\t\t\tDecode\tD\t\tNo Hint \t2")
    print("4\tCaesar\t\t\tEncode\tE")
    print("5\tVigenere\t\tCrypt\tC")
    print("6\t2x2 Hill")
    print("7\t3x3 Hill")
    print("8\tXenocrypt")
    print("9\tBaconian")
    print("10\tRSA")
    print("11\tMorbit")
    print("12\tPollux")
    test = {
        "TEST.0": header(n,na)
    }
    l = []
    q = genQuotes(n+1)
    for i in range(n):
        l.append(input("Q"+str(i+1)+": "))
    test["CIPHER.0"]=genRandMono(0, q[len(q)-1], False, 0, 0)
    for i in range(n):
        question = l[i].split(" ")
        if int(question[0])<=2:
            test["CIPHER."+str(i+1)]=genRandMono(i, q[i], "1" if question[0]=="2" else 0, question[1], question[2])
        if int(question[0])==3:
            test["CIPHER."+str(i+1)]=genRandAffine(i, q[i], question[1])
        if int(question[0])==4:
            test["CIPHER."+str(i+1)]=genRandCaesar(i, q[i], question[1])
        if int(question[0])==5:
            test["CIPHER."+str(i+1)]=genRandVig(i, q[i], question[1])
        if int(question[0])==6:
            test["CIPHER."+str(i+1)]=genRand2x2Hill(i, q[i], question[1])
        if int(question[0])==10:
            test["CIPHER."+str(i+1)]=RSA(i, question[1])
    file = open(na+".json", "w")
    print(test)
    file.write(json.dumps(test))
    file.close()

genTest()
