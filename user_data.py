import numpy as np
import pandas as pd
import random as rd

# t_user
alpha_table = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p','q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
name_set = set()
name = ''

while len(name_set) < 100:
    for i in range(3):
        idx = rd.randint(0, len(alpha_table)-1)
        name = name + alpha_table[idx]
    name_set.add(name)
    name = ''

number_table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
number_set = set()
number = '1'

while len(number_set) < 100:
    for i in range(10):
        idx = rd.randint(0, len(number_table)-1)
        number = number + number_table[idx]
    number_set.add(number)
    number = '1'

addr_table = ['北京', '上海', '广州', '深圳', '成都', '重庆', '杭州', '西安', '武汉', '苏州', '郑州', '南京', '天津', '长沙', '东莞', '宁波', '佛山', '合肥', '青岛']
addr_list = []
addr = ''

while len(addr_list) < 100:
    idx = rd.randint(0, len(addr_table)-1)
    addr = addr + addr_table[idx]
    addr_list.append(addr)
    addr = ''

data = pd.DataFrame()
data['id'] = list(name_set)
data['passwd'] = ['123456' for i in range(100)]
data['name'] = list(name_set)
data['number'] = list(number_set)
data['addr'] = addr_list
data['type'] = ['1' for i in range(100)]

data.index = data['id']
print(data)
data.to_csv('user_data.csv')