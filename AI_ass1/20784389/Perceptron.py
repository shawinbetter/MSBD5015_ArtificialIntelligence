import pandas as pd
import numpy as np

class Perceptron:

    def __init__(self,c=1): #initialize weights and threshold
        self.w = np.array([0.,0.,0.,0.,0.,0.,0.,0.])
        self.threshold = 0.
        self.c = c
    
    def fit(self,x,y):
        pred_val = np.dot(x,self.w.T) - self.threshold 
        is_all_correct = True
        for i in range(len(y)):
            if pred_val[i] >= 0:
                pred_label = 1
            else:
                pred_label = 0
            if pred_label == y[i]:
                continue
            else:
                updated_weight = []
                for k in range(len(self.w)):
                    updated_weight.append(self.w[k] + self.c * float(y[i] - pred_label) * x[i,k]) #update each weight
                self.w = np.array(updated_weight)
                self.threshold = self.threshold - self.c * float(y[i] - pred_label) * 1 #update threshold
                is_all_correct = False
        return is_all_correct
    
    def predict(self,x):
        if np.dot(x,self.w.T) + self.threshold >= 0 :
            return 1
        return 0

#Read data
north_data = pd.read_csv('assign1-data_python3/north.csv',header=None)
south_data = pd.read_csv('assign1-data_python3/south.csv',header=None)
west_data = pd.read_csv('assign1-data_python3/west.csv',header=None)
east_data = pd.read_csv('assign1-data_python3/east.csv',header=None)

#Initial four perceptron
control_north,control_south,control_west,control_east = Perceptron(),Perceptron(),Perceptron(),Perceptron()

is_all_correct = False
while not is_all_correct:
    x,y = np.array(north_data.loc[:,0:7]),np.array(north_data.iloc[:,8]) #shuffle
    is_all_correct = control_north.fit(x,y)
print('Weights of North Perceptron:',control_north.w,' Threshold:',control_north.threshold)


is_all_correct = False
while not is_all_correct:
    x,y = np.array(south_data.loc[:,0:7]),np.array(south_data.iloc[:,8])
    is_all_correct = control_south.fit(x,y)
print('Weights of south Perceptron:',control_south.w,' Threshold:',control_south.threshold)


is_all_correct = False
while not is_all_correct:
    x,y = np.array(west_data.loc[:,0:7]),np.array(west_data.iloc[:,8])
    is_all_correct = control_west.fit(x,y)
print('Weights of west Perceptron:',control_west.w,' Threshold:',control_west.threshold)


is_all_correct = False
while not is_all_correct:
    x,y = np.array(east_data.loc[:,0:7]),np.array(east_data.iloc[:,8])
    is_all_correct = control_east.fit(x,y)
print('Weights of east Perceptron:',control_east.w,' Threshold:',control_east.threshold)

"""
Weights of North Perceptron: [ 1. -4. -4.  0.  0.  0.  0.  1.]  Threshold: 1.0
Weights of south Perceptron: [ 0.  0.  0.  1.  1. -4. -4.  0.]  Threshold: 1.0
Weights of west Perceptron: [-4.  0.  0.  0.  0.  1.  1. -4.]  Threshold: 1.0
Weights of east Perceptron: [ 0.  1.  1. -4. -4.  0.  0.  0.]  Threshold: 1.0
"""