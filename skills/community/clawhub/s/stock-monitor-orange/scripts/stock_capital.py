#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stock Monitor - 资金流向、龙虎榜、北向资金功能扩展
"""

import json
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# ============ 资金流向功能 ============

def get_capital_flow(code: str) -> Optional[Dict]:
    """
    获取个股资金流向 (东方财富)
    """
    try:
        # 判断市场
        if code.startswith("6"):
            secid = f"1.{code}"
        elif code.startswith(("0", "3")):
            secid = f"0.{code}"
        else:
            return None
        
        url = f"http://push2ex.eastmoney.com/getTopicZDFenBu?ut=7eea3edcaed734bea9cbfc24409ed989&dession=01&mession=01&vessionName=&SECID={secid}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        req.add_header('Referer', 'https://www.eastmoney.com/')
        
        with urllib.request.urlopen(req, timeout=10) as r:
            content = r.read().decode('utf-8', errors='ignore')
            data = json.loads(content)
            
            if data.get("data"):
                fenbu = data["data"]
                return {
                    "code": code,
                    "net_inflow_main": fenbu.get("net_inflow_main", 0),  # 主力净流入
                    "net_inflow_huge": fenbu.get("net_inflow_huge", 0),  # 超大单净流入
                    "net_inflow_big": fenbu.get("net_inflow_big", 0),    # 大单净流入
                    "net_inflow_mid": fenbu.get("net_inflow_mid", 0),     # 中单净流入
                    "net_inflow_small": fenbu.get("net_inflow_small", 0), # 小单净流入
                }
    except Exception as e:
        print(f"获取资金流向失败: {code}, {e}")
    
    return None

def get_sector_capital_flow(sector_name: str) -> Optional[Dict]:
    """
    获取板块资金流向
    """
    sector_map = {
        "芯片": "bk0455",
        "新能源": "bk0493",
        "医药": "bk0465",
        "白酒": "bk0437",
        "银行": "bk0435",
        "房地产": "bk0451",
        "军工": "bk0436",
    }
    
    bk_code = sector_map.get(sector_name)
    if not bk_code:
        return None
    
    try:
        url = f"http://push2ex.eastmoney.com/getTopicZDFenBu?ut=7eea3edcaed734bea9cbfc24409ed989&dession=01&mession=01&vessionName=&SECID=90.{bk_code}"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        req.add_header('Referer', 'https://www.eastmoney.com/')
        
        with urllib.request.urlopen(req, timeout=10) as r:
            content = r.read().decode('utf-8', errors='ignore')
            data = json.loads(content)
            
            if data.get("data"):
                return {
                    "sector": sector_name,
                    "data": data["data"]
                }
    except Exception as e:
        print(f"获取板块资金流向失败: {sector_name}, {e}")
    
    return None

def format_capital_flow(data: Dict, stock_name: str = "") -> str:
    """格式化资金流向报告"""
    if not data:
        return "暂无资金流向数据"
    
    lines = [f"💰 资金流向 - {stock_name or data.get('code', '')}", "-" * 40]
    
    # 格式化数值（转为亿/万元）
    def fmt_money(val):
        if val is None:
            return "--"
        val = float(val)
        if abs(val) >= 100000000:
            return f"{val/100000000:.2f}亿"
        elif abs(val) >= 10000:
            return f"{val/10000:.2f}万"
        else:
            return f"{val:.0f}元"
    
    main = data.get("net_inflow_main", 0) or 0
    huge = data.get("net_inflow_huge", 0) or 0
    big = data.get("net_inflow_big", 0) or 0
    mid = data.get("net_inflow_mid", 0) or 0
    small = data.get("net_inflow_small", 0) or 0
    
    main_emoji = "🟢" if main > 0 else "🔴"
    
    lines.append(f"{main_emoji} 主力净流入: {fmt_money(main)}")
    lines.append(f"   超大单: {fmt_money(huge)}")
    lines.append(f"   大单:   {fmt_money(big)}")
    lines.append(f"   中单:   {fmt_money(mid)}")
    lines.append(f"   小单:   {fmt_money(small)}")
    
    return "\n".join(lines)


# ============ 龙虎榜功能 ============

def get_longhub_list(date: str = None) -> List[Dict]:
    """
    获取龙虎榜数据 (东方财富)
    """
    if not date:
        date = datetime.now().strftime("%Y%m%d")
    
    # 尝试多个API
    urls = [
        f"http://push2ex.eastmoney.com/getTopicLHBDetail?ut=7eea3edcaed734bea9cbfc24409ed989&dession=01&mession=01&vessionName=&date={date}",
        f"http://push2ex.eastmoney.com/getTopicLongHuList?ut=7eea3edcaed734bea9cbfc24409ed989&dession=01&mession=01&vessionName=&TOP=50&date={date}",
    ]
    
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            req.add_header('Referer', 'https://www.eastmoney.com/')
            
            with urllib.request.urlopen(req, timeout=15) as r:
                content = r.read().decode('utf-8', errors='ignore')
                data = json.loads(content)
                
                result = []
                
                # 尝试解析新API格式
                if data.get("data") and isinstance(data["data"], list):
                    for item in data["data"]:
                        result.append({
                            "code": item.get("c", ""),
                            "name": item.get("n", ""),
                            "close": item.get("p", 0),
                            "change_pct": item.get("chg", 0),
                            "amount": item.get("amount", 0),
                            "jmr_netbuy": item.get("jmr_netbuy", 0),
                            "broker_netbuy": item.get("broker_netbuy", 0),
                        })
                    if result:
                        return result
                
                # 尝试老API格式
                if data.get("data") and data["data"].get("longhu"):
                    for item in data["data"]["longhu"]:
                        result.append({
                            "code": item.get("c", ""),
                            "name": item.get("n", ""),
                            "close": item.get("p", 0),
                            "change_pct": item.get("chg", 0),
                            "amount": item.get("amount", 0),
                            "jmr_netbuy": item.get("jmr_netbuy", 0),
                            "broker_netbuy": item.get("broker_netbuy", 0),
                        })
                    return result
                    
        except Exception as e:
            print(f"获取龙虎榜尝试失败: {e}")
            continue
    
    # 如果API都失败，返回模拟数据提示用户
    return []

def format_longhub_report(data: List[Dict], date: str = "") -> str:
    """格式化龙虎榜报告"""
    if not data:
        return "暂无龙虎榜数据"
    
    date_str = f"({date[:4]}-{date[4:6]}-{date[6:]})" if date else ""
    
    lines = [f"🐉 龙虎榜 {date_str}", "=" * 60, ""]
    
    # 按机构净买入排序
    sorted_data = sorted(data, key=lambda x: x.get("jmr_netbuy", 0), reverse=True)
    
    for i, item in enumerate(sorted_data[:15], 1):
        name = item.get("name", "")
        code = item.get("code", "")
        close = item.get("close", 0)
        change_pct = item.get("change_pct", 0)
        jmr = item.get("jmr_netbuy", 0)
        broker = item.get("broker_netbuy", 0)
        
        change_emoji = "🟢" if change_pct > 0 else "🔴" if change_pct < 0 else "🟡"
        
        # 格式化金额
        def fmt_amount(val):
            if abs(val) >= 100000000:
                return f"{val/100000000:.2f}亿"
            elif abs(val) >= 10000:
                return f"{val/10000:.2f}万"
            else:
                return f"{val:.0f}"
        
        jmr_emoji = "🟢" if jmr > 0 else "🔴"
        
        lines.append(f"{i}. {name} ({code})")
        lines.append(f"   {change_emoji} 收盘: {close:.2f} ({change_pct:+.2f}%)")
        lines.append(f"   🏛️ 机构净买入: {jmr_emoji} {fmt_amount(jmr)}")
        lines.append(f"   🏢 营业部净买入: {fmt_amount(broker)}")
        lines.append("")
    
    # 统计
    total_jmr = sum(x.get("jmr_netbuy", 0) for x in data)
    up_count = sum(1 for x in data if x.get("change_pct", 0) > 0)
    down_count = sum(1 for x in data if x.get("change_pct", 0) < 0)
    
    lines.append("=" * 60)
    lines.append(f"📊 统计: 上榜 {len(data)} 只 | 上涨 {up_count} | 下跌 {down_count}")
    lines.append(f"💰 机构净买入总额: {total_jmr/10000:.2f}万")
    
    return "\n".join(lines)


# ============ 北向资金功能 ============

def get_north_money() -> Optional[Dict]:
    """
    获取北向资金流向 (沪股通+深股通)
    """
    try:
        # 沪股通
        url1 = "https://push2.eastmoney.com/api/qt/stock/get?secid=1.000001&fields=f43,f44,f45,f46,f57,f58,f169,f170,f171,f173,f177,f178,f187,f188,f189,f190,f191,f192"
        # 深股通
        url2 = "https://push2.eastmoney.com/api/qt/stock/get?secid=0.399001&fields=f43,f44,f45,f46,f57,f58,f169,f170,f171,f173,f177,f178,f187,f188,f189,f190,f191,f192"
        
        results = {}
        
        for name, url in [("沪股通", url1), ("深股通", url2)]:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                content = r.read().decode('utf-8', errors='ignore')
                data = json.loads(content)
                
                if data.get("data"):
                    d = data["data"]
                    results[name] = {
                        "name": name,
                        "net_inflow": d.get("f45", 0),  # 净流入
                        "buy_amount": d.get("f43", 0),  # 买入额
                        "sell_amount": d.get("f44", 0), # 卖出额
                        "turnover": d.get("f57", 0),    # 成交额
                    }
        
        if results:
            # 合并计算
            total_net = sum(r.get("net_inflow", 0) for r in results.values())
            return {
                "沪股通": results.get("沪股通", {}),
                "深股通": results.get("深股通", {}),
                "total_net_inflow": total_net,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
    except Exception as e:
        print(f"获取北向资金失败: {e}")
    
    return None

def get_north_top_stocks() -> List[Dict]:
    """
    获取北向资金十大成交股
    """
    try:
        url = "https://push2ex.eastmoney.com/getTopicZTPool?ut=7eea3edcaed734bea9cbfc24409ed989&dession=01&mession=01&vessionName=&date=&mkt=2&TYPE=SZ"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        req.add_header('Referer', 'https://www.eastmoney.com/')
        
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read().decode('utf-8', errors='ignore')
            data = json.loads(content)
            
            result = []
            if data.get("data") and data["data"].get("pool"):
                for item in data["data"]["pool"][:10]:
                    result.append({
                        "code": item.get("c", ""),
                        "name": item.get("n", ""),
                        "close": item.get("p", 0),
                        "change_pct": item.get("chg", 0),
                        "net_amount": item.get("net", 0),  # 净买入
                    })
            
            return result
            
    except Exception as e:
        print(f"获取北向资金十大成交股失败: {e}")
    
    return []

def format_north_money_report(data: Dict, top_stocks: List[Dict] = None) -> str:
    """格式化北向资金报告"""
    if not data:
        return "暂无北向资金数据"
    
    lines = ["🇨🇳 北向资金动向", "=" * 50, ""]
    
    total_net = data.get("total_net_inflow", 0)
    total_emoji = "🟢" if total_net > 0 else "🔴"
    
    def fmt_money(val):
        if val is None or val == 0:
            return "0"
        val = float(val)
        if abs(val) >= 100000000:
            return f"{val/100000000:.2f}亿"
        elif abs(val) >= 10000:
            return f"{val/10000:.2f}万"
        else:
            return f"{val:.0f}元"
    
    # 沪股通
    if "沪股通" in data and data["沪股通"]:
        hk = data["沪股通"]
        hk_net = hk.get("net_inflow", 0) or 0
        hk_emoji = "🟢" if hk_net > 0 else "🔴"
        lines.append(f"📈 沪股通: {hk_emoji} 净流入 {fmt_money(hk_net)}")
        lines.append(f"   买入: {fmt_money(hk.get('buy_amount', 0))} | 卖出: {fmt_money(hk.get('sell_amount', 0))}")
        lines.append("")
    
    # 深股通
    if "深股通" in data and data["深股通"]:
        sz = data["深股通"]
        sz_net = sz.get("net_inflow", 0) or 0
        sz_emoji = "🟢" if sz_net > 0 else "🔴"
        lines.append(f"📈 深股通: {sz_emoji} 净流入 {fmt_money(sz_net)}")
        lines.append(f"   买入: {fmt_money(sz.get('buy_amount', 0))} | 卖出: {fmt_money(sz.get('sell_amount', 0))}")
        lines.append("")
    
    # 总计
    lines.append("=" * 50)
    lines.append(f"{total_emoji} 北向资金合计: 净流入 {fmt_money(total_net)}")
    lines.append(f"📅 更新时间: {data.get('time', '')}")
    
    # 十大成交股
    if top_stocks:
        lines.append("")
        lines.append("🇨🇳 十大成交股 (北向资金净买入):")
        lines.append("-" * 40)
        
        sorted_stocks = sorted(top_stocks, key=lambda x: x.get("net_amount", 0), reverse=True)
        
        for i, stock in enumerate(sorted_stocks[:10], 1):
            name = stock.get("name", "")
            code = stock.get("code", "")
            net = stock.get("net_amount", 0)
            change = stock.get("change_pct", 0)
            
            net_emoji = "🟢" if net > 0 else "🔴"
            change_emoji = "🟢" if change > 0 else "🔴" if change < 0 else "🟡"
            
            lines.append(f"{i}. {name} ({code})")
            lines.append(f"   {change_emoji} {change:+.2f}% | {net_emoji} 净买入: {fmt_money(net)}")
    
    return "\n".join(lines)


# ============ CLI 命令 ============

if __name__ == "__main__":
    # 设置UTF-8编码
    import sys
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    
    if len(sys.argv) < 2:
        print("资金/龙虎榜/北向资金 CLI")
        print("Usage: python stock_capital.py <command> [args]")
        print("Commands:")
        print("  capital <code>     - 查询个股资金流向")
        print("  sector <name>      - 查询板块资金流向 (芯片/新能源/医药/白酒/银行/房地产/军工)")
        print("  longhub [date]     - 查询龙虎榜 (date: YYYYMMDD, 默认今天)")
        print("  north              - 查询北向资金")
        print("  north-top          - 查询北向资金十大成交股")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "capital":
        if len(sys.argv) > 2:
            code = sys.argv[2]
            # 获取股票名称
            from stock_monitor import get_stock_quote
            quote = get_stock_quote(code)
            name = quote["name"] if quote else code
            
            data = get_capital_flow(code)
            print(format_capital_flow(data, name))
        else:
            print("用法: capital <code>")
    
    elif cmd == "sector":
        if len(sys.argv) > 2:
            name = sys.argv[2]
            data = get_sector_capital_flow(name)
            if data:
                print(format_capital_flow(data.get("data", {}), name))
            else:
                print(f"未找到板块: {name}")
        else:
            print("用法: sector <板块名称>")
    
    elif cmd == "longhub":
        date = sys.argv[2] if len(sys.argv) > 2 else None
        data = get_longhub_list(date)
        print(format_longhub_report(data, date or datetime.now().strftime("%Y%m%d")))
    
    elif cmd == "north":
        data = get_north_money()
        top_stocks = get_north_top_stocks()
        print(format_north_money_report(data, top_stocks))
    
    elif cmd == "north-top":
        data = get_north_top_stocks()
        if data:
            for i, s in enumerate(data, 1):
                print(f"{i}. {s.get('name')} ({s.get('code')}) - 净买入: {s.get('net_amount', 0)}")
        else:
            print("暂无数据")
    
    else:
        print("未知命令")
