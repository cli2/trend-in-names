## -------- this part generate csv files to be used in R -------- ##
import urllib2, re, json, time, sys, random
reload(sys)
sys.setdefaultencoding('utf-8')

with open(r'babyname_f.json','r') as f:
    lines = f.readlines()
    bb_f = json.loads(lines[0])
with open(r'babyname_m.json','r') as f:
    lines = f.readlines()
    bb_m = json.loads(lines[0])
with open(r'act.json','r') as f:
    lines = f.readlines()
    actors = json.loads(lines[0])

## ----- calculate influence rate
def cal_influence(year_3,year_2,year_1,year_0,year_m1,year_m2,year_m3):
    in_32 = (year_3-year_2)/float(year_2)
    in_21 = (year_2-year_1)/float(year_1)
    in_10 = (year_1-year_0)/float(year_0)
    in_01 = (year_0-year_m1)/float(year_m1)
    in_12 = (year_m1-year_m2)/float(year_m2)
    in_23 = (year_m2-year_m3)/float(year_m3)
    influence_rate = in_32+in_21+in_10-in_01-in_12-in_23
    return influence_rate
def get_number(year,year_str):
    if int(year)==int(year_str[0]):
        return int(year_str[1])
    else:
        return 100

influnece_rate_dict = {}
with open("influence_rate.csv",'w') as f:
    f.write("Year"+','+"FirstName"+','+"FullName"+','+"InfluenceToBoy"+','+"InfluenceToGirl"+'\n')
    for year in actors.keys():
        for fullname in actors[year]:
            firstname = fullname.split(" ")[0]
            if firstname in bb_f.keys():
                year0 = int(year)
                yearm1 = year0-1
                yearm2 = year0-2
                yearm3 = year0-3
                year3 = year0+3
                year2 = year0+2
                year1 = year0+2
                year_3 = year_2=year_1=year_0=year_m1=year_m2=year_m3=100
                for i in bb_f[firstname]:
                    if get_number(year3,i)!=100: year_3 = get_number(year3,i)
                    if get_number(year2,i)!=100: year_2 = get_number(year2,i)
                    if get_number(year1,i)!=100: year_1 = get_number(year1,i)
                    if get_number(year0,i)!=100: year_0 = get_number(year0,i)
                    if get_number(yearm3,i)!=100: year_m3 = get_number(yearm3,i)
                    if get_number(yearm2,i)!=100: year_m2 = get_number(yearm2,i)
                    if get_number(yearm1,i)!=100: year_m1 = get_number(yearm1,i)
                # print(year_2,firstname,year2)
                # print bb_f[firstname]
                influence_rate_f = cal_influence(year_3,year_2,year_1,year_0,year_m1,year_m2,year_m3)
            else:
                influence_rate_f = -1
            if firstname in bb_m.keys():
                year0 = int(year)
                yearm1 = year0-1
                yearm2 = year0-2
                yearm3 = year0-3
                year3 = year0+3
                year2 = year0+2
                year1 = year0+2
                year_3 = year_2=year_1=year_0=year_m1=year_m2=year_m3=100
                for i in bb_m[firstname]:
                    if get_number(year3,i)!=100: year_3 = get_number(year3,i)
                    if get_number(year2,i)!=100: year_2 = get_number(year2,i)
                    if get_number(year1,i)!=100: year_1 = get_number(year1,i)
                    if get_number(year0,i)!=100: year_0 = get_number(year0,i)
                    if get_number(yearm3,i)!=100: year_m3 = get_number(yearm3,i)
                    if get_number(yearm2,i)!=100: year_m2 = get_number(yearm2,i)
                    if get_number(yearm1,i)!=100: year_m1 = get_number(yearm1,i)
                # print(year_2,firstname,year2)
                # print bb_f[firstname]
                influence_rate_m = cal_influence(year_3,year_2,year_1,year_0,year_m1,year_m2,year_m3)
            else:
                influence_rate_m = -1
            f.write(year+','+firstname+','+fullname+','+str(influence_rate_m)+','+str(influence_rate_f)+'\n')
            influnece_rate_dict[fullname] = (influence_rate_m,influence_rate_f)
with open("influence_rate.json",'w') as f:
    f.write(json.dumps(influnece_rate_dict))
