## -------- this part generate the movie genre csv files to be used in R -------- ##
import urllib2, re, json, time, sys, random
reload(sys)
sys.setdefaultencoding('utf-8')

with open(r'imdb_act_genre.json','r') as f:
    lines = f.readlines()
    genre_list = json.loads(lines[0])
with open(r'influence_rate.json','r') as f:
    lines = f.readlines()
    influence_rate_dict = json.loads(lines[0])
with open(r'genre_pairs.csv','w') as f:
    f.write("FirstName"+","+"FullName"+","+"Genre"+","+"InfluenceToBoy"+","+"InfluenceToGirl"+"\n")
    for yearlist in genre_list.values():
        for pair in yearlist:
            name = pair[0]
            firstname = name.split(" ")[0]
            genres = pair[1].split("|")
            ir_m = 0;
            ir_f = 0;
            if name in influence_rate_dict.keys():
                ir_m = influence_rate_dict[name][0];
                ir_f = influence_rate_dict[name][1];
            for genre in genres:
                f.write(firstname+","+name+","+genre+","+str(ir_m)+","+str(ir_f)+"\n")
