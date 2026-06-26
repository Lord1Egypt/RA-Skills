#!/usr/bin/env python3
"""
B站搜索脚本
"""
import json
import sys
import requests
import urllib.parse

def load_cookies():
    """从文件加载 cookies"""
    try:
        with open('../references/platform_cookies.json', 'r') as f:
            data = json.load(f)
            return data.get('bilibili', {})
    except:
        return {}

def search_bilibili(keyword, num=10):
    """搜索B站视频"""
    cookies = load_cookies()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'https://search.bilibili.com/all?keyword={urllib.parse.quote(keyword)}',
    }
    
    api_url = 'https://api.bilibili.com/x/web-interface/search/type'
    params = {
        'search_type': 'video',
        'keyword': keyword,
        'page': '1',
        'pagesize': str(num),
        'order': 'click',
    }
    
    try:
        session = requests.Session()
        resp = session.get(api_url, headers=headers, params=params, cookies=cookies, timeout=15)
        data = resp.json()
        
        if data.get('code') == 0:
            videos = data.get('data', {}).get('result', [])
            results = []
            for v in videos[:num]:
                results.append({
                    'title': v.get('title', '').replace('<em class="keyword">', '').replace('</em>', ''),
                    'bvid': v.get('bvid', ''),
                    'link': f"https://www.bilibili.com/video/{v.get('bvid', '')}",
                    'author': v.get('author', ''),
                    'mid': v.get('mid', ''),
                    'play': v.get('play', 0),
                    'danmaku': v.get('danmaku', 0),
                })
            return results
        else:
            return {'error': data.get('message', 'Unknown error')}
    except Exception as e:
        return {'error': str(e)}

def get_user_videos(mid, num=5):
    """获取用户视频列表"""
    cookies = load_cookies()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'https://space.bilibili.com/{mid}',
    }
    
    api_url = 'https://api.bilibili.com/x/space/arc/search'
    params = {
        'mid': str(mid),
        'ps': str(num),
        'tid': '0',
        'pn': '1',
        'order': 'click',
    }
    
    try:
        session = requests.Session()
        resp = session.get(api_url, headers=headers, params=params, cookies=cookies, timeout=15)
        data = resp.json()
        
        if data.get('code') == 0:
            videos = data.get('data', {}).get('list', {}).get('vlist', [])
            results = []
            for v in videos[:num]:
                results.append({
                    'title': v.get('title', ''),
                    'bvid': v.get('bvid', ''),
                    'link': f"https://www.bilibili.com/video/{v.get('bvid', '')}",
                    'play': v.get('play', 0),
                    'comment': v.get('comment', 0),
                })
            return results
        else:
            return {'error': data.get('message', 'Unknown error')}
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'user':
        mid = sys.argv[2] if len(sys.argv) > 2 else '129641517'
        num = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        results = get_user_videos(mid, num)
    else:
        keyword = sys.argv[1] if len(sys.argv) > 1 else '美女'
        num = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        results = search_bilibili(keyword, num)
    
    print(json.dumps(results, ensure_ascii=False, indent=2))
