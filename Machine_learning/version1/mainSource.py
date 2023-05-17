import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('mode.chained_assignment', None)

from keras.models import Sequential
from keras.layers import Dense, SimpleRNN
from keras.optimizers import RMSprop
from keras.callbacks import Callback

df=pd.read_csv("../data/base_camp.csv",na_values=['-999'])
Humidity = df.drop(['T_HMP', 'PRESS' ,'PRECIP'], axis=1)
Temp = df.drop(['RH', 'PRESS' ,'PRECIP'], axis=1)
Pressure = df.drop(['T_HMP', 'RH' ,'PRECIP'], axis=1)
Precipate = df.drop(['T_HMP', 'PRESS' ,'RH'], axis=1)

Humidity.head()

print(Humidity.shape)
print(Temp.shape)
print(Pressure.shape)
print(Precipate.shape)

print("How many NaN are there in the humidity dataset?",Humidity.isna().sum())
print("How many NaN are there in the temperature dataset?",Temp.isna().sum())
print("How many NaN are there in the pressure dataset?",Pressure.isna().sum())

Tp = 7000

train_humidity =  np.array(Humidity.RH[:Tp])
#test_humidity =  np.array(Humidity.RH[Tp:])
train_temp =   np.array(Temp.T_HMP[:Tp])
#test_temp =   np.array(Temp.T_HMP[Tp:])
train_pressure =  np.array(Pressure.PRESS[:Tp])
#test_pressure =   np.array(Pressure.PRESS[Tp:])

np.array(Pressure.PRESS[:Tp])

Pressure.head()

def plot_train_points(quantity='humidity',Tp=7000):
    plt.figure(figsize=(15,4))
    if quantity=='humidity':
        plt.title("Humidity of first {} data points".format(Tp),fontsize=16)
        plt.plot(train_humidity,c='k',lw=1)
    if quantity=='temperature':
        plt.title("Temperature of first {} data points".format(Tp),fontsize=16)
        plt.plot(train_temp,c='k',lw=1)
    if quantity=='pressure':
        plt.title("Pressure of first {} data points".format(Tp),fontsize=16)
        plt.plot(train_pressure,c='k',lw=1)
    plt.grid(True)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.show()

plot_train_points('humidity')

plot_train_points('temperature')

plot_train_points('pressure')

## Data interpolate and fill Nan values
Humidity.interpolate(inplace=True)
Humidity.dropna(inplace=True)

Temp.interpolate(inplace=True)
Temp.dropna(inplace=True)

Pressure.interpolate(inplace=True)
Pressure.dropna(inplace=True)

print(Humidity.shape)
print(Temp.shape)
print(Pressure.shape)

# RNN model for humidity
### Train and test splits on the tp = 7000
train_humidity =  np.array(Humidity.RH[:Tp])
test_humidity =  np.array(Humidity.RH[Tp:])

print("Train data length:", train_humidity.shape)
print("Test data length:", test_humidity.shape)

train_humidity=train_humidity.reshape(-1,1)
test_humidity=test_humidity.reshape(-1,1)

plt.figure(figsize=(15,4))
plt.title("Train and test data plotted together",fontsize=16)
plt.plot(np.arange(Tp),train_humidity,c='blue')
plt.plot(np.arange(Tp,24443),test_humidity,c='orange',alpha=0.7)
plt.legend(['train_humidity','test_humidity'])
plt.grid(True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()

step = 8

# add step elements into train and test
test_humidity = np.append(test_humidity,np.repeat(test_humidity[-1,],step))
train_humidity = np.append(train_humidity,np.repeat(train_humidity[-1,],step))

print("Train data length:", train_humidity.shape)
print("Test data length:", test_humidity.shape)

def convertToMatrix(data, step):
    X, Y =[], []
    for i in range(len(data)-step):
        d=i+step  
        X.append(data[i:d,])
        Y.append(data[d,])
    return np.array(X), np.array(Y)

trainX,trainY =convertToMatrix(train_humidity,step)
testX,testY =convertToMatrix(test_humidity,step)

trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

print("Training data shape:", trainX.shape,', ',trainY.shape)
print("Test data shape:", testX.shape,', ',testY.shape)

## MODEL
def build_simple_rnn(num_units=128, embedding=4,num_dense=32,lr=0.001):
    """
    Builds and compiles a simple RNN model
    Arguments:
              num_units: Number of units of a the simple RNN layer
              embedding: Embedding length
              num_dense: Number of neurons in the dense layer followed by the RNN layer
              lr: Learning rate (uses RMSprop optimizer)
    Returns:
              A compiled Keras model.
    """
    model = Sequential()
    model.add(SimpleRNN(units=num_units, input_shape=(1,embedding), activation="relu"))
    model.add(Dense(num_dense, activation="relu"))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer=RMSprop(lr=lr),metrics=['mse'])
    
    return model

model_humidity = build_simple_rnn(num_units=128,num_dense=32,embedding=8,lr=0.0005)

model_humidity.summary()

class MyCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        if (epoch+1) % 50 == 0 and epoch>0:
            print("Epoch number {} done".format(epoch+1))

batch_size=8
num_epochs = 1000

model_humidity.fit(trainX,trainY, 
          epochs=num_epochs, 
          batch_size=batch_size, 
          callbacks=[MyCallback()],verbose=0)

plt.figure(figsize=(7,5))
plt.title("RMSE loss over epochs",fontsize=16)
plt.plot(np.sqrt(model_humidity.history.history['loss']),c='k',lw=2)
plt.grid(True)
plt.xlabel("Epochs",fontsize=14)
plt.ylabel("Root-mean-squared error",fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.show()

plt.figure(figsize=(15,4))
plt.title("This is what the model saw",fontsize=18)
plt.plot(trainX[:,0][:,0],c='blue')
plt.grid(True)
plt.show()

trainPredict = model_humidity.predict(trainX)
testPredict= model_humidity.predict(testX)
predicted=np.concatenate((trainPredict,testPredict),axis=0)
plt.figure(figsize=(10,4))
plt.title("This is what the model predicted",fontsize=18)
plt.plot(testPredict,c='orange')
plt.grid(True)
plt.show()

Humidity.index.values
index = Humidity.index.values

plt.figure(figsize=(15,5))
plt.title("Humidity: Ground truth and prediction together",fontsize=18)
plt.plot(index,np.array(Humidity.RH),c='blue')
plt.plot(index,predicted,c='orange',alpha=0.75)
plt.legend(['True data','Predicted'],fontsize=15)
plt.axvline(x=Tp, c="r")
plt.grid(True)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylim(-20,120)
plt.show()

#saving the trained model
model.save("Location")

#saving weights
#model.save_weight('model.h5')