import json
import random
def header(n, name):
    ret = '{"TEST.0":{"timed":2,"count":'+str(n+1)+',"questions":['
    for i in range(n):
        ret+=str(i+2)+","
    ret=ret[:-1]
    ret+="],"
    ret+='"title":"'+name+'","useCustomHeader":false,"customHeader":"","testtype":"cregional"},'
    return ret
    
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
    
def genRandAristo(num,quote):
    key = keyStringRandom()
    ret = '"CIPHER.'+str(num)+'":{"cipherString":"'+quote+'","cipherType":"aristocrat","encodeType":"random","offset":1,"shift":1,"offset2":1,"keyword":"","keyword2":"","alphabetSource":"ABCDEFGHIJKLMNOPQRSTUVWXYZ","alphabetDest":"'+key+'","curlang":"en","replacement":{'
    for i in range(26):
        ret+='"'+chr(i+65)+'":"'+key[i]+'",'
    ret=ret[:-1]
    ret+= '},"points":250,"question":"<p>Solve this</p>","editEntry":"'+str(num)+'"},'
    return ret
    
def genRandPatristo(num,quote):
    key = keyStringRandom()
    ret = '"CIPHER.'+str(num)+'":{"cipherString":"'+quote+'","cipherType":"patristocrat","encodeType":"random","offset":1,"shift":1,"offset2":1,"keyword":"","keyword2":"","alphabetSource":"ABCDEFGHIJKLMNOPQRSTUVWXYZ","alphabetDest":"'+key+'","curlang":"en","replacement":{'
    for i in range(26):
        ret+='"'+chr(i+65)+'":"'+key[i]+'",'
    ret=ret[:-1]
    ret+= '},"points":550,"question":"<p>Solve this</p>","editEntry":"'+str(num)+'"},'
    return ret

def genRandAffine(num, quote, enc):
    a = random.choice([3, 5, 7, 9, 11, 15, 17, 19, 21, 23])
    b = random.randint(3, 24)
    ret = '"CIPHER.'+str(num)+'":{"operation":"'
    if enc==0:
        ret+="encode"
    elif enc==1:
        ret+="decode"
    elif enc==2:
        ret+="crypt"
    ret+='","a":'+str(a)+',"b":'+str(b)+',"cipherString":"'+quote+'","cipherType":"affine","solclick1":-1,"solclick2":-1,"replacement":{'
    for i in range(65, 91):
        m = chr(((i-65)*a+b)%26+65)
        ret+='"'+chr(i)+'":"'+m+'",'
    ret=ret[:-1]
    ret+='},"curlang":"en","points":'
    if enc==0:
        ret+="175"
    elif enc==1:
        ret+="150"
    elif enc==2:
        ret+="200"
    ret+=',"question":"<p>'
    if enc==0:
        ret+='Encode this sentence with the Affine cipher. (a,b)=('+str(a)+','+str(b)+').'
    elif enc==1:
        ret+='Decode this sentence which has been encoded with an Affine cipher. (a,b)=('+str(a)+','+str(b)+').'
    elif enc==2:
        one = random.randint(0,13)
        two = random.randint(13,26)
        onemap = (one*a+b)%26
        twomap = (two*a+b)%26
        ret+="Decode this sentence which has been encoded with an Affine cipher. The letters "+chr(one+65)+" and "+chr(two+65)+" map to "+chr(onemap+65)+" and "+chr(twomap+65)+"."
    ret+='</p>","editEntry":"'+str(num)+'"},'
    return ret

def genRandCaesar(num, quote, enc):
    a = random.randint(3,24)
    ret = '"CIPHER.'+str(num)+'":{"operation":"'
    if enc:
        ret+="encode"
    else:
        ret+="decode"
    ret+='","offset":'+str(a)+',"cipherString":"'+quote+'","cipherType":"caesar","replacement":{'
    for i in range(65, 91):
        m = chr(((i-65)+a)%26+65)
        ret+='"'+chr(i)+'":"'+m+'",'
    ret=ret[:-1]
    ret+='},"curlang":"en","points":'
    if enc:
        ret+="150"
    else:
        ret+="125"
    ret+=',"question":"<p>'
    if enc:
        ret+="Encode this sentence with the Caesar cipher with offset "+str(a)+"."
    else:
        ret+="Decode this sentence which has been encoded with an Caesar cipher."
    ret+='</p>","editEntry":"'+str(num)+'"},'
    return ret

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

def genTest():
    n = int(input("Number of Questions: "))
    na = input("Test Name: ")
    print("1a = Aristocrat, 2a = Patristocrat, 3a = Affine Encode, 3b = Affine Decode, 3c = Affine Cryptanalysis, 4a = Caesar Encode, 4b = Caesar Decode")
    l = []
    q = genQuotes(n)
    for i in range(n):
        l.append(input("Q"+str(i+1)+": "))
    t = header(n,na)
    for i in range(n):
        if l[i]=="1a":
            t+=genRandAristo(i+2, q[i])
        elif l[i]=="2a":
            t+=genRandPatristo(i+2, q[i])
        elif l[i]=="3a":
            t+=genRandAffine(i+2, q[i], 1)
        elif l[i]=="3b":
            t+=genRandAffine(i+2, q[i], 0)
        elif l[i]=="3c":
            t+=genRandAffine(i+2, q[i], 2)
        elif l[i]=="4a":
            t+=genRandCaesar(i+2, q[i], False)
        elif l[i]=="4b":
            t+=genRandCaesar(i+2, q[i], True)
        else:
            print("You fucked up, try again")
            exit()
    t=t[:-1]+"}"
    file = open(na+".json", "w")
    file.write(t)
    file.close()

genTest()
