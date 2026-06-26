#!/usr/bin/env python3
"""
微信公众号草稿删除工具
"""

import requests
import json
import sys
import os
import argparse
from typing import List

def get_access_token(appid: str, secret: str) -> str:
    """获取微信公众号access_token"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"
    response = requests.get(url)
    data = response.json()
    
    if 'access_token' in data:
        return data['access_token']
    else:
        print(f"❌ 获取access_token失败: {data}")
        sys.exit(1)

def delete_draft(access_token: str, media_id: str) -> bool:
    """删除单个草稿"""
    url = f"https://api.weixin.qq.com/cgi-bin/draft/delete?access_token={access_token}"
    data = {
        "media_id": media_id
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        
        if result.get('errcode') == 0:
            print(f"✅ 删除成功: {media_id}")
            return True
        else:
            print(f"❌ 删除失败 {media_id}: {result}")
            return False
            
    except Exception as e:
        print(f"❌ 删除请求失败 {media_id}: {e}")
        return False

def delete_multiple_drafts(access_token: str, media_ids: List[str]) -> dict:
    """批量删除草稿"""
    results = {
        'success': [],
        'failed': []
    }
    
    for media_id in media_ids:
        if delete_draft(access_token, media_id):
            results['success'].append(media_id)
        else:
            results['failed'].append(media_id)
    
    return results

def read_media_ids_from_file(file_path: str) -> List[str]:
    """从文件读取Media ID列表"""
    media_ids = []
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    media_ids.append(line)
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        sys.exit(1)
    
    return media_ids

def main():
    parser = argparse.ArgumentParser(description='删除微信公众号草稿')
    parser.add_argument('--media-id', help='单个Media ID')
    parser.add_argument('--media-ids', help='多个Media ID，用逗号分隔')
    parser.add_argument('--file', help='包含Media ID列表的文件')
    parser.add_argument('--appid', default=os.getenv('WECHAT_APP_ID'), help='微信公众号AppID')
    parser.add_argument('--secret', default=os.getenv('WECHAT_APP_SECRET'), help='微信公众号AppSecret')
    parser.add_argument('--force', '-f', action='store_true', help='强制删除，不确认')
    
    args = parser.parse_args()
    
    # 检查参数
    if not args.media_id and not args.media_ids and not args.file:
        print("❌ 请提供Media ID：--media-id, --media-ids 或 --file")
        parser.print_help()
        sys.exit(1)
    
    if not args.appid or not args.secret:
        print("❌ 请设置微信公众号凭证：WECHAT_APP_ID 和 WECHAT_APP_SECRET 环境变量")
        sys.exit(1)
    
    # 获取Media ID列表
    media_ids = []
    
    if args.media_id:
        media_ids.append(args.media_id)
    
    if args.media_ids:
        media_ids.extend([id.strip() for id in args.media_ids.split(',')])
    
    if args.file:
        media_ids.extend(read_media_ids_from_file(args.file))
    
    # 去重
    media_ids = list(set(media_ids))
    
    print(f"📋 准备删除 {len(media_ids)} 个草稿")
    print(f"Media IDs: {media_ids}")
    
    # 获取access_token
    print("🔑 获取access_token...")
    access_token = get_access_token(args.appid, args.secret)
    
    # 确认删除
    if not args.force:
        confirm = input(f"⚠️  确认删除 {len(media_ids)} 个草稿吗？(y/N): ")
        if confirm.lower() != 'y':
            print("❌ 操作取消")
            sys.exit(0)
    else:
        print(f"⚠️  强制删除 {len(media_ids)} 个草稿...")
    
    # 执行删除
    print("🗑️  开始删除草稿...")
    results = delete_multiple_drafts(access_token, media_ids)
    
    # 输出结果
    print("\n" + "="*50)
    print("📊 删除结果汇总:")
    print(f"✅ 成功删除: {len(results['success'])} 个")
    print(f"❌ 删除失败: {len(results['failed'])} 个")
    
    if results['failed']:
        print("\n失败的Media IDs:")
        for media_id in results['failed']:
            print(f"  - {media_id}")
    
    print("="*50)

if __name__ == "__main__":
    main()