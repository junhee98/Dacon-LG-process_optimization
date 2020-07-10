# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 23:04:17 2020

@author: l_jun
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path


#csv 파일들을 불러오자.
submission_ini = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'sample_submission.csv'))
order_ini = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'order.csv'))
changetime_ini = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'change_time.csv'))
stock_ini =  pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'stock.csv'))
maxcount_ini =  pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'max_count.csv'))
cutyield_ini = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'cut_yield.csv'))

class Study( ):
    def __init__(self,input_len=100, output_len_1=18, output_len_2=12, h1=50, h2=50, h3=50):
        
        #히든 레이어 노드 개수
        self.hidden_layer1 = h1
        self.hidden_layer2 = h2
        self.hidden_layer3 = h3
        
        #Event 신경망 가중치 생성
        self.w1 = np.random.randn(input_len,self.hidden_layer1)
        self.w2 = np.random.randn(self.hidden_layer1,self.hidden_layer2)
        self.w3 = np.random.randn(self.hidden_layer2,self.hidden_layer3)
        self.w4 = np.random.randn(self.hidden_layer3,output_len_1)
        
        #MOL 수량 신경망 가중치 생성
        self.w5 = np.random.randn(input_len,self.hidden_layer1)
        self.w6 = np.random.randn(self.hidden_layer1,self.hidden_layer2)
        self.w7 = np.random.randn(self.hidden_layer2,self.hidden_layer3)
        self.w8 = np.random.randn(self.hidden_layer3,output_len_2)

        # Event 종류
        self.mask = np.zeros([18],np.bool) # 가능한 이벤트 검사용 마스크
        self.event_map = {0:'CHECK_1', 1:'CHECK_2', 2:'CHECK_3', 3:'CHECK_4', 4:'PROCESS', 5:'CHANGE_12', 6:'CHANGE_13', 7:'CHANGE_14', 8:'CHANGE_21', 9:'CHANGE_23', 10:'CHANGE_24', 11:'CHANGE_31', 12:'CHANGE_32', 13:'CHANGE_34', 14:'CHANGE_41', 15:'CHANGE_42', 16:'CHANGE_43', 17:'STOP'}

        #공정과정에 필요한 변수를 선언해 보자.
        self.process = False #공정 수행 가능 여부
        self.process_time = 1 #공정이 돌아간 총 시간
        self.process_mode = 0 #공정 모드 1~4
        self.stop = False #정지 기능
        self.stop_time = 1 #정지 되어있는 시간
        self.check = False #체크 수행 여
        self.check_time = 27 #체크 시간
        self.check_mode = 0 # 체크 모드 1~4
        self.change = False #change 기능
        self.change_mode = 0 #change 모드 ex)12 == change_12
        self.mol_A_input = 0 #성형 A라인에 투입개수
        self.mol_B_input = 0 #성형 B라인에 투입개수
        
        self.change_time12 = changetime_ini.loc[0,'time']-1
        self.change_time13 = changetime_ini.loc[1,'time']-1
        self.change_time14 = changetime_ini.loc[2,'time']-1
        self.change_time21 = changetime_ini.loc[3,'time']-1
        self.change_time23 = changetime_ini.loc[4,'time']-1
        self.change_time24 = changetime_ini.loc[5,'time']-1
        self.change_time31 = changetime_ini.loc[6,'time']-1
        self.change_time32 = changetime_ini.loc[7,'time']-1
        self.change_time34 = changetime_ini.loc[8,'time']-1
        self.change_time41 = changetime_ini.loc[9,'time']-1
        self.change_time42 = changetime_ini.loc[10,'time']-1
        self.change_time43 = changetime_ini.loc[11,'time']-1

    def Event(self,inputs):
        # Event 신경망
        net = np.matmul(inputs,self.w1)
        net = self.linear(net)
        net = np.matmul(net,self.w2)
        net = self.linear(net)
        net = np.matmul(net,self.w3)
        net = self.sigmoid(net)
        net = np.matmul(net,self.w4)
        net = self.softmax(net)
        net += 1
        net = net * self.mask
        out1 = self.event_map[np.argmax(net)]
        
        return out1
                
        
    def MOL(self,inputs):
        #MOL 개수 신경망
        net = np.matmul(inputs,self.w5)
        net = self.linear(net)
        net = np.matmul(net,self.w6)
        net = self.linear(net)
        net = np.matmul(net,self.w7)
        net = self.sigmoid(net)
        net = np.matmul(net,self.w8)
        net = self.softmax(net)
        out2 = np.argmax(net)
        out2 /= 2
        return out2
        
    def sigmoid(self,x):
            return 1 / (1 + np.exp(-x))

    def softmax(self,x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    def linear(self,x):
        return x              
            
    def make_inputs(self,i):
        orders = pd.DataFrame(order_ini)
        date = np.array(orders.loc[i,'time':'BLK_4']) #행 선택 요소
        time_process = []
        for i in range(24):
            time_process_cell = []
            time_process_cell.append(date[1]//24)
            time_process_cell.append(date[2]//24)
            time_process_cell.append(date[3]//24)
            time_process_cell.append(date[4]//24)
            time_process.append(time_process_cell)
        
        trash = []
        trash.append(date[1]%24)
        trash.append(date[2]%24)
        trash.append(date[3]%24)
        trash.append(date[4]%24)
        time_process.append(trash)
        time_process = np.array(time_process)
        inputs = time_process
        inputs = inputs.reshape(-1)

        return inputs
    
    def processing(self,i):
        inputs = self.make_inputs(i)
        out1 = self.Event(inputs)
        out2 = self.MOL(inputs)
        
        return out1, out2
        

'''

def sigmoid(x):
        return 1 / (1 + np.exp(-x))

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def linear(x):
    return x

orders = pd.DataFrame(order_ini)
i=int(input("input index: "))
date = np.array(orders.loc[i,'time':'BLK_4']) #행 선택 요소
time_process = []
for i in range(24):
    time_process_cell = []
    time_process_cell.append(date[1]//24)
    time_process_cell.append(date[2]//24)
    time_process_cell.append(date[3]//24)
    time_process_cell.append(date[4]//24)
    time_process.append(time_process_cell)

trash = []
trash.append(date[1]%24)
trash.append(date[2]%24)
trash.append(date[3]%24)
trash.append(date[4]%24)
time_process.append(trash)
time_process = np.array(time_process)


  
h1=25
h2=25
h3=25

hidden_layer1 = h1
hidden_layer2 = h2
hidden_layer3 = h3


input_len = 4
output_len_2 = 6
output_len_1 = 18

#inputs으로 날짜마다의 order를 24로 나누어서 시간별로 order를 계산.
inputs=time_process
inputs=np.array(inputs)

w1 = np.random.randn(input_len,hidden_layer1)
w2 = np.random.randn(hidden_layer1,hidden_layer2)
w3 = np.random.randn(hidden_layer2,hidden_layer3)
w4 = np.random.randn(hidden_layer3,output_len_1)

w5 = np.random.randn(input_len,hidden_layer1)
w6 = np.random.randn(hidden_layer1,hidden_layer2)
w7 = np.random.randn(hidden_layer2,hidden_layer3)
w8 = np.random.randn(hidden_layer3,output_len_2)

# Event 종류
mask = np.zeros([18],np.bool) # 가능한 이벤트 검사용 마스크
event_map = {0:'CHECK_1', 1:'CHECK_2', 2:'CHECK_3', 3:'CHECK_4', 4:'PROCESS', 5:'CHANGE_12', 6:'CHANGE_13', 7:'CHANGE_14', 8:'CHANGE_21', 9:'CHANGE_23', 10:'CHANGE_24', 11:'CHANGE_31', 12:'CHANGE_32', 13:'CHANGE_34', 14:'CHANGE_41', 15:'CHANGE_42', 16:'CHANGE_43', 17:'STOP'}


# Event 신경망
net = np.matmul(inputs,w1)
net = linear(net)
net = np.matmul(net,w2)
net = linear(net)
net = np.matmul(net,w3)
net = sigmoid(net)
net = np.matmul(net,w4)
net = softmax(net)
net += 1
net = net * mask
out1 = event_map[np.argmax(net)]



#MOL 개수 신경망
net = np.matmul(inputs,w5)
net = linear(net)
net = np.matmul(net,w6)
net = linear(net)
net = np.matmul(net, w7)
net = sigmoid(net)
net = np.matmul(net, w8)
net = softmax(net)
out2 = np.argmax(net)
out2 /= 2
'''







