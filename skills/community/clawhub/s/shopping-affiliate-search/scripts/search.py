#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全球购物搜索联盟工具
搜索淘宝/京东/亚马逊等平台商品，自动添加推荐码
"""

import json
import argparse
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

# 配置目录
CONFIG_DIR = Path(__file__).parent.parent / "config"
CONFIG_FILE = CONFIG_DIR / "affiliate_config.json"


class ShoppingAffiliateSearch:
    """购物搜索联盟工具"""
    
    def __init__(self):
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """加载配置"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置
        default_config = {
            "taobao": {
                "pid": "",
                "enabled": True,
                "api_url": "https://api.taobao.com"
            },
            "jd": {
                "union_id": "",
                "enabled": True,
                "api_url": "https://api.jd.com"
            },
            "pdd": {
                "pid": "",
                "enabled": True,
                "api_url": "https://api.pinduoduo.com"
            },
            "amazon": {
                "associate_id": "",
                "enabled": True,
                "api_url": "https://api.amazon.com"
            }
        }
        
        # 保存默认配置
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        
        return default_config
    
    def _save_config(self):
        """保存配置"""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def set_affiliate_id(self, platform: str, affiliate_id: str):
        """设置联盟ID"""
        platform = platform.lower()
        
        if platform == "taobao":
            self.config["taobao"]["pid"] = affiliate_id
        elif platform == "jd":
            self.config["jd"]["union_id"] = affiliate_id
        elif platform == "pdd":
            self.config["pdd"]["pid"] = affiliate_id
        elif platform == "amazon":
            self.config["amazon"]["associate_id"] = affiliate_id
        else:
            raise ValueError(f"不支持的平台: {platform}")
        
        self._save_config()
        print(f"✅ 已设置 {platform} 推荐码: {affiliate_id}")
    
    def search_taobao(self, keyword: str, page: int = 1) -> List[Dict]:
        """搜索淘宝商品"""
        pid = self.config["taobao"]["pid"]
        
        # 构建搜索URL（实际需要调用淘宝API）
        # 这里返回模拟数据
        results = [
            {
                "platform": "淘宝",
                "title": f"{keyword} - 热销爆款",
                "price": "59.00",
                "original_price": "99.00",
                "sales": "5万+",
                "commission_rate": "5%",
                "url": f"https://s.click.taobao.com/t?e=m%3D2%26s%3D{urllib.parse.quote(pid)}%26keyword%3D{urllib.parse.quote(keyword)}",
                "image": "https://img.alicdn.com/example.jpg"
            },
            {
                "platform": "淘宝",
                "title": f"{keyword} - 高性价比",
                "price": "39.00",
                "original_price": "79.00",
                "sales": "3万+",
                "commission_rate": "3%",
                "url": f"https://s.click.taobao.com/t?e=m%3D2%26s%3D{urllib.parse.quote(pid)}%26keyword%3D{urllib.parse.quote(keyword)}",
                "image": "https://img.alicdn.com/example2.jpg"
            }
        ]
        
        return results
    
    def search_jd(self, keyword: str, page: int = 1) -> List[Dict]:
        """搜索京东商品"""
        union_id = self.config["jd"]["union_id"]
        
        results = [
            {
                "platform": "京东",
                "title": f"{keyword} - 自营正品",
                "price": "89.00",
                "original_price": "129.00",
                "sales": "2万+",
                "commission_rate": "2%",
                "url": f"https://union.jd.com/link?u={union_id}&keyword={urllib.parse.quote(keyword)}",
                "image": "https://img14.360buyimg.com/example.jpg"
            }
        ]
        
        return results
    
    def search_pdd(self, keyword: str, page: int = 1) -> List[Dict]:
        """搜索拼多多商品"""
        pid = self.config["pdd"]["pid"]
        
        results = [
            {
                "platform": "拼多多",
                "title": f"{keyword} - 百亿补贴",
                "price": "29.90",
                "original_price": "59.90",
                "sales": "10万+",
                "commission_rate": "10%",
                "url": f"https://mobile.yangkeduo.com/duo_coupon.html?pid={pid}&keyword={urllib.parse.quote(keyword)}",
                "image": "https://img.pddpic.com/example.jpg"
            }
        ]
        
        return results
    
    def search_amazon(self, keyword: str, page: int = 1) -> List[Dict]:
        """搜索亚马逊商品"""
        associate_id = self.config["amazon"]["associate_id"]
        
        results = [
            {
                "platform": "亚马逊",
                "title": f"{keyword} - Best Seller",
                "price": "$29.99",
                "original_price": "$49.99",
                "sales": "10K+",
                "commission_rate": "4%",
                "url": f"https://www.amazon.com/s?k={urllib.parse.quote(keyword)}&tag={associate_id}",
                "image": "https://images-na.ssl-images-amazon.com/example.jpg"
            }
        ]
        
        return results
    
    def search_all(self, keyword: str) -> Dict[str, List[Dict]]:
        """全平台搜索"""
        results = {}
        
        if self.config["taobao"]["pid"]:
            results["淘宝"] = self.search_taobao(keyword)
        
        if self.config["jd"]["union_id"]:
            results["京东"] = self.search_jd(keyword)
        
        if self.config["pdd"]["pid"]:
            results["拼多多"] = self.search_pdd(keyword)
        
        if self.config["amazon"]["associate_id"]:
            results["亚马逊"] = self.search_amazon(keyword)
        
        return results
    
    def format_results(self, results: Dict[str, List[Dict]]) -> str:
        """格式化输出结果"""
        output = []
        output.append("\n" + "=" * 60)
        output.append("🛒 购物搜索结果（已注入推荐码）")
        output.append("=" * 60)
        
        for platform, items in results.items():
            output.append(f"\n【{platform}】")
            output.append("-" * 60)
            
            for i, item in enumerate(items, 1):
                output.append(f"\n{i}. {item['title']}")
                output.append(f"   💰 价格: {item['price']} (原价: {item['original_price']})")
                output.append(f"   📊 销量: {item['sales']}")
                output.append(f"   💵 佣金: {item['commission_rate']}")
                output.append(f"   🔗 推荐链接: {item['url']}")
        
        output.append("\n" + "=" * 60)
        output.append("💰 分享这些链接，用户购买后你将获得佣金！")
        output.append("=" * 60)
        
        return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="全球购物搜索联盟工具 - 搜索商品并注入推荐码"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 配置命令
    config_parser = subparsers.add_parser("config", help="配置推荐码")
    config_parser.add_argument("--taobao", help="淘宝客PID")
    config_parser.add_argument("--jd", help="京东联盟ID")
    config_parser.add_argument("--pdd", help="拼多多PID")
    config_parser.add_argument("--amazon", help="亚马逊联盟ID")
    
    # 搜索命令
    search_parser = subparsers.add_parser("search", help="搜索商品")
    search_parser.add_argument("keyword", help="搜索关键词")
    search_parser.add_argument("--platform", choices=["taobao", "jd", "pdd", "amazon", "all"], 
                              default="all", help="搜索平台")
    search_parser.add_argument("--page", type=int, default=1, help="页码")
    
    args = parser.parse_args()
    
    searcher = ShoppingAffiliateSearch()
    
    if args.command == "config":
        if args.taobao:
            searcher.set_affiliate_id("taobao", args.taobao)
        if args.jd:
            searcher.set_affiliate_id("jd", args.jd)
        if args.pdd:
            searcher.set_affiliate_id("pdd", args.pdd)
        if args.amazon:
            searcher.set_affiliate_id("amazon", args.amazon)
        
        if not any([args.taobao, args.jd, args.pdd, args.amazon]):
            print("当前配置:")
            print(json.dumps(searcher.config, ensure_ascii=False, indent=2))
    
    elif args.command == "search":
        if args.platform == "all":
            results = searcher.search_all(args.keyword)
        elif args.platform == "taobao":
            results = {"淘宝": searcher.search_taobao(args.keyword, args.page)}
        elif args.platform == "jd":
            results = {"京东": searcher.search_jd(args.keyword, args.page)}
        elif args.platform == "pdd":
            results = {"拼多多": searcher.search_pdd(args.keyword, args.page)}
        elif args.platform == "amazon":
            results = {"亚马逊": searcher.search_amazon(args.keyword, args.page)}
        
        print(searcher.format_results(results))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()