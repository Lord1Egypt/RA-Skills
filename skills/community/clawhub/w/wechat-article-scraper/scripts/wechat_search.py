#!/usr/bin/env python3
"""
搜狗微信搜索脚本 - 通用版
用法: python3 wechat_search.py <关键词> [数量]
"""
import asyncio
import json
import re
import sys
import os
import time
from datetime import datetime, timedelta
from playwright.async_api import async_playwright

# 默认参数
DEFAULT_COUNT = 10
DEFAULT_DAYS = 90  # 最近90天（放宽限制）
import os
WORKSPACE = os.path.expanduser('~/.openclaw/workspace')
OUTPUT_FILE = f'{WORKSPACE}/articles.json'


def parse_relative_time(date_text):
    """解析相对时间如 '3小时前', '2天前' 等，以及特殊格式"""
    if not date_text:
        return None
    
    now = datetime.now()
    
    # 处理 document.write(timeConvert('timestamp'))2024-2-23 格式
    # 先提取时间戳
    ts_match = re.search(r"timeConvert\('(\d+)'\)", date_text)
    if ts_match:
        try:
            ts = int(ts_match.group(1))
            return datetime.fromtimestamp(ts)
        except:
            pass
    
    # 清理并提取日期
    clean_date = re.sub(r"document\.write\(.*?\)", '', date_text).strip()
    
    # 匹配 X小时前
    hour_match = re.search(r'(\d+)小时前', clean_date)
    if hour_match:
        hours = int(hour_match.group(1))
        return now - timedelta(hours=hours)
    
    # 匹配 X天前
    day_match = re.search(r'(\d+)天前', clean_date)
    if day_match:
        days = int(day_match.group(1))
        return now - timedelta(days=days)
    
    # 匹配 X周前
    week_match = re.search(r'(\d+)周前', clean_date)
    if week_match:
        weeks = int(week_match.group(1))
        return now - timedelta(weeks=weeks)
    
    # 匹配 X月X日
    if '月' in clean_date and '日' in clean_date:
        try:
            month = int(re.search(r'(\d+)月', clean_date).group(1))
            day = int(re.search(r'月(\d+)日', clean_date).group(1))
            return datetime(now.year, month, day)
        except:
            pass
    
    # 尝试直接解析 YYYY-MM-DD
    try:
        return datetime.strptime(clean_date.strip(), '%Y-%m-%d')
    except:
        pass
    
    return None


def fix_weixin_url(url):
    """修复微信文章URL中的timestamp问题"""
    if not url or 'weixin.qq.com' not in url:
        return url
    
    # 替换 ×tamp= 为 &timestamp=
    url = re.sub(r'×tamp=', '&timestamp=', url)
    
    return url


def clean_date_text(date_text):
    """清理日期文本，去除 JavaScript 代码"""
    if not date_text:
        return ''
    
    # 移除 document.write(timeConvert('...')) 部分
    cleaned = re.sub(r"document\.write\(timeConvert\('[^']+'\)\)", '', date_text)
    # 清理多余空白
    cleaned = cleaned.strip()
    
    return cleaned


async def search_weixin(keyword, count=10, days=90):
    """执行搜狗微信搜索"""
    articles = []
    cutoff_date = datetime.now() - timedelta(days=days)
    
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = await context.new_page()
        
        # 访问搜狗微信搜索
        search_url = f'https://weixin.sogou.com/weixin?type=2&query={keyword}'
        print(f"搜索: {keyword}")
        print(f"URL: {search_url}")
        
        await page.goto(search_url)
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(3000)
        
        # 检查是否遇到验证码
        if await page.query_selector('#captcha'):
            print("⚠️ 遇到验证码，请手动处理...")
            await page.wait_for_timeout(10000)
        
        # 提取搜索结果
        article_data = await page.evaluate('''
            () => {
                const results = [];
                const items = document.querySelectorAll('div.txt-box');
                items.forEach((item) => {
                    const titleEl = item.querySelector('h3 a');
                    const sPElem = item.querySelector('.s-p');
                    let dateText = '';
                    let source = '';
                    
                    if (sPElem) {
                        const allTimeY2 = sPElem.querySelector('.all-time-y2');
                        if (allTimeY2) source = allTimeY2.textContent.trim();
                        
                        const s2 = sPElem.querySelector('.s2');
                        if (s2) dateText = s2.textContent.trim();
                        
                        if (!dateText) {
                            const timeElems = sPElem.querySelectorAll('span');
                            for (let i = 0; i < timeElems.length; i++) {
                                const txt = timeElems[i].textContent.trim();
                                if (txt.includes('前') && (txt.includes('小时') || txt.includes('天') || txt.includes('周'))) {
                                    dateText = txt;
                                    break;
                                }
                            }
                        }
                    }
                    
                    if (titleEl) {
                        results.push({
                            title: titleEl.textContent.trim(),
                            href: titleEl.href,
                            date: dateText,
                            source: source
                        });
                    }
                });
                return results;
            }
        ''')
        
        print(f"提取到 {len(article_data)} 条搜索结果")
        
        # 处理每篇文章
        for art in article_data:
            if len(articles) >= count:
                break
            
            article_date = parse_relative_time(art['date'])
            
            # 过滤日期
            if article_date and article_date >= cutoff_date:
                href = art['href']
                # 修复URL
                href = fix_weixin_url(href)
                print(f"抓取: {art['title'][:40]}... ({clean_date_text(art['date'])})")
                
                try:
                    # 每个文章之间间隔2秒，避免请求过快
                    time.sleep(2)
                    
                    article_page = await context.new_page()
                    await article_page.goto(href, timeout=15000, wait_until='domcontentloaded')
                    await asyncio.sleep(3)
                    
                    # 获取最终URL
                    final_url = article_page.url
                    # 修复最终URL
                    final_url = fix_weixin_url(final_url)
                    
                    # 获取正文内容 - 保留完整内容
                    full_content = ""
                    for sel in ['#js_content', '.rich_media_content', '.article', 'article', 'main']:
                        try:
                            content_elem = await article_page.query_selector(sel)
                            if content_elem:
                                full_content = await content_elem.inner_text()
                                if len(full_content) > 200:
                                    break
                        except:
                            continue
                    
                    await article_page.close()
                    
                    # 保存完整内容
                    articles.append({
                        'title': art['title'],
                        'text': full_content,
                        'url': final_url,
                        'date': clean_date_text(art['date']),  # 清理日期格式
                        'source': art['source'] or '未知公众号'
                    })
                    
                    print(f"  ✓ 成功! 内容长度: {len(full_content)} 字符 ({len(articles)}/{count})")
                    
                except Exception as e:
                    print(f"  ✗ 失败: {e}")
                    continue
        
        await browser.close()
    
    return articles


async def main():
    # 解析参数
    if len(sys.argv) < 2:
        print("用法: python3 wechat_search.py <关键词> [数量]")
        sys.exit(1)
    
    keyword = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_COUNT
    
    print("=" * 50)
    print(f"搜狗微信搜索: {keyword}")
    print(f"目标数量: {count} 篇")
    print("=" * 50)
    
    articles = await search_weixin(keyword, count)
    
    # 保存结果
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"\n完成! 找到 {len(articles)} 篇文章")
    print(f"结果保存至: {OUTPUT_FILE}")


if __name__ == '__main__':
    asyncio.run(main())
