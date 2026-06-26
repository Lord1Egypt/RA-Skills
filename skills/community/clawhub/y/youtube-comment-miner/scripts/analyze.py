#!/usr/bin/env python3
"""
YouTube 评论分析工具
用法: python3 analyze.py [folder]
"""
import json
import os
import sys
from collections import Counter

def load_comments(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data.get('comments', [])

def categorize_comment(text):
    text_lower = text.lower()
    categories = []
    
    # 问题分类
    if any(k in text_lower for k in ['error', 'fail', 'bug', 'not working', 'stuck', 'cannot', "can't", 'unable', 'crash', "doesn't work"]):
        categories.append('问题-技术')
    if any(k in text_lower for k in ['install', 'deploy', 'setup', '配置', '部署', '安装', 'hostinger']):
        categories.append('问题-安装部署')
    if any(k in text_lower for k in ['security', 'privacy', 'safe', 'hack', 'injection', '安全', '隐私', 'vulnerability']):
        categories.append('问题-安全')
    if any(k in text_lower for k in ['ollama', 'local', 'model', 'gpu', 'ram', 'cost', 'expensive', 'token', 'price', 'free']):
        categories.append('问题-成本')
    if any(k in text_lower for k in ['slow', 'performance', 'fast', 'speed', 'memory']):
        categories.append('问题-性能')
    
    # 建议分类
    if any(k in text_lower for k in ['should', 'would be nice', 'wish', 'hope', 'suggest', '建议', '希望', 'please']):
        categories.append('建议-功能')
    if any(k in text_lower for k in ['document', 'tutorial', 'video', 'explain', '文档', '教程', 'guide']):
        categories.append('建议-文档')
    
    return categories if categories else ['其他']

def analyze_folder(folder='.'):
    all_comments = []
    files_processed = []
    
    for f in os.listdir(folder):
        if f.startswith('openclaw_') and f.endswith('.json') and 'analysis' not in f:
            try:
                comments = load_comments(os.path.join(folder, f))
                all_comments.extend(comments)
                files_processed.append(f)
            except Exception as e:
                print(f"Error loading {f}: {e}")
    
    # 分类统计
    category_counts = Counter()
    issues = []
    
    for comment in all_comments:
        text = comment.get('text', '')
        if len(text) < 15:  # 跳过太短的评论
            continue
        cats = categorize_comment(text)
        for cat in cats:
            category_counts[cat] += 1
        if any(c.startswith('问题') for c in cats):
            issues.append({
                'text': text[:500],
                'likes': comment.get('like_count', 0),
                'author': comment.get('author', 'unknown'),
                'categories': cats
            })
    
    # 按点赞排序
    issues.sort(key=lambda x: x['likes'], reverse=True)
    
    return {
        'total_comments': len(all_comments),
        'files_processed': len(files_processed),
        'category_counts': dict(category_counts),
        'issue_examples': issues[:100]
    }

def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print(f"📂 分析文件夹: {folder}")
    print("-" * 40)
    
    result = analyze_folder(folder)
    
    print(f"✅ 总评论数: {result['total_comments']}")
    print(f"📁 处理文件数: {result['files_processed']}")
    print(f"\n📊 分类统计:")
    for cat, count in sorted(result['category_counts'].items(), key=lambda x: -x[1]):
        print(f"   {cat}: {count}")
    
    # 保存分析结果
    output_file = os.path.join(folder, 'analysis_result.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n💾 分析结果已保存到: {output_file}")
    
    # 显示 Top 10 问题
    print(f"\n🔝 Top 10 问题评论:")
    for i, issue in enumerate(result['issue_examples'][:10], 1):
        print(f"\n{i}. [{issue['likes']}👍] @{issue['author']}")
        print(f"   {issue['text'][:150]}...")

if __name__ == '__main__':
    main()
