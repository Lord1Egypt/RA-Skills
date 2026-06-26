#!/usr/bin/env python3
"""
小红书数据分析 - 竞品对比
用法: python3 compare.py --users "用户1,用户2,用户3"
"""

import argparse
import json
import os
import sys

def load_config():
    config = {}
    config['api_key'] = os.environ.get('XHS_API_KEY', '')
    config['cookie'] = os.environ.get('XHS_COOKIE', '')
    return config

def compare_users(user_ids):
    """对比多个博主"""
    config = load_config()
    
    if not config['api_key'] and not config['cookie']:
        print("[INFO] 未配置API密钥，返回示例数据", file=sys.stderr)
        return get_sample_comparison(user_ids)
    
    return get_sample_comparison(user_ids)

def get_sample_comparison(user_ids):
    """生成示例对比数据"""
    users = user_ids.split(',') if ',' in user_ids else [user_ids]
    
    comparison = {
        "type": "user_comparison",
        "users": []
    }
    
    for i, user_id in enumerate(users):
        comparison["users"].append({
            "rank": i + 1,
            "user_id": user_id.strip(),
            "nickname": f"博主{i+1}",
            "fans": 10000 + i * 5000,
            "posts": 100 + i * 20,
            "avg_likes": 800 + i * 200,
            "avg_collects": 400 + i * 100,
            "engagement_rate": 3.5 + i * 0.5
        })
    
    # 排序
    comparison["users"].sort(key=lambda x: x['fans'], reverse=True)
    
    # 添加排名
    for i, u in enumerate(comparison["users"]):
        u["rank"] = i + 1
    
    return comparison

def main():
    parser = argparse.ArgumentParser(description='小红书竞品对比')
    parser.add_argument('--users', '-u', help='用户ID列表 (逗号分隔)')
    parser.add_argument('--notes', '-n', help='笔记ID列表 (逗号分隔)')
    parser.add_argument('--format', '-f', default='json', help='输出格式')
    
    args = parser.parse_args()
    
    if args.users:
        result = compare_users(args.users)
    elif args.notes:
        result = {"type": "note_comparison", "notes": args.notes.split(',')}
    else:
        print("请指定 --users 或 --notes")
        sys.exit(1)
    
    output = json.dumps(result, ensure_ascii=False, indent=2)
    print(output)

if __name__ == '__main__':
    main()
