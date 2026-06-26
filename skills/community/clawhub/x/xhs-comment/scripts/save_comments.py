"""
小红书评论数据保存脚本
用法: python save_comments.py <json_data> <output_dir>
或直接通过 stdin 传入 JSON
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def parse_likes(likes_str):
    """将点赞数字符串转换为整数"""
    if not likes_str:
        return 0
    s = likes_str.strip().replace(',', '')
    if '万' in s:
        return int(float(s.replace('万', '')) * 10000)
    try:
        return int(s)
    except ValueError:
        return 0


def save_comments(data, output_dir=None):
    """保存评论数据到JSON文件"""
    if output_dir is None:
        output_dir = Path.home() / "Downloads" / "xhs_comments"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    blogger_name = data.get('blogger', {}).get('name', 'unknown')
    note_id = data.get('note', {}).get('id', 'unknown')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    filename = f"xhs_comments_{blogger_name}_{note_id}_{timestamp}.json"
    filepath = output_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"已保存: {filepath}")
    print(f"共 {len(data.get('comments', []))} 条评论")
    return str(filepath)


def main():
    if len(sys.argv) > 1:
        # 从命令行参数读取 JSON
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        # 从 stdin 读取
        data = json.load(sys.stdin)
        output_dir = None

    result_path = save_comments(data, output_dir)
    print(result_path)


if __name__ == '__main__':
    main()
