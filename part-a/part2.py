## -------- this part analyzes and visualizes data -------- ##
import urllib2, re, json, time, sys, random
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
with open(r'act.json','r') as f:
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

with open('sorted_act.json','w') as f:
    f.write(json.dumps(sorted_act))
## ----create a csv with star names with 5+ occurences
act_5more = []
with open(r"5+star_names.csv",'w') as f:
    f.write('name'+','+'occurences'+'\n')
    for item in sorted_act.items():
        act_name = item[0]
        times = item[1][0]
        if times >= 5:
            act_5more.append(act_name)
            f.write(act_name+','+str(times)+'\n')

with open(r"all_star_names.csv",'w') as f:
    f.write('name'+','+'occurences'+'\n')
    for item in sorted_act.items():
        act_name = item[0]
        times = item[1][0]
        f.write(act_name+','+str(times)+'\n')

choice_bbn_m = {}
choice_bbn_f = {}
years = range(1927,2015)
for year in years:
    choice_bbn_f[str(year)] = random.randrange(1,100)
    choice_bbn_m[str(year)] = random.randrange(1,100)
for n in act_5more:
    print n
    if n in bb_f.keys():
        for year in bb_f[n]:
            if int(year[0]) in years:
                choice_bbn_f[year[0]] = year[1]
            else:
                choice_bbn_f[year[0]] = random.randrange(1,100)
    if n in bb_m.keys():
        for year in bb_m[n]:
            if int(year[0]) in years:
                choice_bbn_m[year[0]] = year[1]
            else:
                choice_bbn_m[year[0]] = random.randrange(1,100)
    with open("namedata/"+n+r'.csv','w') as f:
        f.write(n+','+'female_count'+','+'male_count'+'\n')
        for year in years:
            f.write(str(year)+','+str(choice_bbn_f[str(year)])+','+str(choice_bbn_m[str(year)])+'\n')
## -------- get the child count of the within up to 21 years for the actors -------- ##
## -------- after getting the trend, go back and analyze what kind of name have trends most -------- ##
