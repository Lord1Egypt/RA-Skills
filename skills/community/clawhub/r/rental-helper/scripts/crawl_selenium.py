#!/usr/bin/env python3
"""
使用 Selenium 抓取动态网页房源（适用于反爬较强的网站）
用法: python crawl_selenium.py --platform 贝壳 --city 北京 --area 朝阳区

需要先安装:
pip install selenium webdriver-manager
"""

import json
import os
import argparse
import time
from datetime import datetime

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/rental-data")
DATA_FILE = os.path.join(DATA_DIR, "listings.json")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_listings():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_listings(listings):
    ensure_data_dir()
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(listings, f, ensure_ascii=False, indent=2)

def crawl_with_selenium(args):
    """使用Selenium抓取"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
        print("请先安装依赖:")
        print("pip install selenium webdriver-manager")
        return
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
    
    # 启动浏览器
    print("正在启动浏览器...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    listings = []
    
    try:
        # 城市代码
        city_codes = {
            '北京': 'bj', '上海': 'sh', '广州': 'gz', '深圳': 'sz',
            '杭州': 'hz', '南京': 'nj', '成都': 'cd', '武汉': 'wh',
        }
        city_code = city_codes.get(args.city, 'bj')
        
        # 构建URL
        if args.platform in ['贝壳', '链家']:
            url = f"https://{city_code}.ke.com/zufang/"
            if args.area:
                url += f"{args.area}/"
            if args.budget:
                url += f"rp{args.budget}/"
            
            print(f"正在访问: {url}")
            driver.get(url)
            time.sleep(3)  # 等待页面加载
            
            # 滚动页面加载更多
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            
            # 解析房源
            items = driver.find_elements(By.CSS_SELECTOR, '[data-houseid]')
            print(f"找到 {len(items)} 个房源元素")
            
            for i, item in enumerate(items[:args.limit]):
                try:
                    # 提取信息
                    title_elem = item.find_element(By.CSS_SELECTOR, 'a[title]')
                    title = title_elem.get_attribute('title')
                    link = title_elem.get_attribute('href')
                    
                    price_elem = item.find_element(By.CSS_SELECTOR, '.price .em, .price em')
                    price = price_elem.text if price_elem else "0"
                    
                    listing = {
                        "id": f"CRAWL_{city_code}_{i}",
                        "name": title[:50] if title else f"房源{i}",
                        "rent": int(price) if price.isdigit() else 0,
                        "source": args.platform,
                        "url": link,
                        "status": "待考虑",
                        "created_at": datetime.now().isoformat(),
                    }
                    listings.append(listing)
                except Exception as e:
                    continue
        
        elif args.platform == '58同城':
            print("⚠️ 58同城反爬较强，建议使用 crawl_listings.py 或手动导入")
        
        elif args.platform == '安居客':
            print("⚠️ 安居客反爬较强，建议使用 crawl_listings.py 或手动导入")
        
    finally:
        driver.quit()
    
    # 保存结果
    if listings:
        print(f"\n✅ 抓取到 {len(listings)} 条房源")
        
        if args.save:
            existing = load_listings()
            for i, l in enumerate(listings):
                l['id'] = f"L{len(existing) + i + 1:03d}"
            existing.extend(listings)
            save_listings(existing)
            print(f"已保存到数据库")
        else:
            print("使用 --save 保存到数据库")
    else:
        print("未抓取到房源")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="使用Selenium抓取房源")
    parser.add_argument("--platform", required=True, choices=['贝壳', '链家'])
    parser.add_argument("--city", default="北京")
    parser.add_argument("--area", help="区域")
    parser.add_argument("--budget", type=int, help="预算上限")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--save", action="store_true")
    
    args = parser.parse_args()
    crawl_with_selenium(args)
