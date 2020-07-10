# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 14:34:06 2020

@author: l_jun
"""


# 여러 세대를 생성하고, 한세대에 몇개의 염색체를 생성할지, 각 염색체에서 생성되는 정보들을 저장하는 방법
# 점수를 매기기 위해서 생산되는 MOL을 stock.csv에 저장하고 order.csv에 맞춰서 공급하는데 수요 맞추치 못하면
# 감점을 하는 형식으로, 또한 모든 과정이 끝난후에 재고가 일정수준 이상 남게 된다면 감점
# PRT 생산도 생각해서 구현시켜주어야 한다.
import os
import generation as g
import Event_Mol as em
import math
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




#------------------------------------------------------------------------------------------------        
        
        
        
        
        
        
# 유전 알고리즘 구현
        
#총 생성할 세대
Generation = 10

#한 세대에 생성할 염색체 개수
Gen_population = 6

score_gen = [] # 하나의 세대의 점수가 저장
w_gen = [] #하나의 세대의 가중치가 저장
df_gen = [] #하나의 세대의 데이터 프레임 저장
#각세대에서 최고점을 기록하는 것을 가져와서 저장하고 가장 마지막에 이중 가장 최고의 점수를 낸것을 가져가자.
best_score = [0] # 가장 높은 점수가 저장
best_w = [] #가장 높은 점수에 해당하는 가중치 저장
best_df = [] #가장 높은 점수에 해당하는 데이터 프레임 저장

c=1

for k in range(Generation):
    #score_gen.clear()
    #w_gen.clear()
    #df_gen.clear() 
    for m in range(Gen_population):
        #하나의 세대를 생성시킨다.(generation을 실행시켜서 이의 정보들을 변수들에 저장한다.)
        #위에서 구현시킨 코드들을 순서대로 진행 시켜서 점수를 매긴다.
        #최고 점수를 가지고 있는 데이터프레임과 가중치를 저장하고, 점수도 저장한다.
        #고득점한 2개의 염색체의 가중치를 저장한다.
        #저장한 가중치로 유전자 변형을 일으킨다.
        #이 가중치를 위에서 언급한 2개의 염색체의 가중치와 함께 다음 세대의 가중치로 활용한다.
        if k==0:
            print(c)
            c+=1
            study = em.Study()
            output, A_line, B_line, studying = g.mains(study)
            listing_A = [] #반환된 데이터 프레임의 A 라인의 process index,process_mode, mol  
            listing_B = [] #반환된 데이터 프레임의 B 라인의 process index,process_mode, mol
            #process 과정에서 필요한 정보들을 추출해 리스트에 저장.
            for i in range(output.shape[0]):
                if output.loc[i,'Event_A'] == 'PROCESS':
                    A = []
                    A.append(i) #해당 인덱스
                    A.append(A_line[i]) ##해당 인덱스의 process_mode
                    A.append(output.loc[i,'MOL_A']) #투입 mol 
                    listing_A.append(A)
                if output.loc[i,'Event_B'] == 'PROCESS':
                    B = []
                    B.append(i)
                    B.append(B_line[i])
                    B.append(output.loc[i,'MOL_B'])
                    listing_B.append(B)
            
            
            
            
            
            #score 측정
            score = 10000
            x=0 #listing_A의 인덱스
            y=0 #listing_B의 인덱스
            z=18 #submission 의 매일 18시 인덱스 초기인덱스는 18 이고 24씩 더해 나가자.
            q = 0 #order의 인덱스
            for j in range(output.shape[0]):
                if j == listing_A[x][0]+48:
                    if listing_A[x][1] == 1:
                        stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1'])+math.trunc(0.975*listing_A[x][2])
                        x += 1
                    elif listing_A[x][1] == 2:
                        stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2'])+math.trunc(0.975*listing_A[x][2])
                        x += 1
                    elif listing_A[x][1] == 3:
                        stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3'])+math.trunc(0.975*listing_A[x][2])
                        x += 1
                    elif listing_A[x][1] == 4:
                        stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4'])+math.trunc(0.975*listing_A[x][2])
                        x += 1
                if j == listing_B[y][0]+48:
                    if listing_B[y][1] == 1:
                        stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1'])+math.trunc(0.975*listing_B[y][2])
                        y += 1
                    elif listing_B[y][1] == 2:
                        stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2'])+math.trunc(0.975*listing_B[y][2])
                        y += 1
                    elif listing_B[y][1] == 3:
                        stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3'])+math.trunc(0.975*listing_B[y][2])
                        y+= 1
                    elif listing_B[y][1] == 4:
                        stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4'])+math.trunc(0.975*listing_B[y][2])
                        y += 1
                if (j == z) and (j<=719): #4월
                    order_1 = int(order_ini.loc[q,'BLK_1'])
                    order_2 = int(order_ini.loc[q,'BLK_2'])
                    order_3 = int(order_ini.loc[q,'BLK_3'])
                    order_4 = int(order_ini.loc[q,'BLK_4'])
                    stock_1 = int(stock_ini.loc[:,'BLK_1'])
                    stock_2 = int(stock_ini.loc[:,'BLK_2'])
                    stock_3 = int(stock_ini.loc[:,'BLK_3'])
                    stock_4 = int(stock_ini.loc[:,'BLK_4'])
                    MOL_1 = int(stock_ini.loc[:,'MOL_1'])
                    MOL_2 = int(stock_ini.loc[:,'MOL_2'])
                    MOL_3 = int(stock_ini.loc[:,'MOL_3'])
                    MOL_4 = int(stock_ini.loc[:,'MOL_4'])
                    cut_1 = int(cutyield_ini.loc[0,'BLK_1'])/100
                    cut_2 = int(cutyield_ini.loc[0,'BLK_2'])/100
                    cut_3 = int(cutyield_ini.loc[0,'BLK_3'])/100
                    cut_4 = int(cutyield_ini.loc[0,'BLK_4'])/100
                    
                    if stock_1 >= order_1:
                        stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
                        
                    else:
                        differ = order_1 - stock_1
                        if MOL_1 >= differ/cut_1:
                            stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1']) - differ/cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1']) + differ*cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
            
                        else:
                            stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1']) - differ/cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1']) + differ*cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
                            score -= 1
                            
                            
                    if stock_2 >= order_2:
                        stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                        
                    else:
                        differ = order_2 - stock_2
                        if MOL_2 >= differ/cut_2:
                            stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2']) - differ/cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2']) + differ*cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                            
                        else:
                            stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2']) - differ/cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2']) + differ*cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                            score -= 1
                            
            
                    if stock_3 >= order_3:
                        stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                        
                    else:
                        differ = order_3 - stock_3
                        if MOL_3 >= differ/cut_3:
                            stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3']) - differ/cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3']) + differ*cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                        else:
                            stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3']) - differ/cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3']) + differ*cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                            score -= 1
            
             
                    if stock_4 >= order_4:
                        stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                        
                    else:
                        differ = order_4 - stock_4
                        if MOL_1 >= differ/cut_1:
                            stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4']) - differ/cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4']) + differ*cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                        else:
                            stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4']) - differ/cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4']) + differ*cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                            score -= 1        
                            
                            
                    z += 24
                    q += 1
                    
                    
                    
                if (j == z) and (j>719) and (j<=1463): #5월
                    order_1 = int(order_ini.loc[q,'BLK_1'])
                    order_2 = int(order_ini.loc[q,'BLK_2'])
                    order_3 = int(order_ini.loc[q,'BLK_3'])
                    order_4 = int(order_ini.loc[q,'BLK_4'])
                    stock_1 = int(stock_ini.loc[:,'BLK_1'])
                    stock_2 = int(stock_ini.loc[:,'BLK_2'])
                    stock_3 = int(stock_ini.loc[:,'BLK_3'])
                    stock_4 = int(stock_ini.loc[:,'BLK_4'])
                    MOL_1 = int(stock_ini.loc[:,'MOL_1'])
                    MOL_2 = int(stock_ini.loc[:,'MOL_2'])
                    MOL_3 = int(stock_ini.loc[:,'MOL_3'])
                    MOL_4 = int(stock_ini.loc[:,'MOL_4'])
                    cut_1 = int(cutyield_ini.loc[1,'BLK_1'])/100
                    cut_2 = int(cutyield_ini.loc[1,'BLK_2'])/100
                    cut_3 = int(cutyield_ini.loc[1,'BLK_3'])/100
                    cut_4 = int(cutyield_ini.loc[1,'BLK_4'])/100
                    
                    if stock_1 >= order_1:
                        stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
                        
                    else:
                        differ = order_1 - stock_1
                        if MOL_1 >= differ/cut_1:
                            stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1']) - differ/cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1']) + differ*cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
            
                        else:
                            stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1']) - differ/cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1']) + differ*cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
                            score -= 1
                            
                            
                    if stock_2 >= order_2:
                        stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                        
                    else:
                        differ = order_2 - stock_2
                        if MOL_2 >= differ/cut_2:
                            stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2']) - differ/cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2']) + differ*cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                            
                        else:
                            stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2']) - differ/cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2']) + differ*cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                            score -= 1
                            
            
                    if stock_3 >= order_3:
                        stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                        
                    else:
                        differ = order_3 - stock_3
                        if MOL_3 >= differ/cut_3:
                            stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3']) - differ/cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3']) + differ*cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                        else:
                            stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3']) - differ/cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3']) + differ*cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                            score -= 1
            
             
                    if stock_4 >= order_4:
                        stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                        
                    else:
                        differ = order_4 - stock_4
                        if MOL_1 >= differ/cut_1:
                            stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4']) - differ/cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4']) + differ*cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                        else:
                            stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4']) - differ/cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4']) + differ*cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                            score -= 1        
                            
                            
                    z += 24
                    q += 1
                    
                    
                if (j == z) and (j>1463) and (j<=2183): #6월
                    order_1 = int(order_ini.loc[q,'BLK_1'])
                    order_2 = int(order_ini.loc[q,'BLK_2'])
                    order_3 = int(order_ini.loc[q,'BLK_3'])
                    order_4 = int(order_ini.loc[q,'BLK_4'])
                    stock_1 = int(stock_ini.loc[:,'BLK_1'])
                    stock_2 = int(stock_ini.loc[:,'BLK_2'])
                    stock_3 = int(stock_ini.loc[:,'BLK_3'])
                    stock_4 = int(stock_ini.loc[:,'BLK_4'])
                    MOL_1 = int(stock_ini.loc[:,'MOL_1'])
                    MOL_2 = int(stock_ini.loc[:,'MOL_2'])
                    MOL_3 = int(stock_ini.loc[:,'MOL_3'])
                    MOL_4 = int(stock_ini.loc[:,'MOL_4'])
                    cut_1 = int(cutyield_ini.loc[2,'BLK_1'])/100
                    cut_2 = int(cutyield_ini.loc[2,'BLK_2'])/100
                    cut_3 = int(cutyield_ini.loc[2,'BLK_3'])/100
                    cut_4 = int(cutyield_ini.loc[2,'BLK_4'])/100
                    
                    if stock_1 >= order_1:
                        stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
                        
                    else:
                        differ = order_1 - stock_1
                        if MOL_1 >= differ/cut_1:
                            stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1']) - differ/cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1']) + differ*cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
            
                        else:
                            stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1']) - differ/cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1']) + differ*cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
                            score -= 1
                            
                            
                    if stock_2 >= order_2:
                        stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                        
                    else:
                        differ = order_2 - stock_2
                        if MOL_2 >= differ/cut_2:
                            stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2']) - differ/cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2']) + differ*cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                            
                        else:
                            stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2']) - differ/cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2']) + differ*cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                            score -= 1
                            
            
                    if stock_3 >= order_3:
                        stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                        
                    else:
                        differ = order_3 - stock_3
                        if MOL_3 >= differ/cut_3:
                            stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3']) - differ/cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3']) + differ*cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                        else:
                            stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3']) - differ/cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3']) + differ*cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                            score -= 1
            
             
                    if stock_4 >= order_4:
                        stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                        
                    else:
                        differ = order_4 - stock_4
                        if MOL_1 >= differ/cut_1:
                            stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4']) - differ/cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4']) + differ*cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                        else:
                            stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4']) - differ/cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4']) + differ*cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                            score -= 1        
                            
                            
                    z += 24
                    q += 1 

            #생성된 염색체를 판단하고 조작하기 위해 각자 필요한 정보를 저장.
            score_gen.append(score)
            w_gen.append(studying.w1)
            w_gen.append(studying.w2)
            w_gen.append(studying.w3)
            w_gen.append(studying.w4)
            w_gen.append(studying.w5)
            w_gen.append(studying.w6)
            w_gen.append(studying.w7)
            w_gen.append(studying.w8)
            df_gen.append(output)
            

            

        else:
            print(c)
            c+=1
            study = em.Study()
            study.w1 = w_gen[(8*m)+0]
            study.w2 = w_gen[(8*m)+1]
            study.w3 = w_gen[(8*m)+2]
            study.w4 = w_gen[(8*m)+3]
            study.w5 = w_gen[(8*m)+4]
            study.w6 = w_gen[(8*m)+5]
            study.w7 = w_gen[(8*m)+6]
            study.w8 = w_gen[(8*m)+7]
            
            output, A_line, B_line, studying = g.mains(study)
            listing_A = [] #반환된 데이터 프레임의 A 라인의 process index,process_mode, mol  
            listing_B = [] #반환된 데이터 프레임의 B 라인의 process index,process_mode, mol
            #process 과정에서 필요한 정보들을 추출해 리스트에 저장.
            for l in range(output.shape[0]):
                if output.loc[l,'Event_A'] == 'PROCESS':
                    A = []
                    A.append(l) #해당 인덱스
                    A.append(A_line[l]) ##해당 인덱스의 process_mode
                    A.append(output.loc[l,'MOL_A']) #투입 mol 
                    listing_A.append(A)
                if output.loc[l,'Event_B'] == 'PROCESS':
                    B = []
                    B.append(l)
                    B.append(B_line[l])
                    B.append(output.loc[l,'MOL_B'])
                    listing_B.append(B)
            
            
            
            
            
            #score 측정
            score = 10000
            x=0 #listing_A의 인덱스
            y=0 #listing_B의 인덱스
            z=18 #submission 의 매일 18시 인덱스 초기인덱스는 18 이고 24씩 더해 나가자.
            q = 0 #order의 인덱스
            for n in range(output.shape[0]):
                if n == listing_A[x][0]+48:
                    if listing_A[x][1] == 1:
                        stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1'])+math.trunc(0.975*listing_A[x][2])
                        x += 1
                    elif listing_A[x][1] == 2:
                        stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2'])+math.trunc(0.975*listing_A[x][2])
                        x += 1
                    elif listing_A[x][1] == 3:
                        stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3'])+math.trunc(0.975*listing_A[x][2])
                        x += 1
                    elif listing_A[x][1] == 4:
                        stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4'])+math.trunc(0.975*listing_A[x][2])
                        x += 1
                if n == listing_B[y][0]+48:
                    if listing_B[y][1] == 1:
                        stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1'])+math.trunc(0.975*listing_B[y][2])
                        y += 1
                    elif listing_B[y][1] == 2:
                        stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2'])+math.trunc(0.975*listing_B[y][2])
                        y += 1
                    elif listing_B[y][1] == 3:
                        stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3'])+math.trunc(0.975*listing_B[y][2])
                        y+= 1
                    elif listing_B[y][1] == 4:
                        stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4'])+math.trunc(0.975*listing_B[y][2])
                        y += 1
                if (n == z) and (n<=719): #4월
                    order_1 = int(order_ini.loc[q,'BLK_1'])
                    order_2 = int(order_ini.loc[q,'BLK_2'])
                    order_3 = int(order_ini.loc[q,'BLK_3'])
                    order_4 = int(order_ini.loc[q,'BLK_4'])
                    stock_1 = int(stock_ini.loc[:,'BLK_1'])
                    stock_2 = int(stock_ini.loc[:,'BLK_2'])
                    stock_3 = int(stock_ini.loc[:,'BLK_3'])
                    stock_4 = int(stock_ini.loc[:,'BLK_4'])
                    MOL_1 = int(stock_ini.loc[:,'MOL_1'])
                    MOL_2 = int(stock_ini.loc[:,'MOL_2'])
                    MOL_3 = int(stock_ini.loc[:,'MOL_3'])
                    MOL_4 = int(stock_ini.loc[:,'MOL_4'])
                    cut_1 = int(cutyield_ini.loc[0,'BLK_1'])/100
                    cut_2 = int(cutyield_ini.loc[0,'BLK_2'])/100
                    cut_3 = int(cutyield_ini.loc[0,'BLK_3'])/100
                    cut_4 = int(cutyield_ini.loc[0,'BLK_4'])/100
                    
                    if stock_1 >= order_1:
                        stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
                        
                    else:
                        differ = order_1 - stock_1
                        if MOL_1 >= differ/cut_1:
                            stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1']) - differ/cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1']) + differ*cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
            
                        else:
                            stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1']) - differ/cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1']) + differ*cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
                            score -= 1
                            
                            
                    if stock_2 >= order_2:
                        stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                        
                    else:
                        differ = order_2 - stock_2
                        if MOL_2 >= differ/cut_2:
                            stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2']) - differ/cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2']) + differ*cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                            
                        else:
                            stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2']) - differ/cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2']) + differ*cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                            score -= 1
                            
            
                    if stock_3 >= order_3:
                        stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                        
                    else:
                        differ = order_3 - stock_3
                        if MOL_3 >= differ/cut_3:
                            stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3']) - differ/cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3']) + differ*cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                        else:
                            stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3']) - differ/cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3']) + differ*cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                            score -= 1
            
             
                    if stock_4 >= order_4:
                        stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                        
                    else:
                        differ = order_4 - stock_4
                        if MOL_1 >= differ/cut_1:
                            stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4']) - differ/cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4']) + differ*cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                        else:
                            stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4']) - differ/cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4']) + differ*cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                            score -= 1        
                            
                            
                    z += 24
                    q += 1
                    
                    
                    
                if (n == z) and (n>719) and (n<=1463): #5월
                    order_1 = int(order_ini.loc[q,'BLK_1'])
                    order_2 = int(order_ini.loc[q,'BLK_2'])
                    order_3 = int(order_ini.loc[q,'BLK_3'])
                    order_4 = int(order_ini.loc[q,'BLK_4'])
                    stock_1 = int(stock_ini.loc[:,'BLK_1'])
                    stock_2 = int(stock_ini.loc[:,'BLK_2'])
                    stock_3 = int(stock_ini.loc[:,'BLK_3'])
                    stock_4 = int(stock_ini.loc[:,'BLK_4'])
                    MOL_1 = int(stock_ini.loc[:,'MOL_1'])
                    MOL_2 = int(stock_ini.loc[:,'MOL_2'])
                    MOL_3 = int(stock_ini.loc[:,'MOL_3'])
                    MOL_4 = int(stock_ini.loc[:,'MOL_4'])
                    cut_1 = int(cutyield_ini.loc[1,'BLK_1'])/100
                    cut_2 = int(cutyield_ini.loc[1,'BLK_2'])/100
                    cut_3 = int(cutyield_ini.loc[1,'BLK_3'])/100
                    cut_4 = int(cutyield_ini.loc[1,'BLK_4'])/100
                    
                    if stock_1 >= order_1:
                        stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
                        
                    else:
                        differ = order_1 - stock_1
                        if MOL_1 >= differ/cut_1:
                            stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1']) - differ/cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1']) + differ*cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
            
                        else:
                            stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1']) - differ/cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1']) + differ*cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
                            score -= 1
                            
                            
                    if stock_2 >= order_2:
                        stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                        
                    else:
                        differ = order_2 - stock_2
                        if MOL_2 >= differ/cut_2:
                            stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2']) - differ/cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2']) + differ*cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                            
                        else:
                            stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2']) - differ/cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2']) + differ*cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                            score -= 1
                            
            
                    if stock_3 >= order_3:
                        stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                        
                    else:
                        differ = order_3 - stock_3
                        if MOL_3 >= differ/cut_3:
                            stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3']) - differ/cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3']) + differ*cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                        else:
                            stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3']) - differ/cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3']) + differ*cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                            score -= 1
            
             
                    if stock_4 >= order_4:
                        stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                        
                    else:
                        differ = order_4 - stock_4
                        if MOL_1 >= differ/cut_1:
                            stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4']) - differ/cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4']) + differ*cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                        else:
                            stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4']) - differ/cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4']) + differ*cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                            score -= 1        
                            
                            
                    z += 24
                    q += 1
                    
                    
                if (n == z) and (n>1463) and (n<=2183): #6월
                    order_1 = int(order_ini.loc[q,'BLK_1'])
                    order_2 = int(order_ini.loc[q,'BLK_2'])
                    order_3 = int(order_ini.loc[q,'BLK_3'])
                    order_4 = int(order_ini.loc[q,'BLK_4'])
                    stock_1 = int(stock_ini.loc[:,'BLK_1'])
                    stock_2 = int(stock_ini.loc[:,'BLK_2'])
                    stock_3 = int(stock_ini.loc[:,'BLK_3'])
                    stock_4 = int(stock_ini.loc[:,'BLK_4'])
                    MOL_1 = int(stock_ini.loc[:,'MOL_1'])
                    MOL_2 = int(stock_ini.loc[:,'MOL_2'])
                    MOL_3 = int(stock_ini.loc[:,'MOL_3'])
                    MOL_4 = int(stock_ini.loc[:,'MOL_4'])
                    cut_1 = int(cutyield_ini.loc[2,'BLK_1'])/100
                    cut_2 = int(cutyield_ini.loc[2,'BLK_2'])/100
                    cut_3 = int(cutyield_ini.loc[2,'BLK_3'])/100
                    cut_4 = int(cutyield_ini.loc[2,'BLK_4'])/100
                    
                    if stock_1 >= order_1:
                        stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
                        
                    else:
                        differ = order_1 - stock_1
                        if MOL_1 >= differ/cut_1:
                            stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1']) - differ/cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1']) + differ*cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
            
                        else:
                            stock_ini.loc[:,'MOL_1'] = int(stock_ini.loc[:,'MOL_1']) - differ/cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1']) + differ*cut_1
                            stock_ini.loc[:,'BLK_1'] = int(stock_ini.loc[:,'BLK_1'])-int(order_ini.loc[q,'BLK_1'])
                            score -= 1
                            
                            
                    if stock_2 >= order_2:
                        stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                        
                    else:
                        differ = order_2 - stock_2
                        if MOL_2 >= differ/cut_2:
                            stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2']) - differ/cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2']) + differ*cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                            
                        else:
                            stock_ini.loc[:,'MOL_2'] = int(stock_ini.loc[:,'MOL_2']) - differ/cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2']) + differ*cut_2
                            stock_ini.loc[:,'BLK_2'] = int(stock_ini.loc[:,'BLK_2'])-int(order_ini.loc[q,'BLK_2'])
                            score -= 1
                            
            
                    if stock_3 >= order_3:
                        stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                        
                    else:
                        differ = order_3 - stock_3
                        if MOL_3 >= differ/cut_3:
                            stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3']) - differ/cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3']) + differ*cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                        else:
                            stock_ini.loc[:,'MOL_3'] = int(stock_ini.loc[:,'MOL_3']) - differ/cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3']) + differ*cut_3
                            stock_ini.loc[:,'BLK_3'] = int(stock_ini.loc[:,'BLK_3'])-int(order_ini.loc[q,'BLK_3'])
                            score -= 1
            
             
                    if stock_4 >= order_4:
                        stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                        
                    else:
                        differ = order_4 - stock_4
                        if MOL_1 >= differ/cut_1:
                            stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4']) - differ/cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4']) + differ*cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                        else:
                            stock_ini.loc[:,'MOL_4'] = int(stock_ini.loc[:,'MOL_4']) - differ/cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4']) + differ*cut_4
                            stock_ini.loc[:,'BLK_4'] = int(stock_ini.loc[:,'BLK_4'])-int(order_ini.loc[q,'BLK_4'])
                            score -= 1        
                            
                            
                    z += 24
                    q += 1            

            
            #생성된 염색체를 판단하고 조작하기 위해 각자 필요한 정보를 저장.
            #score_gen.append(score)
            #w_gen.append(studying.w1)
            #w_gen.append(studying.w2)
            #w_gen.append(studying.w3)
            #w_gen.append(studying.w4)
            #w_gen.append(studying.w5)
            #w_gen.append(studying.w6)
            #w_gen.append(studying.w7)
            #w_gen.append(studying.w8)
            #df_gen.append(output)

            score_gen[m] = score
            w_gen[(8*m)+0] = studying.w1
            w_gen[(8*m)+1] = studying.w2
            w_gen[(8*m)+2] = studying.w3
            w_gen[(8*m)+3] = studying.w4
            w_gen[(8*m)+4] = studying.w5
            w_gen[(8*m)+5] = studying.w6
            w_gen[(8*m)+6] = studying.w7
            w_gen[(8*m)+7] = studying.w8
            df_gen[m] = output
    

    
    #최고점수 나온거 저장하자.        
    max_index_list = np.array(score_gen)
    max_index = max_index_list.argmax()
    if best_score[0] < score_gen[max_index]:
        best_score.clear()
        best_df.clear()
        best_score.append(score_gen[max_index])
        best_df.append(df_gen[max_index])        

    #유전자 조작을 위해서 점수가 좋은 두개의 가중치를 가져와서 조작한다.
    max_index_list = np.array(score_gen)
    find_max = max_index_list.argsort()
    lengths = len(find_max)
    one = find_max[lengths-1]
    two = find_max[lengths-2]
    # best 유전자 가중치
    my_w1 = w_gen[(8*one)+0]
    my_w2 = w_gen[(8*one)+1]
    my_w3 = w_gen[(8*one)+2]
    my_w4 = w_gen[(8*one)+3]
    my_w5 = w_gen[(8*one)+4]
    my_w6 = w_gen[(8*one)+5]
    my_w7 = w_gen[(8*one)+6]
    my_w8 = w_gen[(8*one)+7]
    # 두번째로 성적이 좋은 유전자 가중치
    my2_w1 = w_gen[(8*two)+0] 
    my2_w2 = w_gen[(8*two)+1]
    my2_w3 = w_gen[(8*two)+2]
    my2_w4 = w_gen[(8*two)+3]
    my2_w5 = w_gen[(8*two)+4]
    my2_w6 = w_gen[(8*two)+5]
    my2_w7 = w_gen[(8*two)+6]
    my2_w8 = w_gen[(8*two)+7]
    
    use_w1 = w_gen[(8*one)+0]
    use_w2 = w_gen[(8*one)+1]
    use_w3 = w_gen[(8*one)+2]
    use_w4 = w_gen[(8*one)+3]
    use_w5 = w_gen[(8*one)+4]
    use_w6 = w_gen[(8*one)+5]
    use_w7 = w_gen[(8*one)+6]
    use_w8 = w_gen[(8*one)+7]
    
    #유전자 조작을 해주는 단계
    #아이디어 : 행길이 수 중에 랜덤으로 뽑아 잘라내어 합성시킨다. 한 세대에 발생시킬 염색체 수만큼.
    for v in range(Gen_population):
        
        for h in range(len(my_w1)): 
            cut = np.random.randint(my_w1.shape[1])
            use_w1[h,:cut] = my_w1[h,:cut]
            use_w1[h,cut:] = my2_w1[h,cut:]
        w_gen[(8*v)+0] = use_w1
            
        
        for o in range(len(my_w2)): 
            cut = np.random.randint(my_w2.shape[1])
            use_w2[o,:cut] = my_w2[o,:cut]
            use_w2[o,cut:] = my2_w2[o,cut:]
        w_gen[(8*v)+1] = use_w2
    
    
        for f in range(len(my_w3)): 
            cut = np.random.randint(my_w3.shape[1])
            use_w3[f,:cut] = my_w3[f,:cut]
            use_w3[f,cut:] = my2_w3[f,cut:]
        w_gen[(8*v)+2] = use_w3
            
            
        for w in range(len(my_w4)): 
            cut = np.random.randint(my_w4.shape[1])
            use_w4[w,:cut] = my_w4[w,:cut]
            use_w4[w,cut:] = my2_w4[w,cut:]
        w_gen[(8*v)+3] = use_w4
            
            
        for p in range(len(my_w5)): 
            cut = np.random.randint(my_w5.shape[1])
            use_w5[p,:cut] = my_w5[p,:cut]
            use_w5[p,cut:] = my2_w5[p,cut:]
        w_gen[(8*v)+4] = use_w5
            
            
        for d in range(len(my_w6)): 
            cut = np.random.randint(my_w6.shape[1])
            use_w6[d,:cut] = my_w6[d,:cut]
            use_w6[d,cut:] = my2_w6[d,cut:]
        w_gen[(8*v)+5] = use_w6
    
    
        for e in range(len(my_w7)): 
            cut = np.random.randint(my_w7.shape[1])
            use_w7[e,:cut] = my_w7[e,:cut]
            use_w7[e,cut:] = my2_w7[e,cut:]
        w_gen[(8*v)+6] = use_w7
            
            
        for _ in range(len(my_w8)): 
            cut = np.random.randint(my_w8.shape[1])
            use_w8[_,:cut] = my_w8[_,:cut]
            use_w8[_,cut:] = my2_w8[_,cut:]
        w_gen[(8*v)+7] = use_w8
            
    
    #돌연변이 생성
    mutation = 0.5
    if np.random.uniform(0,1) < mutation:
        i = np.random.randint(0,Gen_population-1)
        j = np.random.randint(0,use_w1.shape[0])
        input_w = np.random.randn(1,use_w1.shape[1])
        w_gen[(8*i)+0][j] = input_w

    if np.random.uniform(0,1) < mutation:
        i = np.random.randint(0,Gen_population-1)
        j = np.random.randint(0,use_w2.shape[0])
        input_w = np.random.randn(1,use_w2.shape[1])
        w_gen[(8*i)+1][j] = input_w
        
    if np.random.uniform(0,1) < mutation:
        i = np.random.randint(0,Gen_population-1)
        j = np.random.randint(0,use_w3.shape[0])
        input_w = np.random.randn(1,use_w3.shape[1])
        w_gen[(8*i)+2][j] = input_w
        
    if np.random.uniform(0,1) < mutation:
        i = np.random.randint(0,Gen_population-1)
        j = np.random.randint(0,use_w4.shape[0])
        input_w = np.random.randn(1,use_w4.shape[1])
        w_gen[(8*i)+3][j] = input_w

    if np.random.uniform(0,1) < mutation:
        i = np.random.randint(0,Gen_population-1)
        j = np.random.randint(0,use_w5.shape[0])
        input_w = np.random.randn(1,use_w5.shape[1])
        w_gen[(8*i)+4][j] = input_w

    if np.random.uniform(0,1) < mutation:
        i = np.random.randint(0,Gen_population-1)
        j = np.random.randint(0,use_w6.shape[0])
        input_w = np.random.randn(1,use_w6.shape[1])
        w_gen[(8*i)+5][j] = input_w
    
    if np.random.uniform(0,1) < mutation:
        i = np.random.randint(0,Gen_population-1)
        j = np.random.randint(0,use_w7.shape[0])
        input_w = np.random.randn(1,use_w7.shape[1])
        w_gen[(8*i)+6][j] = input_w            
    
    if np.random.uniform(0,1) < mutation:
        i = np.random.randint(0,Gen_population-1)
        j = np.random.randint(0,use_w8.shape[0])
        input_w = np.random.randn(1,use_w8.shape[1])
        w_gen[(8*i)+7][j] = input_w
                   
    print("Generation:"+str(k)+"Best score:"+str(best_score[0]))            
           
                
print(best_score)
print(best_df)
            
            
            
            
            
            
            
            
            
            
            
