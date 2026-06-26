#!/usr/bin/env python3
"""
小红书数据分析 - 笔记搜索
用法: python3 search_notes.py --keyword "关键词" --limit 50
"""

import argparse
import json
import os
import sys
import time

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def load_config():
    """加载配置"""
    config = {}
    config_file = os.path.join(os.path.dirname(__file__), 'config.sh')
    
    # 读取环境变量
    config['api_key'] = os.environ.get('XHS_API_KEY', '')
    config['cookie'] = os.environ.get('XHS_COOKIE', '')
    config['delay'] = int(os.environ.get('REQUEST_DELAY', '2'))
    config['timeout'] = int(os.environ.get('REQUEST_TIMEOUT', '30'))
    
    return config

def search_notes(keyword, limit=50, sort='hot', category='笔记'):
    """
     sort='hot',搜索小红书笔记
    
    Args:
        keyword: 搜索关键词
        limit: 返回数量
        sort: 排序方式 (hot/latest/time)
        category: 笔记类型
    
    Returns:
        list: 笔记列表
    """
    config = load_config()
    
    # TODO: 实现实际API调用
    # 这里返回示例数据，用户需要配置自己的API
    
    if not config['api_key'] and not config['cookie']:
        # 返回示例数据用于测试
        print("[INFO] 未配置API密钥，返回示例数据", file=sys.stderr)
        return get_sample_notes(keyword, limit)
    
    # 实际API调用逻辑
    # headers = {"Authorization": f"Bearer {config['api_key']}"}
    # params = {"keyword": keyword, "limit": limit, "sort": sort}
    # response = requests.get(API_ENDPOINT, headers=headers, params=params, timeout=config['timeout'])
    
    return get_sample_notes(keyword, limit)

def get_sample_notes(keyword, limit):
    """生成示例数据"""
    notes = []
    for i in range(min(limit, 10)):
        notes.append({
            "note_id": f"note_{keyword}_{i}",
            "title": f"示例笔记 {keyword} #{i+1}",
            "author": f"博主{i+1}",
            "author_id": f"user_{i+1}",
            "likes": 1000 + i * 100,
            "收藏": 500 + i * 50,
            "comments": 50 + i * 5,
            "shares": 20 + i * 2,
            "tags": [keyword, "示例标签"],
            "create_time": "2026-03-01"
        })
    return notes

def main():
    parser = argparse.ArgumentParser(description='小红书笔记搜索')
    parser.add_argument('--keyword', '-k', required=True, help='搜索关键词')
    parser.add_argument('--limit', '-l', type=int, default=50, help='返回数量')
    parser.add_argument('--sort', '-s', default='hot', choices=['hot', 'latest', 'time'], help='排序方式')
    parser.add_argument('--category', '-c', default='笔记', help='笔记类型')
    parser.add_argument('--format', '-f', default='json', choices=['json', 'csv'], help='输出格式')
    parser.add_argument('--output', '-o', help='输出文件')
    
    args = parser.parse_args()
    
    # 搜索
    notes = search_notes(args.keyword, args.limit, args.sort, args.category)
    
    # 输出
    if args.format == 'json':
        output = json.dumps(notes, ensure_ascii=False, indent=2)
    else:
        # CSV格式
        if notes:
            headers = list(notes[0].keys())
            lines = [','.join(headers)]
            for note in notes:
                lines.append(','.join(str(note.get(h, '')) for h in headers))
            output = '\n'.join(lines)
        else:
            output = ''
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"结果已保存到: {args.output}")
    else:
        print(output)

if __name__ == '__main__':
    main()
