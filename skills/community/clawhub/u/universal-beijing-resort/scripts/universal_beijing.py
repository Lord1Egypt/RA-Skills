#!/usr/bin/env python3
"""北京环球影城游园助手 v1.0.0 - 7项游园工具全覆盖，零配置即装即用
实时排队查询、智能推荐下一步、演出时间、路线规划、营业时间、餐厅推荐、门票价格
数据源：themeparks.wiki公开API + 本地预设数据"""

import os
import sys
import json
import math
import re
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from typing import Any, Optional

# ==================== 配置 ====================
PARK_ID = "68e1d8f0-ed42-4351-af25-160421e37ce0"
PARK_CENTER_LAT = 39.8527
PARK_CENTER_LNG = 116.6812

# ==================== 预设数据：20个游乐设施 ====================
ATTRACTIONS = [
    {
        "id": "c4119cf9-5383-423c-834c-94217ebb6435",
        "name_en": "Harry Potter and the Forbidden Journey™",
        "name_cn": "哈利·波特与禁忌之旅",
        "area": "哈利·波特的魔法世界",
        "lat": 39.8555, "lng": 116.6765,
        "height_min_cm": 122, "thrill_level": 5, "age_min": 8, "duration_min": 5,
        "tags": ["刺激", "室内", "4D沉浸", "魔法"],
        "popularity": 5, "is_indoor": True,
        "description": "骑上魔法扫帚穿越霍格沃茨，全球最热门项目之一",
        "good_for_kids": False, "good_for_teens": True, "good_for_elderly": False,
    },
    {
        "id": "e6ea7bbf-92ca-414a-8112-c473c20f04c3",
        "name_en": "Decepticoaster",
        "name_cn": "霸天虎过山车",
        "area": "变形金刚基地",
        "lat": 39.8545, "lng": 116.6795,
        "height_min_cm": 132, "thrill_level": 5, "age_min": 10, "duration_min": 2,
        "tags": ["刺激", "室外", "过山车", "极速"],
        "popularity": 5, "is_indoor": False,
        "description": "中国最高最快过山车，360度翻滚，132cm以上",
        "good_for_kids": False, "good_for_teens": True, "good_for_elderly": False,
    },
    {
        "id": "bcf1ef30-09fe-48e1-9d82-522a36940285",
        "name_en": "Transformers: Battle for the AllSpark",
        "name_cn": "变形金刚：火源争夺战",
        "area": "变形金刚基地",
        "lat": 39.8548, "lng": 116.6800,
        "height_min_cm": 102, "thrill_level": 4, "age_min": 6, "duration_min": 5,
        "tags": ["刺激", "室内", "3D射击"],
        "popularity": 5, "is_indoor": True,
        "description": "3D射击对战，与擎天柱一起保卫火源",
        "good_for_kids": False, "good_for_teens": True, "good_for_elderly": False,
    },
    {
        "id": "276268df-b9a1-42f3-bca0-3bce263aafa2",
        "name_en": "Jurassic World Adventure",
        "name_cn": "侏罗纪世界大冒险",
        "area": "侏罗纪世界努布拉岛",
        "lat": 39.8515, "lng": 116.6775,
        "height_min_cm": 102, "thrill_level": 4, "age_min": 8, "duration_min": 7,
        "tags": ["刺激", "室内", "暗黑乘骑"],
        "popularity": 5, "is_indoor": True,
        "description": "暗黑乘骑，穿越侏罗纪丛林，102cm以上",
        "good_for_kids": False, "good_for_teens": True, "good_for_elderly": False,
    },
    {
        "id": "f28218da-e74e-4979-b781-b3e6ebc7c461",
        "name_en": "Flight of the Hippogriff™",
        "name_cn": "鹰马飞行",
        "area": "哈利·波特的魔法世界",
        "lat": 39.8558, "lng": 116.6768,
        "height_min_cm": 92, "thrill_level": 3, "age_min": 5, "duration_min": 2,
        "tags": ["温和", "室外", "过山车", "家庭"],
        "popularity": 4, "is_indoor": False,
        "description": "家庭过山车，掠过海格小屋，92cm以上",
        "good_for_kids": True, "good_for_teens": False, "good_for_elderly": False,
    },
    {
        "id": "cbe1cb52-0264-4bc8-993c-e59b5bdb1ffc",
        "name_en": "Despicable Me Minion Mayhem",
        "name_cn": "小黄人闹翻天",
        "area": "小黄人乐园",
        "lat": 39.8500, "lng": 116.6820,
        "height_min_cm": 102, "thrill_level": 3, "age_min": 6, "duration_min": 5,
        "tags": ["温和", "室内", "3D模拟器"],
        "popularity": 4, "is_indoor": True,
        "description": "3D模拟器，小黄人主题，全家可玩",
        "good_for_kids": True, "good_for_teens": False, "good_for_elderly": True,
    },
    {
        "id": "557d7e1b-48ea-4d1f-9e3a-e9baa9b7780b",
        "name_en": "Kung Fu Panda Journey of the Dragon Warrior",
        "name_cn": "功夫熊猫：神龙大侠之旅",
        "area": "功夫熊猫盖世之地",
        "lat": 39.8530, "lng": 116.6835,
        "height_min_cm": 102, "thrill_level": 3, "age_min": 6, "duration_min": 6,
        "tags": ["温和", "室内", "漂流", "国风"],
        "popularity": 4, "is_indoor": True,
        "description": "室内漂流，功夫熊猫主题，国风特色",
        "good_for_kids": True, "good_for_teens": False, "good_for_elderly": False,
    },
    {
        "id": "4671257c-fa62-4cd8-88b8-eb8c466e4858",
        "name_en": "Lights Camera Action!",
        "name_cn": "灯光摄像开拍！",
        "area": "好莱坞",
        "lat": 39.8538, "lng": 116.6810,
        "height_min_cm": 0, "thrill_level": 2, "age_min": 4, "duration_min": 15,
        "tags": ["温和", "室内", "特效体验"],
        "popularity": 3, "is_indoor": True,
        "description": "斯皮尔伯格特效体验，揭秘电影特效",
        "good_for_kids": True, "good_for_teens": False, "good_for_elderly": True,
    },
    {
        "id": "d651ced3-5c24-4bda-b496-f082da00b018",
        "name_en": "Jurassic Flyers",
        "name_cn": "奇遇翼龙",
        "area": "侏罗纪世界努布拉岛",
        "lat": 39.8513, "lng": 116.6778,
        "height_min_cm": 91, "thrill_level": 2, "age_min": 4, "duration_min": 2,
        "tags": ["温和", "室外", "旋转"],
        "popularity": 2, "is_indoor": False,
        "description": "翼龙主题旋转飞椅，幼童友好",
        "good_for_kids": True, "good_for_teens": False, "good_for_elderly": True,
    },
    {
        "id": "f0e70954-da09-4a65-9ae7-805e82728363",
        "name_en": "Super Swirly",
        "name_cn": "超萌漩漩漩",
        "area": "小黄人乐园",
        "lat": 39.8505, "lng": 116.6828,
        "height_min_cm": 80, "thrill_level": 1, "age_min": 3, "duration_min": 2,
        "tags": ["温和", "室内", "旋转", "幼童"],
        "popularity": 2, "is_indoor": True,
        "description": "最温柔的旋转项目，幼童最爱",
        "good_for_kids": True, "good_for_teens": False, "good_for_elderly": True,
    },
    {
        "id": "67dfbe42-1452-47e4-be57-087f8f5894d0",
        "name_en": "Lanterns of Legendary Legends",
        "name_cn": "灯影传奇",
        "area": "小黄人乐园",
        "lat": 39.8508, "lng": 116.6830,
        "height_min_cm": 92, "thrill_level": 2, "age_min": 5, "duration_min": 2,
        "tags": ["温和", "室外", "旋转飞椅"],
        "popularity": 2, "is_indoor": False,
        "description": "灯光旋转飞椅，晚间尤其漂亮",
        "good_for_kids": True, "good_for_teens": False, "good_for_elderly": False,
    },
    {
        "id": "0380a1cb-4f71-402d-886a-88dd3e7f3395",
        "name_en": "Po's Kung Fu Training Camp",
        "name_cn": "阿宝功夫训练营",
        "area": "功夫熊猫盖世之地",
        "lat": 39.8532, "lng": 116.6840,
        "height_min_cm": 0, "thrill_level": 1, "age_min": 3, "duration_min": 10,
        "tags": ["温和", "室内", "互动", "亲子"],
        "popularity": 3, "is_indoor": True,
        "description": "互动体验，小孩最爱，无身高要求",
        "good_for_kids": True, "good_for_teens": False, "good_for_elderly": True,
    },
    {
        "id": "9f170ad3-032d-4a54-a601-82d867229091",
        "name_en": "Carousel of Kung Fu Heroes",
        "name_cn": "功夫旋风旋转飞龙",
        "area": "功夫熊猫盖世之地",
        "lat": 39.8538, "lng": 116.6832,
        "height_min_cm": 92, "thrill_level": 2, "age_min": 4, "duration_min": 2,
        "tags": ["温和", "室外", "旋转"],
        "popularity": 2, "is_indoor": False,
        "description": "温和旋转，幼童友好，92cm以上",
        "good_for_kids": True, "good_for_teens": False, "good_for_elderly": True,
    },
    {
        "id": "b7f731e5-d72c-4227-a8e3-89ff662b3e05",
        "name_en": "Loop-Dee Doop-Dee",
        "name_cn": "萌转过山车",
        "area": "小黄人乐园",
        "lat": 39.8503, "lng": 116.6825,
        "height_min_cm": 92, "thrill_level": 2, "age_min": 4, "duration_min": 2,
        "tags": ["温和", "室外", "过山车", "亲子"],
        "popularity": 3, "is_indoor": False,
        "description": "亲子入门过山车，92cm以上",
        "good_for_kids": True, "good_for_teens": False, "good_for_elderly": False,
    },
    {
        "id": "8bef9380-953a-4add-8fe8-420b7038d50b",
        "name_en": "MINION GAMES",
        "name_cn": "小黄人游戏区",
        "area": "小黄人乐园",
        "lat": 39.8506, "lng": 116.6823,
        "height_min_cm": 0, "thrill_level": 1, "age_min": 3, "duration_min": 15,
        "tags": ["温和", "室外", "互动", "亲子"],
        "popularity": 2, "is_indoor": False,
        "description": "小黄人主题互动游戏区，适合亲子",
        "good_for_kids": True, "good_for_teens": False, "good_for_elderly": True,
    },
    {
        "id": "292ec81b-41ee-4337-9fcf-190bf8ee46e4",
        "name_en": "Kung Fu Games",
        "name_cn": "功夫游戏区",
        "area": "功夫熊猫盖世之地",
        "lat": 39.8534, "lng": 116.6836,
        "height_min_cm": 0, "thrill_level": 1, "age_min": 3, "duration_min": 15,
        "tags": ["温和", "室外", "互动", "亲子"],
        "popularity": 2, "is_indoor": False,
        "description": "功夫主题互动游戏区",
        "good_for_kids": True, "good_for_teens": False, "good_for_elderly": True,
    },
    {
        "id": "41f4b65b-a27b-4a26-86f1-447ba0ba3724",
        "name_en": "Bumblebee Boogie",
        "name_cn": "大黄蜂回旋舞",
        "area": "变形金刚基地",
        "lat": 39.8546, "lng": 116.6798,
        "height_min_cm": 92, "thrill_level": 2, "age_min": 4, "duration_min": 2,
        "tags": ["温和", "室外", "旋转"],
        "popularity": 2, "is_indoor": False,
        "description": "大黄蜂主题旋转飞椅，温和有趣",
        "good_for_kids": True, "good_for_teens": False, "good_for_elderly": False,
    },
    {
        "id": "4880520f-6c3a-49e1-9ac0-85ab9efdf2d4",
        "name_en": "Raptor Encounter",
        "name_cn": "速龙邂逅",
        "area": "侏罗纪世界努布拉岛",
        "lat": 39.8520, "lng": 116.6773,
        "height_min_cm": 0, "thrill_level": 1, "age_min": 3, "duration_min": 10,
        "tags": ["互动", "室外", "体验"],
        "popularity": 3, "is_indoor": False,
        "description": "与恐龙近距离互动体验",
        "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True,
    },
    {
        "id": "c6218fc4-97f3-472a-bf1a-7e0436669ea8",
        "name_en": "Camp Jurassic",
        "name_cn": "侏罗纪营地",
        "area": "侏罗纪世界努布拉岛",
        "lat": 39.8510, "lng": 116.6780,
        "height_min_cm": 0, "thrill_level": 1, "age_min": 3, "duration_min": 20,
        "tags": ["温和", "室外", "探索", "亲子"],
        "popularity": 3, "is_indoor": False,
        "description": "侏罗纪主题探索营地，孩子们最爱",
        "good_for_kids": True, "good_for_teens": False, "good_for_elderly": True,
    },
    {
        "id": "f6375650-a586-44c6-b481-1cf3941ded3c",
        "name_en": "Ollivanders™",
        "name_cn": "奥利凡德魔杖店",
        "area": "哈利·波特的魔法世界",
        "lat": 39.8560, "lng": 116.6764,
        "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 10,
        "tags": ["体验", "室内", "互动", "魔法"],
        "popularity": 4, "is_indoor": True,
        "description": "魔杖选择仪式，哈利波特迷必体验",
        "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True,
    },
]

# ==================== 演出数据 ====================
SHOWS = [
    {"id": "0c16b145-6941-4328-9063-5a8c9380a12f", "name_cn": "不可驯服", "name_en": "Untrainable", "area": "侏罗纪世界努布拉岛", "type": "真人特技秀", "duration_min": 20, "must_see": True, "best_spot": "中间偏右第3-5排", "arrive_early_min": 20},
    {"id": "9a397d58-66c9-4910-9f36-25626e6971bd", "name_cn": "变形金刚：非凡之战", "name_en": "Transformers: More than Meets the Eye", "area": "变形金刚基地", "type": "特效秀", "duration_min": 15, "must_see": True, "best_spot": "正中第2-4排", "arrive_early_min": 15},
    {"id": "94095f0e-b2d2-428a-b8a7-349d2eabbaa7", "name_cn": "霍格沃茨城堡夜间魔法秀", "name_en": "Nighttime Magic at Hogwarts™ Castle", "area": "哈利·波特的魔法世界", "type": "灯光投影秀", "duration_min": 10, "must_see": True, "best_spot": "城堡正前方空地", "arrive_early_min": 30},
    {"id": "bf9b28a9-51fa-4776-a5ca-9f8690eb174c", "name_cn": "环球花车大巡游", "name_en": "Universal on Parade", "area": "好莱坞", "type": "花车巡游", "duration_min": 15, "must_see": True, "best_spot": "好莱坞大道两侧", "arrive_early_min": 15},
    {"id": "33aa27db-973e-4c77-80f9-6aeff3617de9", "name_cn": "未来水世界特技表演", "name_en": "WaterWorld Stunt Show", "area": "好莱坞", "type": "真人特技秀", "duration_min": 20, "must_see": True, "best_spot": "中间区域防溅区外", "arrive_early_min": 20},
    {"id": "e63cce2c-bd1d-47b5-8279-205e49f8d912", "name_cn": "青蛙合唱团", "name_en": "Frog Choir™", "area": "哈利·波特的魔法世界", "type": "街头表演", "duration_min": 10, "must_see": False, "best_spot": "霍格莫德村入口", "arrive_early_min": 5},
    {"id": "f3f71368-bc16-4037-b258-e240bf8c29ba", "name_cn": "三强争霸杯", "name_en": "Triwizard Spirit Rally™", "area": "哈利·波特的魔法世界", "type": "街头表演", "duration_min": 8, "must_see": False, "best_spot": "霍格莫德村广场", "arrive_early_min": 5},
    {"id": "e536bb29-6b41-425b-8ea3-86d4f10e6f77", "name_cn": "小黄人见面会", "name_en": "Minion Meet and Greet", "area": "小黄人乐园", "type": "互动体验", "duration_min": 15, "must_see": False, "best_spot": "小黄人乐园中心", "arrive_early_min": 5},
    {"id": "f0c8f95d-d101-4249-a2e1-942728c24782", "name_cn": "功夫熊猫见面会", "name_en": "Kung Fu Panda Meet and Greet", "area": "功夫熊猫盖世之地", "type": "互动体验", "duration_min": 10, "must_see": False, "best_spot": "翡翠宫前广场", "arrive_early_min": 5},
    {"id": "619c26a6-609a-41be-84cd-f8d5a86e47c8", "name_cn": "功夫熊猫阿宝互动秀", "name_en": "Po Live", "area": "功夫熊猫盖世之地", "type": "互动表演", "duration_min": 10, "must_see": False, "best_spot": "翡翠宫前", "arrive_early_min": 5},
    {"id": "1d56cdc3-4f2d-454d-818f-4dbbd2a01d60", "name_cn": "欢唱好声音巡演", "name_en": "SING on Tour!", "area": "好莱坞", "type": "音乐表演", "duration_min": 15, "must_see": False, "best_spot": "中间位置", "arrive_early_min": 10},
    {"id": "c1b17f67-3cef-4ff8-95ef-11cc19612d01", "name_cn": "小黄人奶油苏打秀", "name_en": "Minions Cream Soda Show", "area": "小黄人乐园", "type": "互动表演", "duration_min": 10, "must_see": False, "best_spot": "小黄人乐园中心", "arrive_early_min": 5},
    {"id": "33915fc6-45f9-45f0-bf8c-3ac07735d055", "name_cn": "天赐智慧桃树", "name_en": "Peach Tree of Heavenly Wisdom", "area": "功夫熊猫盖世之地", "type": "互动体验", "duration_min": 10, "must_see": False, "best_spot": "桃树广场", "arrive_early_min": 5},
    {"id": "0a656330-f67c-4688-b1ff-270bbea2867c", "name_cn": "好莱坞角色见面会", "name_en": "Hollywood Meet and Greet", "area": "好莱坞", "type": "互动体验", "duration_min": 10, "must_see": False, "best_spot": "好莱坞大道", "arrive_early_min": 5},
    {"id": "263535d4-0933-4e6f-9f92-a0f01142dac7", "name_cn": "恐龙宝宝互动", "name_en": "Baby Raptor", "area": "侏罗纪世界努布拉岛", "type": "互动体验", "duration_min": 10, "must_see": False, "best_spot": "侏罗纪岛入口", "arrive_early_min": 5},
    {"id": "e237fbb6-f9c9-42a7-8951-663e90e54aa0", "name_cn": "恐龙多洛雷斯见面会", "name_en": "Aquilops Dolores Meet and Greet", "area": "侏罗纪世界努布拉岛", "type": "互动体验", "duration_min": 10, "must_see": False, "best_spot": "侏罗纪岛", "arrive_early_min": 5},
    {"id": "38623b56-6c0a-4e6c-b29a-e322d87f62df", "name_cn": "霍格沃茨特快列车长", "name_en": "Hogwarts™ Express Conductor", "area": "哈利·波特的魔法世界", "type": "街头表演", "duration_min": 5, "must_see": False, "best_spot": "霍格莫德村车站", "arrive_early_min": 3},
    {"id": "2b2c861f-8737-493e-9aa8-6596bbb633db", "name_cn": "环球流行乐", "name_en": "Universal Pop", "area": "好莱坞", "type": "音乐表演", "duration_min": 10, "must_see": False, "best_spot": "好莱坞大道", "arrive_early_min": 5},
    {"id": "4950cac4-138a-4b69-a467-7c9fc48fb646", "name_cn": "环球中场秀", "name_en": "Universal's Halftime Show", "area": "好莱坞", "type": "表演", "duration_min": 10, "must_see": False, "best_spot": "好莱坞大道", "arrive_early_min": 5},
    {"id": "c0385686-1791-4ff0-8b4f-2019dcb1979c", "name_cn": "海贼王草帽团邂逅", "name_en": "ONE PIECE - Straw Hat Crew Encounter", "area": "好莱坞", "type": "限时互动", "duration_min": 10, "must_see": False, "best_spot": "好莱坞大道", "arrive_early_min": 5},
    {"id": "0578b65e-a6d6-441e-abe0-6c8749e52bfd", "name_cn": "环球清凉夏日", "name_en": "Universal Cool Summer", "area": "全园", "type": "季节限定", "duration_min": 15, "must_see": False, "best_spot": "主通道", "arrive_early_min": 5},
]

# ==================== 餐厅数据 ====================
RESTAURANTS = [
    {"name_cn": "三把扫帚酒吧", "name_en": "Three Broomsticks", "area": "哈利·波特的魔法世界", "cuisine": ["英式", "烤肉"], "price_range": "中等", "price_per_person": 90, "highlights": ["黄油啤酒", "烤鸡腿", "英式炸鱼"], "lat": 39.8557, "lng": 116.6767},
    {"name_cn": "蜂蜜公爵糖果店", "name_en": "Honeydukes", "area": "哈利·波特的魔法世界", "cuisine": ["甜品", "零食"], "price_range": "低", "price_per_person": 40, "highlights": ["巧克力蛙", "比比多味豆", "黄油啤酒冰淇淋"], "lat": 39.8559, "lng": 116.6769},
    {"name_cn": "嗷嗷龙烤肉", "name_en": "Toothsome Chocolate Emporium", "area": "侏罗纪世界努布拉岛", "cuisine": ["烤肉", "西餐"], "price_range": "中等偏高", "price_per_person": 110, "highlights": ["烤肋排", "汉堡", "奶昔"], "lat": 39.8516, "lng": 116.6777},
    {"name_cn": "平先生面馆", "name_en": "Mr. Ping's Noodle House", "area": "功夫熊猫盖世之地", "cuisine": ["中式", "面食"], "price_range": "中等", "price_per_person": 70, "highlights": ["熊猫拉面", "煎饺", "酸辣汤"], "lat": 39.8534, "lng": 116.6837},
    {"name_cn": "熊猫秘境小吃", "name_en": "Panda Secret Snacks", "area": "功夫熊猫盖世之地", "cuisine": ["中式", "小吃"], "price_range": "低", "price_per_person": 45, "highlights": ["包子", "煎饼", "糖葫芦"], "lat": 39.8536, "lng": 116.6842},
    {"name_cn": "小黄人餐厅", "name_en": "Minion Cafe", "area": "小黄人乐园", "cuisine": ["西式", "快餐"], "price_range": "中等", "price_per_person": 75, "highlights": ["小黄人便当", "炸鸡", "薯条"], "lat": 39.8501, "lng": 116.6822},
    {"name_cn": "变形金刚能量站", "name_en": "Transformer Energy Station", "area": "变形金刚基地", "cuisine": ["快餐", "饮品"], "price_range": "中等", "price_per_person": 60, "highlights": ["能量饮料", "热狗", "鸡块"], "lat": 39.8546, "lng": 116.6798},
    {"name_cn": "好莱坞餐厅", "name_en": "Hollywood Restaurant", "area": "好莱坞", "cuisine": ["西式", "美式"], "price_range": "中等偏高", "price_per_person": 100, "highlights": ["牛排", "意面", "沙拉"], "lat": 39.8542, "lng": 116.6812},
    {"name_cn": "侏罗纪汉堡屋", "name_en": "Jurassic Burger", "area": "侏罗纪世界努布拉岛", "cuisine": ["快餐", "汉堡"], "price_range": "中等", "price_per_person": 65, "highlights": ["恐龙汉堡", "薯条", "奶昔"], "lat": 39.8512, "lng": 116.6773},
    {"name_cn": "城市大道星巴克", "name_en": "CityWalk Starbucks", "area": "城市大道", "cuisine": ["咖啡", "甜品"], "price_range": "中等", "price_per_person": 50, "highlights": ["咖啡", "蛋糕", "三明治"], "lat": 39.8560, "lng": 116.6840},
]

# ==================== 门票价格 ====================
TICKET_PRICES = {
    "淡季": {"label": "淡季票", "adult": 418, "child": 315, "senior": 315},
    "平季": {"label": "平季票", "adult": 528, "child": 395, "senior": 395},
    "旺季": {"label": "旺季票", "adult": 598, "child": 449, "senior": 449},
    "特定日": {"label": "特定日票", "adult": 748, "child": 561, "senior": 561},
}

EXPRESS_PASS_PRICES = {
    "3项优速通": 500,
    "5项优速通": 700,
    "无限次优速通": 1200,
}


# ==================== 辅助函数 ====================

def get_ticket_season(date_str: str) -> str:
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return "平季"
    month = date.month
    weekday = date.weekday()
    is_holiday = False
    if month == 1 or month == 2:
        is_holiday = True
    elif month == 10 and date.day <= 7:
        is_holiday = True
    elif month == 5 and date.day <= 3:
        is_holiday = True
    if is_holiday:
        return "特定日"
    if month in [7, 8]:
        return "特定日"
    if weekday >= 5:
        return "旺季"
    if month in [11, 12, 1, 2, 3]:
        return "淡季"
    return "平季"


def calculate_distance(lat1, lng1, lat2, lng2):
    R = 6371
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c * 1000


def estimate_walking_time(distance_m):
    return max(1, int(distance_m / 80))


def filter_attractions_by_profile(attractions, profile):
    filtered = []
    min_height = profile.get("min_height", 0)
    has_kids = profile.get("has_kids", False)
    kids_age = profile.get("kids_age", 0)
    preference = profile.get("preference", "balanced")
    for attr in attractions:
        if attr["height_min_cm"] > 0 and attr["height_min_cm"] > min_height:
            continue
        if kids_age > 0 and kids_age < attr["age_min"]:
            continue
        if preference == "gentle" and attr["thrill_level"] > 2:
            continue
        elif preference == "thrill" and attr["thrill_level"] < 3:
            continue
        if has_kids and kids_age < 7 and attr["thrill_level"] > 3:
            continue
        filtered.append(attr)
    return filtered


def rank_attractions(attractions, live_data, current_location, next_show_time=None, profile=None):
    scored = []
    for attr in attractions:
        score = 0
        info = live_data.get(attr["id"], {})
        wait_time = info.get("wait_time", 0) or 0
        status = info.get("status", "OPERATING")
        if status in ["CLOSED", "DOWN"]:
            continue
        if wait_time < 20:
            score += 30
        elif wait_time < 45:
            score += 20
        elif wait_time < 60:
            score += 10
        score += attr["popularity"] * 3
        if current_location:
            dist = calculate_distance(
                current_location.get("lat", PARK_CENTER_LAT),
                current_location.get("lng", PARK_CENTER_LNG),
                attr["lat"], attr["lng"]
            )
            walk_time = estimate_walking_time(dist)
            if walk_time < 5:
                score += 15
            elif walk_time < 10:
                score += 10
            elif walk_time < 15:
                score += 5
        if profile and profile.get("prefer_indoor", False) and attr["is_indoor"]:
            score += 10
        scored.append((attr, score, wait_time))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


def parse_profile_from_query(query):
    profile = {"preference": "balanced"}
    kids_match = re.search(r"(\d+)\s*岁?\s*(?:小孩|孩子|儿童|宝宝)", query)
    if kids_match:
        age = int(kids_match.group(1))
        profile["has_kids"] = True
        profile["kids_age"] = age
        profile["kids"] = 1
        profile["min_height"] = max(100, age * 6 + 80)
    else:
        kids_match2 = re.search(r"(?:小孩|孩子|儿童|宝宝)", query)
        if kids_match2:
            profile["has_kids"] = True
            profile["kids"] = 1
            profile["kids_age"] = 5
            profile["min_height"] = 110
    adults_match = re.search(r"(\d+)\s*(?:大人|成人|成年)", query)
    if adults_match:
        profile["adults"] = int(adults_match.group(1))
    if any(kw in query for kw in ["刺激", "冒险", "惊险", "过山车"]):
        profile["preference"] = "thrill"
    elif any(kw in query for kw in ["亲子", "温馨", "温和", "小孩", "孩子", "宝宝", "幼"]):
        profile["preference"] = "gentle"
    if any(kw in query for kw in ["室内", "空调", "防晒", "避暑"]):
        profile["prefer_indoor"] = True
    return profile


def format_showtime(raw_time):
    if not raw_time:
        return ""
    if "T" in raw_time:
        return raw_time.split("T")[1][:5]
    return raw_time[:5]


# ==================== API层 (urllib) ====================

def fetch_live_data():
    """获取实时排队数据"""
    url = f"https://api.themeparks.wiki/v1/entity/{PARK_ID}/live"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "UniversalBeijingSkill/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                live_data = {}
                for entity in data.get("liveData", []):
                    entity_id = entity.get("id", "")
                    queue = entity.get("queue", {})
                    standby = queue.get("STANDBY", {})
                    wait_time = standby.get("waitTime")
                    single_rider = queue.get("SINGLE_RIDER", {})
                    sr_wait = single_rider.get("waitTime")
                    show_queue = queue.get("SHOW", {})
                    showtimes = show_queue.get("showtimes", [])
                    next_show = show_queue.get("nextShowTime", "")
                    live_data[entity_id] = {
                        "status": entity.get("status", "OPERATING"),
                        "wait_time": wait_time,
                        "single_rider_wait": sr_wait,
                        "name": entity.get("name", ""),
                        "entity_type": entity.get("entityType", ""),
                        "showtimes": [format_showtime(st) for st in showtimes] if showtimes else [],
                        "next_show_time": format_showtime(next_show),
                    }
                return live_data
            return {}
    except Exception:
        return {}


def fetch_schedule():
    """获取营业时间"""
    url = f"https://api.themeparks.wiki/v1/entity/{PARK_ID}/schedule"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "UniversalBeijingSkill/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                schedules = {}
                for schedule in data.get("schedule", []):
                    date = schedule.get("date", "")
                    schedules[date] = {
                        "openingTime": schedule.get("openingTime", ""),
                        "closingTime": schedule.get("closingTime", ""),
                        "type": schedule.get("type", ""),
                    }
                return schedules
            return {}
    except Exception:
        return {}


# ==================== 7个工具函数 ====================

def universal_ticket(date="", query=""):
    date_str = date if date else datetime.now().strftime("%Y-%m-%d")
    season = get_ticket_season(date_str)
    prices = TICKET_PRICES[season]

    output = f"🎫 北京环球影城门票 - {date_str}\n"
    output += "=" * 30 + "\n\n"
    output += f"📅 {prices['label']}\n\n"
    output += "【单日票】\n"
    output += f"  • 成人票（12-64岁）: ¥{prices['adult']}\n"
    output += f"  • 儿童票（3-11岁）: ¥{prices['child']}\n"
    output += f"  • 长者票（65岁+）: ¥{prices['senior']}\n\n"
    output += "【1.5日票】\n"
    output += f"  • 成人票: ¥{int(prices['adult'] * 1.43)}\n"
    output += f"  • 儿童票: ¥{int(prices['child'] * 1.43)}\n\n"
    output += "【2日票】\n"
    output += f"  • 成人票: ¥{int(prices['adult'] * 1.31)}\n"
    output += f"  • 儿童票: ¥{int(prices['child'] * 1.31)}\n\n"
    output += "【优速通】\n"
    output += f"  • 3项优速通: ¥{EXPRESS_PASS_PRICES['3项优速通']}\n"
    output += f"  • 5项优速通: ¥{EXPRESS_PASS_PRICES['5项优速通']}\n"
    output += f"  • 无限次优速通: ¥{EXPRESS_PASS_PRICES['无限次优速通']}\n\n"
    output += "💡 3岁以下免票 | 门票实名制，需身份证 | 购票渠道：官方App/小程序/飞猪旗舰店"
    return output


def universal_wait_times(query=""):
    live_data = fetch_live_data()
    if not live_data:
        return "❌ 暂时无法获取实时排队信息，请稍后再试"

    operating = []
    closed = []
    for attr in ATTRACTIONS:
        attr_id = attr["id"]
        info = live_data.get(attr_id, {})
        status = info.get("status", "OPERATING")
        wait_time = info.get("wait_time") or 0
        sr_wait = info.get("single_rider_wait")
        if status in ["OPERATING"] and wait_time is not None:
            operating.append((attr, wait_time, sr_wait))
        else:
            closed.append((attr, status))

    if query:
        q = query.lower()
        filtered = []
        for item in operating:
            attr = item[0]
            if q in attr["name_cn"].lower() or q in attr["area"].lower() or any(q in t for t in attr["tags"]):
                filtered.append(item)
        operating = filtered if filtered else operating

    operating.sort(key=lambda x: x[1])

    output = "🎢 北京环球影城实时排队\n"
    output += "=" * 30 + "\n\n"
    output += "✅ 运营中项目：\n"
    for attr, wait, sr_wait in operating[:15]:
        if wait == 0:
            wait_str = "<5min"
            emoji = "🟢"
        elif wait < 20:
            wait_str = f"{wait}min"
            emoji = "🟢"
        elif wait < 60:
            wait_str = f"{wait}min"
            emoji = "🟡"
        else:
            wait_str = f"{wait}min"
            emoji = "🔴"
        sr_info = f" | 单人通道{sr_wait}min" if sr_wait else ""
        output += f"  {emoji} {attr['name_cn']}（{attr['area']}）: {wait_str}{sr_info}\n"

    if closed:
        output += "\n⚠️ 今日暂停项目：\n"
        for attr, status in closed:
            status_text = "今日暂停运营" if status == "CLOSED" else "临时故障"
            output += f"  ⏸ {attr['name_cn']} — {status_text}\n"

    return output


def universal_show_schedule(date="", query=""):
    live_data = fetch_live_data()

    output = "🎭 北京环球影城演出时间表\n"
    output += "=" * 30 + "\n\n"

    output += "⭐ 必看演出：\n\n"
    for show in SHOWS:
        if not show["must_see"]:
            continue
        info = live_data.get(show["id"], {}) if live_data else {}
        status = info.get("status", "")
        showtimes = info.get("showtimes", [])
        next_show = info.get("next_show_time", "")
        status_mark = " ✅" if status == "OPERATING" else (" ⏸" if status == "CLOSED" else "")
        output += f"【{show['name_cn']}】{status_mark}\n"
        output += f"  📍 {show['area']} | ⏱ {show['duration_min']}分钟 | {show['type']}\n"
        output += f"  🎯 最佳位置: {show['best_spot']}\n"
        output += f"  ⏰ 建议提前{show['arrive_early_min']}分钟到场\n"
        if showtimes:
            output += f"  📋 今日场次: {' / '.join(showtimes)}\n"
        elif next_show:
            output += f"  📋 下一场: {next_show}\n"
        output += "\n"

    output += "📺 其他演出与互动：\n\n"
    current_area = ""
    for show in SHOWS:
        if show["must_see"]:
            continue
        info = live_data.get(show["id"], {}) if live_data else {}
        showtimes = info.get("showtimes", [])
        if show["area"] != current_area:
            current_area = show["area"]
            output += f"📍 {current_area}\n"
        times_str = f" · 场次: {'/'.join(showtimes[:3])}" if showtimes else ""
        output += f"  • {show['name_cn']} — {show['type']}，{show['duration_min']}分钟{times_str}\n"

    output += "\n💡 场次时间以当日园区公告为准，建议查看官方App确认"
    return output


def universal_smart_next(query=""):
    if not query:
        return "请告诉我你的情况：\n1️⃣ 几个人？大人几位、小孩几位\n2️⃣ 小孩年龄多大？\n3️⃣ 有什么特别偏好吗？"

    profile = parse_profile_from_query(query)
    live_data = fetch_live_data()

    suitable = filter_attractions_by_profile(ATTRACTIONS, profile)
    if not suitable:
        suitable = ATTRACTIONS

    ranked = rank_attractions(suitable, live_data, {}, None, profile)

    if not ranked:
        return "❌ 当前暂无可用推荐，请稍后再试"

    output = "🎯 推荐下一步：\n\n"
    for i, (attr, score, wait_time) in enumerate(ranked[:3], 1):
        reasons = []
        if wait_time is not None and wait_time < 20:
            reasons.append(f"排队{wait_time}min")
        if attr["is_indoor"]:
            reasons.append("室内有空调")
        if "刺激" in attr["tags"]:
            reasons.append("刺激")
        if profile.get("has_kids") and attr["good_for_kids"]:
            reasons.append("适合小孩")
        reason_str = "，".join(reasons) if reasons else ""
        output += f"{i}. {attr['name_cn']} — {reason_str}\n"

    if live_data:
        upcoming_shows = []
        for show in SHOWS:
            info = live_data.get(show["id"], {})
            next_time = info.get("next_show_time", "")
            if next_time and info.get("status") == "OPERATING":
                upcoming_shows.append((show, next_time))
        if upcoming_shows:
            upcoming_shows.sort(key=lambda x: x[1])
            output += f"\n🎭 即将开始的演出：\n"
            for show, time in upcoming_shows[:3]:
                output += f"  • {show['name_cn']} — {time}开始\n"

    output += "\n💡 还可以问我：实时排队 | 演出时间 | 园区餐厅"
    return output


def universal_route(query=""):
    profile = parse_profile_from_query(query) if query else {"preference": "balanced"}

    output = "📍 北京环球影城一日路线\n"
    output += "=" * 30 + "\n\n"

    preference = profile.get("preference", "balanced")
    has_kids = profile.get("has_kids", False)
    kids_age = profile.get("kids_age", 0)

    if has_kids and kids_age > 0:
        output += f"👨‍👩‍👧 亲子游（小孩{kids_age}岁）\n\n"
    elif preference == "thrill":
        output += "👫 刺激冒险路线\n\n"
    else:
        output += "👫 均衡路线\n\n"

    if preference == "gentle" or (has_kids and kids_age < 7):
        route_steps = [
            ("08:30", "入园", "建议提前30分钟到大门"),
            ("09:00", "功夫熊猫：神龙大侠之旅", "🟢 趁人少先去热门项目"),
            ("10:00", "功夫旋风旋转飞龙", "🟢 温和旋转，幼童友好"),
            ("10:30", "阿宝功夫训练营", "🟡 互动体验，小孩最爱"),
            ("11:30", "平先生面馆", "🍜 中式简餐，人均¥70"),
            ("12:30", "鹰马飞行", "🟡 家庭过山车，92cm以上"),
            ("13:30", "奥利凡德魔杖店", "✨ 魔杖选择仪式，必体验"),
            ("14:00", "三把扫帚酒吧", "🍺 黄油啤酒+烤鸡腿"),
            ("15:00", "未来水世界特技表演", "🎭 必看！提前20分钟到"),
            ("16:00", "小黄人闹翻天", "🟡 3D模拟器，全家可玩"),
            ("16:45", "萌转过山车", "🟢 亲子入门过山车"),
            ("17:30", "超萌漩漩漩", "🟢 最温柔的项目"),
            ("18:00", "环球花车大巡游", "🎪 提前15分钟占位"),
            ("19:30", "灯影传奇", "✨ 灯光旋转飞椅"),
            ("20:30", "霍格沃茨城堡夜间魔法秀", "🎆 必看！提前30分钟占位"),
        ]
    elif preference == "thrill":
        route_steps = [
            ("08:30", "入园", "建议提前30分钟到大门"),
            ("09:00", "霸天虎过山车", "🔴 趁人少先冲最刺激，132cm+"),
            ("09:30", "哈利·波特与禁忌之旅", "🔴 全园最热门，趁早排"),
            ("10:30", "变形金刚：火源争夺战", "🔴 3D射击对战"),
            ("11:30", "侏罗纪世界大冒险", "🔴 暗黑乘骑，102cm+"),
            ("12:30", "嗷嗷龙烤肉", "🍖 烤肋排，人均¥110"),
            ("13:30", "大黄蜂回旋舞", "🟡 大黄蜂主题旋转"),
            ("14:00", "灯光摄像开拍！", "🟡 斯皮尔伯格特效体验"),
            ("15:00", "变形金刚：非凡之战", "🎭 必看特效秀"),
            ("16:00", "不可驯服", "🎭 侏罗纪主题真人秀"),
            ("17:00", "小黄人闹翻天", "🟡 刺激3D模拟器"),
            ("18:00", "环球花车大巡游", "🎪 提前15分钟占位"),
            ("19:00", "鹰马飞行", "🟡 二刷哈利波特区"),
            ("20:30", "霍格沃茨城堡夜间魔法秀", "🎆 必看！提前30分钟占位"),
        ]
    else:
        route_steps = [
            ("08:30", "入园", "建议提前30分钟到大门"),
            ("09:00", "哈利·波特与禁忌之旅", "🔴 全园最热门，趁早排"),
            ("10:00", "鹰马飞行", "🟡 家庭过山车，顺路"),
            ("10:30", "奥利凡德魔杖店", "✨ 魔杖选择仪式"),
            ("11:00", "三把扫帚酒吧", "🍺 黄油啤酒+午餐"),
            ("12:00", "变形金刚：火源争夺战", "🔴 3D射击，热门"),
            ("13:00", "霸天虎过山车", "🔴 午后人少，132cm+"),
            ("14:00", "侏罗纪世界大冒险", "🔴 暗黑乘骑"),
            ("15:00", "不可驯服", "🎭 必看！提前20分钟到"),
            ("16:00", "功夫熊猫：神龙大侠之旅", "🟢 室内漂流，国风主题"),
            ("17:00", "小黄人闹翻天", "🟡 3D模拟器"),
            ("18:00", "环球花车大巡游", "🎪 提前15分钟占位"),
            ("19:00", "未来水世界特技表演", "🎭 经典特技秀"),
            ("20:30", "霍格沃茨城堡夜间魔法秀", "🎆 必看！提前30分钟占位"),
        ]

    for time_slot, name, tip in route_steps:
        output += f"{time_slot} {name}\n   💡 {tip}\n\n"

    output += "💡 还可以问我：实时排队 | 推荐下一步 | 演出时间"
    return output


def universal_schedule(days=7):
    schedules = fetch_schedule()
    days = min(days, 14)

    output = "🗓 北京环球影城近期营业时间\n"
    output += "=" * 30 + "\n\n"

    if not schedules:
        for i in range(days):
            date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
            weekday = (datetime.now() + timedelta(days=i)).strftime("%w")
            weekday_name = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"][int(weekday)]
            open_time = "09:00"
            close_time = "20:00" if int(weekday) >= 5 else "19:00"
            output += f"{date} {weekday_name}: {open_time} - {close_time}\n"
        return output

    for i in range(min(days, 14)):
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        weekday = (datetime.now() + timedelta(days=i)).strftime("%w")
        weekday_name = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"][int(weekday)]
        info = schedules.get(date, {})
        raw_open = info.get("openingTime", "")
        raw_close = info.get("closingTime", "")
        open_time = format_showtime(raw_open) or "09:00"
        close_time = format_showtime(raw_close) or "20:00"
        output += f"{date} {weekday_name}: {open_time} - {close_time}\n"

    return output


def universal_dining(query=""):
    results = RESTAURANTS
    if query:
        q = query.lower()
        filtered = []
        for r in results:
            if q in r["name_cn"].lower() or q in r["area"].lower() or any(q in c.lower() for c in r["cuisine"]):
                filtered.append(r)
        results = filtered if filtered else RESTAURANTS

    results = results[:6]

    output = "🍽 园区餐厅推荐\n"
    output += "=" * 30 + "\n\n"

    for r in results:
        output += f"【{r['name_cn']}】\n"
        output += f"  📍 {r['area']} | {r['price_range']} | 人均{r['price_per_person']}元\n"
        output += f"  🍜 {', '.join(r['cuisine'])}\n"
        output += f"  ⭐ {', '.join(r['highlights'][:2])}\n\n"

    output += "💡 园区用餐建议：\n"
    output += "• 错峰就餐：11点前或14点后人少\n"
    output += "• 黄油啤酒必喝：三把扫帚酒吧和蜂蜜公爵都有\n"
    output += "• 出园后可在城市大道用餐（无需门票）"
    return output


# ==================== 工具注册表 ====================
TOOLS = {
    "universal_ticket": universal_ticket,
    "universal_wait_times": universal_wait_times,
    "universal_show_schedule": universal_show_schedule,
    "universal_smart_next": universal_smart_next,
    "universal_route": universal_route,
    "universal_schedule": universal_schedule,
    "universal_dining": universal_dining,
}


# ==================== CLI入口 ====================

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in TOOLS:
        print("用法: python universal_beijing.py <tool_name> [args_json]")
        print(f"可用工具: {', '.join(TOOLS.keys())}")
        sys.exit(1)

    tool_name = sys.argv[1]
    tool_func = TOOLS[tool_name]

    args = {}
    if len(sys.argv) > 2:
        try:
            args = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            args = {"query": sys.argv[2]}

    result = tool_func(**args)
    print(result)


if __name__ == "__main__":
    main()
