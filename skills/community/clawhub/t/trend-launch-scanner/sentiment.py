#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场情绪指标系统
获取大盘状态、板块热度、涨跌停数量
"""
import requests
import json
import time
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("C:/Users/Administrator/.qclaw/workspace-ag01/data/trend_scan")


def get_market_breadth():
    """
    获取大盘涨跌家数（市场宽度）
    """
    try:
        # 东方财富市场概况接口
        url = "https://push2.eastmoney.com/api/qt/stock/get"
        params = {
            "secid": "1.000001",  # 上证指数
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
            "ut": "fa5fd1943c7b386f172d6893dbfba10b"
        }
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        
        if data.get("data"):
            d = data["data"]
            return {
                "index_name": d.get("f14", "上证指数"),
                "price": d.get("f2", 0),
                "change_pct": d.get("f3", 0),
                "volume": d.get("f5", 0),
                "up_count": d.get("f15", 0),  # 上涨家数
                "down_count": d.get("f16", 0),  # 下跌家数
                "hold_count": d.get("f17", 0),  # 平盘家数
            }
    except Exception as e:
        print(f"获取市场宽度失败: {e}")
    
    return None


def get_limit_up_count():
    """
    获取涨跌停数量
    """
    try:
        # 涨停股接口
        url = "https://push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": 1,
            "pz": 1000,
            "po": 1,
            "np": 1,
            "fltt": 2,
            "invt": 2,
            "fid": "f3",
            "fs": "m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23",
            "fields": "f12,f14,f3,f62",
            "ut": "fa5fd1943c7b386f172d6893dbfba10b"
        }
        r = requests.get(url, params=params, timeout=15)
        data = r.json()
        
        up_count = 0
        down_count = 0
        
        if data.get("data") and data["data"].get("diff"):
            for item in data["data"]["diff"]:
                change = item.get("f3", 0)
                if change >= 9.9:  # 涨停（接近10%）
                    up_count += 1
                elif change <= -9.9:  # 跌停
                    down_count += 1
        
        return {"up": up_count, "down": down_count}
    except Exception as e:
        print(f"获取涨跌停失败: {e}")
        return {"up": 0, "down": 0}


def get_sector_performance():
    """
    获取行业板块表现
    """
    try:
        # 东方财富行业板块接口
        url = "https://push2.eastmoney.com/api/qt/clist/get"
        params = {
            "pn": 1,
            "pz": 20,
            "po": 1,
            "np": 1,
            "fltt": 2,
            "invt": 2,
            "fid": "f3",
            "fs": "m:90+t:2+f:!50,m:90+t:3+f:!50,m:90+t:4+f:!50,m:90+t:9+f:!50",
            "fields": "f12,f14,f3,f4,f8",
            "ut": "fa5fd1943c7b386f172d6893dbfba10b"
        }
        r = requests.get(url, params=params, timeout=15)
        data = r.json()
        
        sectors = []
        if data.get("data") and data["data"].get("diff"):
            for item in data["data"]["diff"][:10]:  # 取前10
                sectors.append({
                    "code": item.get("f12", ""),
                    "name": item.get("f14", ""),
                    "change_pct": item.get("f3", 0),
                    "volume": item.get("f8", 0),
                })
        
        return sectors
    except Exception as e:
        print(f"获取板块表现失败: {e}")
        return []


def get_market_sentiment():
    """
    综合市场情绪
    """
    print("获取市场情绪数据...")
    
    # 获取主要指数
    indices = []
    index_codes = [
        ("1.000001", "上证指数"),
        ("0.399001", "深证成指"),
        ("0.399006", "创业板指"),
        ("1.000016", "沪深300"),
    ]
    
    for secid, name in index_codes:
        try:
            url = "https://push2.eastmoney.com/api/qt/stock/get"
            params = {
                "secid": secid,
                "fields": "f14,f2,f3",
                "ut": "fa5fd1943c7b386f172d6893dbfba10b"
            }
            r = requests.get(url, params=params, timeout=5)
            data = r.json()
            
            if data.get("data"):
                indices.append({
                    "name": data["data"].get("f14", name),
                    "price": data["data"].get("f2", 0),
                    "change_pct": data["data"].get("f3", 0),
                })
            time.sleep(0.3)
        except:
            pass
    
    # 获取涨跌停数量
    limit_up = get_limit_up_count()
    
    # 获取板块表现
    sectors = get_sector_performance()
    
    # 综合情绪判断
    sentiment = "neutral"
    sentiment_desc = "中性"
    
    if indices:
        avg_change = sum(i["change_pct"] for i in indices) / len(indices)
        
        if avg_change > 1.5 and limit_up["up"] > 50:
            sentiment = "bullish"
            sentiment_desc = "强势"
        elif avg_change > 0.5 and limit_up["up"] > 30:
            sentiment = "positive"
            sentiment_desc = "偏强"
        elif avg_change < -1.5 and limit_up["down"] > 50:
            sentiment = "bearish"
            sentiment_desc = "弱势"
        elif avg_change < -0.5 and limit_up["down"] > 30:
            sentiment = "negative"
            sentiment_desc = "偏弱"
    
    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "indices": indices,
        "limit_up": limit_up,
        "top_sectors": sectors,
        "sentiment": sentiment,
        "sentiment_desc": sentiment_desc,
    }


def format_sentiment_message(sentiment_data):
    """格式化情绪消息"""
    lines = []
    
    lines.append("📊 市场情绪")
    lines.append(f"{sentiment_data['time']}")
    lines.append("──────────────")
    lines.append("")
    
    # 指数表现
    lines.append("【主要指数】")
    for idx in sentiment_data["indices"]:
        change = idx["change_pct"]
        arrow = "▲" if change >= 0 else "▼"
        lines.append(f"  {idx['name']:<8} {arrow}{abs(change):.2f}%")
    lines.append("")
    
    # 涨跌停
    lines.append("【涨跌停】")
    lines.append(f"  涨停 {sentiment_data['limit_up']['up']} 只")
    lines.append(f"  跌停 {sentiment_data['limit_up']['down']} 只")
    lines.append("")
    
    # 热门板块
    if sentiment_data["top_sectors"]:
        lines.append("【热门板块】")
        for i, sector in enumerate(sentiment_data["top_sectors"][:5]):
            change = sector["change_pct"]
            arrow = "▲" if change >= 0 else "▼"
            lines.append(f"  {i+1}. {sector['name']} {arrow}{abs(change):.1f}%")
        lines.append("")
    
    # 情绪判断
    emoji = "🟢" if sentiment_data["sentiment"] in ["bullish", "positive"] else \
            "🔴" if sentiment_data["sentiment"] in ["bearish", "negative"] else "🟡"
    lines.append(f"{emoji} 市场情绪: {sentiment_data['sentiment_desc']}")
    
    return "\n".join(lines)


if __name__ == "__main__":
    print("市场情绪系统测试")
    print("=" * 50)
    
    sentiment = get_market_sentiment()
    print()
    print(format_sentiment_message(sentiment))
