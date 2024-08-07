import numpy as np
import pandas as pd
import random as rd

n = 1000000

user_data = pd.read_csv('user_data.csv')
goods_data = pd.read_csv('goods_data.csv')

gid_table = goods_data['id']
uid_table = user_data['id']

id_set = set()
while len(id_set) < n:
    id = rd.randint(1000, 5000000)
    id_set.add(id)

gid_list = []
uid_list = []
for i in range(n):
    idx1 = rd.randint(0, len(gid_table) - 1)
    idx2 = rd.randint(0, len(uid_table) - 1)
    gid_list.append(gid_table[idx1])
    uid_list.append(uid_table[idx2])

year_table = []
month_table = []
for i in range(2018, 2025):
    year_table.append(str(i))
for i in range(1, 13):
    month_table.append(str(i))
time_list = []
time = ''
while len(time_list) < n:
    idx1 = rd.randint(1, len(year_table) - 1)
    idx2 = rd.randint(1, len(month_table) - 1)
    year = year_table[idx1]
    month = month_table[idx2]
    time = year + '-' + month
    time_list.append(time)
    time = ''

money_list = []
for i in range(n):
    money = rd.randint(1000, 5000000)
    money_list.append(money)

data = pd.DataFrame()
data['id'] = list(id_set)
data['gid'] = gid_list
data['uid'] = uid_list
data['buy_time'] = time_list
data['money'] = money_list

data.index = data['id']
print(data)
data.to_csv('order_data.csv')