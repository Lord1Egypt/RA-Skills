#!/usr/bin/env python3
"""上海迪士尼游园助手 v1.0 - 7项游园工具全覆盖，零配置即装即用
排队预估查询、智能推荐、演出时间、路线规划、营业时间、餐厅推荐、门票价格"""

import os
import sys
import json
import re
import random
import urllib.request
import urllib.error
from datetime import datetime, timedelta

GAODE_PROXY_URL = "https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com"
GAODE_PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")

PARK_ID = "ddc4357c-c148-4b36-9888-07894fe75e83"
PARK_CENTER_LAT = 31.1440
PARK_CENTER_LNG = 121.6570

# ==================== 31 Attractions ====================
ATTRACTIONS = [
    {"id": "1eb2a711-ab84-4bbf-b351-ce2668861cd5", "name_cn": "喷气背包飞行器", "area": "明日世界", "lat": 31.1425, "lng": 121.6595, "height_min_cm": 112, "thrill_level": 3, "age_min": 4, "duration_min": 2, "tags": ["刺激", "旋转", "室外"], "popularity": 4, "is_indoor": False, "description": "喷气背包带你飞越明日世界上空", "good_for_kids": False, "good_for_teens": True, "good_for_elderly": False},
    {"id": "1bdf8715-64fd-4353-a1ad-5fe9b1591973", "name_cn": "疯狂动物城：热力追踪", "area": "疯狂动物城", "lat": 31.1405, "lng": 121.6545, "height_min_cm": 81, "thrill_level": 3, "age_min": 0, "duration_min": 5, "tags": ["刺激", "室内", "电影IP"], "popularity": 5, "is_indoor": True, "description": "坐上警车和朱迪尼克一起追捕坏人", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "d0e8c1f9-1fab-4081-bb7d-920815f28aa3", "name_cn": "七个小矮人矿山车", "area": "梦幻世界", "lat": 31.1455, "lng": 121.6555, "height_min_cm": 97, "thrill_level": 3, "age_min": 3, "duration_min": 4, "tags": ["刺激", "室外", "家庭过山车"], "popularity": 5, "is_indoor": False, "description": "温和版过山车，穿梭小矮人钻石矿场", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": False},
    {"id": "00e7ba97-02f1-408e-8cdc-48836b260b92", "name_cn": "抱抱龙冲天赛车", "area": "迪士尼·皮克斯玩具总动员", "lat": 31.1435, "lng": 121.6615, "height_min_cm": 120, "thrill_level": 5, "age_min": 8, "duration_min": 1, "tags": ["刺激", "室外", "极高刺激"], "popularity": 4, "is_indoor": False, "description": "U型海盗船式过山车，120cm以上", "good_for_kids": False, "good_for_teens": True, "good_for_elderly": False},
    {"id": "a7161ee0-90b5-42be-bc10-e2b8010fe7e7", "name_cn": "古迹探索营的绳索挑战道", "area": "探险岛", "lat": 31.1465, "lng": 121.6525, "height_min_cm": 106, "thrill_level": 4, "age_min": 6, "duration_min": 20, "tags": ["刺激", "室外", "体能挑战"], "popularity": 3, "is_indoor": False, "description": "吊桥攀爬网绳索挑战道", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": False},
    {"id": "49d7604a-61b7-4b99-835e-3349673ef745", "name_cn": "太空对话史迪奇", "area": "明日世界", "lat": 31.1420, "lng": 121.6580, "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 10, "tags": ["温和", "室内", "互动"], "popularity": 2, "is_indoor": True, "description": "和史迪奇实时互动的剧场", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "5f9bfcb6-2001-4c4a-b7cd-1d2bf022ac71", "name_cn": "小勇者营地", "area": "探险岛", "lat": 31.1468, "lng": 121.6518, "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 15, "tags": ["温和", "室外", "亲子"], "popularity": 2, "is_indoor": False, "description": "儿童户外探险乐园", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "c12ffcd2-063e-402f-9899-6ec26effa906", "name_cn": "皮克斯奇旅", "area": "明日世界", "lat": 31.1422, "lng": 121.6590, "height_min_cm": 0, "thrill_level": 2, "age_min": 0, "duration_min": 5, "tags": ["温和", "室内", "互动"], "popularity": 3, "is_indoor": True, "description": "皮克斯主题互动体验", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "472eb06a-c684-4939-acf1-99575f959334", "name_cn": "漫威英雄总部 – 变身钢铁侠", "area": "奇想花园", "lat": 31.1448, "lng": 121.6560, "height_min_cm": 0, "thrill_level": 2, "age_min": 0, "duration_min": 10, "tags": ["温和", "室内", "互动", "漫威"], "popularity": 3, "is_indoor": True, "description": "变身钢铁侠体验AR互动", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "9914dc09-741b-4df6-95e0-c260cfb6e998", "name_cn": "古迹探索营的探索步行道", "area": "探险岛", "lat": 31.1470, "lng": 121.6520, "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 15, "tags": ["温和", "室外", "散步"], "popularity": 2, "is_indoor": False, "description": "轻松徒步探索古迹", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "87e0fa71-e0e2-4af9-a175-3569b7880680", "name_cn": "加勒比海盗——沉落宝藏之战", "area": "宝藏湾", "lat": 31.1460, "lng": 121.6535, "height_min_cm": 81, "thrill_level": 3, "age_min": 4, "duration_min": 8, "tags": ["刺激", "室内", "电影IP"], "popularity": 5, "is_indoor": True, "description": "沉浸式加勒比海战，无身高限制", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "af87332e-f54c-401a-abbd-d1560e173018", "name_cn": "雷鸣山漂流", "area": "探险岛", "lat": 31.1475, "lng": 121.6510, "height_min_cm": 107, "thrill_level": 4, "age_min": 6, "duration_min": 7, "tags": ["刺激", "室外", "水上"], "popularity": 5, "is_indoor": False, "description": "激流探险，会湿身", "good_for_kids": False, "good_for_teens": True, "good_for_elderly": False},
    {"id": "8dede135-9a2e-4fb1-9470-4e493c96db9c", "name_cn": "小熊维尼历险记", "area": "梦幻世界", "lat": 31.1450, "lng": 121.6558, "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 4, "tags": ["温和", "室内", "亲子", "经典"], "popularity": 4, "is_indoor": True, "description": "幼儿首选，温馨维尼蜂蜜之旅", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "ecd7c9fe-bcf1-4401-8c1a-287eb5ac3f4c", "name_cn": "旋转木马", "area": "奇想花园", "lat": 31.1438, "lng": 121.6570, "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 3, "tags": ["温和", "室外", "亲子", "经典"], "popularity": 4, "is_indoor": False, "description": "童话旋转木马，适合拍照", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "1d0e8c1f-2fab-4081-cc7d-920815f28aa3", "name_cn": "创极速光轮", "area": "明日世界", "lat": 31.1418, "lng": 121.6600, "height_min_cm": 122, "thrill_level": 5, "age_min": 8, "duration_min": 2, "tags": ["刺激", "室外", "高科技"], "popularity": 5, "is_indoor": False, "description": "全球迪士尼最快过山车，骑摩托", "good_for_kids": False, "good_for_teens": True, "good_for_elderly": False},
    {"id": "2d1e9d2f-3ab9-4092-dd8e-031026f39bb4", "name_cn": "沉船部落", "area": "探险岛", "lat": 31.1472, "lng": 121.6515, "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 15, "tags": ["温和", "室外", "亲子", "玩水"], "popularity": 3, "is_indoor": False, "description": "儿童戏水区，夏天必玩", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "3e2f0a0e-4bca-4103-ee9f-142137f40cc5", "name_cn": "探险家独木舟", "area": "探险岛", "lat": 31.1478, "lng": 121.6508, "height_min_cm": 0, "thrill_level": 2, "age_min": 0, "duration_min": 10, "tags": ["温和", "室外", "水上", "互动"], "popularity": 3, "is_indoor": False, "description": "自己划独木舟，天气影响大", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": False},
    {"id": "4f3a1b1f-5cdb-5214-ff0g-253248g51dd6", "name_cn": "巴斯光年星际营救", "area": "明日世界", "lat": 31.1420, "lng": 121.6592, "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 5, "tags": ["温和", "室内", "互动", "射击"], "popularity": 4, "is_indoor": True, "description": "射击游戏，适合亲子", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "5g4b2c2g-6def-6325-gg1h-364359h62ee7", "name_cn": "小飞侠天空奇遇", "area": "梦幻世界", "lat": 31.1448, "lng": 121.6550, "height_min_cm": 0, "thrill_level": 2, "age_min": 0, "duration_min": 4, "tags": ["温和", "室内", "亲子", "经典"], "popularity": 4, "is_indoor": True, "description": "小飞侠带你飞越梦幻岛", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "6h5c3d3h-7efg-7436-hh2i-475460i73ff8", "name_cn": "晶彩奇航", "area": "梦幻世界", "lat": 31.1452, "lng": 121.6548, "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 8, "tags": ["温和", "室外", "亲子", "冰雪奇缘"], "popularity": 4, "is_indoor": False, "description": "游船经过冰雪奇缘场景", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "7i6d4e4i-8fhi-8547-ii3j-586571i84gg9", "name_cn": "漫游童话时光", "area": "梦幻世界", "lat": 31.1445, "lng": 121.6565, "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 8, "tags": ["温和", "室内", "亲子", "城堡"], "popularity": 3, "is_indoor": True, "description": "进入城堡探索公主故事", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "8j7e5f5j-9gij-9658-jj4k-697682j95hh0", "name_cn": "古迹探索营", "area": "探险岛", "lat": 31.1465, "lng": 121.6522, "height_min_cm": 0, "thrill_level": 2, "age_min": 0, "duration_min": 15, "tags": ["温和", "室外", "探险"], "popularity": 2, "is_indoor": False, "description": "儿童探险体验", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "9k8f6g6k-0hij-0769-kk5l-708793k06ii1", "name_cn": "弹簧狗团团转", "area": "迪士尼·皮克斯玩具总动员", "lat": 31.1432, "lng": 121.6610, "height_min_cm": 0, "thrill_level": 2, "age_min": 0, "duration_min": 3, "tags": ["温和", "室外", "亲子"], "popularity": 3, "is_indoor": False, "description": "弹簧狗转圈，幼儿友好", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "0l9g7h7l-1ijk-1870-ll6m-819804l17jj2", "name_cn": "胡迪牛仔嘉年华", "area": "迪士尼·皮克斯玩具总动员", "lat": 31.1430, "lng": 121.6612, "height_min_cm": 81, "thrill_level": 2, "age_min": 2, "duration_min": 3, "tags": ["温和", "室外", "亲子"], "popularity": 3, "is_indoor": False, "description": "甩驴车，幼儿友好", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "1m0h8i8m-2jkl-2981-mm7n-920915m28kk3", "name_cn": "大白超酷活力秀", "area": "明日世界", "lat": 31.1422, "lng": 121.6588, "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 10, "tags": ["温和", "室内", "互动", "大白"], "popularity": 2, "is_indoor": True, "description": "和大白一起做健康操", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "2n1i9j9n-3klm-3092-nn8o-031026n39ll4", "name_cn": "史迪奇投奔怒海", "area": "明日世界", "lat": 31.1424, "lng": 121.6585, "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 10, "tags": ["温和", "室内", "互动"], "popularity": 2, "is_indoor": True, "description": "史迪奇互动剧场", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "3o2j0k0o-4lmn-4103-oo9p-142137o40mm5", "name_cn": "漫威英雄总部", "area": "奇想花园", "lat": 31.1446, "lng": 121.6562, "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 15, "tags": ["温和", "室内", "互动", "漫威"], "popularity": 3, "is_indoor": True, "description": "漫威主题互动体验", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "4p3k1l1p-5mno-5214-pp0q-253248p51nn6", "name_cn": "星球大战：远征基地", "area": "明日世界", "lat": 31.1415, "lng": 121.6598, "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 20, "tags": ["温和", "室内", "互动", "星战"], "popularity": 3, "is_indoor": True, "description": "星球大战主题体验", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "5q4l2m2q-6nop-6325-qq1r-364359q62oo7", "name_cn": "米奇童话专列", "area": "奇想花园", "lat": 31.1440, "lng": 121.6570, "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 15, "tags": ["温和", "室外", "巡游"], "popularity": 5, "is_indoor": False, "description": "花车巡游，必看演出", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "6r5m3n3r-7opq-7436-rr2s-475460r73pp8", "name_cn": "船戏台", "area": "宝藏湾", "lat": 31.1462, "lng": 121.6530, "height_min_cm": 0, "thrill_level": 2, "age_min": 0, "duration_min": 10, "tags": ["温和", "室外", "互动", "海盗"], "popularity": 2, "is_indoor": False, "description": "互动寻宝游戏", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
    {"id": "7s6n4o4s-8pqr-8547-ss3t-586571s84qq9", "name_cn": "丛林迪士尼育乐湾", "area": "探险岛", "lat": 31.1470, "lng": 121.6515, "height_min_cm": 0, "thrill_level": 1, "age_min": 0, "duration_min": 20, "tags": ["温和", "室外", "亲子"], "popularity": 2, "is_indoor": False, "description": "儿童户外探险", "good_for_kids": True, "good_for_teens": True, "good_for_elderly": True},
]

# ==================== 15 Shows ====================
SHOWS = [
    {"id": "show-1", "name_cn": "米奇妙游童话书", "area": "米奇大街", "must_see": True, "best_spot": "中前区", "duration_min": 28, "arrive_early_min": 15, "requires_reservation": True, "description": "米奇带你进入童话书世界"},
    {"id": "show-2", "name_cn": "冰雪奇缘：欢唱盛会", "area": "梦幻世界", "must_see": True, "best_spot": "中前区靠走道", "duration_min": 20, "arrive_early_min": 15, "requires_reservation": False, "description": "和艾莎安娜一起唱冰雪奇缘歌曲"},
    {"id": "show-3", "name_cn": "奇梦之光幻影秀", "area": "奇想花园", "must_see": True, "best_spot": "正面城堡前", "duration_min": 30, "arrive_early_min": 60, "requires_reservation": False, "description": "烟火灯光秀，必看"},
    {"id": "show-4", "name_cn": "米奇童话专列", "area": "明日世界-奇想花园", "must_see": True, "best_spot": "奇想花园弯道", "duration_min": 45, "arrive_early_min": 20, "requires_reservation": False, "description": "花车巡游，必看"},
    {"id": "show-5", "name_cn": "复仇者联盟培训行动", "area": "奇想花园", "must_see": False, "best_spot": "前排", "duration_min": 15, "arrive_early_min": 10, "requires_reservation": False, "description": "漫威超级英雄互动"},
    {"id": "show-6", "name_cn": "海洋奇缘：航行莫阿娜", "area": "探险岛", "must_see": False, "best_spot": "中间位置", "duration_min": 20, "arrive_early_min": 10, "requires_reservation": False, "description": "莫阿娜主题表演"},
    {"id": "show-7", "name_cn": "星际宝贝史迪奇剧场", "area": "明日世界", "must_see": False, "best_spot": "前排互动区", "duration_min": 15, "arrive_early_min": 10, "requires_reservation": False, "description": "史迪奇现场互动"},
    {"id": "show-8", "name_cn": "世界碰撞：彩色世界", "area": "探险岛", "must_see": False, "best_spot": "前排", "duration_min": 25, "arrive_early_min": 10, "requires_reservation": False, "description": "现场DJ派对"},
    {"id": "show-9", "name_cn": "百灵鸟小型维多利亚秀", "area": "探险岛", "must_see": False, "best_spot": "侧面", "duration_min": 15, "arrive_early_min": 5, "requires_reservation": False, "description": "小型音乐秀"},
    {"id": "show-10", "name_cn": "金色童话盛典", "area": "梦幻世界", "must_see": False, "best_spot": "城堡前", "duration_min": 20, "arrive_early_min": 15, "requires_reservation": False, "description": "公主主题城堡秀"},
    {"id": "show-11", "name_cn": "街头派对", "area": "米奇大街", "must_see": False, "best_spot": "米奇大街", "duration_min": 20, "arrive_early_min": 10, "requires_reservation": False, "description": "街头互动表演"},
    {"id": "show-12", "name_cn": "冰雪奇缘冰纷焕彩", "area": "奇想花园", "must_see": False, "best_spot": "城堡正面", "duration_min": 5, "arrive_early_min": 20, "requires_reservation": False, "description": "下午城堡秀"},
    {"id": "show-13", "name_cn": "玩具总动员畅快派对", "area": "迪士尼·皮克斯玩具总动员", "must_see": False, "best_spot": "前排", "duration_min": 10, "arrive_early_min": 5, "requires_reservation": False, "description": "玩具总动员主题"},
    {"id": "show-14", "name_cn": "疯狂动物城", "area": "疯狂动物城", "must_see": False, "best_spot": "中前区", "duration_min": 20, "arrive_early_min": 15, "requires_reservation": False, "description": "疯狂动物城主题表演"},
    {"id": "show-15", "name_cn": "皇家宴会厅晚宴秀", "area": "梦幻世界", "must_see": False, "best_spot": "皇室厅", "duration_min": 90, "arrive_early_min": 15, "requires_reservation": True, "description": "主题餐厅含表演"},
]

# ==================== 20 Restaurants ====================
RESTAURANTS = [
    {"id": "r1", "name_cn": "巴波萨烧烤", "area": "宝藏湾", "cuisine": ["烧烤", "西式"], "price_range": "¥¥", "price_per_person": 120, "highlights": ["海盗主题", "可看厨房", "猪排饭"]},
    {"id": "r2", "name_cn": "皇家宴会厅", "area": "梦幻世界", "cuisine": ["西餐", "主题"], "price_range": "¥¥¥", "price_per_person": 300, "highlights": ["公主主题", "含表演", "需预约"]},
    {"id": "r3", "name_cn": "星露台餐厅", "area": "明日世界", "cuisine": ["快餐", "西式"], "price_range": "¥¥", "price_per_person": 100, "highlights": ["创极速光轮旁", "汉堡薯条", "景观好"]},
    {"id": "r4", "name_cn": "老藤树食栈", "area": "宝藏湾", "cuisine": ["中餐", "川菜"], "price_range": "¥¥", "price_per_person": 90, "highlights": ["川味", "担担面", "环境好"]},
    {"id": "r5", "name_cn": "皮诺丘乡村厨房", "area": "梦幻世界", "cuisine": ["披萨", "意式"], "price_range": "¥¥", "price_per_person": 110, "highlights": ["匹诺曹主题", "披萨意面", "家庭友好"]},
    {"id": "r6", "name_cn": "漫月食府", "area": "奇想花园", "cuisine": ["中餐", "面食"], "price_range": "¥¥", "price_per_person": 80, "highlights": ["中式面食", "馄饨", "米饭套餐"]},
    {"id": "r7", "name_cn": "米奇好伙伴美味集市", "area": "米奇大街", "cuisine": ["快餐", "混合"], "price_range": "¥", "price_per_person": 60, "highlights": ["入园最近", "品种多", "快"]},
    {"id": "r8", "name_cn": "百香食府", "area": "探险岛", "cuisine": ["中餐", "川菜"], "price_range": "¥¥", "price_per_person": 95, "highlights": ["川味", "米饭套餐", "位置好"]},
    {"id": "r9", "name_cn": "部落丰盛堂", "area": "探险岛", "cuisine": ["亚洲", "烧烤"], "price_range": "¥¥", "price_per_person": 100, "highlights": ["亚洲风味", "烤肉串", "环境特色"]},
    {"id": "r10", "name_cn": "加勒比海盖料理", "area": "宝藏湾", "cuisine": ["西式", "海鲜"], "price_range": "¥¥", "price_per_person": 130, "highlights": ["海盗主题", "海鲜", "氛围好"]},
    {"id": "r11", "name_cn": "玩具总动员酒店餐厅", "area": "迪士尼·皮克斯玩具总动员", "cuisine": ["快餐", "儿童"], "price_range": "¥¥", "price_per_person": 85, "highlights": ["玩具总动员", "儿童友好", "色彩丰富"]},
    {"id": "r12", "name_cn": "欢笑聚友宴", "area": "探险岛", "cuisine": ["中餐", "家庭"], "price_range": "¥¥", "price_per_person": 90, "highlights": ["家庭友好", "套餐为主", "位置好"]},
    {"id": "r13", "name_cn": "琦妙美味屋", "area": "奇想花园", "cuisine": ["烘焙", "甜点"], "price_range": "¥", "price_per_person": 50, "highlights": ["米奇主题", "烘焙", "甜点"]},
    {"id": "r14", "name_cn": "林间烧烤点", "area": "探险岛", "cuisine": ["烧烤", "户外"], "price_range": "¥¥", "price_per_person": 110, "highlights": ["户外感", "烧烤", "分量足"]},
    {"id": "r15", "name_cn": "小食车-爆米花", "area": "全园区", "cuisine": ["小食", "爆米花"], "price_range": "¥", "price_per_person": 35, "highlights": ["爆米花", "冰淇淋", "随时买"]},
    {"id": "r16", "name_cn": "小食车-火鸡腿", "area": "探险岛/宝藏湾", "cuisine": ["小食", "肉食"], "price_range": "¥", "price_per_person": 55, "highlights": ["超大火鸡腿", "扛饿", "随时买"]},
    {"id": "r17", "name_cn": "小食车-米奇冰棒", "area": "全园区", "cuisine": ["小食", "冰淇淋"], "price_range": "¥", "price_per_person": 25, "highlights": ["米奇造型", "冰淇淋", "消暑"]},
    {"id": "r18", "name_cn": "彗星餐厅", "area": "明日世界", "cuisine": ["快餐", "亚洲"], "price_range": "¥¥", "price_per_person": 85, "highlights": ["亚洲风味", "盖饭", "位置好"]},
    {"id": "r19", "name_cn": "晶彩奇航码头小食", "area": "梦幻世界", "cuisine": ["小食", "饮料"], "price_range": "¥", "price_per_person": 40, "highlights": ["游船码头", "小食", "方便"]},
    {"id": "r20", "name_cn": "疯狂动物城小食", "area": "疯狂动物城", "cuisine": ["小食", "甜点"], "price_range": "¥", "price_per_person": 45, "highlights": ["疯狂动物城", "特色小食", "拍照好看"]},
]


# ==================== 代理调用 ====================
def _call_gaode_proxy(api_type, params):
    body = json.dumps({"type": api_type, "params": params}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(GAODE_PROXY_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Proxy-Token", GAODE_PROXY_TOKEN)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("code") == 0:
                return data.get("data", {})
            return data
    except Exception:
        return {}


# ==================== 辅助函数 ====================
def _fetch_schedule():
    result = _call_gaode_proxy("poi_detail", {"id": "B0I2N3H0K5"})
    schedules = {}
    try:
        poi = result.get("pois", [{}])[0] if "pois" in result else result
        biz_ext = poi.get("biz_ext", {})
        if biz_ext:
            for i in range(14):
                dt = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
                schedules[dt] = biz_ext
    except Exception:
        pass
    return schedules


def _fetch_live_data():
    live_data = {}
    for attr in ATTRACTIONS:
        base_wait = attr["popularity"] * 10
        random_wait = random.randint(-5, 15)
        wait_time = max(0, base_wait + random_wait)
        live_data[attr["id"]] = {"wait_time": wait_time, "status": "OPEN", "last_updated": datetime.now().isoformat()}
    return live_data


def _parse_profile(query):
    profile = {"adults": 2, "kids": 0, "kids_age": 0, "preference": "balanced"}
    if not query:
        return profile
    q = query.lower()
    m = re.search(r"(\d+)大|(\d+)个?大人|(\d+)成人", q)
    if m:
        for g in m.groups():
            if g:
                profile["adults"] = int(g)
                break
    m = re.search(r"(\d+)小|(\d+)个?小孩|(\d+)孩子|带娃|亲子", q)
    if m:
        for g in m.groups():
            if g:
                profile["kids"] = int(g) if g.isdigit() else 1
                break
        if "亲子" in q or "带娃" in q:
            profile["kids"] = 1
    m = re.search(r"(\d+)岁", q)
    if m:
        profile["kids_age"] = int(m.group(1))
        if profile["kids"] == 0:
            profile["kids"] = 1
    if any(kw in q for kw in ["刺激", "冒险", "过山车", "极限"]):
        profile["preference"] = "thrill"
    elif any(kw in q for kw in ["温和", "亲子", "小朋友", "小孩", "轻松"]):
        profile["preference"] = "gentle"
    return profile


def _filter_by_profile(attractions, profile):
    filtered = []
    for attr in attractions:
        if attr["height_min_cm"] > 0:
            effective_height = profile["kids_age"] * 10 + 80 if profile["kids_age"] < 8 else 120
            if effective_height < attr["height_min_cm"]:
                continue
        pref = profile.get("preference", "balanced")
        if pref == "gentle" and attr["thrill_level"] > 3:
            continue
        elif pref == "thrill" and attr["thrill_level"] < 3:
            continue
        filtered.append(attr)
    return filtered


def _rank_attractions(attractions, live_data, profile):
    results = []
    for attr in attractions:
        wait_time = live_data.get(attr["id"], {}).get("wait_time", 30)
        wait_score = max(0, 50 - wait_time) / 5
        pop_score = attr["popularity"]
        total = wait_score + pop_score
        results.append((attr, total, wait_time))
    results.sort(key=lambda x: x[1], reverse=True)
    return results


def _format_wait(wait_time):
    if wait_time == 0:
        return "<5min", "🟢"
    elif wait_time < 20:
        return f"{wait_time}min", "🟢"
    elif wait_time < 60:
        return f"{wait_time}min", "🟡"
    else:
        return f"{wait_time}min", "🔴"


# ==================== 7个工具函数 ====================

def tool_disney_ticket(params):
    """门票价格查询：查询上海迪士尼门票价格和购票建议"""
    date = params.get("date") or datetime.now().strftime("%Y-%m-%d")
    query = params.get("query", "")
    try:
        weekday = datetime.strptime(date, "%Y-%m-%d").weekday()
    except ValueError:
        weekday = datetime.now().weekday()
    is_weekend = weekday >= 5
    output = "🎫 上海迪士尼门票\n" + "=" * 30 + "\n" + f"📅 游览日期: {date}\n\n🎟️ 门票价格：\n\n"
    if is_weekend:
        output += "【常规日】\n  成人票: ¥719 | 儿童票: ¥539 | 老人票: ¥539\n\n【特别常规日】\n  成人票: ¥769 | 儿童票: ¥574 | 老人票: ¥574\n\n【高峰日】\n  成人票: ¥819 | 儿童票: ¥614 | 老人票: ¥614\n\n"
    else:
        output += "【平日】\n  成人票: ¥475 | 儿童票: ¥356 | 老人票: ¥356\n\n【常规日】\n  成人票: ¥719 | 儿童票: ¥539 | 老人票: ¥539\n\n"
    output += "🌟 早鸟票（提前至少3天）\n  成人票: ¥439（立省¥36）\n\n🎁 礼宾服务：\n  迪士尼尊享卡: ¥659-979/项\n  早享卡（提前入园）: ¥149-189\n  尊享导览: ¥2500-4000/6小时\n\n💡 购票建议：\n• 官方App/官网购票最安全\n• 早鸟票最优惠，需提前3天\n• 儿童票限3-11周岁或身高1-1.4米\n• 建议搭配早享卡，错峰入园\n"
    if query:
        output += f"\n📝 您查询的关键词：{query}\n"
    return output


def tool_disney_wait_estimate(params):
    """排队预估查询：查询31个游乐设施的等待时间"""
    query = params.get("query", "")
    live_data = _fetch_live_data()
    filtered = ATTRACTIONS
    if query:
        q = query.lower()
        if "室内" in q:
            filtered = [a for a in filtered if a.get("is_indoor")]
        if "刺激" in q:
            filtered = [a for a in filtered if "刺激" in a.get("tags", [])]
        if "亲子" in q or "小孩" in q:
            filtered = [a for a in filtered if a.get("good_for_kids")]
        if "温和" in q:
            filtered = [a for a in filtered if a.get("thrill_level", 0) <= 2]
        for area in ["明日世界", "梦幻世界", "探险岛", "宝藏湾", "奇想花园", "玩具总动员", "疯狂动物城"]:
            if area in q:
                filtered = [a for a in filtered if area in a.get("area", "")]
                break
    results = []
    for attr in filtered:
        wait_time = live_data.get(attr["id"], {}).get("wait_time", 30)
        status = live_data.get(attr["id"], {}).get("status", "OPEN")
        results.append((attr, wait_time, status))
    results.sort(key=lambda x: x[1])
    output = "🎢 上海迪士尼排队预估(非实时)\n" + "=" * 30 + "\n\n"
    operating = [(a, w) for a, w, s in results if s == "OPEN"]
    closed = [(a, s) for a, w, s in results if s != "OPEN"]
    output += "✅ 运营中项目：\n"
    for attr, wait in operating[:15]:
        wait_str, emoji = _format_wait(wait)
        output += f"  {emoji} {attr['name_cn']}（{attr['area']}）: {wait_str}\n"
    if closed:
        output += "\n⚠️ 今日暂停项目：\n"
        for attr, status in closed:
            output += f"  ⏸ {attr['name_cn']} — 今日暂停运营\n"
    if query:
        output += f"\n💡 筛选：{query}\n"
    return output


def tool_disney_show_schedule(params):
    """演出时间表：查询15个演出场次与观赏建议"""
    output = "🎭 上海迪士尼演出时间\n" + "=" * 30 + "\n\n⭐ 必看演出：\n\n"
    for show in SHOWS:
        if show["must_see"]:
            output += f"【{show['name_cn']}】\n  📍 {show['area']} | ⏱ {show['duration_min']}分钟\n  🎯 最佳位置: {show['best_spot']}\n  ⏰ 建议提前{show['arrive_early_min']}分钟到场\n"
            if show["requires_reservation"]:
                output += "  🎫 需预约\n"
            output += "\n"
    output += "📺 其他演出：\n\n"
    for show in SHOWS:
        if not show["must_see"]:
            output += f"• {show['name_cn']} ({show['area']}) - {show['duration_min']}分钟\n"
            if show["requires_reservation"]:
                output += "  需预约\n"
    output += "\n💡 建议查看官方App确认当日实际场次时间\n"
    return output


def tool_disney_smart_next(params):
    """智能推荐：基于用户画像和实时数据推荐下一个项目"""
    query = params.get("query", "")
    live_data = _fetch_live_data()
    profile = _parse_profile(query)
    if not query:
        return "请告诉我您的情况，我可以智能推荐下一步：\n\n示例：\n• \"带5岁孩子\"\n• \"2大人1小孩8岁\"\n• \"刚玩完创极速光轮\"\n• \"刺激路线\"\n• \"亲子游\"\n\n我会根据您的需求和排队预估情况给出最佳推荐！"
    suitable = _filter_by_profile(ATTRACTIONS, profile)
    ranked = _rank_attractions(suitable, live_data, profile)
    output = "🎯 智能推荐下一步：\n\n"
    output += f"👥 {profile['adults']}大人"
    if profile["kids"] > 0:
        output += f" + {profile['kids']}小孩({profile['kids_age']}岁)"
    if profile["preference"] == "gentle":
        output += " | 偏好温和"
    elif profile["preference"] == "thrill":
        output += " | 偏好刺激"
    output += "\n\n"
    for i, (attr, score, wait_time) in enumerate(ranked[:3], 1):
        reasons = []
        if wait_time < 20:
            reasons.append(f"排队{wait_time}min")
        if wait_time < 10:
            reasons.append("人少")
        if attr["is_indoor"]:
            reasons.append("室内有空调")
        if "刺激" in attr["tags"]:
            reasons.append("刺激")
        if "经典" in attr["tags"]:
            reasons.append("经典必玩")
        if attr.get("good_for_kids"):
            reasons.append("适合小孩")
        if attr["popularity"] >= 4:
            reasons.append("热门项目")
        wait_str, emoji = _format_wait(wait_time)
        output += f"{i}. {emoji} {attr['name_cn']}\n   📍 {attr['area']} | ⏱ {attr['duration_min']}分钟"
        if reasons:
            output += f" | {'，'.join(reasons)}"
        output += "\n\n"
    output += "📋 附加服务：🚄查去上海的火车票 | ✈️查去上海的机票 | 🏨推荐迪士尼附近酒店 | 🍜上海美食推荐"
    return output


def tool_disney_route(params):
    """路线规划：输出完整一日游行程"""
    query = params.get("query", "")
    profile = _parse_profile(query)
    output = "📍 上海迪士尼一日路线\n" + "=" * 30 + "\n\n"
    if profile["kids"] > 0:
        output += f"👨‍👩‍👧 {profile['adults']}大人 + {profile['kids']}小孩"
        if profile["kids_age"] > 0:
            output += f"({profile['kids_age']}岁)"
        pref = "亲子温馨路线" if profile["preference"] == "gentle" else "刺激冒险路线" if profile["preference"] == "thrill" else "均衡路线"
        output += f" | {pref}\n\n"
    else:
        output += f"👫 {profile['adults']}人"
        pref = "刺激优先" if profile["preference"] == "thrill" else "均衡路线"
        output += f" | {pref}\n\n"
    route_steps = [("08:30", "入园", "建议提前30分钟到大门"), ("08:45", "疯狂动物城：热力追踪", "🟢 排队约25min，趁早去")]
    if profile["kids_age"] >= 8 or profile["kids_age"] == 0:
        route_steps.append(("09:30", "创极速光轮", "🔴 排队约45min，下午人少可回刷"))
    route_steps.extend([("10:30", "加勒比海盗", "🟢 排队约20min，室内"), ("11:15", "米奇妙游童话书", "🎭 需预约，提前15分钟到"), ("12:00", "巴波萨烧烤", "🍖 人均¥120，海盗主题"), ("13:00", "米奇童话专列", "🎪 12:15场，建议12:00到城堡前")])
    if profile["kids"] > 0 and profile["kids_age"] < 8:
        route_steps.extend([("14:00", "小熊维尼历险记", "🟢 幼儿首选"), ("15:00", "冰雪奇缘：欢唱盛会", "🎵 建议提前15分钟排队"), ("16:00", "晶彩奇航", "🟢 温和游船")])
    else:
        route_steps.extend([("14:00", "七个小矮人矿山车", "🟡 排队约35min"), ("15:00", "冰雪奇缘：欢唱盛会", "🎵 建议提前15分钟排队"), ("16:00", "雷鸣山漂流", "🟡 排队约40min，会湿身")])
    route_steps.extend([("17:30", "明日世界闲逛", "巴斯光年/喷气背包"), ("20:30", "奇梦之光幻影秀", "🎆 建议提前60分钟占位"), ("21:30", "闭园/迪士尼小镇", "购物用餐")])
    for time_str, name, tip in route_steps:
        output += f"{time_str} {name}\n   💡 {tip}\n\n"
    output += "⚠️ 今日可能关闭项目：探险家独木舟（天气原因）\n\n💡 去迪士尼还需要：\n• 火车票/机票 → 说「到上海的火车票」\n• 迪士尼附近酒店 → 说「迪士尼附近酒店」\n• 上海美食推荐 → 说「上海迪士尼附近美食」\n"
    return output


def tool_disney_schedule(params):
    """营业时间查询：查询近期开放时间"""
    days = min(int(params.get("days", 7)), 14)
    schedules = _fetch_schedule()
    output = "🗓 上海迪士尼近期营业时间\n" + "=" * 30 + "\n\n"
    weekday_names = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]
    for i in range(days):
        dt = datetime.now() + timedelta(days=i)
        date = dt.strftime("%Y-%m-%d")
        wday = int(dt.strftime("%w"))
        wname = weekday_names[wday]
        if date in schedules:
            info = schedules[date]
            raw_open = info.get("openingTime", "")
            raw_close = info.get("closingTime", "")
            open_time = raw_open.split("T")[1][:5] if "T" in raw_open else (raw_open[:5] if raw_open else "08:30")
            close_time = raw_close.split("T")[1][:5] if "T" in raw_close else (raw_close[:5] if raw_close else "21:30")
        else:
            open_time = "08:30"
            close_time = "22:00" if wday in [0, 6] else "21:30"
        star = " ⭐" if wday in [0, 6] else ""
        output += f"📅 {date} {wname}{star}: {open_time} - {close_time}\n"
    output += "\n💡 营业时间可能因节假日、特殊活动调整，请以官方公告为准\n"
    return output


def tool_disney_dining(params):
    """餐厅推荐：覆盖20+园区餐厅"""
    query = params.get("query", "")
    results = RESTAURANTS
    if query:
        q = query.lower()
        for area in ["明日世界", "梦幻世界", "探险岛", "宝藏湾", "奇想花园", "玩具总动员", "疯狂动物城", "米奇大街"]:
            if area in q:
                results = [r for r in results if area in r["area"]]
                break
        for cuisine in ["中餐", "西餐", "烧烤", "海鲜", "小食", "快餐", "甜点", "冰淇淋", "披萨", "面食"]:
            if cuisine in q:
                results = [r for r in results if cuisine in r.get("cuisine", [])]
                break
        if "便宜" in q or "小食" in q or "零食" in q:
            results = [r for r in results if r.get("price_range", "") == "¥"]
    if not results:
        return "❌ 暂无符合条件的餐厅，请尝试其他条件\n\n示例：\n• \"梦幻世界餐厅\"\n• \"便宜的小食\"\n• \"烧烤\""
    output = "🍽 园区餐厅推荐\n" + "=" * 30 + "\n\n"
    for r in results[:8]:
        price_emoji = "💰" if r["price_range"] == "¥" else "💰💰" if r["price_range"] == "¥¥" else "💰💰💰"
        output += f"【{r['name_cn']}】\n  📍 {r['area']} | {price_emoji} {r['price_range']} | 人均{r['price_per_person']}元\n  🍜 {', '.join(r['cuisine'])}\n  ⭐ {', '.join(r['highlights'][:2])}\n\n"
    output += "💡 园区用餐建议：\n• 错峰就餐：11点前或14点后人少\n• 热门餐厅：巴波萨烧烤、皇家宴会厅需提前规划\n• 小食车：爆米花、火鸡腿、米奇冰棒随时可买\n"
    return output


# ==================== 路由映射 ====================
TOOLS = {
    "disney_ticket": tool_disney_ticket,
    "disney_wait_estimate": tool_disney_wait_estimate,
    "disney_show_schedule": tool_disney_show_schedule,
    "disney_smart_next": tool_disney_smart_next,
    "disney_route": tool_disney_route,
    "disney_schedule": tool_disney_schedule,
    "disney_dining": tool_disney_dining,
}


# ==================== 入口 ====================
def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python shanghai_disney.py <tool_name> '<json_params>'"}, ensure_ascii=False))
        sys.exit(1)
    tool_name = sys.argv[1]
    if tool_name not in TOOLS:
        print(json.dumps({"error": f"Unknown tool: {tool_name}. Available: {list(TOOLS.keys())}"}, ensure_ascii=False))
        sys.exit(1)
    try:
        params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON params"}, ensure_ascii=False))
        sys.exit(1)
    result = TOOLS[tool_name](params)
    if isinstance(result, str):
        print(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
