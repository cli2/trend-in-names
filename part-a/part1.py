## -------- this part collects and manipulates data and save data into json files -------- ##
import urllib2, re, json, time, sys
from bs4 import BeautifulSoup
from collections import OrderedDict
reload(sys)
sys.setdefaultencoding('utf-8')

## -------- parse wikipedia -------- ##

response_m = urllib2.urlopen('https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor')
response_f = urllib2.urlopen('https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actress')
html_m = response_m.read()
html_f = response_f.read()
#-parse actors and store in a dict
s_m = BeautifulSoup(html_m,'lxml')
table_m = s_m.find_all('table',{'class':"wikitable sortable"})[0].find_all('tr')
dict_m = {}
for i in range(len(table_m)):
    if table_m[i].find_all('td', {'style': "background:#FAEB86"}) != []:
        if table_m[i].find_all('th') != []:
            dict_m[table_m[i].find_all('th')[0].find_all('a')[0].string] = [table_m[i].find_all('td')[0].find_all('a')[0].string]
        else:
            dict_m[table_m[i-1].find_all('th')[0].find_all('a')[0].string].append(table_m[i].find_all('td')[0].find_all('a')[0].string)
#-parse actresses and store in a dict
s_f = BeautifulSoup(html_f,'lxml')
table_f = s_f.find_all('table',{'class':"wikitable sortable"})[0].find_all('tr')
dict_f = {}
for i in range(len(table_f)):
    if table_f[i].find_all('td', {'style': "background:#FAEB86"}) != []:
        if table_f[i].find_all('th') != []:
            dict_f[table_f[i].find_all('th')[0].find_all('a')[0].string] = [table_f[i].find_all('td')[0].find_all('a')[0].string]
        else:
            dict_f[table_f[i-1].find_all('th')[0].find_all('a')[0].string].append(table_f[i].find_all('td')[0].find_all('a')[0].string)
with open(r'acad_actors.json','w') as f:
    f.write(json.dumps(dict_m))
with open(r'acad_actress.json','w') as f:
    f.write(json.dumps(dict_f))
print "html parsing finished"

## -------- extract baby names and years-------- ## store in a dict whose key is the name, value is a list of tuples (year,number)

bb_m = {}
bb_f = {}
th = 100 #-threshold for lowest record of names
with open(r'data/NationalNames.csv','r') as f:
    lines = f.readlines()
    for line in lines[1:]:
        l = line.split(',')
        name = l[1]
        year = l[2]
        gender = l[3]
        count = l[4].rstrip('\n')
        if int(year)>=1927 and int(count)>th: #-turns out int() is faster than str comparison
            if gender == 'F':
                if name not in bb_f.keys():
                    bb_f[name] = [(year,count)]
                else:
                    bb_f[name].append((year,count))
            else:
                if name not in bb_m.keys():
                    bb_m[name] = [(year,count)]
                else:
                    bb_m[name].append((year,count))
with open(r'babyname_f.json','w') as f:
    f.write(json.dumps(bb_f))
with open(r'babyname_m.json','w') as f:
    f.write(json.dumps(bb_m))
print "baby names parsing finished"

## -------- parse imdb dataset -------- ##
dict_imdb = {}
dict_imdb_genre = {}
year = range(1927,2017)
for i in year:
    dict_imdb[str(i)]=[]
    dict_imdb_genre[str(i)]=[]
with open(r'data/movie_metadata.csv','r') as f:
    lines = f.readlines()
    for line in lines[1:]:
        l = line.split(',')
        a2 = l[6]
        a1 = l[10]
        a3 = l[14]
        year = l[23]
        genre = l[9]
        if year != '' and len(year)==4 and int(year)<2017 and int(year)>1926:
            if len(dict_imdb[year]) <=5:
                dict_imdb[year].append(a1)
                dict_imdb_genre[year].append((a1,genre))
                if len(dict_imdb[year]) <=5:
                    dict_imdb[year].append(a2)
                    dict_imdb_genre[year].append((a2,genre))
                    if len(dict_imdb[year]) <=5:
                        dict_imdb[year].append(a3)
                        dict_imdb_genre[year].append((a3,genre))
with open(r'imdb_act.json','w') as f:
    f.write(json.dumps(dict_imdb))
with open(r'imdb_act_genre.json','w') as f:
    f.write(json.dumps(dict_imdb_genre))
print "movie star parsing finished"

## -------- merge imdb with academy award -------- ## a better way to do this?

d_act = dict_imdb
for key in dict_f.keys():
    for i in dict_f[key]:
        d_act[key].append(i)
for key in dict_m.keys():
    for i in dict_m[key]:
        d_act[key].append(i)
with open(r'act.json','w') as f:
    f.write(json.dumps(d_act))
