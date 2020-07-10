# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 16:35:50 2020

@author: l_jun
"""
import os
import pandas as pd
import numpy as np
from pathlib import Path
import Event_Mol as em
import random

def setting_func():
    submission_ini = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'sample_submission.csv'))
    order_ini = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'order.csv'))
    changetime_ini = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'change_time.csv'))
    stock_ini =  pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'stock.csv'))
    maxcount_ini =  pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'max_count.csv'))
    cutyield_int = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'cut_yield.csv'))
    
    
    em.mask = np.zeros([18],np.bool) # 가능한 이벤트 검사용 마스크
    em.event_map = {0:'CHECK_1', 1:'CHECK_2', 2:'CHECK_3', 3:'CHECK_4', 4:'PROCESS', 5:'CHANGE_12', 6:'CHANGE_13', 7:'CHANGE_14', 8:'CHANGE_21', 9:'CHANGE_23', 10:'CHANGE_24', 11:'CHANGE_31', 12:'CHANGE_32', 13:'CHANGE_34', 14:'CHANGE_41', 15:'CHANGE_42', 16:'CHANGE_43', 17:'STOP'}
    
    #공정과정에 필요한 변수를 선언해 보자.
    em.process = False #공정 수행 가능 여부
    em.process_time = 1 #공정이 돌아간 총 시간
    em.process_mode = 0 #공정 모드 1~4
    em.stop = False #정지 기능
    em.stop_time = 1 #정지 되어있는 시간
    em.check = False #체크 수행 여
    em.check_time = 27 #체크 시간
    em.check_mode = 0 # 체크 모드 1~4
    em.change = False #change 기능
    em.change_mode = 0 #change 모드 ex)12 == change_12
    em.mol_A_input = 0 #성형 A라인에 투입개수
    em.mol_B_input = 0 #성형 B라인에 투입개수
    
    em.change_time12 = changetime_ini.loc[0,'time']-1
    em.change_time13 = changetime_ini.loc[1,'time']-1
    em.change_time14 = changetime_ini.loc[2,'time']-1
    em.change_time21 = changetime_ini.loc[3,'time']-1
    em.change_time23 = changetime_ini.loc[4,'time']-1
    em.change_time24 = changetime_ini.loc[5,'time']-1
    em.change_time31 = changetime_ini.loc[6,'time']-1
    em.change_time32 = changetime_ini.loc[7,'time']-1
    em.change_time34 = changetime_ini.loc[8,'time']-1
    em.change_time41 = changetime_ini.loc[9,'time']-1
    em.change_time42 = changetime_ini.loc[10,'time']-1
    em.change_time43 = changetime_ini.loc[11,'time']-1
    
def mains(vs):
    gen = 0 #세대수(유전 알고리즘)
    process_gen = 50 #진행시키고자 하는 세대수(유전 알고리즘)
    
    #csv 파일들을 불러오자.
    submission_ini = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'sample_submission.csv'))
    order_ini = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'order.csv'))
    changetime_ini = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'change_time.csv'))
    stock_ini =  pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'stock.csv'))
    maxcount_ini =  pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'max_count.csv'))
    cutyield_ini = pd.read_csv(os.path.join(Path(__file__).resolve().parent, 'cut_yield.csv'))
    
    
    #line A
    
    study = vs #최초 인스턴스 생성  
    list_A =[]
    list_B =[]
    gen += 1 #세대 진행
    setting_func()
    study.mask[0] = True
    study.mask[1] = True
    study.mask[2] = True
    study.mask[3] = True
    for i in range(order_ini.shape[0]): #총 공정 날짜수
        maxcount = maxcount_ini.loc[i,'count']
        for j in range(24): #하루 24시간
            event , mol = study.processing(i)
            if maxcount == 0:
                if event == 'CHECK_1':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 1
                      study.process = False
                      study.mask[4] = False
                      study.mask[0] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = False
                          study.mask[1] = True
                          study.mask[2] = True
                          study.mask[3] = True
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 1
                      study.mask[0] = False
                      study.mask[4] = True          
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)
                  
                elif event == 'CHECK_2':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 2
                      study.process = False
                      study.mask[4] = False
                      study.mask[1] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = True
                          study.mask[1] = False
                          study.mask[2] = True
                          study.mask[3] = True
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 2
                      study.mask[1] = False
                      study.mask[4] = True  
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
                elif event == 'CHECK_3':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 3
                      study.process = False
                      study.mask[4] = False
                      study.mask[2] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = True
                          study.mask[1] = True
                          study.mask[2] = False
                          study.mask[3] = True
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 3
                      study.mask[2] = False
                      study.mask[4] = True
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
                elif event == 'CHECK_4':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 4
                      study.process = False
                      study.mask[4] = False
                      study.mask[3] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = True
                          study.mask[1] = True
                          study.mask[2] = True
                          study.mask[3] = False
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 4
                      study.mask[3] = False
                      study.mask[4] = True
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
                elif event == 'PROCESS':
                  if study.process_mode == 1:
                      list_A.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time < 98):
                          study.process = True
                          study.mask[4] = True
                          study.mask[0] = False
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt1 = em.submission_ini.loc[24*i+j,'PRT_1']
                          prt1 = prt1 - mol
                      elif (study.process_time >= 98) and (study.process_time < 140):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt1 = em.submission_ini.loc[24*i+j,'PRT_1']
                          prt1 = prt1 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time12) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 12
                              study.mask[5] = True
                              study.change_time12 = changetime_ini.loc[0,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time13) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 13
                              study.mask[6] = True
                              study.change_time13 = changetime_ini.loc[1,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time14) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 14
                              study.mask[7] = True
                              study.change_time14 = changetime_ini.loc[2,'time']-1        
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27   
                            
                            
                  elif study.process_mode == 2:
                      list_A.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time <98):
                          study.process = True
                          study.mask[4] = True
                          study.mask[1] = False
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt2 = em.submission_ini.loc[24*i+j,'PRT_2']
                          prt2 = prt2 - mol
                      elif (study.process_time >= 98) and (study.process_time <140):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt2 = em.submission_ini.loc[24*i+j,'PRT_2']
                          prt2 = prt2 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time21) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 21
                              study.mask[8] = True
                              study.change_time21 = changetime_ini.loc[3,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time23) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 23
                              study.mask[9] = True
                              study.change_time23 = changetime_ini.loc[4,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time24) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 24
                              study.mask[10] = True
                              study.change_time24 = changetime_ini.loc[5,'time']-1
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27
                            
                            
                  elif study.process_mode == 3:
                      list_A.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time <98):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt3 = em.submission_ini.loc[24*i+j,'PRT_3']
                          prt3 = prt3 - mol
                      elif (study.process_time >= 98) and (study.process_time <140):
                          study.process = True
                          study.mask[4] = True
                          study.mask[2] = False
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt3 = em.submission_ini.loc[24*i+j,'PRT_3']
                          prt3 = prt3 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time31) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 31
                              study.mask[11] = True
                              study.change_time31 = changetime_ini.loc[6,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time32) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 32
                              study.mask[12] = True
                              study.change_time32 = changetime_ini.loc[7,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time34) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 34
                              study.mask[13] = True
                              study.change_time34 = changetime_ini.loc[8,'time']-1
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27
                            
                            
                  elif study.process_mode == 4:
                      list_A.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time <98):
                          study.process = True
                          study.mask[4] = True
                          study.mask[3] = False
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt4 = em.submission_ini.loc[24*i+j,'PRT_4']
                          prt4 = prt4 - mol
                      elif (study.process_time >= 98) and (study.process_time <140):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt4 = em.submission_ini.loc[24*i+j,'PRT_4']
                          prt4 = prt4 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0 
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time41) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 41
                              study.mask[14] = True
                              study.change_time41 = changetime_ini.loc[9,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time42) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 42
                              study.mask[15] = True
                              study.change_time42 = changetime_ini.loc[10,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time43) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 43
                              study.mask[16] = True
                              study.change_time43 = changetime_ini.loc[11,'time']-1
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  submission_ini.loc[24*i+j,'MOL_A'] = 0          
                            
                elif event == 'CHANGE_12':
                  if study.change_time12 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 12
                      study.mask[5] = True
                      study.change_time12 -= 1
                      study.process_time += 1
                  elif study.change_time12 == 0:
                      study.process_mode = 2
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[5] = False
                      study.change_time12 = changetime_ini.loc[0,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
                elif event == 'CHANGE_13':
                  if study.change_time13 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 13
                      study.mask[6] = True
                      study.change_time13 -= 1
                      study.process_time += 1
                  elif study.change_time13 == 0:
                      study.process_mode = 3
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[6] = False
                      study.change_time13 = changetime_ini.loc[1,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
                elif event == 'CHANGE_14':
                  if study.change_time14 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 14
                      study.mask[7] = True
                      study.change_time14 -= 1
                      study.process_time += 1
                  elif study.change_time14 == 0:
                      study.process_mode = 4
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[7] = False
                      study.change_time14 = changetime_ini.loc[2,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
                elif event == 'CHANGE_21':
                  if study.change_time21 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 21
                      study.mask[8] = True
                      study.change_time21 -= 1
                      study.process_time += 1
                  elif study.change_time21 == 0:
                      study.process_mode = 1
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[8] = False
                      study.change_time21 = changetime_ini.loc[3,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
                elif event == 'CHANGE_23':
                  if study.change_time23 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 23
                      study.mask[9] = True
                      study.change_time23 -= 1
                      study.process_time += 1
                  elif study.change_time23 == 0:
                      study.process_mode = 3
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[9] = False
                      study.change_time23 = changetime_ini.loc[4,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
                elif event == 'CHANGE_24':
                  if study.change_time24 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 24
                      study.mask[10] = True
                      study.change_time24 -= 1
                      study.process_time += 1
                  elif study.change_time24 == 0:
                      study.process_mode = 4
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[10] = False
                      study.change_time24 = changetime_ini.loc[5,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
                elif event == 'CHANGE_31':
                  if study.change_time31 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 31
                      study.mask[11] = True
                      study.change_time31 -= 1
                      study.process_time += 1
                  elif study.change_time31 == 0:
                      study.process_mode = 1
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[11] = False
                      study.change_time31 = changetime_ini.loc[6,'time']-1      
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)
                    
                elif event == 'CHANGE_32':
                  if study.change_time32 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 32
                      study.mask[12] = True
                      study.change_time32 -= 1
                      study.process_time += 1
                  elif study.change_time32 == 0:
                      study.process_mode = 2
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[12] = False
                      study.change_time32 = changetime_ini.loc[7,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
                elif event == 'CHANGE_34':
                  if study.change_time34 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 34
                      study.mask[13] = True
                      study.change_time34 -= 1
                      study.process_time += 1
                  elif study.change_time34 == 0:
                      study.process_mode = 4
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[13] = False
                      study.change_time34 = changetime_ini.loc[8,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
                elif event == 'CHANGE_41':
                  if study.change_time41 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 41
                      study.mask[14] = True
                      study.change_time41 -= 1
                      study.process_time += 1
                  elif study.change_time41 == 0:
                      study.process_mode = 1
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[14] = False
                      study.change_time41 = changetime_ini.loc[9,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
                elif event == 'CHANGE_42':
                  if study.change_time42 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 42
                      study.mask[15] = True
                      study.change_time42 -= 1
                      study.process_time += 1
                  elif study.change_time42 == 0:
                      study.process_mode = 2
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[15] = False
                      study.change_time42 = changetime_ini.loc[10,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
                elif event == 'CHANGE_43':
                  if study.change_time43 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 43
                      study.mask[16] = True
                      study.change_time43 -= 1
                      study.process_time += 1
                  elif study.change_time43 == 0:
                      study.process_mode = 3
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[16] = False
                      study.change_time43 = changetime_ini.loc[11,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
                elif event == 'STOP':
                  if study.stop_time == 192:
                      study.stop = False
                      study.process_time = 1
                      study.process_mode = 0
                      study.mask[17] = False
                      study.check = True
                      study.check_time = 27
                      study.check_mode = 0
                      study.stop_time = 1
                      study.mask[0] = True
                      study.mask[1] = True
                      study.mask[2] = True
                      study.mask[3] = True
                      study.mask[4] = False
                  elif (study.stop_time >= 0) and (study.stop_time <192):
                      study.process_mode = 0
                      study.process_time = 1
                      study.process = False
                      study.stop = True
                      study.mask[4] = False
                      study.mask[17] = True
                      study.stop_time += 1
                      study.check_time = 27
                      study.check = False
                      study.mask[0] = False
                      study.mask[1] = False
                      study.mask[2] = False
                      study.mask[3] = False
                      random_check = random.randint(0,200)
                      if (random_check >= 0) and (random_check <= 10):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 1
                          study.mask[0] = True
                          study.check_time = 27
                      elif (random_check > 10) and (random_check <= 20):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 2
                          study.mask[1] = True
                          study.check_time = 27
                      elif (random_check > 20) and (random_check <= 30):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 3
                          study.mask[2] = True
                          study.check_time = 27
                      elif (random_check > 30) and (random_check <= 40):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 4
                          study.mask[3] = True
                          study.check_time = 27          
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)
                  
                  
            else:
              if event == 'CHECK_1':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 1
                      study.process = False
                      study.mask[4] = False
                      study.mask[0] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = False
                          study.mask[1] = True
                          study.mask[2] = True
                          study.mask[3] = True
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 1
                      study.mask[0] = False
                      study.mask[4] = True          
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)
                  
              elif event == 'CHECK_2':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 2
                      study.process = False
                      study.mask[4] = False
                      study.mask[1] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = True
                          study.mask[1] = False
                          study.mask[2] = True
                          study.mask[3] = True
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 2
                      study.mask[1] = False
                      study.mask[4] = True  
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
              elif event == 'CHECK_3':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 3
                      study.process = False
                      study.mask[4] = False
                      study.mask[2] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = True
                          study.mask[1] = True
                          study.mask[2] = False
                          study.mask[3] = True
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 3
                      study.mask[2] = False
                      study.mask[4] = True
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
              elif event == 'CHECK_4':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 4
                      study.process = False
                      study.mask[4] = False
                      study.mask[3] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = True
                          study.mask[1] = True
                          study.mask[2] = True
                          study.mask[3] = False
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 4
                      study.mask[3] = False
                      study.mask[4] = True
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
              elif event == 'PROCESS':
                  if study.process_mode == 1:
                      list_A.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time < 98):
                          study.process = True
                          study.mask[4] = True
                          study.mask[0] = False
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt1 = em.submission_ini.loc[24*i+j,'PRT_1']
                          prt1 = prt1 - mol
                      elif (study.process_time >= 98) and (study.process_time < 140):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt1 = em.submission_ini.loc[24*i+j,'PRT_1']
                          prt1 = prt1 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time12) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 12
                              study.mask[5] = True
                              study.change_time12 = changetime_ini.loc[0,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time13) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 13
                              study.mask[6] = True
                              study.change_time13 = changetime_ini.loc[1,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time14) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 14
                              study.mask[7] = True
                              study.change_time14 = changetime_ini.loc[2,'time']-1        
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27   
                            
                            
                  elif study.process_mode == 2:
                      list_A.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time <98):
                          study.process = True
                          study.mask[4] = True
                          study.mask[1] = False
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt2 = em.submission_ini.loc[24*i+j,'PRT_2']
                          prt2 = prt2 - mol
                      elif (study.process_time >= 98) and (study.process_time <140):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt2 = em.submission_ini.loc[24*i+j,'PRT_2']
                          prt2 = prt2 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time21) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 21
                              study.mask[8] = True
                              study.change_time21 = changetime_ini.loc[3,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time23) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 23
                              study.mask[9] = True
                              study.change_time23 = changetime_ini.loc[4,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time24) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 24
                              study.mask[10] = True
                              study.change_time24 = changetime_ini.loc[5,'time']-1
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27
                            
                            
                  elif study.process_mode == 3:
                      list_A.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time <98):
                          study.process = True
                          study.mask[4] = True
                          study.mask[2] = False
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt3 = em.submission_ini.loc[24*i+j,'PRT_3']
                          prt3 = prt3 - mol
                      elif (study.process_time >= 98) and (study.process_time <140):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt3 = em.submission_ini.loc[24*i+j,'PRT_3']
                          prt3 = prt3 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time31) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 31
                              study.mask[11] = True
                              study.change_time31 = changetime_ini.loc[6,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time32) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 32
                              study.mask[12] = True
                              study.change_time32 = changetime_ini.loc[7,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time34) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 34
                              study.mask[13] = True
                              study.change_time34 = changetime_ini.loc[8,'time']-1
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27
                            
                            
                  elif study.process_mode == 4:
                      list_A.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time <98):
                          study.process = True
                          study.mask[4] = True
                          study.mask[3] = False
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt4 = em.submission_ini.loc[24*i+j,'PRT_4']
                          prt4 = prt4 - mol
                      elif (study.process_time >= 98) and (study.process_time <140):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_A_input = mol #나중에 라인분리시 조정필요
                          prt4 = em.submission_ini.loc[24*i+j,'PRT_4']
                          prt4 = prt4 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0 
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time41) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 41
                              study.mask[14] = True
                              study.change_time41 = changetime_ini.loc[9,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time42) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 42
                              study.mask[15] = True
                              study.change_time42 = changetime_ini.loc[10,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time43) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 43
                              study.mask[16] = True
                              study.change_time43 = changetime_ini.loc[11,'time']-1
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  submission_ini.loc[24*i+j,'MOL_A'] = mol          
                            
              elif event == 'CHANGE_12':
                  if study.change_time12 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 12
                      study.mask[5] = True
                      study.change_time12 -= 1
                      study.process_time += 1
                  elif study.change_time12 == 0:
                      study.process_mode = 2
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[5] = False
                      study.change_time12 = changetime_ini.loc[0,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
              elif event == 'CHANGE_13':
                  if study.change_time13 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 13
                      study.mask[6] = True
                      study.change_time13 -= 1
                      study.process_time += 1
                  elif study.change_time13 == 0:
                      study.process_mode = 3
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[6] = False
                      study.change_time13 = changetime_ini.loc[1,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
              elif event == 'CHANGE_14':
                  if study.change_time14 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 14
                      study.mask[7] = True
                      study.change_time14 -= 1
                      study.process_time += 1
                  elif study.change_time14 == 0:
                      study.process_mode = 4
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[7] = False
                      study.change_time14 = changetime_ini.loc[2,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
              elif event == 'CHANGE_21':
                  if study.change_time21 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 21
                      study.mask[8] = True
                      study.change_time21 -= 1
                      study.process_time += 1
                  elif study.change_time21 == 0:
                      study.process_mode = 1
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[8] = False
                      study.change_time21 = changetime_ini.loc[3,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
              elif event == 'CHANGE_23':
                  if study.change_time23 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 23
                      study.mask[9] = True
                      study.change_time23 -= 1
                      study.process_time += 1
                  elif study.change_time23 == 0:
                      study.process_mode = 3
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[9] = False
                      study.change_time23 = changetime_ini.loc[4,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
              elif event == 'CHANGE_24':
                  if study.change_time24 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 24
                      study.mask[10] = True
                      study.change_time24 -= 1
                      study.process_time += 1
                  elif study.change_time24 == 0:
                      study.process_mode = 4
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[10] = False
                      study.change_time24 = changetime_ini.loc[5,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
              elif event == 'CHANGE_31':
                  if study.change_time31 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 31
                      study.mask[11] = True
                      study.change_time31 -= 1
                      study.process_time += 1
                  elif study.change_time31 == 0:
                      study.process_mode = 1
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[11] = False
                      study.change_time31 = changetime_ini.loc[6,'time']-1      
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)
                    
              elif event == 'CHANGE_32':
                  if study.change_time32 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 32
                      study.mask[12] = True
                      study.change_time32 -= 1
                      study.process_time += 1
                  elif study.change_time32 == 0:
                      study.process_mode = 2
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[12] = False
                      study.change_time32 = changetime_ini.loc[7,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
              elif event == 'CHANGE_34':
                  if study.change_time34 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 34
                      study.mask[13] = True
                      study.change_time34 -= 1
                      study.process_time += 1
                  elif study.change_time34 == 0:
                      study.process_mode = 4
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[13] = False
                      study.change_time34 = changetime_ini.loc[8,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
              elif event == 'CHANGE_41':
                  if study.change_time41 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 41
                      study.mask[14] = True
                      study.change_time41 -= 1
                      study.process_time += 1
                  elif study.change_time41 == 0:
                      study.process_mode = 1
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[14] = False
                      study.change_time41 = changetime_ini.loc[9,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
              elif event == 'CHANGE_42':
                  if study.change_time42 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 42
                      study.mask[15] = True
                      study.change_time42 -= 1
                      study.process_time += 1
                  elif study.change_time42 == 0:
                      study.process_mode = 2
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[15] = False
                      study.change_time42 = changetime_ini.loc[10,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
              elif event == 'CHANGE_43':
                  if study.change_time43 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 43
                      study.mask[16] = True
                      study.change_time43 -= 1
                      study.process_time += 1
                  elif study.change_time43 == 0:
                      study.process_mode = 3
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[16] = False
                      study.change_time43 = changetime_ini.loc[11,'time']-1
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)      
                        
              elif event == 'STOP':
                  if study.stop_time == 192:
                      study.stop = False
                      study.process_time = 1
                      study.process_mode = 0
                      study.mask[17] = False
                      study.check = True
                      study.check_time = 27
                      study.check_mode = 0
                      study.stop_time = 1
                      study.mask[0] = True
                      study.mask[1] = True
                      study.mask[2] = True
                      study.mask[3] = True
                      study.mask[4] = False
                  elif (study.stop_time >= 0) and (study.stop_time <192):
                      study.process_mode = 0
                      study.process_time = 1
                      study.process = False
                      study.stop = True
                      study.mask[4] = False
                      study.mask[17] = True
                      study.stop_time += 1
                      study.check_time = 27
                      study.check = False
                      study.mask[0] = False
                      study.mask[1] = False
                      study.mask[2] = False
                      study.mask[3] = False
                      random_check = random.randint(0,200)
                      if (random_check >= 0) and (random_check <= 10):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 1
                          study.mask[0] = True
                          study.check_time = 27
                      elif (random_check > 10) and (random_check <= 20):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 2
                          study.mask[1] = True
                          study.check_time = 27
                      elif (random_check > 20) and (random_check <= 30):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 3
                          study.mask[2] = True
                          study.check_time = 27
                      elif (random_check > 30) and (random_check <= 40):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 4
                          study.mask[3] = True
                          study.check_time = 27
                                             
                  submission_ini.loc[24*i+j,'Event_A'] = event
                  list_A.append(study.process_mode)
    
    
    
    #lineB
                            
    setting_func()
    study.mask[0] = True
    study.mask[1] = True
    study.mask[2] = True
    study.mask[3] = True
    for i in range(order_ini.shape[0]): #총 공정 날짜수
        maxcount = maxcount_ini.loc[i,'count']
        for j in range(24): #하루 24시간
            event , mol = study.processing(i)
            if maxcount == 0:
                if event == 'CHECK_1':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 1
                      study.process = False
                      study.mask[4] = False
                      study.mask[0] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = False
                          study.mask[1] = True
                          study.mask[2] = True
                          study.mask[3] = True
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 1
                      study.mask[0] = False
                      study.mask[4] = True          
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)
                  
                elif event == 'CHECK_2':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 2
                      study.process = False
                      study.mask[4] = False
                      study.mask[1] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = True
                          study.mask[1] = False
                          study.mask[2] = True
                          study.mask[3] = True
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 2
                      study.mask[1] = False
                      study.mask[4] = True  
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event      
                        
                elif event == 'CHECK_3':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 3
                      study.process = False
                      study.mask[4] = False
                      study.mask[2] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = True
                          study.mask[1] = True
                          study.mask[2] = False
                          study.mask[3] = True
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 3
                      study.mask[2] = False
                      study.mask[4] = True
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event      
                        
                elif event == 'CHECK_4':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 4
                      study.process = False
                      study.mask[4] = False
                      study.mask[3] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = True
                          study.mask[1] = True
                          study.mask[2] = True
                          study.mask[3] = False
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 4
                      study.mask[3] = False
                      study.mask[4] = True
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event      
                        
                elif event == 'PROCESS':
                  if study.process_mode == 1:
                      list_B.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time < 98):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt1 = em.submission_ini.loc[24*i+j,'PRT_1']
                          prt1 = prt1 - mol
                      elif (study.process_time >= 98) and (study.process_time < 140):
                          study.process = True
                          study.mask[4] = True
                          study.mask[0] = False
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt1 = em.submission_ini.loc[24*i+j,'PRT_1']
                          prt1 = prt1 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time12) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 12
                              study.mask[5] = True
                              study.change_time12 = changetime_ini.loc[0,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time13) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 13
                              study.mask[6] = True
                              study.change_time13 = changetime_ini.loc[1,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time14) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 14
                              study.mask[7] = True
                              study.change_time14 = changetime_ini.loc[2,'time']-1        
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27   
                            
                            
                  elif study.process_mode == 2:
                      list_B.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time <98):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt2 = em.submission_ini.loc[24*i+j,'PRT_2']
                          prt2 = prt2 - mol
                      elif (study.process_time >= 98) and (study.process_time <140):
                          study.process = True
                          study.mask[4] = True
                          study.mask[1] = False
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt2 = em.submission_ini.loc[24*i+j,'PRT_2']
                          prt2 = prt2 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time21) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 21
                              study.mask[8] = True
                              study.change_time21 = changetime_ini.loc[3,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time23) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 23
                              study.mask[9] = True
                              study.change_time23 = changetime_ini.loc[4,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time24) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 24
                              study.mask[10] = True
                              study.change_time24 = changetime_ini.loc[5,'time']-1
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27
                            
                            
                  elif study.process_mode == 3:
                      list_B.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time <98):
                          study.process = True
                          study.mask[4] = True
                          study.mask[2] = False
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt3 = em.submission_ini.loc[24*i+j,'PRT_3']
                          prt3 = prt3 - mol
                      elif (study.process_time >= 98) and (study.process_time <140):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt3 = em.submission_ini.loc[24*i+j,'PRT_3']
                          prt3 = prt3 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time31) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 31
                              study.mask[11] = True
                              study.change_time31 = changetime_ini.loc[6,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time32) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 32
                              study.mask[12] = True
                              study.change_time32 = changetime_ini.loc[7,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time34) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 34
                              study.mask[13] = True
                              study.change_time34 = changetime_ini.loc[8,'time']-1
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27
                            
                            
                  elif study.process_mode == 4:
                      list_B.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time <98):
                          study.process = True
                          study.mask[4] = True
                          study.mask[3] = False
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt4 = em.submission_ini.loc[24*i+j,'PRT_4']
                          prt4 = prt4 - mol
                      elif (study.process_time >= 98) and (study.process_time <140):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt4 = em.submission_ini.loc[24*i+j,'PRT_4']
                          prt4 = prt4 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0 
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time41) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 41
                              study.mask[14] = True
                              study.change_time41 = changetime_ini.loc[9,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time42) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 42
                              study.mask[15] = True
                              study.change_time42 = changetime_ini.loc[10,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time43) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 43
                              study.mask[16] = True
                              study.change_time43 = changetime_ini.loc[11,'time']-1
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27
                            
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  submission_ini.loc[24*i+j,'MOL_B'] = 0
                  
                elif event == 'CHANGE_12':
                  if study.change_time12 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 12
                      study.mask[5] = True
                      study.change_time12 -= 1
                      study.process_time += 1
                  elif study.change_time12 == 0:
                      study.process_mode = 2
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[5] = False
                      study.change_time12 = changetime_ini.loc[0,'time']-1
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)      
                        
                elif event == 'CHANGE_13':
                  if study.change_time13 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 13
                      study.mask[6] = True
                      study.change_time13 -= 1
                      study.process_time += 1
                  elif study.change_time13 == 0:
                      study.process_mode = 3
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[6] = False
                      study.change_time13 = changetime_ini.loc[1,'time']-1
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)      
                        
                elif event == 'CHANGE_14':
                  if study.change_time14 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 14
                      study.mask[7] = True
                      study.change_time14 -= 1
                      study.process_time += 1
                  elif study.change_time14 == 0:
                      study.process_mode = 4
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[7] = False
                      study.change_time14 = changetime_ini.loc[2,'time']-1
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)      
                        
                elif event == 'CHANGE_21':
                  if study.change_time21 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 21
                      study.mask[8] = True
                      study.change_time21 -= 1
                      study.process_time += 1
                  elif study.change_time21 == 0:
                      study.process_mode = 1
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[8] = False
                      study.change_time21 = changetime_ini.loc[3,'time']-1
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)      
                        
                elif event == 'CHANGE_23':
                  if study.change_time23 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 23
                      study.mask[9] = True
                      study.change_time23 -= 1
                      study.process_time += 1
                  elif study.change_time23 == 0:
                      study.process_mode = 3
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[9] = False
                      study.change_time23 = changetime_ini.loc[4,'time']-1
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)      
                        
                elif event == 'CHANGE_24':
                  if study.change_time24 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 24
                      study.mask[10] = True
                      study.change_time24 -= 1
                      study.process_time += 1
                  elif study.change_time24 == 0:
                      study.process_mode = 4
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[10] = False
                      study.change_time24 = changetime_ini.loc[5,'time']-1
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)      
                        
                elif event == 'CHANGE_31':
                  if study.change_time31 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 31
                      study.mask[11] = True
                      study.change_time31 -= 1
                      study.process_time += 1
                  elif study.change_time31 == 0:
                      study.process_mode = 1
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[11] = False
                      study.change_time31 = changetime_ini.loc[6,'time']-1      
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)
                    
                elif event == 'CHANGE_32':
                  if study.change_time32 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 32
                      study.mask[12] = True
                      study.change_time32 -= 1
                      study.process_time += 1
                  elif study.change_time32 == 0:
                      study.process_mode = 2
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[12] = False
                      study.change_time32 = changetime_ini.loc[7,'time']-1
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)      
                        
                elif event == 'CHANGE_34':
                  if study.change_time34 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 34
                      study.mask[13] = True
                      study.change_time34 -= 1
                      study.process_time += 1
                  elif study.change_time34 == 0:
                      study.process_mode = 4
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[13] = False
                      study.change_time34 = changetime_ini.loc[8,'time']-1
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)      
                        
                elif event == 'CHANGE_41':
                  if study.change_time41 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 41
                      study.mask[14] = True
                      study.change_time41 -= 1
                      study.process_time += 1
                  elif study.change_time41 == 0:
                      study.process_mode = 1
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[14] = False
                      study.change_time41 = changetime_ini.loc[9,'time']-1
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)      
                        
                elif event == 'CHANGE_42':
                  if study.change_time42 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 42
                      study.mask[15] = True
                      study.change_time42 -= 1
                      study.process_time += 1
                  elif study.change_time42 == 0:
                      study.process_mode = 2
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[15] = False
                      study.change_time42 = changetime_ini.loc[10,'time']-1
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)      
                        
                elif event == 'CHANGE_43':
                  if study.change_time43 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 43
                      study.mask[16] = True
                      study.change_time43 -= 1
                      study.process_time += 1
                  elif study.change_time43 == 0:
                      study.process_mode = 3
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[16] = False
                      study.change_time43 = changetime_ini.loc[11,'time']-1
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)      
                        
                elif event == 'STOP':
                  if study.stop_time == 192:
                      study.stop = False
                      study.process_time = 1
                      study.process_mode = 0
                      study.mask[17] = False
                      study.check = True
                      study.check_time = 27
                      study.check_mode = 0
                      study.stop_time = 1
                      study.mask[0] = True
                      study.mask[1] = True
                      study.mask[2] = True
                      study.mask[3] = True
                      study.mask[4] = False
                  elif (study.stop_time >= 0) and (study.stop_time <192):
                      study.process_mode = 0
                      study.process_time = 1
                      study.process = False
                      study.stop = True
                      study.mask[4] = False
                      study.mask[17] = True
                      study.stop_time += 1
                      study.check_time = 27
                      study.check = False
                      study.mask[0] = False
                      study.mask[1] = False
                      study.mask[2] = False
                      study.mask[3] = False
                      random_check = random.randint(0,200)
                      if (random_check >= 0) and (random_check <= 10):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 1
                          study.mask[0] = True
                          study.check_time = 27
                      elif (random_check > 10) and (random_check <= 20):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 2
                          study.mask[1] = True
                          study.check_time = 27
                      elif (random_check > 20) and (random_check <= 30):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 3
                          study.mask[2] = True
                          study.check_time = 27
                      elif (random_check > 30) and (random_check <= 40):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 4
                          study.mask[3] = True
                          study.check_time = 27
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)
                
            else:
              if event == 'CHECK_1':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 1
                      study.process = False
                      study.mask[4] = False
                      study.mask[0] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = False
                          study.mask[1] = True
                          study.mask[2] = True
                          study.mask[3] = True
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 1
                      study.mask[0] = False
                      study.mask[4] = True          
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)
                  
              elif event == 'CHECK_2':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 2
                      study.process = False
                      study.mask[4] = False
                      study.mask[1] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = True
                          study.mask[1] = False
                          study.mask[2] = True
                          study.mask[3] = True
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 2
                      study.mask[1] = False
                      study.mask[4] = True  
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)      
                        
              elif event == 'CHECK_3':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 3
                      study.process = False
                      study.mask[4] = False
                      study.mask[2] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = True
                          study.mask[1] = True
                          study.mask[2] = False
                          study.mask[3] = True
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 3
                      study.mask[2] = False
                      study.mask[4] = True
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)      
                        
              elif event == 'CHECK_4':
                  if study.check_time > 0:
                      study.check = True
                      study.check_mode = 4
                      study.process = False
                      study.mask[4] = False
                      study.mask[3] = True
                      study.check_time -= 1
                      randomchange_check = random.randint(0,500)
                      if (randomchange_check >= 0) and (randomchange_check <= 10):
                          study.mask[0] = True
                          study.mask[1] = True
                          study.mask[2] = True
                          study.mask[3] = False
                  elif study.check_time == 0:
                      study.check = False
                      study.process = True
                      study.process_mode = 4
                      study.mask[3] = False
                      study.mask[4] = True
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  list_B.append(study.process_mode)      
                        
              elif event == 'PROCESS':
                  if study.process_mode == 1:
                      list_B.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time < 98):
                          study.process = True
                          study.mask[4] = True
                          study.mask[0] = False
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt1 = em.submission_ini.loc[24*i+j,'PRT_1']
                          prt1 = prt1 - mol
                      elif (study.process_time >= 98) and (study.process_time < 140):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt1 = em.submission_ini.loc[24*i+j,'PRT_1']
                          prt1 = prt1 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time12) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 12
                              study.mask[5] = True
                              study.change_time12 = changetime_ini.loc[0,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time13) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 13
                              study.mask[6] = True
                              study.change_time13 = changetime_ini.loc[1,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time14) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 14
                              study.mask[7] = True
                              study.change_time14 = changetime_ini.loc[2,'time']-1        
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27   
                            
                            
                  elif study.process_mode == 2:
                      list_B.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time <98):
                          study.process = True
                          study.mask[4] = True
                          study.mask[1] = False
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt2 = em.submission_ini.loc[24*i+j,'PRT_2']
                          prt2 = prt2 - mol
                      elif (study.process_time >= 98) and (study.process_time <140):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt2 = em.submission_ini.loc[24*i+j,'PRT_2']
                          prt2 = prt2 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time21) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 21
                              study.mask[8] = True
                              study.change_time21 = changetime_ini.loc[3,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time23) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 23
                              study.mask[9] = True
                              study.change_time23 = changetime_ini.loc[4,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time24) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 24
                              study.mask[10] = True
                              study.change_time24 = changetime_ini.loc[5,'time']-1
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27
                            
                            
                  elif study.process_mode == 3:
                      list_B.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time <98):
                          study.process = True
                          study.mask[4] = True
                          study.mask[2] = False
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt3 = em.submission_ini.loc[24*i+j,'PRT_3']
                          prt3 = prt3 - mol
                      elif (study.process_time >= 98) and (study.process_time <140):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt3 = em.submission_ini.loc[24*i+j,'PRT_3']
                          prt3 = prt3 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time31) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 31
                              study.mask[11] = True
                              study.change_time31 = changetime_ini.loc[6,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time32) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 32
                              study.mask[12] = True
                              study.change_time32 = changetime_ini.loc[7,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time34) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 34
                              study.mask[13] = True
                              study.change_time34 = changetime_ini.loc[8,'time']-1
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27
                            
                            
                  elif study.process_mode == 4:
                      list_B.append(study.process_mode)
                      if (study.process_time >= 0) and (study.process_time <98):
                          study.process = True
                          study.mask[4] = True
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt4 = em.submission_ini.loc[24*i+j,'PRT_4']
                          prt4 = prt4 - mol
                      elif (study.process_time >= 98) and (study.process_time <140):
                          study.process = True
                          study.mask[4] = True
                          study.mask[3] = False
                          study.process_time += 1
                          study.mol_B_input = mol #나중에 라인분리시 조정필요
                          prt4 = em.submission_ini.loc[24*i+j,'PRT_4']
                          prt4 = prt4 - mol
                          random_stop_change = random.randint(0,1000)
                          if (random_stop_change >=0) and (random_stop_change <=10):
                              study.process_mode = 0 
                              study.process_time = 1
                              study.process = False
                              study.stop = True
                              study.mask[4] = False
                              study.mask[17] = True
                              study.check_time = 27
                              study.stop_time = 1
                          elif (random_stop_change > 10) and (random_stop_change <= 20) and ((study.process_time + study.change_time41) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 41
                              study.mask[14] = True
                              study.change_time41 = changetime_ini.loc[9,'time']-1
                          elif (random_stop_change > 20) and (random_stop_change <= 30) and ((study.process_time + study.change_time42) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 42
                              study.mask[15] = True
                              study.change_time42 = changetime_ini.loc[10,'time']-1
                          elif (random_stop_change > 30) and (random_stop_change <= 40) and ((study.process_time + study.change_time43) < 140):
                              study.process = False
                              study.change = True
                              study.mask[4] = False
                              study.change_mode = 43
                              study.mask[16] = True
                              study.change_time43 = changetime_ini.loc[11,'time']-1
                      elif study.process_time == 140:
                          study.process_mode = 0
                          study.process_time = 1
                          study.process = False
                          study.mask[4] = False
                          study.mask[17] = True
                          study.stop = True
                          study.check_time = 27
                  submission_ini.loc[24*i+j,'Event_B'] = event
                  submission_ini.loc[24*i+j,'MOL_B'] = mol          
                            
              elif event == 'CHANGE_12':
                  if study.change_time12 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 12
                      study.mask[5] = True
                      study.change_time12 -= 1
                      study.process_time += 1
                  elif study.change_time12 == 0:
                      study.process_mode = 2
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[5] = False
                      study.change_time12 = changetime_ini.loc[0,'time']-1
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event      
                        
              elif event == 'CHANGE_13':
                  if study.change_time13 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 13
                      study.mask[6] = True
                      study.change_time13 -= 1
                      study.process_time += 1
                  elif study.change_time13 == 0:
                      study.process_mode = 3
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[6] = False
                      study.change_time13 = changetime_ini.loc[1,'time']-1
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event      
                        
              elif event == 'CHANGE_14':
                  if study.change_time14 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 14
                      study.mask[7] = True
                      study.change_time14 -= 1
                      study.process_time += 1
                  elif study.change_time14 == 0:
                      study.process_mode = 4
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[7] = False
                      study.change_time14 = changetime_ini.loc[2,'time']-1
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event      
                        
              elif event == 'CHANGE_21':
                  if study.change_time21 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 21
                      study.mask[8] = True
                      study.change_time21 -= 1
                      study.process_time += 1
                  elif study.change_time21 == 0:
                      study.process_mode = 1
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[8] = False
                      study.change_time21 = changetime_ini.loc[3,'time']-1
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event      
                        
              elif event == 'CHANGE_23':
                  if study.change_time23 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 23
                      study.mask[9] = True
                      study.change_time23 -= 1
                      study.process_time += 1
                  elif study.change_time23 == 0:
                      study.process_mode = 3
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[9] = False
                      study.change_time23 = changetime_ini.loc[4,'time']-1
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event      
                        
              elif event == 'CHANGE_24':
                  if study.change_time24 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 24
                      study.mask[10] = True
                      study.change_time24 -= 1
                      study.process_time += 1
                  elif study.change_time24 == 0:
                      study.process_mode = 4
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[10] = False
                      study.change_time24 = changetime_ini.loc[5,'time']-1
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event      
                        
              elif event == 'CHANGE_31':
                  if study.change_time31 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 31
                      study.mask[11] = True
                      study.change_time31 -= 1
                      study.process_time += 1
                  elif study.change_time31 == 0:
                      study.process_mode = 1
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[11] = False
                      study.change_time31 = changetime_ini.loc[6,'time']-1      
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event
                    
              elif event == 'CHANGE_32':
                  if study.change_time32 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 32
                      study.mask[12] = True
                      study.change_time32 -= 1
                      study.process_time += 1
                  elif study.change_time32 == 0:
                      study.process_mode = 2
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[12] = False
                      study.change_time32 = changetime_ini.loc[7,'time']-1
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event      
                        
              elif event == 'CHANGE_34':
                  if study.change_time34 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 34
                      study.mask[13] = True
                      study.change_time34 -= 1
                      study.process_time += 1
                  elif study.change_time34 == 0:
                      study.process_mode = 4
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[13] = False
                      study.change_time34 = changetime_ini.loc[8,'time']-1
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event      
                        
              elif event == 'CHANGE_41':
                  if study.change_time41 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 41
                      study.mask[14] = True
                      study.change_time41 -= 1
                      study.process_time += 1
                  elif study.change_time41 == 0:
                      study.process_mode = 1
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[14] = False
                      study.change_time41 = changetime_ini.loc[9,'time']-1
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event      
                        
              elif event == 'CHANGE_42':
                  if study.change_time42 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 42
                      study.mask[15] = True
                      study.change_time42 -= 1
                      study.process_time += 1
                  elif study.change_time42 == 0:
                      study.process_mode = 2
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[15] = False
                      study.change_time42 = changetime_ini.loc[10,'time']-1
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event      
                        
              elif event == 'CHANGE_43':
                  if study.change_time43 > 0: 
                      study.process = False
                      study.change = True
                      study.mask[4] = False
                      study.change_mode = 43
                      study.mask[16] = True
                      study.change_time43 -= 1
                      study.process_time += 1
                  elif study.change_time43 == 0:
                      study.process_mode = 3
                      study.process = True
                      study.change = False
                      study.change_mode = 0
                      study.mask[4] = True
                      study.mask[16] = False
                      study.change_time43 = changetime_ini.loc[11,'time']-1
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event      
                        
              elif event == 'STOP':
                  if study.stop_time == 192:
                      study.stop = False
                      study.process_time = 1
                      study.process_mode = 0
                      study.mask[17] = False
                      study.check = True
                      study.check_time = 27
                      study.check_mode = 0
                      study.stop_time = 1
                      study.mask[0] = True
                      study.mask[1] = True
                      study.mask[2] = True
                      study.mask[3] = True
                      study.mask[4] = False
                  elif (study.stop_time >= 0) and (study.stop_time <192):
                      study.process_mode = 0
                      study.process_time = 1
                      study.process = False
                      study.stop = True
                      study.mask[4] = False
                      study.mask[17] = True
                      study.stop_time += 1
                      study.check_time = 27
                      study.check = False
                      study.mask[0] = False
                      study.mask[1] = False
                      study.mask[2] = False
                      study.mask[3] = False
                      random_check = random.randint(0,200)
                      if (random_check >= 0) and (random_check <= 10):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 1
                          study.mask[0] = True
                          study.check_time = 27
                      elif (random_check > 10) and (random_check <= 20):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 2
                          study.mask[1] = True
                          study.check_time = 27
                      elif (random_check > 20) and (random_check <= 30):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 3
                          study.mask[2] = True
                          study.check_time = 27
                      elif (random_check > 30) and (random_check <= 40):
                          study.stop = False
                          study.mask[17] = False
                          study.stop_time = 1
                          study.check = True
                          study.check_mode = 4
                          study.mask[3] = True
                          study.check_time = 27
                  list_B.append(study.process_mode)
                  submission_ini.loc[24*i+j,'Event_B'] = event           
                          

    return submission_ini , list_A, list_B, study
'''
sub = mains()
sub.to_csv('sample_submission.csv', index=False)

os.system("pause")               
'''                        
                        
