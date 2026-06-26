#!/usr/bin/env python3
"""
Shopping Price Checker - Safe Mode
Uses web_search to gather public price information only.

⚠️ COMPLIANCE NOTICE:
This script does NOT perform automated scraping. It uses search engine APIs
to retrieve publicly indexed information, similar to a manual user searching
on Google/Bing/DuckDuckGo.
"""

import sys
import json
from datetime import datetime
from typing import List, Dict, Optional


class ProductInfo:
    """Represents a product info item from search results."""
    
    def __init__(self, platform: str, title: str, price_str: str = "",
                 url: str = "", snippet: str = "", 
                 estimated_price: float = None):
        self.platform = platform
        self.title = title
        self.price_str = price_str
        self.estimated_price = estimated_price
        self.url = url
        self.snippet = snippet
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'platform': self.platform,
            'title': self.title,
            'price_str': self.price_str,
            'estimated_price': self.estimated_price,
            'url': self.url,
            'snippet': self.snippet,
            'created_at': self.created_at.isoformat()
        }


class PriceChecker:
    """
    Safe price comparison using search engine results only.
    
    NO DIRECT PLATFORM ACCESS:
    - No HTTP requests to shopping sites
    - No JavaScript execution
    - No cookie manipulation
    - No login attempts
    - Only uses search API results
    """
    
    PLATFORM_MAPPING = {
        'jd': {'name': '京东', 'site': 'jd.com'},
        'tmall': {'name': '天猫', 'site': 'tmall.com'},
        'taobao': {'name': '淘宝', 'site': 'taobao.com'},
        'pdd': {'name': '拼多多', 'site': 'pinduoduo.com'},
        '1688': {'name': '1688', 'site': '1688.com'},
        'suning': {'name': '苏宁易购', 'site': 'suning.com'},
        'yiwugou': {'name': '义乌购', 'site': 'yiwugou.com'},
        'vipshop': {'name': '唯品会', 'site': 'vipshop.com'}
    }
    
    DEFAULT_PLATFORMS = ['jd', 'tmall', 'taobao', 'pdd']
    
    def __init__(self):
        self.results: List[ProductInfo] = []
        self.search_queries_used = []
    
    def search_public_info(self, query: str, platforms: List[str] = None, 
                          max_results_per_platform: int = 5):
        """
        Search for product info via search engine API.
        
        This is equivalent to manually searching on:
        web_search(query="iPhone site:jd.com")
        web_search(query="iPhone site:tmall.com")
        ... etc
        """
        if platforms is None:
            platforms = self.DEFAULT_PLATFORMS
        
        print(f"\n🔍 搜索商品：{query}")
        print(f"   平台：{', '.join([self.PLATFORM_MAPPING[p]['name'] for p in platforms])}")
        print(f"   ⚠️ 仅使用搜索引擎公开数据\n")
        
        # Build combined search query
        site_operators = [f"site:{self.PLATFORM_MAPPING[p]['site']}" for p in platforms]
        combined_query = f"{query} {' OR '.join(site_operators)}"
        
        print(f"📝 搜索查询：{combined_query}\n")
        
        # In actual implementation, this would call:
        # result = web_search(query=combined_query, count=20)
        # But we can't call tools here, so structure data for the agent to use
        
        self.search_queries_used.append(combined_query)
        
        # Placeholder: The agent will fill in real search results
        # This is just the structure
        return {
            'query': combined_query,
            'platforms': platforms,
            'max_results': max_results_per_platform,
            'instructions': "Call web_search() with the above query to get real data"
        }
    
    def extract_from_search_result(self, search_result_text: str) -> List[ProductInfo]:
        """
        Parse text from search results to extract product info.
        
        Focuses only on what's visible in search snippets:
        - Titles
        - Prices shown in snippets  
        - URLs
        - Short descriptions
        """
        products = []
        
        # This would parse the actual search result text
        # For now, returns empty list as placeholder
        # Real implementation would use regex/parsing on search_result_text
        
        return products
    
    def generate_report(self, products: List[ProductInfo], query: str) -> str:
        """Generate markdown report from collected product info."""
        
        if not products:
            return """
❌ **未从搜索结果中找到相关商品信息**

可能原因:
- 该商品在搜索引擎中索引有限
- 关键词不够精确，请尝试更具体的名称
- 某些平台的商品可能未被公开索引

建议:
1. 换用更具体的商品名称
2. 接受这是估算价格，最终核实请去各平台官网
            """
        
        # Sort by price (if available)
        priced_products = [p for p in products if p.estimated_price]
        unpriced_products = [p for p in products if not p.estimated_price]
        
        sorted_products = sorted(priced_products, key=lambda x: x.estimated_price or 999999)
        sorted_products.extend(unpriced_products)
        
        report_lines = [
            f"# 🛒 [{query}] 比价报告",
            f"",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"",
            f"⚠️ **数据来源**: 搜索引擎公开索引信息",
            f"💡 **提示**: 实际购买时请在各平台核实最新价格",
            f""
        ]
        
        # Find cheapest option
        best_deal = sorted_products[0] if sorted_products else None
        
        if best_deal and best_deal.estimated_price:
            report_lines.extend([
                "## 💡 核心结论",
                f"💡 **推荐渠道**: {best_deal.platform} - ¥{best_deal.estimated_price:.2f}",
                ""
            ])
        
        # Summary table
        report_lines.extend([
            "## 📊 价格对比表",
            "",
            "| 排名 | 平台 | 标题片段 | 价格 | 链接 |",
            "|------|------|----------|------|------|"
        ])
        
        for i, product in enumerate(sorted_products[:10], 1):
            platform_name = self.PLATFORM_MAPPING.get(
                self._detect_platform(product.platform), 
                {'name': product.platform}
            )['name']
            
            price_display = f"¥{product.estimated_price:.2f}" if product.estimated_price else "未显示"
            title_snippet = product.title[:30] + "..." if len(product.title) > 30 else product.title
            
            row = f"| {i} | {platform_name} | {title_snippet} | {price_display} | [查看]({product.url}) |"
            report_lines.append(row)
        
        # Detailed analysis
        report_lines.extend([
            "",
            "---",
            "",
            "## 🔍 详细分析"
        ])
        
        for i, product in enumerate(sorted_products[:5], 1):
            platform_name = self.PLATFORM_MAPPING.get(
                self._detect_platform(product.platform),
                {'name': product.platform}
            )['name']
            
            report_lines.extend([
                f"### {i}. {platform_name}",
                f"- **商品**: {product.title}",
                f"- **价格**: ¥{product.estimated_price:.2f} (如果显示)" if product.estimated_price else "- **价格**: 未在摘要中显示",
                f"- **来源**: 搜索引擎索引结果",
                ""
            ])
        
        # Recommendations section
        report_lines.extend([
            "---",
            "",
            "## ✅ 购买建议",
            "",
            "### 重要提醒",
            "1. **核实价格**: 上述价格来自搜索引擎快照，可能与实际页面不同",
            "2. **会员价**: 部分平台会员有额外折扣，需登录后查看",
            "3. **优惠活动**: 促销活动期间价格可能更低",
            "4. **官方渠道**: 高价值商品建议选择官方旗舰店或自营",
            "",
            "### 下一步操作",
            "如需最准确的价格，建议:",
            "1. 点击表格中的链接直接访问各平台",
            "2. 登录后查看实际价格和优惠券",
            "3. 告诉我你看到的价格，我帮你整理最终对比"
        ])
        
        return '\n'.join(report_lines)
    
    def _detect_platform(self, url_or_name: str) -> str:
        """Detect platform code from URL or name."""
        url_or_name = url_or_name.lower()
        
        if 'jd.com' in url_or_name or 'jd.com' in url_or_name:
            return 'jd'
        elif 'tmall.com' in url_or_name:
            return 'tmall'
        elif 'taobao.com' in url_or_name:
            return 'taobao'
        elif 'pinduoduo.com' in url_or_name or 'yangkeduo.com' in url_or_name:
            return 'pdd'
        elif '1688.com' in url_or_name:
            return '1688'
        elif 'suning.com' in url_or_name:
            return 'suning'
        elif 'yiwugou.com' in url_or_name:
            return 'yiwugou'
        elif 'vipshop.com' in url_or_name:
            return 'vipshop'
        
        return ''
    
    def save_to_json(self, products: List[ProductInfo], query: str, 
                    filename: str = None):
        """Save results to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"shopping_compare_{timestamp}.json"
        
        report = self.generate_report(products, query)
        
        data = {
            'query': query,
            'search_method': 'web_search_public_data',
            'compliance_note': 'No automated scraping performed',
            'products': [p.to_dict() for p in products],
            'report': report,
            'generated_at': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filename


def main():
    """CLI entry point for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Safe Shopping Price Checker (Web Search Only)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Compliance Notice:
------------------
This tool uses search engine APIs to gather publicly indexed information.
It does NOT directly access or scrape target websites.

Usage example:
  python price_checker.py "iPhone 15 Pro Max"
        
⚠️ Remember: Verify prices on official platforms before purchasing!
        """
    )
    parser.add_argument('query', help='Product name to search')
    parser.add_argument('--platforms', '-p', 
                       help='Comma-separated platform codes (jd,tmall,taobao,pdd,etc.)')
    parser.add_argument('--output', '-o', help='Output JSON filename')
    
    args = parser.parse_args()
    
    # Initialize checker
    checker = PriceChecker()
    
    # Parse platforms
    platforms = None
    if args.platforms:
        platforms = [p.strip().lower() for p in args.platforms.split(',')]
    
    # Prepare search parameters
    search_params = checker.search_public_info(args.query, platforms)
    
    print("\n📋 搜索参数准备完成:")
    print(f"   Query: {search_params['query']}")
    print(f"   Platforms: {search_params['platforms']}")
    print(f"\n   ⚠️ 实际使用时，Agent 会调用 web_search() API 获取真实数据")
    print(f"   然后解析搜索结果生成比价报告")
    
    # Placeholder: In real usage, the agent handles the web_search call
    # and passes results back to this script for report generation
    
    print("\n✅ 安全模式已启用 - 所有数据来自搜索引擎公开索引")


if __name__ == '__main__':
    main()
