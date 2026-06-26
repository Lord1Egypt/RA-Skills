#!/usr/bin/env python3
"""
repeat_detect.py - 轻量重复模式检测脚本
检测同一问题是否在 30 天内出现 ≥3 次、跨 2 个以上任务
仅做提示，不做系统性修复
"""

import os
import re
import datetime

REFLECTIONS_DIR = os.path.expanduser("~/.openclaw/workspace/reflections")
MISTAKES_FILE = os.path.join(REFLECTIONS_DIR, "mistakes.md")
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")

# ==================== 关键词提取 ====================

def extract_keywords_from_content(content):
    """从错误描述中提取关键词"""
    # 去除代码块、URL等干扰
    text = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', ' ', text)
    # 提取长度2-10的词作为关键词
    keywords = re.findall(r'[\u4e00-\u9fa5]{2,10}|[a-zA-Z]{3,15}', text)
    # 过滤常见无意义词
    stopwords = {'错误', '问题', '修复', '解决', '处理', '方法', '描述', '记录', '更新'}
    keywords = [k for k in keywords if k not in stopwords and len(k) >= 2]
    return keywords

# ==================== 30天内同一问题检测 ====================

def detect_repeated_problems():
    """检测30天内同一问题出现≥3次的情况"""
    if not os.path.exists(MISTAKES_FILE):
        return []
    
    with open(MISTAKES_FILE, encoding="utf-8") as f:
        content = f.read()
    
    # 提取所有错误条目（表格行）
    table_match = re.search(r'\| 日期 \|.*?\n\|.*?\|', content, re.DOTALL)
    if not table_match:
        return []
    
    table_text = table_match.group(0)
    rows = [r.strip() for r in table_text.split('\n') if r.strip().startswith('|') and '---' not in r]
    
    # 解析表格行
    entries = []
    today = datetime.datetime.now()
    thirty_days_ago = today - datetime.timedelta(days=30)
    
    for row in rows:
        cols = [c.strip() for c in row.split('|')[1:-1]]
        if len(cols) < 7:
            continue
        date_str = cols[0]
        error_desc = cols[1]
        try:
            entry_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            if entry_date >= thirty_days_ago:
                keywords = extract_keywords_from_content(error_desc)
                entries.append({
                    "date": date_str,
                    "description": error_desc,
                    "keywords": keywords
                })
        except ValueError:
            continue
    
    # 按关键词分组，统计出现次数
    keyword_count = {}
    keyword_entries = {}
    
    for entry in entries:
        for kw in entry["keywords"]:
            if len(kw) < 3:
                continue
            if kw not in keyword_count:
                keyword_count[kw] = 0
                keyword_entries[kw] = []
            keyword_count[kw] += 1
            keyword_entries[kw].append(entry)
    
    # 找出现 ≥3 次的关键词
    repeated = []
    for kw, count in keyword_count.items():
        if count >= 3:
            unique_dates = set(e["date"] for e in keyword_entries[kw])
            if len(unique_dates) >= 2:
                repeated.append({
                    "keyword": kw,
                    "count": count,
                    "dates": sorted(unique_dates),
                    "entries": keyword_entries[kw]
                })
    
    return repeated

# ==================== 输出报告 ====================

def generate_report(repeated_problems):
    """生成重复问题报告"""
    if not repeated_problems:
        return None
    
    lines = ["⚠️ 检测到重复问题，建议从根因解决：\n"]
    
    for item in repeated_problems:
        lines.append(f"关键词「{item['keyword']}」")
        lines.append(f"  出现次数：{item['count']} 次")
        lines.append(f"  涉及日期：{', '.join(item['dates'])}")
        lines.append(f"  最近描述：{item['entries'][-1]['description'][:60]}...")
        lines.append("")
    
    lines.append("建议：不是修一个一个的条目，而是从系统层面找根本原因。")
    lines.append("  1. 这些条目的共同特征是什么？")
    lines.append("  2. 是流程问题还是工具问题？")
    lines.append("  3. 如何从源头避免再次发生？")
    
    return "\n".join(lines)

def main():
    print("正在检测重复问题（30天内 ≥3次、跨 ≥2个任务）...")
    
    repeated = detect_repeated_problems()
    
    if repeated:
        report = generate_report(repeated)
        print(f"\n{report}")
    else:
        print("未检测到重复问题 ✓")

if __name__ == "__main__":
    main()
