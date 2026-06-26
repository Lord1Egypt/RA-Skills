#!/usr/bin/env python3
"""
批量详细分析小说
生成详细的分析报告
"""

import os
import re
import json
import time
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
NOVEL_DIR = BASE_DIR.parent / "novel_data" / "txt"
OUTPUT_DIR = BASE_DIR / "references" / "ch11-拆书档案" / "reports"
PROGRESS_FILE = BASE_DIR / "references" / "ch11-拆书档案" / "progress.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)


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


def extract_content(filepath, max_chars=10000):
    """提取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(max_chars)
        return content
    except:
        return ''


def extract_chapters(filepath):
    """提取章节数量"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        chapter_patterns = [
            r'第[一二三四五六七八九十百千万零\d]+[章节回]',
            r'Chapter\s*\d+',
            r'CHAPTER\s*\d+',
            r'【第[一二三四五六七八九十百千万零\d]+[章节回]】',
        ]
        
        chapter_count = 0
        for pattern in chapter_patterns:
            matches = re.findall(pattern, content)
            chapter_count = max(chapter_count, len(matches))
        
        return chapter_count
    except:
        return 0


def analyze_novel_detailed(filepath, filename):
    """详细分析小说"""
    content = extract_content(filepath)
    if not content:
        return None
    
    name = clean_novel_name(filename)
    file_size = os.path.getsize(filepath)
    word_count = file_size // 3
    chapter_count = extract_chapters(filepath)
    
    # 分析小说类型
    novel_type = "未知"
    type_keywords = {
        "变身文": ["变身", "男变女", "TS", "性转"],
        "穿越文": ["穿越", "重生", "转世"],
        "重生文": ["重生", "回到"],
        "转生文": ["转生", "异世界"]
    }
    
    for t, keywords in type_keywords.items():
        for kw in keywords:
            if kw in filename or kw in content[:2000]:
                novel_type = t
                break
        if novel_type != "未知":
            break
    
    # 分析变身类型
    transform_type = "未知"
    transform_keywords = {
        "男变女": ["男变女", "TS", "性转女"],
        "女变男": ["女变男"],
        "变萝莉": ["萝莉", "变萝"],
        "变妖物": ["狐", "蛇", "妖", "龙"]
    }
    
    for t, keywords in transform_keywords.items():
        for kw in keywords:
            if kw in filename:
                transform_type = t
                break
        if transform_type != "未知":
            break
    
    # 分析背景
    background = "未知"
    bg_keywords = {
        "火影同人": ["火影", "忍者"],
        "海贼同人": ["海贼", "恶魔果实"],
        "漫威同人": ["漫威", "复仇者"],
        "异世界": ["异世界", "异界"],
        "仙侠": ["修仙", "仙侠"],
        "校园": ["校园", "学院"]
    }
    
    for t, keywords in bg_keywords.items():
        for kw in keywords:
            if kw in filename or kw in content[:2000]:
                background = t
                break
        if background != "未知":
            break
    
    return {
        "filename": filename,
        "name": name,
        "type": novel_type,
        "transform_type": transform_type,
        "background": background,
        "word_count": word_count,
        "chapter_count": chapter_count,
        "file_size": file_size
    }


def generate_report(novel_info, content):
    """生成分析报告"""
    report = f"""# {novel_info['name']}

> 分析日期：{datetime.now().strftime('%Y-%m-%d')}

---

## 基本信息

| 属性 | 值 |
|------|------|
| **类型** | {novel_info['type']} |
| **变身类型** | {novel_info['transform_type']} |
| **背景** | {novel_info['background']} |
| **字数** | {novel_info['word_count']:,} |
| **章节数** | {novel_info['chapter_count']} |

---

## 内容摘要

{content[:500] if content else '无'}

---

*本报告由批量分析脚本自动生成*
"""
    return report


def load_progress():
    """加载进度"""
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_progress(progress):
    """保存进度"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def main():
    print("开始批量详细分析小说...")
    
    files = list(Path(NOVEL_DIR).glob("*.txt"))
    print(f"总文件数: {len(files)}")
    
    progress = load_progress()
    processed = set(progress.get('processed', []))
    
    count = 0
    for i, filepath in enumerate(files):
        if filepath.name in processed:
            continue
        
        if i % 10 == 0:
            print(f"处理进度: {i}/{len(files)}")
        
        try:
            info = analyze_novel_detailed(str(filepath), filepath.name)
            if info:
                content = extract_content(str(filepath))
                report = generate_report(info, content)
                
                report_file = OUTPUT_DIR / f"{info['name']}.md"
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(report)
                
                processed.add(filepath.name)
                count += 1
                
                if count % 50 == 0:
                    progress['processed'] = list(processed)
                    save_progress(progress)
        except Exception as e:
            print(f"处理失败: {filepath.name} - {e}")
            continue
    
    progress['processed'] = list(processed)
    progress['last_run'] = datetime.now().isoformat()
    save_progress(progress)
    
    print(f"\n分析完成!")
    print(f"本次处理: {count}")
    print(f"累计处理: {len(processed)}")


if __name__ == "__main__":
    main()
