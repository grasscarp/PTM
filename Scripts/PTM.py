#!/usr/bin/env python
# coding: utf-8

# Pathogen Transport Model
# Author: Xinyi Cheng
# Date: 2019/12/24 [Merry Christmas! =0w0=]
# Usage: python PTM.py [-dswt] path st


from plotnine import *
import pandas as pd
import argparse
import random
import time


######### set arguements #########
parser = argparse.ArgumentParser()
#positional arguments
parser.add_argument('path', type=str, help='input path of a csv file')
parser.add_argument('st', type=str, help='the sequence type of pathogens being showed')
#optional arguments
parser.add_argument('--date','-d', type=str, default='%Y-%m-%d', help='format of inputted date (default: %%Y-%%m-%%d)')
parser.add_argument('--same_st','-s', type=bool, default=True, help='only link pathogens of same sequence type (default: True)')
parser.add_argument('--same_ward','-w', type=bool, default=False, help='only link pathogens from same ward (default: False)')
parser.add_argument('--thresh','-t', type=int, default=2, help='the threshold of SNP number to link (default: 2)')
args = parser.parse_args()


####### input and preprocess #######
df0=pd.read_csv(args.path)
df1=df0.copy()

#将ward转成float编号
reflect=pd.DataFrame(index=set(df0['ID ward']))
ward_len=len(reflect)
reflect['code']=range(ward_len)  #加code列是为了画图时每个ward占等宽的行
df1.loc[df1.index,['ID ward','gNN ward']]=df1.loc[df1.index,['ID ward','gNN ward']].replace(reflect.index,reflect.code)
if ward_len>60:
    pd.set_option('display.max_rows',ward_len)
    print(reflect)

#加上随机波动（float），避免画图遮挡
for i in list(set(df1.ID)):
    df1.loc[df1.ID==i,'ID ward']+=random.uniform(-0.2,0.2)
    df1.loc[df1.gNN==i,'gNN ward']=(df1.loc[df1.ID==i,'ID ward']).iloc[0]
df1['gNN ward']=df1['gNN ward'].astype(float)

#生成y坐标的病区labels
if ward_len>60:
    breaks_y = range(0,ward_len,int(ward_len/10))
    labels_y = reflect[reflect.code.isin(breaks_y)].index
else:
    breaks_y = range(ward_len)
    labels_y = reflect.index

#将date转化成float编号
df2=df1.copy()
for i in df2.index:
    ts_ID=time.strptime(df2.loc[i,'ID date'], args.date)
    ts_gNN=time.strptime(df2.loc[i,'gNN date'], args.date)
    df2.loc[i,'ID date']=time.mktime(ts_ID)
    df2.loc[i,'gNN date']=time.mktime(ts_gNN)

#生成x坐标的时间labels
date = df2['ID date'].copy().sort_values()
early = date.values[0]
old = date.values[-1]
breaks_x = range(early,old,int((old-early)/6))
labels_x = []
for i in list(breaks_x):
    tl_ID = time.localtime(i)
    labels_x.append(time.strftime(args.date,tl_ID))


############# plot #############
df_st=df2[df2['ID ST']==args.st]
df_st_link=df_st[df_st['SNP']<=args.thresh]  #设置连线的条件
if args.same_st:
    df_sd_link=df_st_link[df_st_link['ID ST']==df_st_link['gNN ST']]
if args.same_ward:
    df_st_link=df_st_link[abs(df_st_link['ID ward']-df_st_link['gNN ward'])<=0.4]

a = (ggplot(df_st,aes('ID date','ID ward',color='ID ward'))
 + geom_point()
 + scale_y_continuous(breaks=breaks_y,labels=labels_y)
 + scale_x_continuous(breaks=breaks_x,labels=labels_x)
 + theme(text = element_text(family = "SimHei"))
 + ggtitle('transmission model of ST%s'%args.st)
)
print(a + geom_segment(df_st_link,aes(x='ID date',xend='gNN date',y='ID ward',yend='gNN ward'),alpha=0.3))
