# -*- coding: utf-8 -*-
"""ml_models.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10Jjz8zCIYFliOfRi0nLQQgOuuSsOB1y6

**Project 1 group 8**

# **Data Preprocessing Stage**

## **Read data from file**
"""

import os
import codecs
def readfile(filename):
	current_path=os.path.abspath(os.curdir)
	file_path=os.path.join(current_path,filename)
	if not os.path.exists(file_path):
		print("error:file not found:"+filename)
		return ""
	f=codecs.open(file_path,"r","utf-8")
	s=f.read()
	f.close()
	return s
test_data=readfile("test-public.txt")
test_data=test_data.splitlines()
print("length of testing data:"+str(len(test_data)))
train_data=readfile("train.txt")
train_data=train_data.splitlines()
print("length of training data:"+str(len(train_data)))

"""## **preprocessing data**

- training data
"""

min_num=99999
max_num=0
train_list=[]
num_dict={}
source_set=set()
i=1
for temp_str in train_data:
  temp=temp_str.split('\t')
  num_target=[]
  for j in range(1,len(temp)):
    # temp_list=[]
    # temp_list.append(int(temp[0]))
    # temp_list.append(int(temp[j]))
    train_list.append((int(temp[0]),int(temp[j])))
    i=i+1
    source_set.add(temp[0])
    num_target.append(temp[j])
    if int(temp[j])<min_num:
      min_num=int(temp[j])
    if int(temp[j])>max_num:
      max_num=int(temp[j]) 
  num_dict[int(temp[0])]=num_target
print("preprocessed training data length:"+str(len(train_list)))

"""**validate original data:**"""

print(train_list[0:20])

"""- add negative data"""

import random
train_input=[]
train_res=[]
source_list=list(source_set)
for i in range(0,500000):
  x=random.randint(0,len(train_list))
  train_input.append(train_list[x])
  train_res.append(1)
  # print("generating positive:"+str(i))
i=0
while i<500000:
  x=int(random.choice(source_list))
  # y=random.randint(min_num,max_num)
  y=int(random.choice(source_list))
  if x!=y and y not in num_dict[x]:
    train_input.append((x,y))
    train_res.append(0)
    # print("generating negative:"+str(i))
    i=i+1
    num_dict[x].append(y)
  else:
    continue
print(len(train_input))
print(len(train_res))

"""**check validity**"""

print(train_input[0:20])
print(train_res[0:20])
print(min_num)
print(max_num)
print(train_input[500000:500020])
print(train_res[500000:500020])

"""- testing data

*remove first line (no data)*
"""

del test_data[0]

test_list=[]

for temp_str in test_data:
  temp=temp_str.split('\t')
  
  # temp_list=[]
  # temp_list.append(int(temp[1]))
  # temp_list.append(int(temp[2]))
  test_list.append((int(temp[1]),int(temp[2])))
print("preprocessed testing data length:"+str(len(test_list)))

"""**check validity**"""

print(test_list[0:20])

"""- Feature Engineering"""

test_edges=test_list
train_edges=[]

temp_val=train_input[0]
for item in train_data:
  temp_str=item.split("\t")
  source=int(temp_str[0])
  targets=[]
  for i in range(1,len(temp_str)):
    targets.append(int(temp_str[i]))
  train_edges.append((source,targets))

print(train_edges[0])
print(train_edges[1])

import networkx as nx
graph=nx.Graph()
for item in train_edges:
  current_list=[]
  for ele in item[1]:
    current_list.append((item[0],ele))
  graph.add_edges_from(current_list)
print(graph)

"""- Validatation dataset"""

from sklearn.model_selection import train_test_split
data_train, data_dev, label_train, label_dev = train_test_split(train_input,train_res,test_size=0.3)

"""# **Build Model, Training and Making Predictions**

"""

"""## **Decision Tree Classifier**

- Build model
"""

from sklearn.tree import DecisionTreeClassifier
tree=DecisionTreeClassifier()

"""- hyper-parameter tuning"""

from sklearn.metrics import roc_auc_score
score=0
set_state=-1
for state in range(0,20):
  tree.set_params(random_state=state)
  tree.fit(data_train,label_train)
  predictions=tree.predict(data_dev)
  this_score=roc_auc_score(label_dev,predictions)
  print("state=",state," ,score=",this_score)
  if this_score>score:
    score=this_score
    set_state=state
tree.set_params(random_state=set_state)
print('---------Best Model----------')
print("state=",set_state)

"""- Training"""

tree.fit(data_train,label_train)

"""- Make Predictions"""

test_res=tree.predict_proba(test_list)
test_res=test_res.tolist()
final_res=[]
for ele in test_res:
  final_res.append(ele[1])

"""- get output file"""

current_path=os.path.abspath(os.curdir)
file_path=os.path.join(current_path,"output.csv")
f=codecs.open(file_path,"w","utf-8")
f.write("Id,Predicted\n")
for i in range(0,2000):
  f.write(str(i+1)+","+str(final_res[i])+"\n")
f.close()

"""## **Random Forest Classifier**

- Build model
"""

from sklearn.ensemble import RandomForestClassifier
forest=RandomForestClassifier()

"""- hyper-parameter tuning"""

from sklearn.metrics import roc_auc_score
score=0
set_state=-1
set_depth=-1
for depth in range(2,20):
  for state in range(0,20):
    forest.set_params(random_state=state,max_depth=depth)
    forest.fit(data_train,label_train)
    predictions=forest.predict(data_dev)
    this_score=roc_auc_score(label_dev,predictions)
    print("state=",state," ,depth=",depth," ,score=",this_score)
    if this_score>score:
      score=this_score
      set_state=state
      set_depth=depth
forest.set_params(random_state=set_state,max_depth=set_depth)
print('---------Best Model----------')
print("state=",set_state,"depth=",set_depth)

"""- Training"""

forest.fit(data_train,label_train)

"""- Make Predictions"""

test_res=forest.predict_proba(test_list)
test_res=test_res.tolist()
final_res=[]
for ele in test_res:
  final_res.append(ele[1])

"""- get output file"""

current_path=os.path.abspath(os.curdir)
file_path=os.path.join(current_path,"output.csv")
f=codecs.open(file_path,"w","utf-8")
f.write("Id,Predicted\n")
for i in range(0,2000):
  f.write(str(i+1)+","+str(final_res[i])+"\n")
f.close()


