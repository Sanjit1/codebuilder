import json
import random
f = open("quotes_dataset.csv", "r")
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
    print("1a = Aristocrat, 2a = Patristocrat")
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
        else:
            print("You fucked up, try again")
            exit()
    t=t[:-1]+"}"
    file = open(na+".json", "w")
    file.write(t)
    file.close()

genTest()
