#preprocess
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import pandas
from nltk.corpus import stopwords
import re
import unicodedata
from nltk.tag.stanford import CoreNLPNERTagger
import urllib2

#url = r"C:\Users\Akshat\Documents\dumps\company_lemmatize.csv"
#url = r"C:\Users\Akshat\Documents\dumps\lemm_all.csv"
url2 = r"C:\Users\Akshat\Documents\dumps\dirty_data2.csv"

#java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000


data = pandas.read_csv(url2,header=None)
dat = data.values
#print dat
x = dat.tolist()
#print type(x)
#print x
X_flat=[]
token =[]
xl=[]
yl=[]


for i in x:
    for j in i:
        X_flat.append(j)    #flattening 

for i in X_flat:
    token.append(word_tokenize(i))

for j in token:                             ####alpha numeric only
    for w in j:
        re.sub('[^A-Za-z0-9]+', '', w)

#print token
bag = ['limited','Limited','PRIVATE','LIMITED','ltd','Ltd',
       'ltd.','LTD','LTD.','Ltd.','Pvt.Ltd','PVT.LTD','pvt.ltd','Pvt.ltd','Ind.ltd',
       'pvt','Pvt','PVT','private','Private','INDIA','co.','CO','CO.','Co.','CO.Pvt','(',',']
StopBag=["surat",'dubai']
stop = set(stopwords.words('english') + bag + StopBag )
index = None

for i in range(len(token)):
        
        li = token[i]
        for word in li:
            if word in bag :
                index = li.index(word)    ####truncate trailing clutter
                break
            else:
                index = None

        token[i] = li[0:index]

#print token

for lis in token:
    for word in lis:                        ####remove stop words
        if word in stop:
            lis.remove(word)
        else:
            pass
        
#print token


def lemma(x):
    lem = WordNetLemmatizer()
    for i in range(len(x)):                     #####LEMMATIZE
        for j in range(len(x[i])):
            try:
                x[i][j] = lem.lemmatize(x[i][j]).encode('ascii','ignore')
            except Exception as e:
               print e 
               print j
               #break
    return x
tok = lemma(token)
#print tok

lis=[]

def detokenize(y):
    for u in y:
        uc = "".join([" " +r if not r.startswith("'") and r not in string.punctuation else r for r in u]).strip()
        lis.append(uc)
    return lis  

to = detokenize(tok)


def FirstCaps(x):
    for i in range(len(x)):
        x[i] = string.capwords(x[i])
    return x

toke = FirstCaps(to)

#print x

#print "after operation ::\n\n"

#print "Nooowww :::::::::::::::::::::"

tok = filter(None,toke)

#print len(tok)

def flatten(x):
    x_flat = []
    for i in x:
        for j in i:
            x_flat.append(j)
    return x_flat

def ner(x):
    cnlp = CoreNLPNERTagger
    t = []
    k =[]
    v = []
    for i in x:
        t.append(word_tokenize(i))
    #print t

    for i in t:
        
        for j in range(len(i)):
                
            i[j]=cnlp(url="http://localhost:9000/").tag(i[j].split())

    
    mainLis = t
    #print MainLis
    for MinLis in mainLis:
        for miniLis in MinLis:
            for tup in miniLis:
                miniLis[miniLis.index(tup)] = list(tup)
    for i in mainLis:
        for j in i:
            mainLis[mainLis.index(i)][i.index(j)] = flatten(j)
    for i in mainLis:
        mainLis[mainLis.index(i)] = flatten(i)

    for i in mainLis:
        for j in range(len(i)):
            mainLis[mainLis.index(i)][j] = i[j].encode('ascii')
            
    return mainLis

try:
    taggedList =  ner(tok)
except Exception as e:
    print e


#print taggedList

    
banTags = set(['COUNTRY','CITY','LOCATION'])

for i in taggedList:
    if(i[-1] in banTags):
        taggedList[taggedList.index(i)] = i[:len(i)-2]

    else:
        pass

#print taggedList

for i in taggedList:

    del i[1::2]
    taggedList[taggedList.index(i)]= i

for i in taggedList:
    print i

    
        
        
            




        




    

