#!/usr/bin/env python3
"""
钢材价格抓取脚本 - 浏览器自动化方案
支持：我的钢铁网、兰格钢铁网
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# 价格数据文件
PRICE_FILE = DATA_DIR / "prices.json"

def run_browser_command(cmd: list, timeout: int = 60) -> tuple:
    """运行 browser 命令"""
    full_cmd = ["agent-browser"] + cmd
    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except Exception as e:
        return -1, "", str(e)


def scrape_mysteel(steel_type: str, region: str) -> Optional[Dict]:
    """
    抓取我的钢铁网价格
    
    使用搜索功能查找具体品种和地区的价格
    """
    # 构建搜索关键词
    search_keyword = f"{region}{steel_type}价格"
    url = f"https://search.mysteel.com/search?keyword={search_keyword}"
    
    print(f"正在抓取: 我的钢铁网 {steel_type} {region}")
    
    session_name = f"mysteel_{int(time.time())}"
    
    try:
        # 打开搜索页面
        ret, _, err = run_browser_command([
            "--session-name", session_name,
            "open", url
        ])
        if ret != 0:
            return {"source": "mysteel", "type": steel_type, "region": region,
                    "price": None, "error": f"打开页面失败: {err}"}
        
        time.sleep(3)
        run_browser_command(["--session-name", session_name, "wait", "--load", "networkidle"])
        
        # 获取页面内容
        ret, content, err = run_browser_command([
            "--session-name", session_name,
            "get", "text", "body"
        ])
        
        # 关闭 session
        run_browser_command(["--session-name", session_name, "close"])
        
        if ret != 0:
            return {"source": "mysteel", "type": steel_type, "region": region,
                    "price": None, "error": f"获取内容失败: {err}"}
        
        return parse_mysteel_content(content, steel_type, region)
        
    except Exception as e:
        run_browser_command(["--session-name", session_name, "close"])
        return {"source": "mysteel", "type": steel_type, "region": region,
                "price": None, "error": str(e)}


def parse_mysteel_content(content: str, steel_type: str, region: str) -> Dict:
    """解析我的钢铁网页面内容"""
    lines = content.split('\n')
    
    # 简单解析：查找包含价格数字的行
    prices = []
    for line in lines:
        line = line.strip()
        # 查找类似 "3850" 或 "3,850" 的价格格式
        import re
        matches = re.findall(r'(\d{3,4})', line)
        for m in matches:
            price = int(m)
            if 2000 <= price <= 8000:  # 合理的价格范围
                prices.append(price)
    
    if prices:
        avg_price = sum(prices) / len(prices)
        return {
            "source": "mysteel",
            "type": steel_type,
            "region": region,
            "price": round(avg_price, 2),
            "unit": "元/吨",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().isoformat(),
            "note": "从我的钢铁网抓取"
        }
    
    return {
        "source": "mysteel",
        "type": steel_type,
        "region": region,
        "price": None,
        "error": "未找到价格数据",
        "date": datetime.now().strftime("%Y-%m-%d"),
    }


def scrape_zhaogang(steel_type: str, region: str) -> Optional[Dict]:
    """
    抓取找钢网价格
    
    网站: https://www.zhaogang.com/
    价格页面使用行情接口
    """
    # 找钢网行情页面
    url = "https://www.zhaogang.com/market"
    
    print(f"正在抓取: 找钢网 {steel_type} {region}")
    
    session_name = f"zhaogang_{int(time.time())}"
    
    try:
        # 打开页面
        ret, _, err = run_browser_command([
            "--session-name", session_name,
            "open", url
        ])
        if ret != 0:
            return {"source": "zhaogang", "type": steel_type, "region": region,
                    "price": None, "error": f"打开页面失败: {err}"}
        
        time.sleep(4)
        run_browser_command(["--session-name", session_name, "wait", "--load", "networkidle"])
        
        # 获取内容
        ret, content, err = run_browser_command([
            "--session-name", session_name,
            "get", "text", "body"
        ])
        
        run_browser_command(["--session-name", session_name, "close"])
        
        if ret != 0:
            return {"source": "zhaogang", "type": steel_type, "region": region,
                    "price": None, "error": f"获取内容失败: {err}"}
        
        return parse_zhaogang_content(content, steel_type, region)
        
    except Exception as e:
        run_browser_command(["--session-name", session_name, "close"])
        return {"source": "zhaogang", "type": steel_type, "region": region,
                "price": None, "error": str(e)}


def parse_zhaogang_content(content: str, steel_type: str, region: str) -> Dict:
    """解析找钢网页面内容"""
    import re
    
    lines = content.split('\n')
    prices = []
    
    for line in lines:
        line = line.strip()
        matches = re.findall(r'(\d{3,4})', line)
        for m in matches:
            price = int(m)
            if 3000 <= price <= 5500:
                prices.append(price)
    
    if prices:
        prices.sort()
        median_price = prices[len(prices) // 2]
        return {
            "source": "zhaogang",
            "type": steel_type,
            "region": region,
            "price": median_price,
            "unit": "元/吨",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().isoformat(),
            "note": "从找钢网抓取"
        }
    
    return {
        "source": "zhaogang",
        "type": steel_type,
        "region": region,
        "price": None,
        "error": "未找到价格数据",
        "date": datetime.now().strftime("%Y-%m-%d"),
    }





def parse_lange_content(content: str, steel_type: str, region: str) -> Dict:
    """解析兰格钢铁网页面内容"""
    lines = content.split('\n')
    
    prices = []
    import re
    for line in lines:
        line = line.strip()
        matches = re.findall(r'(\d{3,4})', line)
        for m in matches:
            price = int(m)
            if 2000 <= price <= 8000:
                prices.append(price)
    
    if prices:
        avg_price = sum(prices) / len(prices)
        return {
            "source": "lange",
            "type": steel_type,
            "region": region,
            "price": round(avg_price, 2),
            "unit": "元/吨",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().isoformat(),
            "note": "从兰格钢铁网抓取"
        }
    
    return {
        "source": "lange",
        "type": steel_type,
        "region": region,
        "price": None,
        "error": "未找到价格数据",
        "date": datetime.now().strftime("%Y-%m-%d"),
    }


def load_prices() -> List[Dict]:
    """加载历史价格数据"""
    if PRICE_FILE.exists():
        with open(PRICE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_prices(data: List[Dict]):
    """保存价格数据"""
    with open(PRICE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def query_price(source: str, steel_type: str, region: str, cache_hours: int = 2) -> Optional[Dict]:
    """
    查询价格（优先使用缓存）
    
    Args:
        source: 数据源 (mysteel/lange)
        steel_type: 钢材品种
        region: 地区
        cache_hours: 缓存有效期（小时）
    """
    # 检查缓存
    prices = load_prices()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 查找今日缓存
    for p in prices:
        if (p.get("source") == source and 
            p.get("type") == steel_type and 
            p.get("region") == region and
            p.get("date") == today):
            # 检查缓存时间
            timestamp = p.get("timestamp", "")
            if timestamp:
                try:
                    from datetime import datetime as dt
                    cached_time = dt.fromisoformat(timestamp)
                    elapsed = (dt.now() - cached_time).total_seconds() / 3600
                    if elapsed < cache_hours:
                        print(f"使用缓存数据 (缓存 {elapsed:.1f} 小时)")
                        return p
                except:
                    pass
    
    # 抓取新数据
    if source == "mysteel":
        data = scrape_mysteel(steel_type, region)
    elif source == "zhaogang":
        data = scrape_zhaogang(steel_type, region)
    else:
        return None
    
    # 保存到缓存
    if data and data.get("price"):
        # 删除旧记录
        prices = [p for p in prices if not (
            p.get("source") == source and 
            p.get("type") == steel_type and 
            p.get("region") == region and
            p.get("date") == today
        )]
        prices.append(data)
        save_prices(prices)
    
    return data


def list_supported_types():
    """列出支持的钢材品种"""
    types = {
        "mysteel": ["螺纹钢", "热轧板卷", "冷轧板卷", "中厚板", "H型钢", "角钢", "槽钢", "工字钢"],
        "lange": ["螺纹钢", "热轧板卷", "冷轧板卷", "中厚板", "H型钢", "角钢", "槽钢", "工字钢"]
    }
    
    print("支持的钢材品种:")
    for source, type_list in types.items():
        print(f"\n[{source}]")
        for t in type_list:
            print(f"  - {t}")
    
    regions = ["唐山", "上海", "北京", "天津", "广州", "杭州", "南京", "武汉", "重庆", "西安", "沈阳"]
    print("\n支持的地区:")
    for r in regions:
        print(f"  - {r}")


def main():
    parser = argparse.ArgumentParser(description="钢材价格抓取工具")
    parser.add_argument("--source", choices=["mysteel", "zhaogang", "all"], default="zhaogang",
                       help="数据源")
    parser.add_argument("--type", default="螺纹钢", help="钢材品种")
    parser.add_argument("--region", default="唐山", help="地区")
    parser.add_argument("--list-types", action="store_true", help="列出支持的品种")
    parser.add_argument("--no-cache", action="store_true", help="不使用缓存")
    
    args = parser.parse_args()
    
    if args.list_types:
        list_supported_types()
        return
    
    cache_hours = 0 if args.no_cache else 2
    
    if args.source == "all":
        sources = ["zhaogang", "mysteel"]
    else:
        sources = [args.source]
    
    print(f"查询: {args.type} {args.region}")
    print("-" * 40)
    
    for source in sources:
        result = query_price(source, args.type, args.region, cache_hours)
        if result:
            print(f"\n[{source}]")
            if result.get("price"):
                print(f"  价格: {result['price']} {result['unit']}")
                print(f"  日期: {result['date']}")
                if result.get("note"):
                    print(f"  备注: {result['note']}")
            else:
                print(f"  错误: {result.get('error', '未知错误')}")
        else:
            print(f"\n[{source}] 抓取失败")


if __name__ == "__main__":
    main()
