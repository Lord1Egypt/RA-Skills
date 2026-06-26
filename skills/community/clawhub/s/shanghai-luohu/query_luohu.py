#!/usr/bin/env python3
"""
上海落户公示查询工具
功能：抓取上海国际人才网的落户公示信息并使用浏览器打开
支持：macOS, Windows, Linux 全平台
"""

import subprocess
import sys
import re
import argparse
import platform
import webbrowser
from urllib.request import urlopen, Request
from datetime import datetime

# 公示列表页 URL
LIST_URL = "https://www.sh-italent.com/News/NewsList.aspx?TagID=5696"
BASE_URL = "https://www.sh-italent.com"

# User-Agent
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def get_platform():
    """获取当前操作系统"""
    system = platform.system().lower()
    if system == 'darwin':
        return 'macos'
    elif system == 'windows':
        return 'windows'
    elif system == 'linux':
        return 'linux'
    return system


def fetch_url(url):
    """获取网页内容"""
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"错误：无法获取 {url}: {e}")
        return None


def extract_links(html_content):
    """从列表页面提取公示链接"""
    pattern = r'href="(https://www\.sh-italent\.com/Article/\d+/\d+\.shtml)"'
    links = re.findall(pattern, html_content)
    return links


def extract_article_info(html_content):
    """提取公示文章信息"""
    title_match = re.search(r'<title>([^<]+)</title>', html_content)
    title = title_match.group(1).replace('_上海国际人才网', '').strip() if title_match else "未知标题"
    
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', html_content)
    date = date_match.group(1) if date_match else "未知日期"
    
    return {'title': title, 'date': date}


def open_browser(urls, browser=None):
    """打开浏览器（跨平台）"""
    platform_name = get_platform()
    
    print(f"正在打开浏览器...")
    
    # 如果指定了浏览器，尝试使用指定的浏览器
    if browser:
        try:
            # 使用 webbrowser 模块
            browser_map = {
                'Chrome': 'chrome',
                'Firefox': 'firefox',
                'Edge': 'edge',
                'Safari': 'safari',
                'Brave': 'brave',
                'Opera': 'opera',
            }
            browser_name = browser_map.get(browser, browser.lower())
            
            for url in urls:
                webbrowser.get(browser_name).open(url)
            return True
        except:
            print(f"警告：无法使用 {browser}，使用默认浏览器")
    
    # macOS 特殊处理：使用 AppleScript 支持多标签页
    if platform_name == 'macos':
        return open_browser_macos(urls, browser)
    
    # Windows / Linux: 使用默认浏览器
    try:
        for url in urls:
            webbrowser.open(url)
        return True
    except Exception as e:
        print(f"打开浏览器失败: {e}")
        return False


def open_browser_macos(urls, browser=None):
    """macOS 使用 AppleScript 打开浏览器"""
    if browser is None:
        browser = 'Safari'
    
    browser_names = {
        'Safari': 'Safari',
        'Chrome': 'Google Chrome',
        'Firefox': 'Firefox',
        'Edge': 'Microsoft Edge',
        'Brave': 'Brave',
        'Opera': 'Opera',
    }
    
    app_name = browser_names.get(browser, 'Safari')
    
    applescript = f'''
tell application "{app_name}"
    activate
'''
    for i, url in enumerate(urls):
        applescript += f'''
    open location "{url}"
    delay 0.5
'''
    applescript += '''
end tell
'''
    
    try:
        subprocess.run(['osascript', '-e', applescript], check=True)
        return True
    except:
        # 回退到 webbrowser
        try:
            for url in urls:
                webbrowser.open(url)
            return True
        except:
            return False


def main():
    parser = argparse.ArgumentParser(description='上海落户公示信息查询工具')
    parser.add_argument('-b', '--browser', 
                        choices=['Safari', 'Chrome', 'Firefox', 'Edge', 'Brave', 'Opera'],
                        help='指定使用的浏览器')
    parser.add_argument('-n', '--no-browser', action='store_true',
                        help='不打开浏览器，仅输出查询结果')
    parser.add_argument('-c', '--company', type=str,
                        help='查询指定公司的落户公示名单')
    parser.add_argument('-p', '--person', type=str,
                        help='查询指定人员的落户公示')
    args = parser.parse_args()
    
    print("=" * 50)
    print("    上海落户公示信息查询")
    print("=" * 50)
    print()
    
    # 1. 获取公示列表页面
    print("[1/4] 获取公示列表页面...")
    list_html = fetch_url(LIST_URL)
    if not list_html:
        print("错误：无法获取公示列表页面")
        sys.exit(1)
    print("✓ 列表页面获取成功")
    print()
    
    # 2. 提取公示链接
    print("[2/4] 解析公示链接...")
    links = extract_links(list_html)
    
    if not links:
        print("错误：未找到公示链接")
        sys.exit(1)
    
    # 区分人才引进和居转户公示
    talent_url = None
    juzhuan_url = None
    
    for link in links[:5]:
        html_content = fetch_url(link)
        if html_content:
            if '引进人才' in html_content and talent_url is None:
                talent_url = link
            elif '居住证' in html_content and juzhuan_url is None:
                juzhuan_url = link
    
    print(f"✓ 人才引进公示: {talent_url}")
    print(f"✓ 居转户公示: {juzhuan_url}")
    print()
    
    # 3. 获取公示详情
    print("[3/4] 获取公示详情...")
    
    talent_info = None
    juzhuan_info = None
    
    if talent_url:
        talent_html = fetch_url(talent_url)
        if talent_html:
            talent_info = extract_article_info(talent_html)
            print(f"  人才引进: {talent_info['title']}")
            print(f"  公示日期: {talent_info['date']}")
    
    if juzhuan_url:
        juzhuan_html = fetch_url(juzhuan_url)
        if juzhuan_html:
            juzhuan_info = extract_article_info(juzhuan_html)
            print(f"  居转户: {juzhuan_info['title']}")
            print(f"  公示日期: {juzhuan_info['date']}")
    
    print()
    
    # 4. 输出汇总
    print("[4/4] 查询结果汇总")
    print("=" * 50)
    print()
    
    print("【一】人才引进公示")
    if talent_info and talent_url:
        print(f"  公示标题: {talent_info['title']}")
        print(f"  公示日期: {talent_info['date']}")
        print(f"  公示链接: {talent_url}")
    else:
        print("  未找到公示信息")
    print()
    
    print("【二】居转户公示")
    if juzhuan_info and juzhuan_url:
        print(f"  公示标题: {juzhuan_info['title']}")
        print(f"  公示日期: {juzhuan_info['date']}")
        print(f"  公示链接: {juzhuan_url}")
    else:
        print("  未找到公示信息")
    print()
    
    print("=" * 50)
    print(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"运行平台: {get_platform().upper()}")
    print("=" * 50)
    print()
    
    # 5. 打开浏览器
    if args.no_browser:
        print("提示：跳过浏览器打开（使用了 --no-browser 参数）")
    else:
        urls_to_open = [LIST_URL]
        if talent_url:
            urls_to_open.append(talent_url)
        if juzhuan_url:
            urls_to_open.append(juzhuan_url)
        
        if open_browser(urls_to_open, args.browser):
            print("✓ 浏览器已打开")
        else:
            print("提示：请手动访问以下链接查看公示：")
            for url in urls_to_open:
                print(f"  {url}")
    
    print()
    print("提示：公示期通常为 5 天，每月两次公示（月中和月底）")


if __name__ == "__main__":
    main()
