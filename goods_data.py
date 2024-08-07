import numpy as np
import pandas as pd
import random as rd

id_set = set()
alpha_table = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']
while len(id_set) < 200:
    id = rd.randint(1, 5000000)
    id_set.add(id)
print(id_set)

name_set = set()
name = ''
while len(name_set) < 200:
    for i in range(5):
        idx = rd.randint(0, len(alpha_table) - 1)
        name = name + alpha_table[idx]
    name_set.add(name)
    name = ''

price_list = []
for i in range(200):
    p = rd.randint(1000, 50001)
    price_list.append(p)

data = pd.DataFrame()
data['id'] = list(id_set)
data['name'] = list(name_set)
data['price'] = price_list

data.index = data['id']
print(data)
data.to_csv('goods_data.csv')