#!/usr/bin/env python3
"""
钢材现货价格查询脚本
支持：我的钢铁网、兰格钢铁网
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Dict, List
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# 缓存文件
CACHE_FILE = DATA_DIR / "price_cache.json"

# 数据源配置
SOURCES = {
    "mysteel": {
        "name": "我的钢铁网",
        "base_url": "https://www.mysteel.com",
        "price_url": "https://list1.mysteel.com/market/p-831-----010101-0-010102-------1.html"
    },
    "lange": {
        "name": "兰格钢铁网",
        "base_url": "https://www.lgmi.com",
        "price_url": "https://www.lgmi.com/market/"
    }
}

# 品种代码映射（我的钢铁网）
STEEL_TYPES = {
    "螺纹钢": "010101",
    "热轧板卷": "010102",
    "冷轧板卷": "010103",
    "中厚板": "010104",
    "H型钢": "010105",
    "无缝钢管": "010106",
    "焊管": "010107",
    "角钢": "010108",
    "槽钢": "010109",
    "工字钢": "010110"
}

# 地区代码映射
REGIONS = {
    "北京": "110000",
    "天津": "120000",
    "河北": "130000",
    "唐山": "130200",
    "石家庄": "130100",
    "邯郸": "130400",
    "山西": "140000",
    "内蒙古": "150000",
    "辽宁": "210000",
    "沈阳": "210100",
    "大连": "210200",
    "吉林": "220000",
    "黑龙江": "230000",
    "上海": "310000",
    "江苏": "320000",
    "南京": "320100",
    "苏州": "320500",
    "无锡": "320200",
    "浙江": "330000",
    "杭州": "330100",
    "宁波": "330200",
    "安徽": "340000",
    "福建": "350000",
    "江西": "360000",
    "山东": "370000",
    "济南": "370100",
    "青岛": "370200",
    "河南": "410000",
    "郑州": "410100",
    "湖北": "420000",
    "武汉": "420100",
    "湖南": "430000",
    "广东": "440000",
    "广州": "440100",
    "深圳": "440300",
    "广西": "450000",
    "海南": "460000",
    "重庆": "500000",
    "四川": "510000",
    "成都": "510100",
    "贵州": "520000",
    "云南": "530000",
    "西藏": "540000",
    "陕西": "610000",
    "西安": "610100",
    "甘肃": "620000",
    "青海": "630000",
    "宁夏": "640000",
    "新疆": "650000"
}


def get_cache() -> Dict:
    """读取缓存数据"""
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(data: Dict):
    """保存缓存数据"""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_mysteel_price(steel_type: str, region: Optional[str] = None) -> List[Dict]:
    """
    从我的钢铁网抓取价格数据
    注：实际实现需要根据网站结构调整选择器
    """
    results = []
    
    type_code = STEEL_TYPES.get(steel_type)
    if not type_code:
        print(f"未找到品种: {steel_type}", file=sys.stderr)
        return results
    
    region_code = REGIONS.get(region) if region else ""
    
    # 构造URL（根据实际网站结构调整）
    url = f"https://list1.mysteel.com/market/p-831-----{type_code}-{region_code}-010102-------1.html"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 这里需要根据实际网页结构调整解析逻辑
        # 示例：查找价格表格
        price_table = soup.find("table", class_="market-table")
        if price_table:
            rows = price_table.find_all("tr")[1:]  # 跳过表头
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 4:
                    results.append({
                        "region": cols[0].text.strip(),
                        "type": cols[1].text.strip(),
                        "price": cols[2].text.strip(),
                        "change": cols[3].text.strip(),
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "source": "mysteel"
                    })
    except Exception as e:
        print(f"抓取失败: {e}", file=sys.stderr)
    
    return results


def fetch_lange_price(steel_type: str, region: Optional[str] = None) -> List[Dict]:
    """
    从兰格钢铁网抓取价格数据
    注：实际实现需要根据网站结构调整选择器
    """
    results = []
    
    url = "https://www.lgmi.com/market/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        # 实际实现需要根据兰格网的API或页面结构调整
        # 这里为示例结构
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 解析逻辑待实现
        # 示例占位
        pass
        
    except Exception as e:
        print(f"抓取失败: {e}", file=sys.stderr)
    
    return results


def query_price(source: str, steel_type: str, region: Optional[str] = None, use_cache: bool = True) -> List[Dict]:
    """查询价格（优先使用缓存）"""
    
    cache_key = f"{source}_{steel_type}_{region or 'all'}"
    
    if use_cache:
        cache = get_cache()
        cached_data = cache.get(cache_key)
        if cached_data:
            cache_time = datetime.fromisoformat(cached_data.get("timestamp", "1970-01-01"))
            # 缓存有效期2小时
            if (datetime.now() - cache_time).total_seconds() < 7200:
                return cached_data.get("data", [])
    
    # 抓取新数据
    if source == "mysteel":
        results = fetch_mysteel_price(steel_type, region)
    elif source == "lange":
        results = fetch_lange_price(steel_type, region)
    else:
        print(f"未知数据源: {source}", file=sys.stderr)
        return []
    
    # 更新缓存
    cache = get_cache()
    cache[cache_key] = {
        "timestamp": datetime.now().isoformat(),
        "data": results
    }
    save_cache(cache)
    
    return results


def format_output(results: List[Dict]) -> str:
    """格式化输出结果"""
    if not results:
        return "暂无数据"
    
    lines = []
    lines.append(f"{'地区':<10} {'品种':<10} {'价格':<10} {'涨跌':<8} {'日期':<12}")
    lines.append("-" * 55)
    
    for item in results:
        lines.append(f"{item.get('region', '-'):<10} {item.get('type', '-'):<10} "
                    f"{item.get('price', '-'):<10} {item.get('change', '-'):<8} "
                    f"{item.get('date', '-'):<12}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="钢材现货价格查询")
    parser.add_argument("--source", choices=["mysteel", "lange"], default="mysteel",
                        help="数据源")
    parser.add_argument("--type", required=True, help="钢材品种")
    parser.add_argument("--region", help="地区")
    parser.add_argument("--no-cache", action="store_true", help="不使用缓存")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    
    args = parser.parse_args()
    
    # 查询价格
    results = query_price(
        source=args.source,
        steel_type=args.type,
        region=args.region,
        use_cache=not args.no_cache
    )
    
    # 输出结果
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_output(results))


if __name__ == "__main__":
    main()
