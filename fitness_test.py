#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 16:00:37 2023

@author: sheng
"""
# import modules
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import os
from os import path

# import data
folder_path = '/Users/sheng/Downloads/MuscleHub_AB'

app=pd.read_csv(path.join(folder_path,'applications.csv')).sort_values('email')
print(app.head())
test = pd.read_csv(path.join(folder_path,'fitness_tests.csv')).sort_values('email')
print(test.head())
pur = pd.read_csv(path.join(folder_path,'purchases.csv')).sort_values('email')
print(pur.head())
visits= pd.read_csv(path.join(folder_path,'visits.csv')).sort_values('email')
print(visits.head())

# Create and examine a DataFrame 
app_test = pd.merge(app,test, left_on = ['first_name','last_name','email'],right_on=['first_name','last_name','email'],how='outer')
app_test_pur = pd.merge(app_test,pur,left_on=['first_name','last_name','email'],right_on=['first_name','last_name','email'],how='outer')
all_df=pd.merge(app_test_pur,visits,left_on=['first_name','last_name','email'],right_on=['first_name','last_name','email'],how='outer')
all_df=all_df[all_df['visit_date']>='7-1-17']
print(all_df.shape)

# Create a visualization
all_df['test_or_not'] = ['A' if pd.notnull(x) else 'B' for x in all_df['fitness_test_date']]
print(all_df['test_or_not'].value_counts())


plt.figure(figsize=(12,6))
plt.pie(all_df['test_or_not'].value_counts()
, labels=['A','B']
,autopct = "%1.1f%%",)
plt.axis('equal')
plt.show()

# Calculate completion percentage
all_df['app_or_not']=['A' if pd.notnull(x) else 'B' for x in all_df['application_date']]

test_and_app=all_df.groupby(['test_or_not','app_or_not']).size().reset_index(name='count')
print(test_and_app)

test_and_app_pivot = test_and_app.pivot(index='test_or_not',
columns='app_or_not',
values='count').reset_index()
test_and_app_pivot['total']=test_and_app_pivot.sum(axis=1)
test_and_app_pivot['ratio']=test_and_app_pivot['A']/test_and_app_pivot['total']
print(test_and_app_pivot)

# inferential analysis
# Does fitness test affect application?

contingency = ([2175,325],[2254,250])
print(f"P value is {chi2_contingency(contingency)[1]}")
# those who did test has significantly lower percentage of application.

# Calculate purchase percentage
all_df['purchase_or_not']=all_df.purchase_date.apply(lambda x: 'not member' if pd.isnull(x) else 'member')
app_pur_or_not=all_df[all_df['app_or_not']=='A'].groupby(['purchase_or_not','test_or_not']).size().reset_index(name='count')

# Does finishing fitness test affect purchase rate?
app_pur_or_not_pivot=app_pur_or_not.pivot(index='test_or_not',
columns='purchase_or_not',values='count').reset_index()
app_pur_or_not_pivot['total']=app_pur_or_not_pivot.sum(axis=1)
app_pur_or_not_pivot['ratio']=app_pur_or_not_pivot['member']/app_pur_or_not_pivot['total']
print(app_pur_or_not_pivot)
contingency2=([250,75],[200,50])
print(f'P value is {chi2_contingency(contingency2)[1]}')
# despite those who did fitness test has higher rate of membership sign-up, no significance were detected

# Calculate percentage of ALL visitors who purchased memberships
all_df['membership']=all_df['purchase_date'].apply(lambda x: 'member' if pd.notnull(x) else 'not_member')
pur_test_or_not=all_df.groupby(['test_or_not','membership']).size().reset_index(name='count')
pur_test_or_not_pivot = pur_test_or_not.pivot(index='test_or_not',
columns= 'membership', values='count')
pur_test_or_not_pivot['total']=pur_test_or_not_pivot.sum(axis=1)
pur_test_or_not_pivot['ratio']=pur_test_or_not_pivot['member']/pur_test_or_not_pivot['total']
print(pur_test_or_not_pivot)

# does fitness test affect purchase?
contingency3=([250,2250],[200,2304])
print(f"P value is {chi2_contingency(contingency3)[1]}")

# Create visualizations
fig,ax1 = plt.subplots(figsize=(12,6))
plt.bar(range(len(test_and_app_pivot['test_or_not'])),test_and_app_pivot['ratio'])
ax1.set_xticklabels(['No Fitness Test', 'Fitness Test'])
plt.ylabel('ratio')
plt.show()

fig,ax2 = plt.subplots(figsize=(12,6))
plt.bar(range(len(app_pur_or_not_pivot)),app_pur_or_not_pivot['ratio'])
ax2.set_xticklabels(['No Fitness Test','Fitness Test'])
ax2.set_yticklabels(['5%','10%','15%','20%'])
plt.ylabel('Percentage')
plt.show()
