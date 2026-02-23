import sys,requests
from bs4 import BeautifulSoup

P=53
MOD=2**64

#GETTING WORD FREQUENCIES FROM URL
def word_frequency(url):
    headers={ "User-Agent": "Mozilla/5.0"}
    page=requests.get(url,headers=headers,timeout=10)
    soup=BeautifulSoup(page.text,"html.parser")

    if soup.body:
        text=soup.body.get_text(separator=" ")
    else:
        text=""

    words=[]
    word=""
    for i in text:
        if i.isalnum():
            word+=i.lower()          
        else:
            if word:
                words.append(word)
                word=""
    if word:
        words.append(word)

    frequency={}
    for j in words:
        frequency[j]=frequency.get(j,0)+1
    return frequency
#Actualfrequencies for both urls
url1 = sys.argv[1]
url2 = sys.argv[2]
freq1 = word_frequency(url1)
freq2 = word_frequency(url2)
print("Unique words URL1:", len(freq1))
print("Unique words URL2:", len(freq2))
#POLYNOMIAL HASH
def polynomial_hash(word):
    h=0
    power=1
    for i in word:
        h+=ord(i)*power           
        power*=P
    return h & ((1<<64)-1)          
#SIMHASH
def calc_simhash(frequency):
    vector=[0]*64
    for i in frequency:
        h=polynomial_hash(i)
        for j in range(64):       
            if(h>>j)&1:
                vector[j]+=frequency[i]   
            else:
                vector[j]-=frequency[i]
    simhash=0
    for i in range(64):
        if vector[i]>0:
            simhash|=(1<<i)
    return simhash
#SIMHASH CALCULATION FROM THE FREQUENCIES 
simhash1 = calc_simhash(freq1)
simhash2 = calc_simhash(freq2)
common_bits = 0
for i in range(64):
    if ((simhash1 >> i) & 1) == ((simhash2 >> i) & 1):
        common_bits += 1

print("Simhash for url-1:", simhash1)
print("Simhash for url-2:", simhash2)
print("Common bits between url1 & url2:", common_bits)