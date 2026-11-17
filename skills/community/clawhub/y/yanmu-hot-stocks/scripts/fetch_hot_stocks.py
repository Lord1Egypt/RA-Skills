#!/usr/bin/env python3
"""
研木 — 热门股票获取脚本
根据市场类型动态获取热门股票列表
"""
import sys
import json
import argparse
from typing import List, Dict

# ============ 内置热门股票数据库（课程演示用） ============
FALLBACK_STOCKS = {
    "a-share": [
        {"rank": 1, "name": "宁德时代", "code": "300750.SZ", "desc": "动力电池+储能全球龙头，市占率持续提升"},
        {"rank": 2, "name": "贵州茅台", "code": "600519.SH", "desc": "白酒行业绝对龙头，品牌壁垒深厚"},
        {"rank": 3, "name": "比亚迪", "code": "002594.SZ", "desc": "新能源车+电池一体化龙头"},
    ],
    "hk": [
        {"rank": 1, "name": "腾讯控股", "code": "00700.HK", "desc": "中国互联网科技龙头"},
        {"rank": 2, "name": "美团", "code": "03690.HK", "desc": "本地生活服务龙头"},
        {"rank": 3, "name": "阿里巴巴", "code": "09988.HK", "desc": "电商+云计算双轮驱动"},
    ],
    "us": [
        {"rank": 1, "name": "NVIDIA", "code": "NVDA", "desc": "AI芯片全球龙头"},
        {"rank": 2, "name": "Apple", "code": "AAPL", "desc": "全球消费电子+服务生态龙头"},
        {"rank": 3, "name": "Microsoft", "code": "MSFT", "desc": "云计算+AI平台领导者"},
    ],
}

MARKET_NAMES = {
    "a-share": "A股",
    "hk": "港股",
    "us": "美股",
}

MARKET_ALIASES = {
    "a": "a-share", "a_share": "a-share", "ashare": "a-share",
    "a股": "a-share", "a 股": "a-share",
    "h": "hk", "hk": "hk", "港股": "hk",
    "u": "us", "us": "us", "us stock": "us", "美股": "us",
}


def try_fetch_from_sina(market: str) -> List[Dict]:
    """尝试从新浪财经获取热门股票（A股）"""
    # 在实际课程中，这里可以用 web_fetch 替代
    # 以下为模拟代码结构
    return None


def try_fetch_from_yahoo(market: str) -> List[Dict]:
    """尝试从Yahoo Finance获取热门股票（美股/港股）"""
    return None


def get_hot_stocks(market: str) -> List[Dict]:
    """获取热门股票，按优先级尝试各数据源"""
    market_key = MARKET_ALIASES.get(market.lower(), market)
    
    if market_key not in FALLBACK_STOCKS:
        print(f"❌ 不支持的市场类型: {market}")
        print(f"支持的选项: {', '.join(MARKET_NAMES.keys())}")
        sys.exit(1)
    
    return FALLBACK_STOCKS[market_key]


def format_output(market: str, stocks: List[Dict]) -> str:
    """格式化输出热门股票列表"""
    market_name = MARKET_NAMES.get(market, market)
    lines = [
        f"📊 【热门股票推荐 · {market_name}】\n",
    ]
    for s in stocks:
        medal = ["🥇", "🥈", "🥉"][s["rank"] - 1]
        lines.append(f"{medal} **{s['name']}** (`{s['code']}`) — {s['desc']}")
    
    lines.append(f"\n📌 输入序号或股票代码选择研究标的（或输入 `自定义` 手动输入代码）：")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="热门股票推荐")
    parser.add_argument("--market", "-m", required=True, 
                       choices=["a-share", "hk", "us", "a", "h", "u"],
                       help="市场类型")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text",
                       help="输出格式")
    args = parser.parse_args()
    
    stocks = get_hot_stocks(args.market)
    
    if args.format == "json":
        print(json.dumps({"market": args.market, "stocks": stocks}, ensure_ascii=False, indent=2))
    else:
        print(format_output(args.market, stocks))


if __name__ == "__main__":
    main()
