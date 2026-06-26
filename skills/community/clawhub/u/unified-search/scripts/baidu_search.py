#!/usr/bin/env python3
import sys
import io
import json
import urllib.parse
import requests
import re
from bs4 import BeautifulSoup

# 修复 Windows 控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def search_baidu(query, max_results=10):
    """使用百度搜索 - 优化版本"""
    try:
        # 百度搜索URL
        search_url = f"https://www.baidu.com/s?wd={urllib.parse.quote(query)}&ie=utf-8&tn=baidu"
        
        # 设置请求头，模拟真实浏览器
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        
        print(f"正在搜索: {query}", file=sys.stderr)
        
        # 发送请求
        session = requests.Session()
        response = session.get(search_url, headers=headers, timeout=15, allow_redirects=True)
        print(f"响应状态码: {response.status_code}", file=sys.stderr)
        print(f"最终URL: {response.url}", file=sys.stderr)
        
        # 检查是否有验证页面
        if 'verify' in response.url or '验证码' in response.text[:500]:
            return [{
                "error": "百度需要人机验证",
                "suggestion": "请使用浏览器搜索方式（Playwright），或者直接访问 https://www.baidu.com",
                "alternative": "使用 browser 工具进行搜索"
            }]
        
        response.encoding = 'utf-8'
        
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        
        # ==========================================
        # 策略1: 查找百度标准搜索结果 (c-container)
        # ==========================================
        print("策略1: 查找标准搜索结果...", file=sys.stderr)
        
        for result in soup.find_all('div', class_='c-container'):
            try:
                # 查找标题
                title_elem = result.find('h3')
                if not title_elem:
                    continue
                    
                link_elem = title_elem.find('a')
                if not link_elem:
                    continue
                    
                title = link_elem.get_text(strip=True)
                url = link_elem.get('href', '')
                
                if not title or not url:
                    continue
                    
                # 修复URL
                if url.startswith('//'):
                    url = 'https:' + url
                    
                # 查找摘要
                snippet = ""
                snippet_elem = result.find('div', class_='c-abstract')
                if snippet_elem:
                    snippet = snippet_elem.get_text(strip=True)
                else:
                    # 尝试其他摘要类名
                    for cls in ['c-content', 'c-span-last', 'content-right_8Zs40']:
                        elem = result.find('div', class_=cls)
                        if elem:
                            snippet = elem.get_text(strip=True)
                            break
                
                if title and url and url.startswith('http'):
                    results.append({
                        "title": title,
                        "url": url,
                        "snippet": snippet
                    })
            except Exception as e:
                print(f"解析结果时出错: {e}", file=sys.stderr)
                continue
        
        # ==========================================
        # 策略2: 查找所有带标题的链接
        # ==========================================
        if len(results) < 3:
            print(f"策略2: 查找更多结果 (当前: {len(results)})...", file=sys.stderr)
            
            for heading in soup.find_all(['h1', 'h2', 'h3', 'h4']):
                link = heading.find('a')
                if link:
                    title = link.get_text(strip=True)
                    url = link.get('href', '')
                    if title and url and len(title) > 5:
                        if url.startswith('//'):
                            url = 'https:' + url
                        if url.startswith('http'):
                            # 检查是否已存在
                            exists = any(r['url'] == url for r in results)
                            if not exists:
                                results.append({
                                    "title": title,
                                    "url": url,
                                    "snippet": ""
                                })
        
        # ==========================================
        # 策略3: 查找知识图谱/快速回答
        # ==========================================
        print("策略3: 查找知识图谱...", file=sys.stderr)
        
        # 查找百度百科/快速回答
        for cls in ['c-span18', 'opr-result-top', 'c-border']:
            kg_elem = soup.find('div', class_=cls)
            if kg_elem:
                kg_title = kg_elem.find('h2') or kg_elem.find('h3')
                if kg_title:
                    title_text = kg_title.get_text(strip=True)
                    if title_text and len(title_text) > 2:
                        kg_snippet = kg_elem.get_text(strip=True)[:500]
                        results.insert(0, {
                            "title": f"📌 {title_text}",
                            "url": search_url,
                            "snippet": kg_snippet,
                            "is_knowledge": True
                        })
                        break
        
        # ==========================================
        # 去重和过滤
        # ==========================================
        seen_urls = set()
        unique_results = []
        for r in results:
            url = r.get('url', '')
            if url and url not in seen_urls:
                # 过滤掉百度内部链接（除了知识图谱）
                if r.get('is_knowledge') or ('baidu.com' not in url) or ('link.baidu.com' in url):
                    seen_urls.add(url)
                    # 移除内部标记
                    r.pop('is_knowledge', None)
                    unique_results.append(r)
        
        print(f"最终结果: {len(unique_results)} 个", file=sys.stderr)
        
        # 如果还是没有结果，返回备用方案
        if not unique_results:
            return [{
                "title": "💡 使用浏览器搜索",
                "url": "https://www.bing.com",
                "snippet": "建议使用 ClawX 的 browser 工具进行搜索，更加稳定可靠。",
                "alternative": "browser"
            }]
        
        return unique_results[:max_results]
        
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return [{
            "error": str(e),
            "suggestion": "使用 browser 工具进行搜索"
        }]

def print_results_formatted(results):
    """格式化输出结果"""
    if not results:
        print("未找到搜索结果")
        return
        
    for i, result in enumerate(results, 1):
        if 'error' in result:
            print(f"❌ {result['error']}")
            if 'suggestion' in result:
                print(f"💡 {result['suggestion']}")
            continue
            
        print(f"\n{i}. {result.get('title', '无标题')}")
        if result.get('url'):
            print(f"   🔗 {result['url']}")
        if result.get('snippet'):
            snippet = result['snippet'][:200] + ('...' if len(result['snippet']) > 200 else '')
            print(f"   📝 {snippet}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Please provide a search query"}))
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    results = search_baidu(query)
    
    # 检查是否需要格式化输出
    if '--format' in sys.argv or '-f' in sys.argv:
        print_results_formatted(results)
    else:
        print(json.dumps(results, ensure_ascii=False))
