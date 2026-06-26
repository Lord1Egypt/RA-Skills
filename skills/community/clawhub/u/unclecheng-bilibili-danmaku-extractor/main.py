#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B站弹幕提取工具
提取指定视频的所有弹幕，输出JSON和Markdown格式文件
"""

import re
import json
import argparse
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import requests

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com/',
    'Origin': 'https://www.bilibili.com'
}


def extract_bvid(url_or_bvid: str) -> str:
    """从URL或字符串中提取BV号"""
    if url_or_bvid.startswith("BV"):
        return url_or_bvid
    match = re.search(r'BV[\w]+', url_or_bvid)
    if match:
        return match.group()
    raise ValueError(f"无法从 '{url_or_bvid}' 中提取BV号")


def get_video_info(bvid: str) -> dict:
    """获取视频信息"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
    data = resp.json()
    if data['code'] == 0:
        info = data['data']
        return {
            'bvid': bvid,
            'title': info.get('title', '未知标题'),
            'desc': info.get('desc', ''),
            'owner': info.get('owner', {}).get('name', '未知UP主'),
            'stat': info.get('stat', {}),
            'duration': info.get('duration', 0),
            'cid': info.get('cid', 0),
            'pubdate': info.get('pubdate', 0)
        }
    raise ValueError(f"获取视频信息失败: {data.get('message', 'Unknown error')}")


def get_danmakus(cid: str) -> list:
    """获取视频所有弹幕"""
    url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
    resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=15)
    resp.encoding = 'utf-8'
    danmakus = []

    type_map = {1: '滚动', 4: '底端', 5: '顶端', 6: '逆向', 7: '高级', 8: '代码'}

    try:
        root = ET.fromstring(resp.text)
        for d in root.findall('d'):
            p = d.get('p', '').split(',')
            if len(p) >= 5:
                danmakus.append({
                    'text': d.text or '',
                    'time': float(p[0]),
                    'type': type_map.get(int(p[1]), '未知'),
                    'type_code': int(p[1]),
                    'color': p[3],
                    'timestamp': int(p[4])
                })
    except ET.ParseError:
        import zlib
        try:
            decompressed = zlib.decompress(resp.content)
            root = ET.fromstring(decompressed.decode('utf-8'))
            for d in root.findall('d'):
                p = d.get('p', '').split(',')
                if len(p) >= 5:
                    danmakus.append({
                        'text': d.text or '',
                        'time': float(p[0]),
                        'type': type_map.get(int(p[1]), '未知'),
                        'type_code': int(p[1]),
                        'color': p[3],
                        'timestamp': int(p[4])
                    })
        except Exception as e:
            print(f"弹幕解压解析失败: {e}")

    return danmakus


def format_time(seconds: float) -> str:
    """将秒数格式化为 mm:ss 或 hh:mm:ss"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def export_to_json(video_info: dict, danmakus: list, output_dir: Path) -> Path:
    """导出弹幕到JSON文件"""
    export_data = {
        'video_info': {
            'bvid': video_info['bvid'],
            'title': video_info['title'],
            'owner': video_info['owner'],
            'duration': video_info['duration'],
            'stat': video_info['stat'],
            'pubdate': video_info['pubdate']
        },
        'export_time': datetime.now().isoformat(),
        'total_count': len(danmakus),
        'danmakus': danmakus
    }

    output_path = output_dir / f"{video_info['bvid']}_弹幕_{len(danmakus)}条.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    return output_path


def export_to_markdown(video_info: dict, danmakus: list, output_dir: Path) -> Path:
    """导出弹幕到Markdown文件"""
    lines = []
    lines.append(f"# {video_info['title']}")
    lines.append("")
    lines.append(f"> **BV号**: `{video_info['bvid']}`  ")
    lines.append(f"> **UP主**: {video_info['owner']}  ")
    lines.append(f"> **弹幕总数**: {len(danmakus)} 条  ")
    lines.append(f"> **导出时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"**视频简介**: {video_info['desc'][:200]}{'...' if len(video_info['desc']) > 200 else ''}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"## 全部弹幕 (共 {len(danmakus)} 条)")
    lines.append("")

    for i, d in enumerate(danmakus, 1):
        time_str = format_time(d['time'])
        text = d['text'].replace('\n', ' ')
        lines.append(f"`[{time_str}]` {text}")

    output_path = output_dir / f"{video_info['bvid']}_弹幕_{len(danmakus)}条.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return output_path


def main():
    parser = argparse.ArgumentParser(description='B站弹幕提取工具')
    parser.add_argument('url', help='B站视频链接或BV号')
    parser.add_argument('-o', '--output', help='输出目录 (默认: 当前目录)', default='.')
    args = parser.parse_args()

    try:
        bvid = extract_bvid(args.url)
        print(f"正在提取弹幕: {bvid}")

        print("正在获取视频信息...")
        video_info = get_video_info(bvid)
        title = video_info['title']
        cid = video_info.get('cid', 0)

        if not cid:
            raise ValueError("无法获取视频CID，请检查视频链接是否有效")

        print(f"正在获取弹幕 (视频: {title})...")
        danmakus = get_danmakus(str(cid))
        print(f"获取到 {len(danmakus)} 条弹幕")

        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)

        print("正在导出JSON文件...")
        json_path = export_to_json(video_info, danmakus, output_dir)
        print(f"JSON已保存: {json_path}")

        print("正在导出Markdown文件...")
        md_path = export_to_markdown(video_info, danmakus, output_dir)
        print(f"Markdown已保存: {md_path}")

        print("\n" + "=" * 60)
        print("导出完成!")
        print("=" * 60)
        print(f"视频: {title}")
        print(f"弹幕数: {len(danmakus)} 条")
        print(f"JSON: {json_path}")
        print(f"Markdown: {md_path}")

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())