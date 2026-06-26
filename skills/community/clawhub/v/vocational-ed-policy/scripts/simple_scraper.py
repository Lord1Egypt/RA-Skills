#!/usr/bin/env python3
"""
简单的教育部职业教育政策抓取工具
Simple Ministry of Education Vocational Education Policy Scraper

临时解决方案 - 用于框架技能实现完成前
Temporary workaround - before the framework skill is implemented
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
    DEPENDENCIES_OK = True
except ImportError:
    DEPENDENCIES_OK = False
    print("警告: 需要安装 requests 和 beautifulsoup4")
    print("Warning: requests and beautifulsoup4 need to be installed")
    print("运行: pip install requests beautifulsoup4 lxml")


def scrape_moe_voc_ed(days=7):
    """抓取教育部职业教育相关政策 | Scrape MOE vocational education policies"""
    
    if not DEPENDENCIES_OK:
        return {"error": "Missing dependencies", "count": 0, "results": []}
    
    # 计算日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    results = []
    
    try:
        # 抓取首页
        print(f"正在抓取教育部首页... (最近{days}天)")
        url = "https://www.moe.gov.cn/"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 查找包含"职业教育"的链接
        links = soup.find_all('a', href=True)
        for link in links:
            title = link.get('title', '')
            href = link.get('href', '')
            
            # 关键词匹配
            if '职业' in title and ('教育' in title or '培训' in title):
                # 提取日期（从父元素或相邻元素）
                date_element = link.find_previous(['span', 'div'])
                date_str = date_element.get_text(strip=True) if date_element else ''
                
                # 格式化URL
                if href.startswith('/'):
                    full_url = urljoin(url, href)
                else:
                    full_url = href
                
                results.append({
                    'title': title,
                    'url': full_url,
                    'date': date_str,
                    'source': '教育部'
                })
        
    except Exception as e:
        return {"error": str(e), "count": 0, "results": []}
    
    return {
        "count": len(results),
        "results": results[:10],  # 限制返回前10个
        "date_range": f"{start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}"
    }


if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    
    result = scrape_moe_voc_ed(days)
    
    print("\n" + "="*50)
    print("教育部职业教育政策抓取结果")
    print("="*50)
    print(f"时间范围: {result.get('date_range', 'N/A')}")
    print(f"找到文件: {result['count']}")
    print()
    
    if result.get('error'):
        print(f"错误: {result['error']}")
    else:
        for item in result['results']:
            print(f"- {item['title']}")
            print(f"  日期: {item['date']}")
            print(f"  链接: {item['url']}")
            print()
    
    # 保存JSON
    output_file = Path(f"moe_voc_ed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    output_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"结果已保存到: {output_file}")


from urllib.parse import urljoin