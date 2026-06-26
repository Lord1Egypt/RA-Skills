#!/usr/bin/env python3
"""
抖音搜索脚本
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
            return data.get('douyin', {})
    except:
        return {}

def search_douyin(keyword, num=10):
    """搜索抖音视频"""
    cookies = load_cookies()
    if not cookies:
        return {'error': 'No cookies found. Please provide Douyin cookies first.'}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'https://www.douyin.com/search/{urllib.parse.quote(keyword)}',
    }
    
    api_url = 'https://www.douyin.com/aweme/v1/web/search/item/'
    params = {
        'device_platform': 'webapp',
        'aid': '6383',
        'channel': 'channel_pc_web',
        'search_channel': 'aweme',
        'keyword': keyword,
        'offset': '0',
        'count': str(num),
    }
    
    try:
        session = requests.Session()
        resp = session.get(api_url, headers=headers, params=params, cookies=cookies, timeout=15)
        data = resp.json()
        
        if data.get('status_code') == 0:
            videos = data.get('data', [])
            results = []
            for v in videos[:num]:
                aweme = v.get('aweme_info', {})
                author = aweme.get('author', {})
                stats = aweme.get('statistics', {})
                
                results.append({
                    'desc': aweme.get('desc', '')[:50],
                    'nickname': author.get('nickname', ''),
                    'digg_count': stats.get('digg_count', 0),
                    'comment_count': stats.get('comment_count', 0),
                    'aweme_id': aweme.get('aweme_id', ''),
                    'link': f"https://www.douyin.com/video/{aweme.get('aweme_id', '')}",
                })
            return results
        else:
            return {'error': data.get('status_msg', 'Unknown error')}
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    keyword = sys.argv[1] if len(sys.argv) > 1 else '美女'
    num = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    results = search_douyin(keyword, num)
    print(json.dumps(results, ensure_ascii=False, indent=2))
