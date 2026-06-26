#!/usr/bin/env python3
"""
交互式网页抓取 - 需要登录时提示用户
用法: python crawl_interactive.py --platform 58 --city 成都 --area 春熙路
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

def crawl_with_browser(args):
    """使用浏览器抓取，需要登录时提示用户"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
        print("❌ 请先安装依赖:")
        print("   pip3 install selenium webdriver-manager")
        return
    
    # 配置Chrome选项（非无头模式，方便用户登录）
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1200,800")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
    
    # 启动浏览器
    print("🚀 正在启动浏览器...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    listings = []
    
    try:
        # 城市代码映射
        city_codes = {
            '北京': 'bj', '上海': 'sh', '广州': 'gz', '深圳': 'sz',
            '杭州': 'hz', '南京': 'nj', '成都': 'cd', '武汉': 'wh',
            '西安': 'xa', '重庆': 'cq',
        }
        
        if args.platform == '58':
            city_code = city_codes.get(args.city, 'cd')
            # 58同城商铺搜索
            url = f"https://{city_code}.58.com/shangpu/"
            if args.area:
                from urllib.parse import quote
                url += f"?key={quote(args.area.encode('utf-8'))}"
            
            print(f"\n🌐 正在打开: {url}")
            driver.get(url)
            
            # 检查是否需要登录
            print("\n⏳ 等待页面加载...")
            time.sleep(3)
            
            # 检查登录状态
            try:
                # 58同城的登录检测
                login_indicators = [
                    "login",
                    "登录",
                    "扫码登录",
                    "手机登录"
                ]
                
                page_source = driver.page_source.lower()
                need_login = any(indicator in page_source for indicator in login_indicators)
                
                if need_login:
                    print("\n" + "="*60)
                    print("🔐 检测到需要登录")
                    print("="*60)
                    print("\n请在浏览器中完成登录：")
                    print("1. 扫码登录 或 手机验证码登录")
                    print("2. 登录完成后，按回车键继续...")
                    print("\n⚠️  注意：请不要关闭浏览器窗口")
                    print("="*60)
                    input("\n登录完成后请按回车键继续...")
                    
                    # 等待用户登录完成
                    time.sleep(2)
                    print("\n✅ 继续抓取...")
                
            except Exception as e:
                print(f"检查登录状态时出错: {e}")
            
            # 抓取房源
            print("\n🔍 正在抓取房源...")
            time.sleep(3)
            
            # 滚动加载更多
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            
            # 解析房源列表
            try:
                # 58同城商铺列表选择器
                items = driver.find_elements(By.CSS_SELECTOR, '.list-item, .house-item, .item')
                print(f"\n📋 找到 {len(items)} 个房源")
                
                for i, item in enumerate(items[:args.limit]):
                    try:
                        # 提取标题
                        title_elem = item.find_element(By.CSS_SELECTOR, 'h2, .title, a[title]')
                        title = title_elem.text or title_elem.get_attribute('title')
                        
                        # 提取链接
                        link = title_elem.get_attribute('href')
                        
                        # 提取价格
                        price = "0"
                        try:
                            price_elem = item.find_element(By.CSS_SELECTOR, '.price, .money, .strongbox')
                            price_text = price_elem.text
                            import re
                            price_match = re.search(r'(\d+)', price_text)
                            if price_match:
                                price = price_match.group(1)
                        except:
                            pass
                        
                        # 提取面积
                        area = 0
                        try:
                            area_elem = item.find_element(By.CSS_SELECTOR, '.area, .size')
                            area_text = area_elem.text
                            import re
                            area_match = re.search(r'(\d+)', area_text)
                            if area_match:
                                area = int(area_match.group(1))
                        except:
                            pass
                        
                        # 筛选
                        if args.max_rent and int(price) > args.max_rent:
                            continue
                        if args.min_area and area < args.min_area:
                            continue
                        
                        listing = {
                            "id": f"CRAWL_{i}",
                            "name": title[:50] if title else f"房源{i}",
                            "rent": int(price) if price.isdigit() else 0,
                            "area": area,
                            "source": "58同城",
                            "url": link,
                            "status": "待考虑",
                            "created_at": datetime.now().isoformat(),
                        }
                        listings.append(listing)
                        
                        print(f"\n【{len(listings)}】{listing['name']}")
                        print(f"   租金: {listing['rent']}元/月")
                        print(f"   面积: {listing['area']}㎡")
                        print(f"   链接: {link}")
                        
                    except Exception as e:
                        continue
                
            except Exception as e:
                print(f"抓取房源时出错: {e}")
        
        elif args.platform == '贝壳':
            city_code = city_codes.get(args.city, 'cd')
            url = f"https://{city_code}.ke.com/zufang/"
            if args.area:
                from urllib.parse import quote
                url += f"{quote(args.area.encode('utf-8'))}/"
            if args.max_rent:
                url += f"rp{args.max_rent}/"
            
            print(f"\n🌐 正在打开: {url}")
            driver.get(url)
            
            print("\n⏳ 等待页面加载...")
            time.sleep(3)
            
            # 检查是否需要登录
            try:
                if "login" in driver.page_source.lower() or "登录" in driver.page_source:
                    print("\n" + "="*60)
                    print("🔐 检测到需要登录")
                    print("="*60)
                    print("\n请在浏览器中完成登录")
                    input("\n登录完成后请按回车键继续...")
                    time.sleep(2)
            except:
                pass
            
            # 抓取房源
            print("\n🔍 正在抓取房源...")
            time.sleep(3)
            
            try:
                items = driver.find_elements(By.CSS_SELECTOR, '[data-houseid]')
                print(f"\n📋 找到 {len(items)} 个房源")
                
                for i, item in enumerate(items[:args.limit]):
                    try:
                        title_elem = item.find_element(By.CSS_SELECTOR, 'a[title]')
                        title = title_elem.get_attribute('title')
                        link = title_elem.get_attribute('href')
                        
                        price_elem = item.find_element(By.CSS_SELECTOR, '.price .em, .price em')
                        price = price_elem.text
                        
                        listing = {
                            "id": f"CRAWL_{i}",
                            "name": title[:50] if title else f"房源{i}",
                            "rent": int(price) if price.isdigit() else 0,
                            "source": "贝壳",
                            "url": link,
                            "status": "待考虑",
                            "created_at": datetime.now().isoformat(),
                        }
                        listings.append(listing)
                        
                        print(f"\n【{len(listings)}】{listing['name']}")
                        print(f"   租金: {listing['rent']}元/月")
                        print(f"   链接: {link}")
                        
                    except:
                        continue
                        
            except Exception as e:
                print(f"抓取房源时出错: {e}")
        
    finally:
        # 询问是否关闭浏览器
        print("\n" + "="*60)
        close = input("是否关闭浏览器? (y/n): ")
        if close.lower() == 'y':
            driver.quit()
            print("✅ 浏览器已关闭")
        else:
            print("✅ 浏览器保持打开状态")
    
    # 保存结果
    if listings:
        print(f"\n\n✅ 共抓取到 {len(listings)} 条房源")
        
        if args.save:
            existing = load_listings()
            for i, l in enumerate(listings):
                l['id'] = f"L{len(existing) + i + 1:03d}"
            existing.extend(listings)
            save_listings(existing)
            print(f"✅ 已保存到数据库")
    else:
        print("\n\n❌ 未抓取到房源")
        print("建议：")
        print("1. 检查是否登录成功")
        print("2. 尝试刷新页面")
        print("3. 更换平台重试")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="交互式网页抓取")
    parser.add_argument("--platform", required=True, choices=['58', '贝壳'], help="平台")
    parser.add_argument("--city", default="成都", help="城市")
    parser.add_argument("--area", help="区域/商圈")
    parser.add_argument("--max-rent", type=int, help="最高租金")
    parser.add_argument("--min-area", type=int, help="最小面积")
    parser.add_argument("--limit", type=int, default=10, help="抓取数量")
    parser.add_argument("--save", action="store_true", help="保存到数据库")
    
    args = parser.parse_args()
    crawl_with_browser(args)
