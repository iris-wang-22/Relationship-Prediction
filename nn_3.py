# -*- coding: utf-8 -*-
"""SML models.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/162RiBtcvbbZ-PxaKAkwN4p6lUKFl3Ku9

- Read Data
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

train_data=readfile("train.csv")
test_data=readfile("test.csv")

"""- Data Transforming"""

data_train=[]
label_train=[]
temp_list=train_data.splitlines()
del temp_list[0]
for item in temp_list:
  temp=item.split(",")
  data_train.append([float(temp[0]),float(temp[1]),float(temp[2])])
  label_train.append(int(temp[3]))
data_test=[]
temp_list=test_data.splitlines()
del temp_list[0]
for item in temp_list:
  temp=item.split(",")
  data_test.append([float(temp[0]),float(temp[1]),float(temp[2])])

print(len(data_train))
print(len(label_train))
print(len(data_test))

print(data_train[0:20])
print(label_train[0:20])
print(data_train[30000:30020])
print(label_train[30000:30020])
print(data_test[0:100])

from sklearn.model_selection import train_test_split
X_train, X_dev, Y_train, Y_dev = train_test_split(data_train, label_train, test_size=0.3, random_state=0)

"""- Fully Connected NN

**3 Layers**
"""

# def AUC(yTrue, yPred):
#     import tensorflow as tf
#     auc = tf.metrics.auc(yTrue, yPred)
#     return auc[0]
import tensorflow as tf
from tensorboard.plugins.hparams import api
from keras import models as md
from keras import layers as lr
import numpy as np
best_model=""
best_acc=0.0
best_hp={}

# units1=api.HParam("num_units_layer_1",api.Discrete([4,8,16,32,64,128]))#dense layer
# units2=api.HParam("num_units_layer_2",api.Discrete([4,8,16,32,64,128]))#dense layer
# units3=api.HParam("num_units_layer_2",api.Discrete([4,8,16,32,64,128]))#dense layer
# optimizerfunc=api.HParam("optimizer",api.Discrete(["adam","sgd"]))#optimizer
# X_train=np.array(data_train)
# Y_train=np.array(label_train)
for u1 in [4,8,16,32,64,128]:
  for u2 in [4,8,16,32,64,128]:
    for u3 in [4,8,16,32,64,128]:
      for opt in ["adam","sgd"]:

        model = md.Sequential()
        model.add(lr.Dense(u1,activation="relu"))
        model.add(lr.Dense(u2,activation="relu"))
        model.add(lr.Dense(u3,activation="relu"))
        model.add(lr.Dropout(0.2))
        model.add(lr.Dense(1,activation="sigmoid"))
        model.compile(optimizer=opt,loss="binary_crossentropy",metrics=["accuracy"])#compile the model
        model.fit(X_train, Y_train, epochs=32, batch_size=16)#fit the model
        loss, acc = model.evaluate(X_dev, Y_dev)
        hp={"num_units_layer_1":u1,"num_units_layer_2":u2,"num_units_layer_3":u3,"optimizer":opt}
        print("current model:"+str(hp))
        print("loss:"+str(loss)+",accuracy:"+str(acc))
        if acc>best_acc:
          best_acc=acc
          best_hp=hp
          best_model=model
print("Best Model:"+str(best_hp)+",accuracy"+str(best_acc))

Y_test=best_model.predict(data_test).tolist()
print(len(Y_test))

current_path=os.path.abspath(os.curdir)
file_path=os.path.join(current_path,"output.csv")
f=codecs.open(file_path,"w","utf-8")
f.write("Id,Predicted\n")
for i in range(0,len(Y_test)):
  f.write(str(i+1)+","+str(Y_test[i][0])+"\n")
f.close()