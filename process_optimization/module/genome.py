import os
import pandas as pd
import numpy as np
from pathlib import Path
from module.simulator import Simulator
simulator = Simulator()
submission_ini = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'sample_submission.csv'))
order_ini = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'order.csv'))
changetime_ini = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'change_time.csv'))
class Genome():
    def __init__(self, score_ini, input_len, output_len_1, output_len_2, h1=50, h2=50, h3=50):
        # 평가 점수 초기화
        self.score = score_ini
        
        # 히든레이어 노드 개수
        self.hidden_layer1 = h1
        self.hidden_layer2 = h2
        self.hidden_layer3 = h3
        
        # Event 신경망 가중치 생성(line A)
        self.w1 = np.random.randn(input_len, self.hidden_layer1)
        self.w2 = np.random.randn(self.hidden_layer1, self.hidden_layer2)
        self.w3 = np.random.randn(self.hidden_layer2, self.hidden_layer3)
        self.w4 = np.random.randn(self.hidden_layer3, output_len_1)
        
        # MOL 수량 신경망 가중치 생성(line A)
        self.w5 = np.random.randn(input_len, self.hidden_layer1)
        self.w6 = np.random.randn(self.hidden_layer1, self.hidden_layer2)
        self.w7 = np.random.randn(self.hidden_layer2, self.hidden_layer3)
        self.w8 = np.random.randn(self.hidden_layer3, output_len_2)
        
        # Event 신경망 가중치 생성(line B)
        self.w9 = np.random.randn(input_len, self.hidden_layer1)
        self.w10 = np.random.randn(self.hidden_layer1, self.hidden_layer2)
        self.w11 = np.random.randn(self.hidden_layer2, self.hidden_layer3)
        self.w12 = np.random.randn(self.hidden_layer3, output_len_1)

        # MOL 수량 신경망 가중치 생성(line B)
        self.w13 = np.random.randn(input_len, self.hidden_layer1)
        self.w14 = np.random.randn(self.hidden_layer1, self.hidden_layer2)
        self.w15 = np.random.randn(self.hidden_layer2, self.hidden_layer3)
        self.w16 = np.random.randn(self.hidden_layer3, output_len_2)


        # Event 종류
        self.mask = np.zeros([18], np.bool) # 가능한 이벤트 검사용 마스크
        self.event_map = {0:'CHECK_1', 1:'CHECK_2', 2:'CHECK_3', 3:'CHECK_4', 4:'PROCESS', 5:'CHANGE_12', 6:'CHANGE_13', 7:'CHANGE_14', 8:'CHANGE_21', 9:'CHANGE_23', 10:'CHANGE_24', 11:'CHANGE_31', 12:'CHANGE_32', 13:'CHANGE_34', 14:'CHANGE_41', 15:'CHANGE_42', 16:'CHANGE_43', 17:'STOP'}
        
        self.check_time = 28    # 28시간 검사를 완료했는지 검사, CHECK Event시 -1, processtime_time >=98 이면 28
        self.process = 0        # 생산 가능 여부, 0 이면 28 시간 검사 필요
        self.process_mode = 0   # 생산 물품 번호 0~3, stop시 4
        self.process_time = 0   # 생산시간이 얼마나 지속되었는지 검사, PROCESS +1, CHANGE +1, 최대 140
        
        self.change_mode = 0 # change mode   ex)'CHANGE_12' => 12
        self.change_time = 0 # change event 에 소요되는 시간
        self.change = 0 #change event 가능 여부
        self.stop_time = 0 #stop event 가 진행된 시간
        self.changetimes = 2 # change 이벤트 제한횟수에 쓰이는 변수
        self.stop = 0 #stop 이벤트의 가능 여부
        

        
    def update_mask(self):
        self.mask[:] = False
        if self.process == 0:
            if self.check_time == 28:
                self.mask[:4] = True
            if self.check_time < 28:
                self.mask[self.process_mode] = True
        if self.process == 1:
            self.mask[4] = True
            if self.process_time > 98:
                self.mask[:4] = True
                #self.mask[17] = True
            if self.change == 1:
                if self.change_mode == 12:
                    self.mask[5] = True
                    if self.change_time != 0:
                        self.mask[:5] = False
                if self.change_mode == 13:
                    self.mask[6] = True
                    if self.change_time != 0:
                        self.mask[:5] = False
                if self.change_mode == 14:
                    self.mask[7] = True
                    if self.change_time != 0:
                        self.mask[:5] = False
                if self.change_mode == 21:
                    self.mask[8] = True
                    if self.change_time != 0:
                        self.mask[:5] = False
                if self.change_mode == 23:
                    self.mask[9] = True
                    if self.change_time != 0:
                        self.mask[:5] = False
                if self.change_mode == 24:
                    self.mask[10] = True
                    if self.change_time != 0:
                        self.mask[:5] = False
                if self.change_mode == 31:
                    self.mask[11] = True
                    if self.change_time != 0:
                        self.mask[:5] = False
                if self.change_mode == 32:
                    self.mask[12] = True
                    if self.change_time != 0:
                        self.mask[:5] = False
                if self.change_mode == 34:
                    self.mask[13] = True
                    if self.change_time != 0:
                        self.mask[:5] = False
                if self.change_mode == 41:
                    self.mask[14] = True
                    if self.change_time != 0:
                        self.mask[:5] = False
                if self.change_mode == 42:
                    self.mask[15] = True
                    if self.change_time != 0:
                        self.mask[:5] = False
                if self.change_mode == 43:
                    self.mask[16] = True
                    if self.change_time != 0:
                        self.mask[:5] = False
        #if self.stop == 1:
            #self.mask[:] = False
            #if self.process_time > 98:
                #self.mask[:5] = True
                #self.mask[17] = True
            #if self.stop_time <= 28:
                #self.mask[17] = True
            #if self.stop_time > 28:
                #self.mask[:4] = True
                #self.mask[17] = True
            #if self.stop_time == 192:
                #self.mask[:4] = True








    def forward(self, inputs):
        # Event 신경망(line A)
        net = np.matmul(inputs, self.w1)
        net = self.linear(net)
        net = np.matmul(net, self.w2)
        net = self.linear(net)
        net = np.matmul(net, self.w3)
        net = self.sigmoid(net)
        net = np.matmul(net, self.w4)
        net = self.softmax(net)
        net += 1
        net = net * self.mask
        out1 = self.event_map[np.argmax(net)]
        
        # Event 신경먕(line B)
        net = np.matmul(inputs, self.w9)
        net = self.linear(net)
        net = np.matmul(net, self.w10)
        net = self.linear(net)
        net = np.matmul(net, self.w11)
        net = self.sigmoid(net)
        net = np.matmul(net, self.w12)
        net = self.softmax(net)
        net += 1
        net = net * self.mask
        out3 = self.event_map[np.argmax(net)]

        # MOL 수량 신경망(line A)
        net = np.matmul(inputs, self.w5)
        net = self.linear(net)
        net = np.matmul(net, self.w6)
        net = self.linear(net)
        net = np.matmul(net, self.w7)
        net = self.sigmoid(net)
        net = np.matmul(net, self.w8)
        net = self.softmax(net)
        out2 = np.argmax(net)
        out2 /= 2

        # MOL 수량 신경망(line B)
        net = np.matmul(inputs, self.w13)
        net = self.linear(net)
        net = np.matmul(net, self.w14)
        net = self.linear(net)
        net = np.matmul(net, self.w15)
        net = self.sigmoid(net)
        net = np.matmul(net, self.w16)
        net = self.softmax(net)
        out4 = np.argmax(net)
        out4 /= 2 
        return out1, out2, out3, out4

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def softmax(self, x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)
    
    def linear(self, x):
        return x
    
    def create_order(self, order):
        for i in range(30):
            order.loc[91+i,:] = ['0000-00-00', 0, 0, 0, 0]        
        return order
   
    def predict(self, order):
        order = self.create_order(order)
        self.submission = submission_ini
        self.submission.loc[:, 'PRT_1':'PRT_4'] = 0
        for s in range(self.submission.shape[0]):
            self.update_mask()
            inputs = np.array(order.loc[s//24:(s//24+30), 'BLK_1':'BLK_4']).reshape(-1)
            inputs = np.append(inputs, s%24)
            out1, out2, out3, out4 = self.forward(inputs)
            
            if out1 == 'CHECK_1':
                if self.process == 1:
                    self.process = 0
                    self.check_time = 28
                self.check_time -= 1
                self.process_mode = 0
                self.stop = 0
                self.stop_time = 0
                if self.check_time == 0:
                    self.process = 1
                    self.process_time = 0
                    self.changetime = 2
            elif out1 == 'CHECK_2':
                if self.process == 1:
                    self.process = 0
                    self.check_time = 28
                self.check_time -= 1
                self.process_mode = 1
                self.stop = 0
                self.stop_time = 0
                if self.check_time == 0:
                    self.process = 1
                    self.process_time = 0
                    self.changetime = 2
            elif out1 == 'CHECK_3':
                if self.process == 1:
                    self.process = 0
                    self.check_time = 28
                self.check_time -= 1
                self.process_mode = 2
                self.stop = 0
                self.stop_time = 0
                if self.check_time == 0:
                    self.process = 1
                    self.process_time = 0
                    self.changetime = 2
            elif out1 == 'CHECK_4':
                if self.process == 1:
                    self.process = 0
                    self.check_time = 28
                self.check_time -= 1
                self.process_mode = 3
                self.stop = 0
                self.stop_time = 0
                if self.check_time == 0:
                    self.process = 1
                    self.process_time = 0
                    self.changetime = 2
            elif out1 == 'PROCESS':
                self.process_time += 1
                if self.process_time >= 98:
                    self.check_time = 28
                    self.stop_time = 0
                    self.stop = 1
                if self.process_time == 140:
                    self.process = 0
                    self.check_time = 28
                    self.process_mode = 4
                    #self.stop_time = 0
                    #self.stop = 1
                #if ((self.process_time + int(changetime_ini.loc[0,'time'])) < 140) and (self.process_mode == 0): #change12
                    #if (self.changetime != 0) and (self.process_time >= 30):
                        #self.change_mode = 12
                        #self.change_time = int(changetime_ini.loc[0,'time'])
                        #self.change = 1
                        #self.changetime -= 1
                if ((self.process_time + int(changetime_ini.loc[1,'time'])) < 140) and (self.process_mode == 0): #change13
                    if (self.changetime != 0) and (self.process_time >= 30):
                        self.change_mode = 13
                        self.change_time = int(changetime_ini.loc[1,'time'])
                        self.change = 1
                        self.changetime -= 1
                if ((self.process_time + int(changetime_ini.loc[2,'time'])) < 140) and (self.process_mode == 0): #change14
                    if (self.changetime != 0) and (self.process_time >= 30):
                        self.change_mode = 14
                        self.change_time = int(changetime_ini.loc[2,'time'])
                        self.change = 1
                        self.changetime -= 1
                #if ((self.process_time + int(changetime_ini.loc[3,'time'])) < 140) and (self.process_mode == 1): #change21 
                    #if (self.changetime != 0) and (self.process_time >= 30):
                        #self.change_mode = 21
                        #self.change_time = int(changetime_ini.loc[3,'time'])
                        #self.change = 1
                        #self.changetime -= 1
                if ((self.process_time + int(changetime_ini.loc[4,'time'])) < 140) and (self.process_mode == 1): #change23
                    if (self.changetime != 0) and (self.process_time >= 30):
                        self.change_mode = 23
                        self.change_time = int(changetime_ini.loc[4,'time'])
                        self.change = 1
                        self.changetime -= 1 
                if ((self.process_time + int(changetime_ini.loc[5,'time'])) < 140) and (self.process_mode == 1): #change24
                    if (self.changetime != 0) and (self.process_time >= 30):
                        self.change_mode = 24
                        self.change_time = int(changetime_ini.loc[5,'time'])
                        self.change = 1
                        self.changetime -= 1
                #if ((self.process_time + int(changetime_ini.loc[6,'time'])) < 140) and (self.process_mode == 2): #change31
                    #if (self.changetime != 0) and (self.process_time >= 30):
                        #self.change_mode = 31
                        #self.change_time = int(changetime_ini.loc[6,'time'])
                        #self.change = 1
                        #self.changetime -= 1
                #if ((self.process_time + int(changetime_ini.loc[7,'time'])) < 140) and (self.process_mode == 2): #change32
                    #if (self.changetime != 0) and (self.process_time >= 30):
                        #self.change_mode = 32
                        #self.change_time = int(changetime_ini.loc[7,'time'])
                        #self.change = 1
                        #self.changetime -= 1
                #if ((self.process_time + int(changetime_ini.loc[8,'time'])) < 140) and (self.process_mode == 2): #change34 
                    #if (self.changetime != 0) and (self.process_time >= 30):
                        #self.change_mode = 34
                        #self.change_time = int(changetime_ini.loc[8,'time'])
                        #self.change = 1
                        #self.changetime -= 1
                #if ((self.process_time + int(changetime_ini.loc[9,'time'])) < 140) and (self.process_mode == 3): #change41
                    #if (self.changetime != 0) and (self.process_time >= 30):
                        #self.change_mode = 41
                        #self.change_time = int(changetime_ini.loc[9,'time'])
                        #self.change = 1
                        #self.changetime -= 1
                #if ((self.process_time + int(changetime_ini.loc[10,'time'])) < 140) and (self.process_mode == 3): #change42
                    #if (self.changetime != 0) and (self.process_time >= 30):
                        #self.change_mode = 42
                        #self.change_time = int(changetime_ini.loc[10,'time'])
                        #self.change = 1
                        #self.changetime -= 1
                if ((self.process_time + int(changetime_ini.loc[11,'time'])) < 140) and (self.process_mode == 3): #change43
                    if (self.changetime != 0) and (self.process_time >= 30):
                        self.change_mode = 43
                        self.change_time = int(changetime_ini.loc[11,'time'])
                        self.change = 1
                        self.changetime -= 1


            elif out1 == 'CHANGE_12':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 12) and (self.change_time == 0):
                    self.process_mode = 1
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0
                
            elif out1 == 'CHANGE_13':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 13) and (self.change_time == 0):
                    self.process_mode = 2
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            elif out1 == 'CHANGE_14':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 14) and (self.change_time == 0):
                    self.process_mode = 3
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            elif out1 == 'CHANGE_21':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 21) and (self.change_time == 0):
                    self.process_mode = 0
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            elif out1 == 'CHANGE_23':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 23) and (self.change_time == 0):
                    self.process_mode = 2
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0
                                   
            elif out1 == 'CHANGE_24':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 24) and (self.change_time == 0):
                    self.process_mode = 3
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0
               
            elif out1 == 'CHANGE_31':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 31) and (self.change_time == 0):
                    self.process_mode = 0
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            elif out1 == 'CHANGE_32':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 32) and (self.change_time == 0):
                    self.process_mode = 1
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            elif out1 == 'CHANGE_34':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 34) and (self.change_time == 0):
                    self.process_mode = 3
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            elif out1 == 'CHANGE_41':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 41) and (self.change_time == 0):
                    self.process_mode = 0
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0
                
            elif out1 == 'CHANGE_42':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 42) and (self.change_time == 0):
                    self.process_mode = 1
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            elif out1 == 'CHANGE_43':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 43) and (self.change_time == 0):
                    self.process_mode = 2
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            #elif out1 == 'STOP':
                #self.stop_time += 1
                #self.stop = 1
                #if self.process == 1:
                    #self.process = 0
                    #self.process_mode = 0
                    #self.process_time = 0
                
                #if self.stop_time == 192:
                    #self.stop = 0
                    #self.stop_time = 0
                    #self.check_time = 28




            self.submission.loc[s, 'Event_A'] = out1
            if self.submission.loc[s, 'Event_A'] == 'PROCESS':
                self.submission.loc[s, 'MOL_A'] = out2
            else:
                self.submission.loc[s, 'MOL_A'] = 0

        # 23일간 MOL = 0
        self.submission.loc[:24*23, 'MOL_A'] = 0
        

        
        # 변수 초기화
        self.check_time = 28    # 28시간 검사를 완료했는지 검사, CHECK Event시 -1, processtime_time >=98 이면 28
        self.process = 0        # 생산 가능 여부, 0 이면 28 시간 검사 필요
        self.process_mode = 0   # 생산 물품 번호 0~3, stop시 4
        self.process_time = 0   # 생산시간이 얼마나 지속되었는지 검사, PROCESS +1, CHANGE +1, 최대 140
        
        self.change_mode = 0 # change mode   ex)'CHANGE_12' => 12
        self.change_time = 0 # change event 에 소요되는 시간
        self.change = 0 #change event 가능 여부
        self.stop_time = 0 #stop event 가 진행된 시간
        self.changetimes = 2 # change 이벤트 제한횟수에 쓰이는 변수
        self.stop = 0 #stop 이벤트의 가능 여부

        for k in range(self.submission.shape[0]):
            self.update_mask()
            inputs = np.array(order.loc[k//24:(k//24+30), 'BLK_1':'BLK_4']).reshape(-1)
            inputs = np.append(inputs, k%24)
            out1, out2, out3, out4 = self.forward(inputs)
            
            if out3 == 'CHECK_1':
                if self.process == 1:
                    self.process = 0
                    self.check_time = 28
                self.check_time -= 1
                self.process_mode = 0
                self.stop = 0
                self.stop_time = 0
                if self.check_time == 0:
                    self.process = 1
                    self.process_time = 0
                    self.changetime = 2
            elif out3 == 'CHECK_2':
                if self.process == 1:
                    self.process = 0
                    self.check_time = 28
                self.check_time -= 1
                self.process_mode = 1
                self.stop = 0
                self.stop_time = 0
                if self.check_time == 0:
                    self.process = 1
                    self.process_time = 0
                    self.changetime = 2
            elif out3 == 'CHECK_3':
                if self.process == 1:
                    self.process = 0
                    self.check_time = 28
                self.check_time -= 1
                self.process_mode = 2
                self.stop = 0
                self.stop_time = 0
                if self.check_time == 0:
                    self.process = 1
                    self.process_time = 0
                    self.changetime = 2
            elif out3 == 'CHECK_4':
                if self.process == 1:
                    self.process = 0
                    self.check_time = 28
                self.check_time -= 1
                self.process_mode = 3
                self.stop = 0
                self.stop_time = 0
                if self.check_time == 0:
                    self.process = 1
                    self.process_time = 0
                    self.changetime = 2
            elif out3 == 'PROCESS':
                self.process_time += 1
                if self.process_time >= 98:
                    self.check_time = 28
                    self.stop_time = 0
                    self.stop = 1
                if self.process_time == 140:
                    self.process = 0
                    self.check_time = 28
                    self.process_mode = 4
                    self.stop_time = 0
                    self.stop = 1
                #if ((self.process_time + int(changetime_ini.loc[0,'time'])) < 140) and (self.process_mode == 0): #change12
                    #if (self.changetime != 0) and (self.process_time >= 30):
                        #self.change_mode = 12
                        #self.change_time = int(changetime_ini.loc[0,'time'])
                        #self.change = 1
                        #self.changetime -= 1
                if ((self.process_time + int(changetime_ini.loc[1,'time'])) < 140) and (self.process_mode == 0): #change13
                    if (self.changetime != 0) and (self.process_time >= 30):
                        self.change_mode = 13
                        self.change_time = int(changetime_ini.loc[1,'time'])
                        self.change = 1
                        self.changetime -= 1
                if ((self.process_time + int(changetime_ini.loc[2,'time'])) < 140) and (self.process_mode == 0): #change14
                    if (self.changetime != 0) and (self.process_time >= 30):
                        self.change_mode = 14
                        self.change_time = int(changetime_ini.loc[2,'time'])
                        self.change = 1
                        self.changetime -= 1
                #if ((self.process_time + int(changetime_ini.loc[3,'time'])) < 140) and (self.process_mode == 1): #change21 
                    #if (self.changetime != 0) and (self.process_time >= 30):
                        #self.change_mode = 21
                        #self.change_time = int(changetime_ini.loc[3,'time'])
                        #self.change = 1
                        #self.changetime -= 1
                if ((self.process_time + int(changetime_ini.loc[4,'time'])) < 140) and (self.process_mode == 1): #change23
                    if (self.changetime != 0) and (self.process_time >= 30):
                        self.change_mode = 23
                        self.change_time = int(changetime_ini.loc[4,'time'])
                        self.change = 1
                        self.changetime -= 1 
                if ((self.process_time + int(changetime_ini.loc[5,'time'])) < 140) and (self.process_mode == 1): #change24
                    if (self.changetime != 0) and (self.process_time >= 30):
                        self.change_mode = 24
                        self.change_time = int(changetime_ini.loc[5,'time'])
                        self.change = 1
                        self.changetime -= 1
                #if ((self.process_time + int(changetime_ini.loc[6,'time'])) < 140) and (self.process_mode == 2): #change31
                    #if (self.changetime != 0) and (self.process_time >= 30):
                        #self.change_mode = 31
                        #self.change_time = int(changetime_ini.loc[6,'time'])
                        #self.change = 1
                        #self.changetime -= 1
                #if ((self.process_time + int(changetime_ini.loc[7,'time'])) < 140) and (self.process_mode == 2): #change32
                    #if (self.changetime != 0) and (self.process_time >= 30):
                        #self.change_mode = 32
                        #self.change_time = int(changetime_ini.loc[7,'time'])
                        #self.change = 1
                        #self.changetime -= 1
                #if ((self.process_time + int(changetime_ini.loc[8,'time'])) < 140) and (self.process_mode == 2): #change34 
                    #if (self.changetime != 0) and (self.process_time >= 30):
                        #self.change_mode = 34
                        #self.change_time = int(changetime_ini.loc[8,'time'])
                        #self.change = 1
                        #self.changetime -= 1
                #if ((self.process_time + int(changetime_ini.loc[9,'time'])) < 140) and (self.process_mode == 3): #change41
                    #if (self.changetime != 0) and (self.process_time >= 30):
                        #self.change_mode = 41
                        #self.change_time = int(changetime_ini.loc[9,'time'])
                        #self.change = 1
                        #self.changetime -= 1
                #if ((self.process_time + int(changetime_ini.loc[10,'time'])) < 140) and (self.process_mode == 3): #change42
                    #if (self.changetime != 0) and (self.process_time >= 30):
                        #self.change_mode = 42
                        #self.change_time = int(changetime_ini.loc[10,'time'])
                        #self.change = 1
                        #self.changetime -= 1
                if ((self.process_time + int(changetime_ini.loc[11,'time'])) < 140) and (self.process_mode == 3): #change43
                    if (self.changetime != 0) and (self.process_time >= 30):
                        self.change_mode = 43
                        self.change_time = int(changetime_ini.loc[11,'time'])
                        self.change = 1
                        self.changetime -= 1


            elif out3 == 'CHANGE_12':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 12) and (self.change_time == 0):
                    self.process_mode = 1
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0
                
            elif out3 == 'CHANGE_13':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 13) and (self.change_time == 0):
                    self.process_mode = 2
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            elif out3 == 'CHANGE_14':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 14) and (self.change_time == 0):
                    self.process_mode = 3
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            elif out3 == 'CHANGE_21':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 21) and (self.change_time == 0):
                    self.process_mode = 0
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            elif out3 == 'CHANGE_23':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 23) and (self.change_time == 0):
                    self.process_mode = 2
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0
                                   
            elif out3 == 'CHANGE_24':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 24) and (self.change_time == 0):
                    self.process_mode = 3
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0
               
            elif out3 == 'CHANGE_31':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 31) and (self.change_time == 0):
                    self.process_mode = 0
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            elif out3 == 'CHANGE_32':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 32) and (self.change_time == 0):
                    self.process_mode = 1
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            elif out3 == 'CHANGE_34':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 34) and (self.change_time == 0):
                    self.process_mode = 3
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            elif out3 == 'CHANGE_41':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 41) and (self.change_time == 0):
                    self.process_mode = 0
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0
                
            elif out3 == 'CHANGE_42':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 42) and (self.change_time == 0):
                    self.process_mode = 1
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            elif out3 == 'CHANGE_43':
                self.change_time -= 1 
                self.process_time += 1       
                if (self.change_mode == 43) and (self.change_time == 0):
                    self.process_mode = 2
                    self.change_mode = 0
                    self.change_time = 0
                    self.change = 0

            #elif out3 == 'STOP':
                #self.stop_time += 1
                #self.stop = 1
                #if self.process == 1:
                    #self.process = 0
                    #self.process_mode = 0
                    #self.process_time = 0
                
                #if self.stop_time == 192:
                    #self.stop = 0
                    #self.stop_time = 0
                    #self.check_time = 28





            self.submission.loc[k, 'Event_B'] = out3
            if self.submission.loc[k, 'Event_B'] == 'PROCESS':
                self.submission.loc[k, 'MOL_B'] = out4
            else:
                self.submission.loc[k, 'MOL_B'] = 0

        # 23일간 MOL = 0
        self.submission.loc[:24*23, 'MOL_B'] = 0 

        #변수 초기화                  
        self.check_time = 28    # 28시간 검사를 완료했는지 검사, CHECK Event시 -1, processtime_time >=98 이면 28
        self.process = 0        # 생산 가능 여부, 0 이면 28 시간 검사 필요
        self.process_mode = 0   # 생산 물품 번호 0~3, stop시 4
        self.process_time = 0   # 생산시간이 얼마나 지속되었는지 검사, PROCESS +1, CHANGE +1, 최대 140
        
        self.change_mode = 0 # change mode   ex)'CHANGE_12' => 12
        self.change_time = 0 # change event 에 소요되는 시간
        self.change = 0 #change event 가능 여부
        self.stop_time = 0 #stop event 가 진행된 시간
        self.changetimes = 2 # change 이벤트 제한횟수에 쓰이는 변수
        self.stop = 0 #stop 이벤트의 가능 여부



        return self.submission    
    
def genome_score(genome):
    submission = genome.predict(order_ini)    
    genome.submission = submission    
    genome.score, _ = simulator.get_score(submission)    
    return genome