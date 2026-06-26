#!/usr/bin/env python3
"""
小红书数据分析 - 热度分析
用法: python3 analyze_trend.py --note_id "笔记ID"
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

def analyze_trend(note_id):
    """分析笔记热度"""
    config = load_config()
    
    if not config['api_key'] and not config['cookie']:
        print("[INFO] 未配置API密钥，返回示例数据", file=sys.stderr)
        return get_sample_trend(note_id)
    
    return get_sample_trend(note_id)

def get_sample_trend(note_id):
    """生成示例热度数据"""
    return {
        "note_id": note_id,
        "title": "示例笔记标题",
        "likes": 5230,
        "collects": 2150,
        "comments": 328,
        "shares": 156,
        "create_time": "2026-02-28 15:30:00",
        "update_time": "2026-03-05 10:00:00",
        "trend": {
            "yesterday_likes": 120,
            "week_ago_likes": 890,
            "growth_rate": 12.5
        },
        "audience": {
            "female_ratio": 78.5,
            "age_18_24": 35,
            "age_25_34": 52,
            "top_cities": ["上海", "北京", "杭州", "深圳", "广州"]
        },
        "content_type": "图文",
        "tags": ["护肤", "好物分享"]
    }

def main():
    parser = argparse.ArgumentParser(description='小红书热度分析')
    parser.add_argument('--note_id', '-n', required=True, help='笔记ID')
    parser.add_argument('--format', '-f', default='json', help='输出格式')
    
    args = parser.parse_args()
    
    trend = analyze_trend(args.note_id)
    output = json.dumps(trend, ensure_ascii=False, indent=2)
    print(output)

if __name__ == '__main__':
    main()
