#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zotero 文献搜索工具（支持本地 API 和远程 API）

用法:
    python zotero_search.py --query "RTHS" --limit 10
    python zotero_search.py --local --query "RTHS"  # 使用本地 API
"""

import argparse
import json
import os
import sys
import requests
from pathlib import Path


def get_api_key():
    """从配置文件或环境变量获取 Zotero API Key"""
    # 方式 1: 工作空间配置（优先）
    workspace_config = Path(r'D:\Personal\OpenClaw\.config\zotero\api_key')
    if workspace_config.exists():
        with open(workspace_config, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    # 方式 2: 用户目录配置
    user_config = Path.home() / '.config' / 'zotero' / 'api_key'
    if user_config.exists():
        with open(user_config, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    # 方式 3: 环境变量
    api_key = os.environ.get('ZOTERO_API_KEY')
    if api_key:
        return api_key
    
    return None


def get_local_api_key():
    """从配置文件获取 Zotero 本地 API 密钥"""
    # 方式 1: 本地 API 专用密钥
    config_path = Path.home() / '.config' / 'zotero' / 'local_api_key'
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    # 方式 2: 通用 API Key
    return get_api_key()


def search_local(query, limit=10, base_url='http://localhost:23119/api'):
    """使用 Zotero 本地 API 搜索（API v3）"""
    # Zotero 7 本地 API v3 端点
    search_url = f"{base_url}/3/items"
    params = {
        'q': query,
        'limit': limit,
        'format': 'json'
    }
    
    # 获取本地 API 密钥
    api_key = get_local_api_key()
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    
    try:
        response = requests.get(search_url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            print("403 Forbidden: 需要 API 密钥")
            print("请在 Zotero 中获取本地 API 密钥:")
            print("  编辑 → 首选项 → 高级 → 本地 API 服务")
            print("然后保存到：~/.config/zotero/local_api_key")
            return []
        else:
            print(f"本地 API 错误：{response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        print("无法连接到 Zotero 本地 API (localhost:23119)")
        print("请确保 Zotero 7 已启动并开启了本地 API 服务")
        return []
    except Exception as e:
        print(f"本地 API 搜索失败：{e}")
        return []


def search_local_collections(base_url='http://localhost:23119/api'):
    """获取本地 API 的分类列表"""
    collections_url = f"{base_url}/collections"
    try:
        response = requests.get(collections_url, timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []


def get_user_id(api_key):
    """获取 Zotero UserID"""
    url = "https://api.zotero.org/keys/" + api_key
    response = requests.get(url, headers={'Zotero-API-Key': api_key})
    if response.status_code == 200:
        data = response.json()
        return data.get('userID')
    return None


def search_library(query, api_key, user_id, limit=10):
    """搜索 Zotero 文献库（远程 API）"""
    base_url = f"https://api.zotero.org/users/{user_id}/items"
    params = {
        'q': query,
        'limit': limit,
        'format': 'json',
        'key': api_key
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"错误：{response.status_code}")
        print(response.text)
        return []


def search_collection(collection_name, api_key, user_id, limit=10):
    """搜索特定分类的文献"""
    # 先获取分类 ID
    collections_url = f"https://api.zotero.org/users/{user_id}/collections"
    params = {'key': api_key}
    response = requests.get(collections_url, params=params)
    
    if response.status_code != 200:
        print(f"获取分类失败：{response.status_code}")
        return []
    
    collections = response.json()
    collection_id = None
    for coll in collections:
        if coll['data']['name'] == collection_name:
            collection_id = coll['data']['key']
            break
    
    if not collection_id:
        print(f"未找到分类：{collection_name}")
        return []
    
    # 搜索该分类下的文献
    items_url = f"https://api.zotero.org/users/{user_id}/collections/{collection_id}/items"
    params = {'limit': limit, 'key': api_key}
    response = requests.get(items_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"错误：{response.status_code}")
        return []


def format_results(items):
    """格式化搜索结果"""
    results = []
    for item in items:
        data = item.get('data', {})
        creators = data.get('creators', [])
        authors = ', '.join([f"{c.get('firstName', '')} {c.get('lastName', '')}" for c in creators[:2]])
        if len(creators) > 2:
            authors += " et al."
        
        result = {
            'title': data.get('title', '无标题'),
            'authors': authors,
            'date': data.get('date', '无日期'),
            'DOI': data.get('DOI', ''),
            'publicationTitle': data.get('publicationTitle', ''),
            'itemType': data.get('itemType', '')
        }
        results.append(result)
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Zotero 文献搜索工具')
    parser.add_argument('--query', '-q', type=str, help='搜索关键词')
    parser.add_argument('--collection', '-c', type=str, help='分类名称')
    parser.add_argument('--limit', '-l', type=int, default=10, help='返回结果数量')
    parser.add_argument('--json', action='store_true', help='以 JSON 格式输出')
    parser.add_argument('--local', action='store_true', help='使用 Zotero 本地 API (localhost:23119)')
    parser.add_argument('--api-url', type=str, default='http://localhost:23119/api', 
                       help='本地 API 地址（默认：http://localhost:23119/api）')
    
    args = parser.parse_args()
    
    if not args.query and not args.collection:
        print("错误：请指定 --query 或 --collection")
        parser.print_help()
        sys.exit(1)
    
    print(f"搜索：{args.query or args.collection}")
    print(f"模式：{'本地 API' if args.local else '远程 API'}")
    print("-" * 60)
    
    # 本地 API 搜索
    if args.local:
        print(f"API 地址：{args.api_url}")
        items = search_local(args.query or '', args.limit, args.api_url)
        if items:
            results = format_results(items)
            if args.json:
                print(json.dumps(results, ensure_ascii=False, indent=2))
            else:
                for i, item in enumerate(results, 1):
                    print(f"\n[{i}] {item['title']}")
                    print(f"    作者：{item['authors']}")
                    print(f"    年份：{item['date']}")
                    print(f"    期刊：{item['publicationTitle']}")
                    if item['DOI']:
                        print(f"    DOI: {item['DOI']}")
                print(f"\n共找到 {len(results)} 篇文献")
        else:
            print("未找到文献或无法连接本地 API")
        return
    
    # 远程 API 搜索
    try:
        api_key = get_api_key()
    except ValueError as e:
        print(f"错误：{e}")
        sys.exit(1)
    
    # 获取 UserID
    user_id = get_user_id(api_key)
    if not user_id:
        print("错误：无法获取 UserID，请检查 API Key")
        sys.exit(1)
    
    print(f"Zotero UserID: {user_id}")
    
    # 搜索
    if args.query:
        items = search_library(args.query, api_key, user_id, args.limit)
    else:
        items = search_collection(args.collection, api_key, user_id, args.limit)
    
    # 格式化结果
    results = format_results(items)
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for i, item in enumerate(results, 1):
            print(f"\n[{i}] {item['title']}")
            print(f"    作者：{item['authors']}")
            print(f"    年份：{item['date']}")
            print(f"    期刊：{item['publicationTitle']}")
            if item['DOI']:
                print(f"    DOI: {item['DOI']}")
    
    print(f"\n共找到 {len(results)} 篇文献")


if __name__ == '__main__':
    main()
