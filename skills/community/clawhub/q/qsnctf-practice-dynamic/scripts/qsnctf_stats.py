#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import argparse
from datetime import datetime

API_VIEWLIST = "https://www.qsnctf.com/api/5dboard/viewlist"
API_PLAYLIST = "https://www.qsnctf.com/api/5dboard/playlist"

def get_answer_info(limit=10):
    try:
        response = requests.get(API_VIEWLIST, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") == 200:
            items = data.get("data", {}).get("list", {}).get("answerInfoItems", [])
            if limit > 0:
                items = items[:limit]
            return items
        else:
            print(f"API错误: {data.get('msg', '未知错误')}")
            return []
    except requests.RequestException as e:
        print(f"网络请求错误: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return []

def get_ranking():
    try:
        response = requests.get(API_PLAYLIST, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") == 200:
            return data.get("data", {}).get("list", [])
        else:
            print(f"API错误: {data.get('msg', '未知错误')}")
            return []
    except requests.RequestException as e:
        print(f"网络请求错误: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return []

def format_answer_info(items):
    if not items:
        return "暂无解题动态"
    
    output = []
    output.append("=" * 60)
    output.append("青少年CTF练习场 - 近期解题动态")
    output.append("=" * 60)
    output.append(f"{'用户名':<20} {'题目类别':<25} {'时间':<20}")
    output.append("-" * 60)
    
    for item in items:
        username = item.get("username", "N/A")
        category = item.get("category", "N/A")
        time = item.get("time", "N/A")
        output.append(f"{username:<20} {category:<25} {time:<20}")
    
    output.append("=" * 60)
    return "\n".join(output)

def format_ranking(items):
    if not items:
        return "暂无排行榜数据"
    
    output = []
    output.append("=" * 70)
    output.append("青少年CTF练习场 - 排行榜 TOP 20")
    output.append("=" * 70)
    output.append(f"{'排名':<6} {'用户名':<25} {'积分':<10} {'等级':<6}")
    output.append("-" * 70)
    
    for item in items:
        grade = item.get("grade", "N/A")
        username = item.get("username", "N/A")
        score = item.get("score", "N/A")
        level = item.get("level", "N/A")
        output.append(f"{grade:<6} {username:<25} {score:<10} Lv.{level}")
    
    output.append("=" * 70)
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="青少年CTF练习场动态查询工具")
    parser.add_argument("action", choices=["ranking", "dynamic", "all"], 
                        help="ranking: 获取排行榜 | dynamic: 获取解题动态 | all: 获取全部")
    parser.add_argument("-n", "--number", type=int, default=10, 
                        help="获取解题动态的数量(默认10条，0表示全部)")
    
    args = parser.parse_args()
    
    if args.action == "ranking":
        items = get_ranking()
        print(format_ranking(items))
    elif args.action == "dynamic":
        items = get_answer_info(args.number)
        print(format_answer_info(items))
    elif args.action == "all":
        print("\n")
        ranking_items = get_ranking()
        print(format_ranking(ranking_items))
        print("\n")
        dynamic_items = get_answer_info(args.number)
        print(format_answer_info(dynamic_items))

if __name__ == "__main__":
    main()
