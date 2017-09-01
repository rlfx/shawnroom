#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Tech_accuracy(object):
    def __init__(self,data,period):
        self.data = data
        self.period = period
    
    def accuracy(self,variable):
        acc = self.data.copy()
        tmp = acc[acc[variable] == 1].index
        
        acc_pos = 0
        acc_neg = 0
        n = 0
        
        for idx in tmp:
            try:
                acc_body = sum(acc.loc[idx+1:idx+self.period+1,'diff'])
                acc_trend = sum(acc.loc[idx+1:idx+self.period+1,'previous_trend'])
                
                if acc_body >= 0:
                    acc_pos += acc_body  
                else:
                    acc_neg += acc_body  
                    
                
                    acc_move = acc.loc[idx+1,'Open'] - acc.loc[idx+self.period+1,'Close']
                    if acc_move > 0:
                        n += 1
            except:
                pass
            
            acc_pos_mean = acc_pos / len(tmp)
            acc_neg_mean = acc_neg / len(tmp)
            #print(acc_body,acc_trend,acc_move)
        if len(tmp) > 0 :
            print(variable,':',len(tmp),'observation.','accuracy:',n/len(tmp))
            print(variable,'-- average pos mean:',acc_pos_mean)
            print(variable,'-- average neg mean:',acc_neg_mean) 
        else:
            print(variable,'never shows up.')
            
    def MFE_MAE(self,variable,tick):
        mfed = self.data.copy()
        mfe_list = []
        mae_list = []
        tmp = mfed[mfed[variable] == 1].index
        for idx in tmp:
            try:
                max_c = max(mfed.loc[idx+1:idx+tick+1,'Close'])
                min_c = min(mfed.loc[idx+1:idx+tick+1,'Close'])
                p_sell = mfed.loc[idx+1,'Open']
                
                mfe = p_sell - min_c
                if mfe < 0:
                    mfe = 0
                
                mae = max_c - p_sell
                if mae < 0:
                    mae = 0
                
                mfe_list.append(mfe)
                mae_list.append(mae)
            except:
                pass
        
        mfe_q1 = np.percentile(mfe_list,25)
        mae_q1 = np.percentile(mae_list,25)
        print('q1_mfe = ',mfe_q1)
        print('q1_mae = ',mae_q1)
        
        return mfe_list,mae_list


data = pd.read_csv('tech15m.csv',encoding = 'utf-8')
tacc = Tech_accuracy(data,40)
for each in ['black3','three_outside_up','three_outside_down','threeINdown','even','morning']:
    tacc.accuracy(each)
    mfe_list,mae_list = tacc.MFE_MAE(each,40)
    plt.hist(mfe_list)
    plt.hist(mae_list)

