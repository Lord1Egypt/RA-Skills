#!/usr/bin/env python3
"""
批量分析小说
提取小说类型、变身类型、背景等信息
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
NOVEL_DIR = BASE_DIR.parent / "novel_data" / "txt"
OUTPUT_DIR = BASE_DIR / "references" / "ch11-拆书档案"


def clean_novel_name(filename):
    """清理小说文件名"""
    name = filename.replace('.txt', '')
    name = re.sub(r'_\d+$', '', name)
    name = re.sub(r'_Unicode$', '', name)
    name = re.sub(r'_作者.*', '', name)
    name = re.sub(r'⊙.*', '', name)
    name = re.sub(r'_tags_.*', '', name)
    name = re.sub(r'\(\d+\)$', '', name)
    name = re.sub(r'（.*）$', '', name)
    name = re.sub(r'《|》', '', name)
    name = re.sub(r'【.*】', '', name)
    name = re.sub(r'_第.*章.*', '', name)
    return name.strip()


def extract_novel_info(filepath, max_lines=100):
    """提取小说信息"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = ''
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                content += line
        return content
    except:
        return ''


def analyze_novel(filepath, filename):
    """分析小说"""
    content = extract_novel_info(filepath)
    if not content:
        return None

    name = clean_novel_name(filename)

    novel_type = "未知"
    if "变身" in filename or "变身" in content[:500]:
        novel_type = "变身文"
    elif "穿越" in filename or "穿越" in content[:500]:
        novel_type = "穿越文"
    elif "重生" in filename or "重生" in content[:500]:
        novel_type = "重生文"
    elif "转生" in filename or "转生" in content[:500]:
        novel_type = "转生文"

    transform_type = "未知"
    if "男变女" in filename or "TS" in filename.upper():
        transform_type = "男变女"
    elif "女变男" in filename:
        transform_type = "女变男"
    elif "萝莉" in filename or "萝" in filename:
        transform_type = "变萝莉"
    elif "狐" in filename or "蛇" in filename or "妖" in filename:
        transform_type = "变妖物"
    elif "萌" in filename:
        transform_type = "变萌妹"

    background = "未知"
    if "火影" in filename:
        background = "火影同人"
    elif "海贼" in filename:
        background = "海贼同人"
    elif "漫威" in filename:
        background = "漫威同人"
    elif "异世界" in filename or "异界" in filename:
        background = "异世界"
    elif "仙侠" in filename or "修仙" in filename:
        background = "仙侠"
    elif "校园" in filename or "学院" in filename:
        background = "校园"
    elif "末世" in filename:
        background = "末世"

    file_size = os.path.getsize(filepath)
    word_count = file_size // 3

    return {
        "filename": filename,
        "name": name,
        "type": novel_type,
        "transform_type": transform_type,
        "background": background,
        "word_count": word_count,
        "file_size": file_size
    }


def main():
    print("开始批量分析小说...")
    files = list(Path(NOVEL_DIR).glob("*.txt"))
    print(f"总文件数: {len(files)}")

    results = []
    seen_names = set()

    for i, filepath in enumerate(files):
        if i % 100 == 0:
            print(f"处理进度: {i}/{len(files)}")

        info = analyze_novel(str(filepath), filepath.name)
        if info and info['name'] not in seen_names:
            results.append(info)
            seen_names.add(info['name'])

    print(f"去重后小说数: {len(results)}")

    results.sort(key=lambda x: x['word_count'], reverse=True)

    output_file = os.path.join(OUTPUT_DIR, "novel_list.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"分析结果已保存到: {output_file}")

    type_stats = {}
    for r in results:
        t = r['type']
        type_stats[t] = type_stats.get(t, 0) + 1

    print("\n类型统计:")
    for t, c in sorted(type_stats.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")

    transform_stats = {}
    for r in results:
        t = r['transform_type']
        transform_stats[t] = transform_stats.get(t, 0) + 1

    print("\n变身类型统计:")
    for t, c in sorted(transform_stats.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")

    background_stats = {}
    for r in results:
        t = r['background']
        background_stats[t] = background_stats.get(t, 0) + 1

    print("\n背景统计:")
    for t, c in sorted(background_stats.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")


if __name__ == "__main__":
    main()
