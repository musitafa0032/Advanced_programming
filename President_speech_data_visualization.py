import os,json
import argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


speech_dir = r'C:/Users/Dell/Desktop/course/Semester2/test/'
parser = argparse.ArgumentParser()
parser.add_argument("--terms",help="a list of up to five items",nargs=(1,5),type=str)
parser.add_argument("--path",help="speech directory", nargs='?',type=str, default=speech_dir)
parser.add_argument("--title",help="plot title",nargs='?',type=str, default=None)
parser.add_argument("--output",help="plot name",nargs='?',type=str, default=None)
args=parser.parse_args()


speech_list=list()
speech_date=list()

try:
    files=os.listdir(speech_dir)
    for file in files:
        with open(args.path+file,"r") as infile:
            speech = json.load(infile)
            speech_list.append(speech["Speech"])
            speech_date.append(speech["Date"])
except OSError:
    print(f' Watch out! path {args.path} does not exist')
        
D=[]
S=[]
T=[]
nomatch=[]
in_list=[]

vectorizer = TfidfVectorizer(stop_words="english",ngram_range=(1,3))
x=vectorizer.fit_transform(speech_list)
x=np.asarray(x.todense())
words_list=vectorizer.get_feature_names()
targets=[]
for word in args.terms:
    targets.append(word)
for n in range(x.shape[0]):
    for target in targets:
        try:
            i=words_list.index(target)
            in_list.append(i)
            T.append(target)
        except ValueError:
            nomatch.append(target)

for word in set(nomatch):
    print(f'{word} does not exist')

if len(in_list) != 0:
        for n in range(x.shape[0]):
            for i in in_list[:len(set(T))]:
                S.append(x[n][i])
                D.append(speech_date[n])



df = pd.DataFrame({"Date": D,"Score":S,"Terms":T})
df["Date"]=pd.to_datetime(df.Date)
sns.set(style="whitegrid")

if args.title != None:
    sns.lineplot(data=df,x="Date",y="Score",hue="Terms").set_title(args.title)
else:
    sns.lineplot(data=df,x="Date",y="Score",hue="Terms")

if args.output == None:
    s=" ".join(targets)
    output_name=s.replace(" ","_")
    plt.savefig(output_name+'.png')   
else:
    plt.savefig(args.output+'.png')

