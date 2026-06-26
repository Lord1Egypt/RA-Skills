#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zotero 文献导入工具（通过 DOI）

用法:
    python zotero_import.py --doi "10.1002/eqe.1234"
    python zotero_import.py --doi-list dois.txt
"""

import argparse
import json
import os
import requests
from pathlib import Path


def get_api_key():
    """从配置文件或环境变量获取 Zotero API Key"""
    config_path = Path.home() / '.config' / 'zotero' / 'api_key'
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    api_key = os.environ.get('ZOTERO_API_KEY')
    if api_key:
        return api_key
    
    raise ValueError("未找到 Zotero API Key")


def get_user_id(api_key):
    """获取 Zotero UserID"""
    url = "https://api.zotero.org/api/checkkeys/" + api_key
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('userID')
    return None


def import_by_doi(doi, api_key, user_id, collection_key=None):
    """通过 DOI 导入文献到 Zotero"""
    # 使用 Zotero 的翻译器 API 获取文献元数据
    translate_url = "https://translate.zotero.org/translate/web"
    params = {
        'url': f'https://doi.org/{doi}',
        'translator': '5c957833-82e3-42f9-b57f-743263e6a808'  # DOI translator
    }
    
    response = requests.get(translate_url, params=params)
    if response.status_code != 200:
        print(f"获取文献元数据失败：{response.status_code}")
        return None
    
    try:
        metadata = response.json()
    except json.JSONDecodeError:
        print("无法解析元数据")
        return None
    
    if not metadata:
        print("未找到文献信息")
        return None
    
    # 创建新文献
    base_url = f"https://api.zotero.org/users/{user_id}/items"
    headers = {
        'Zotero-API-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    # 准备文献数据
    item_data = metadata[0] if isinstance(metadata, list) else metadata
    
    # 添加分类
    if collection_key:
        item_data['collections'] = [collection_key]
    
    # 创建请求
    response = requests.post(base_url, headers=headers, json=[item_data])
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 成功导入文献")
        print(f"   标题：{item_data.get('title', '无标题')}")
        print(f"   作者：{', '.join([f\"{c.get('firstName', '')} {c.get('lastName', '')}\" for c in item_data.get('creators', [])[:2]])}")
        print(f"   DOI: {doi}")
        return result
    else:
        print(f"❌ 导入失败：{response.status_code}")
        print(response.text)
        return None


def get_collection_key(collection_name, api_key, user_id):
    """获取分类的 Key"""
    url = f"https://api.zotero.org/users/{user_id}/collections"
    params = {'key': api_key}
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return None
    
    collections = response.json()
    for coll in collections:
        if coll['data']['name'] == collection_name:
            return coll['data']['key']
    
    return None


def main():
    parser = argparse.ArgumentParser(description='Zotero 文献导入工具')
    parser.add_argument('--doi', type=str, help='DOI 号')
    parser.add_argument('--doi-list', type=str, help='DOI 列表文件')
    parser.add_argument('--collection', '-c', type=str, help='目标分类名称')
    
    args = parser.parse_args()
    
    if not args.doi and not args.doi_list:
        print("错误：请指定 --doi 或 --doi-list")
        parser.print_help()
        sys.exit(1)
    
    try:
        api_key = get_api_key()
    except ValueError as e:
        print(f"错误：{e}")
        sys.exit(1)
    
    user_id = get_user_id(api_key)
    if not user_id:
        print("错误：无法获取 UserID")
        sys.exit(1)
    
    print(f"Zotero UserID: {user_id}")
    print("-" * 60)
    
    # 获取分类 Key（如果指定了分类）
    collection_key = None
    if args.collection:
        collection_key = get_collection_key(args.collection, api_key, user_id)
        if collection_key:
            print(f"目标分类：{args.collection}")
        else:
            print(f"警告：未找到分类 '{args.collection}'，文献将导入到未分类")
    
    # 导入文献
    dois = []
    if args.doi:
        dois = [args.doi.strip()]
    elif args.doi_list:
        with open(args.doi_list, 'r', encoding='utf-8') as f:
            dois = [line.strip() for line in f if line.strip()]
    
    success_count = 0
    for doi in dois:
        print(f"\n导入：{doi}")
        result = import_by_doi(doi, api_key, user_id, collection_key)
        if result:
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"导入完成：成功 {success_count}/{len(dois)} 篇")


if __name__ == '__main__':
    main()
