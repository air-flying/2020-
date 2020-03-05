# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 10:27:03 2020

@author: youhui
"""

import time
import json
import requests
from datetime import datetime
import csv

from pyecharts.charts import Line
import pyecharts.options as opts
import pandas as pd
from snapshot_selenium import snapshot
from pyecharts.render import make_snapshot

from pyecharts.charts import Map



def catch_daily():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_cn_day_counts&callback=&_={}'.format(int(time.time()*1000))
#    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_={}'.format(int(time.time()*1000))
    data = json.loads(requests.get(url=url).json()['data'])
    data.sort(key=lambda x:x['date'])
    
    date_list = list()
    confirm_list = list()
    suspect_list = list()
    dead_list = list()
    heal_list = list()
    
    for item in data:
        month, day = item['date'].split('/')
        date_list.append(datetime.strptime('2020-{}-{}'.format(month, day), '%Y-%m-%d'))
        confirm_list.append(int(item['confirm']))
        suspect_list.append(int(item['suspect']))
        dead_list.append(int(item['dead']))
        heal_list.append(int(item['heal']))
    return date_list, confirm_list, suspect_list, dead_list, heal_list

def save_daily():
    date_list, confirm_list, suspect_list, dead_list, heal_list = catch_daily()
    
    save_name = time.strftime('%Y-%m-%d') + '-daily.csv'
    save_dir = 'C:/Users/youhui/Desktop/数据小组/学习/2019疫情分析/'
    save_path = save_dir + save_name
    with open(save_path, 'w', newline='') as daily:
        writer = csv.writer(daily)
        writer.writerow(['date', 'confirm', 'suspect', 'dead', 'heal'])
        for i in range(len(date_list)):       
            writer.writerow([date_list[i], confirm_list[i], suspect_list[i], dead_list[i], heal_list[i]])
    print('{} has been saved!'.format(save_name))

save_daily()

#------------------------------------------------------------------------------------------------------------

save_name = time.strftime('%Y-%m-%d') + '-daily.csv'
save_dir = 'C:/Users/youhui/Desktop/数据小组/学习/2019疫情分析/'
save_path = save_dir + save_name
data = pd.read_csv(save_path)

date_list = list(data['date'])
datetime_list = list()
for item in date_list:
    datetime_list.append(item.split(' ')[0])
confirm_list = list(data['confirm'])
suspect_list = list(data['suspect'])
dead_list = list(data['dead'])
heal_list = list(data['heal'])

line = Line()
line.add_xaxis(datetime_list)
line.add_yaxis('confirm', confirm_list, is_smooth=True,
               markline_opts=opts.MarkLineOpts(data=opts.MarkLineItem(type_='average')),
               markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='max'),
                                                 opts.MarkPointItem(type_='min')]))
line.add_yaxis('suspect', suspect_list, is_smooth=True,
               markline_opts=opts.MarkLineOpts(data=opts.MarkLineItem(type_='average')),
               markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='max'),
                                                 opts.MarkPointItem(type_='min')]))
line.add_yaxis('dead', dead_list, is_smooth=True,
               markline_opts=opts.MarkLineOpts(data=opts.MarkLineItem(type_='average')),
               markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='max'),
                                                 opts.MarkPointItem(type_='min')]))
line.add_yaxis('heal', heal_list, is_smooth=True,
               markline_opts=opts.MarkLineOpts(data=opts.MarkLineItem(type_='average')),
               markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='max'),
                                                 opts.MarkPointItem(type_='min')]))
line.set_series_opts(opts.LabelOpts(is_show=False))
line.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),
                     yaxis_opts=opts.AxisOpts(name='人数', min_=3),
                     title_opts=opts.TitleOpts(title='nCoV疫情曲线图'))
line.render(save_dir + 'nCoV疫情曲线图.html')
make_snapshot(snapshot, save_dir + 'nCoV疫情曲线图.html', save_dir + 'nCoV疫情曲线图.png')

#-----------------------------------------------------------------------------------------------------------------

def catch_china():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_={}'.format(int(time.time()*1000))
    data = json.loads(requests.get(url=url).json()['data'])
    china_dict = data['areaTree'][0]['children']
    
    province_list = list()
    confirm_list = list()
    suspect_list = list()
    dead_list = list()
    heal_list = list()
    
    for item in china_dict:
        province_list.append(item['name'])     
        confirm_list.append(int(item['total']['confirm']))
        suspect_list.append(int(item['total']['suspect']))
        dead_list.append(int(item['total']['dead']))
        heal_list.append(int(item['total']['heal']))
    return province_list, confirm_list, suspect_list, dead_list, heal_list

def save_china():
    province_list, confirm_list, suspect_list, dead_list, heal_list = catch_china()
    save_name = time.strftime('%Y-%m-%d') + '-china.csv'
    save_dir = 'C:/Users/youhui/Desktop/数据小组/学习/2019疫情分析/'
    save_path = save_dir + save_name
    with open(save_path, 'w', newline='', encoding='utf-8') as china:
        writer = csv.writer(china)
        writer.writerow(['province', 'confirm', 'suspect', 'dead', 'heal'])
        for i in range(len(province_list)):       
            writer.writerow([province_list[i], confirm_list[i], suspect_list[i], dead_list[i], heal_list[i]])
    print('{} has been saved!'.format(save_name))    

save_china()

#------------------------------------------------------------------------------------------------------------

save_name = time.strftime('%Y-%m-%d') + '-china.csv'
save_dir = 'C:/Users/youhui/Desktop/数据小组/学习/2019疫情分析/'
save_path = save_dir + save_name
data = pd.read_csv(save_path)

province_list = list(data['province'])
confirm_list = list(data['confirm'])
heal_list = list(data['heal'])
confirm_map = list(zip(province_list, confirm_list))
heal_map = list(zip(province_list, heal_list))
china_map = Map()
china_map.add('confirm', confirm_map, maptype='china')
china_map.add('suspect', heal_map, maptype='china')
china_map.set_global_opts(title_opts=opts.TitleOpts(title='全国新型冠状病毒疫情地图（确诊数）'),
                          visualmap_opts=opts.VisualMapOpts(is_show=True,
                                                            split_number=6,
                                                            is_piecewise=True,
                                                            pos_top='center',
                                                            pieces=[{'min': 10000, 'color': '#7f1818'},
                                                                    {'min': 1000, 'max': 10000},
                                                                    {'min': 500, 'max': 999},
                                                                    {'min': 100, 'max': 499},
                                                                    {'min': 10, 'max': 99},
                                                                    {'min': 0, 'max': 5}]))
china_map.render(save_dir + '全国疫情地图.html')
make_snapshot(snapshot, save_dir + '全国疫情地图.html', save_dir + '全国疫情地图.png')
