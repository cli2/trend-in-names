## -------- this part analyzes and visualizes data -------- ##
import urllib2, re, json, time, sys
from bs4 import BeautifulSoup
from collections import OrderedDict
reload(sys)
sys.setdefaultencoding('utf-8')

## -------- retrieve data from stored files -------- ##
with open(r'babyname_f.json','r') as f:
    lines = f.readlines()
    bb_f = json.loads(lines[0])
with open(r'babyname_m.json','r') as f:
    lines = f.readlines()
    bb_m = json.loads(lines[0])
with open(r'actors.json','r') as f:
    lines = f.readlines()
    actors = json.loads(lines[0])

## -------- retrieve data from stored files -------- ##
#-- thirty most common first names of actors/actresses
act_name_oc = {}
for year in actors.keys():
    for name in actors[year]:
        first_name = name.split(' ')[0]
        if first_name in act_name_oc.keys():
            act_name_oc[first_name][0] += 1
            act_name_oc[first_name][1].append(year)
        else:
            act_name_oc[first_name] = [1, [year]]
sorted_act = OrderedDict(sorted(act_name_oc.items(), key = lambda x: x[1][0]))
choice_act = sorted_act.items()[-1:]
choice_bbn_m = {}
choice_bbn_f = {}
years = range(1927,2015)
for year in years:
    choice_bbn_f[str(year)] = "50"
    choice_bbn_m[str(year)] = "50"
for i in range(len(choice_act)):
    n = choice_act[i][0]
    if n in bb_f.keys():
        for item in bb_f[n]:
            if int(item[0]) in years:
                choice_bbn_f[item[0]] = item[1]
            else:
                choice_bbn_f[item[0]] = 50
    if n in bb_m.keys():
        for item in bb_m[n]:
            if int(item[0]) in years:
                choice_bbn_m[item[0]] = item[1]
            else:
                choice_bbn_m[item[0]] = 50
print actors['1966']
print choice_act[0][1]
with open(choice_act[0][0]+r'.csv','w') as f:
    f.write(choice_act[0][0]+','+'female'+','+'male'+'\n')
    for year in years:
        f.write(str(year)+','+choice_bbn_f[str(year)]+','+choice_bbn_m[str(year)]+'\n')
## -------- get the child count of the within up to 21 years for the actors -------- ##
## -------- after getting the trend, go back and analyze what kind of name have trends most -------- ##
