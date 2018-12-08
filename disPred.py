######################## # # #Cleaning our data# # # #####################
import pandas as pd
import csv
from collections import defaultdict

disease_list = []

def return_list(disease):
    disease_list = []
    match = disease.replace('^','_').split('_')
    ctr = 1
    for group in match:
        if ctr%2==0:
            disease_list.append(group)
        ctr = ctr + 1

    return disease_list
#Writing our cleaned data
with open("Scraped-Data/dataset_uncleaned.csv") as csvfile:
    reader = csv.reader(csvfile)
    disease=""
    weight = 0
    disease_list = []
    dict_wt = {}
    dict_=defaultdict(list)
    for row in reader:

        if row[0]!="\xc2\xa0" and row[0]!="":
            disease = row[0]
            disease_list = return_list(disease)
            weight = row[1]

        if row[2]!="\xc2\xa0" and row[2]!="":
            symptom_list = return_list(row[2])

            for d in disease_list:
                for s in symptom_list:
                    dict_[d].append(s)
                dict_wt[d] = weight

    # print (dict_)
with open("Scraped-Data/dataset_clean.csv","w") as csvfile:
    writer = csv.writer(csvfile)
    for key,values in dict_.items():
        for v in values:
            #key = str.encode(key)
            key = str.encode(key).decode('utf-8')
            #.strip()
            #v = v.encode('utf-8').strip()
            #v = str.encode(v)
            writer.writerow([key,v,dict_wt[key]])

columns = ['Source','Target','Weight']
data = pd.read_csv("Scraped-Data/dataset_clean.csv",names=columns, encoding ="ISO-8859-1")


data.to_csv("Scraped-Data/dataset_clean.csv",index=False)
slist = []
dlist = []
with open("Scraped-Data/nodetable.csv","w") as csvfile:
    writer = csv.writer(csvfile)

    for key,values in dict_.items():
        for v in values:
            if v not in slist:
                writer.writerow([v,v,"symptom"])
                slist.append(v)
        if key not in dlist:
            writer.writerow([key,key,"disease"])
            dlist.append(key)

nt_columns = ['Id','Label','Attribute']
nt_data = pd.read_csv("Scraped-Data/nodetable.csv",names=nt_columns, encoding ="ISO-8859-1",)

nt_data.to_csv("Scraped-Data/nodetable.csv",index=False)








####################### # # #Analysing our cleaned data# # # #########################
data = pd.read_csv("Scraped-Data/dataset_clean.csv", encoding ="ISO-8859-1")
# print(len(data['Source'].unique()))
# print(len(data['Target'].unique()))
df = pd.DataFrame(data)
df_1 = pd.get_dummies(df.Target)

df_s = df['Source']
df_pivoted = pd.concat([df_s,df_1], axis=1)
df_pivoted.drop_duplicates(keep='first',inplace=True)
# print(df_pivoted[:5])

cols = df_pivoted.columns
cols = cols[1:]
df_pivoted = df_pivoted.groupby('Source').sum()
df_pivoted = df_pivoted.reset_index()
# print(df_pivoted[:5])


df_pivoted.to_csv("Scraped-Data/df_pivoted.csv")
x = df_pivoted[cols]
y = df_pivoted['Source']
print(x)
print(y)

# # Trying out our classifier to learn diseases from the symptoms
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
mnb = MultinomialNB()
mnb = mnb.fit(x_train, y_train)
mnb.score(x_test, y_test)
print()






################# # # Inferences on train and test split# # ################
mnb_tot = MultinomialNB()
mnb_tot = mnb_tot.fit(x, y)
mnb_tot.score(x, y)

disease_pred = mnb_tot.predict(x)
disease_real = y.values
for i in range(0, len(disease_real)):
    if disease_pred[i]!=disease_real[i]:
        print ('Pred: {0} Actual:{1}'.format(disease_pred[i], disease_real[i]))






####################### # # Training a decision tree # # ###################
from sklearn.tree import DecisionTreeClassifier
print ("DecisionTree")
dt = DecisionTreeClassifier()
clf_dt=dt.fit(x,y)
print ("Acurracy: ", clf_dt.score(x,y))






from sklearn import tree 
####################### # # # Analysis of the Manual data # # # ######################################
data = pd.read_csv("Manual-Data/Training.csv")
#  # data.columns
df = pd.DataFrame(data)
# The manual data contains approximately 4920 rows.
cols = df.columns
cols = cols[:-1]
x = df[cols]
y = df['prognosis']





######################## #Trying out our classifier to learn diseases from the symptoms #######################
import seaborn as sns
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
mnb = MultinomialNB()
mnb = mnb.fit(x_train, y_train)
# print(mnb.score(x_test, y_test))

'''
from sklearn import model_selection  #changed from=> import cross_validation
print ("cross result========")
scores = model_selection.cross_val_score(mnb, x_test, y_test, cv=3)
print (scores)
print (scores.mean())
# We use the testing dataset to actually test our Multinomial Bayes model
'''
test_data = pd.read_csv("Manual-Data/Testing.csv")
# print(test_data.head())

testx = test_data[cols]
testy = test_data['prognosis']
mnb.score(testx, testy)






####################### # # # Training a decision tree# # # #######################
from sklearn.tree import DecisionTreeClassifier
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
print ("DecisionTree")
dt = DecisionTreeClassifier()
clf_dt=dt.fit(x_train,y_train)
print ("Acurracy: ", clf_dt.score(x_test,y_test))

'''
from sklearn import model_selection  #changed from=> import cross_validation
print ("cross result========")
scores = model_selection.cross_val_score(mnb, x_test, y_test, cv=3)
print (scores)
print (scores.mean())
'''

print ("Acurracy on the actual test data: ", clf_dt.score(testx,testy))
# dt.__getstate__()

#Finding the Feature importances
import numpy as np
importances = dt.feature_importances_
indices = np.argsort(importances)[::-1]

# # Print the feature ranking
print("Feature ranking:")
features = cols
for f in range(10):
    print("%d. feature %d - %s (%f)" % (f + 1, indices[f], features[indices[f]] ,importances[indices[f]]))

feature_dict = {}
for i,f in enumerate(features):
    feature_dict[f] = i
print(feature_dict['stomach_pain'])
print(feature_dict['redness_of_eyes'])
s1 = feature_dict['stomach_pain']
s2 = feature_dict['redness_of_eyes']


sample_b = [i/int(s1) if i == int(s1) else i*0 for i in range(len(features))]
sample_a = [i/int(s2) if i == int(s2) else i*0 for i in range(len(features))]
a = np.matrix(sample_a)
b = np.matrix(sample_b)
bb = a + b
sample_b = np.array(sample_b).reshape(1,len(sample_b))
sample_a = np.array(sample_a).reshape(1,len(sample_a))
# print(sample_b,sample_a)

print(dt.predict(bb))
# print(dt.predict_proba(bb))