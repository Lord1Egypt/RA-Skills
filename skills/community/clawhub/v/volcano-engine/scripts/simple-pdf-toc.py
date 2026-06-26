#!/usr/bin/env python3
"""
火山引擎PDF目录提取脚本（简化版）
提取PDF的目录结构、章节概览
"""

import PyPDF2
import re
import json
import sys
from pathlib import Path

def extract_toc_from_pdf(pdf_path):
    """从PDF提取目录结构"""
    print(f"分析PDF文件: {pdf_path}")
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        print(f"总页数: {total_pages}")
        
        # 寻找目录页（通常在前10页）
        toc_pages = []
        toc_content = []
        
        for page_num in range(min(10, total_pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            
            # 检查是否是目录页
            if text and ('目录' in text or 'Contents' in text or 'Table of Contents' in text):
                toc_pages.append(page_num + 1)
                toc_content.append({
                    'page': page_num + 1,
                    'text': text
                })
                print(f"找到目录页: 第 {page_num + 1} 页")
        
        return pdf_reader, toc_pages, toc_content

def analyze_toc_content(toc_content):
    """分析目录内容，提取章节结构"""
    chapters = []
    
    for toc in toc_content:
        text = toc['text']
        page_num = toc['page']
        
        # 分割成行
        lines = text.split('\n')
        
        # 寻找章节标题
        for line in lines:
            line = line.strip()
            
            # 匹配章节编号 (如 "1. ", "2.1 ", "3.2.1 ")
            chapter_match = re.match(r'^(\d+(?:\.\d+)*)[\s\.]+(.+)', line)
            if chapter_match:
                chapter_num = chapter_match.group(1)
                chapter_title = chapter_match.group(2).strip()
                
                # 简单提取页号（如果存在）
                page_match = re.search(r'(\d+)$', chapter_title)
                page_ref = None
                if page_match:
                    try:
                        page_ref = int(page_match.group(1))
                        # 从标题中移除页号
                        chapter_title = re.sub(r'\s*\d+$', '', chapter_title)
                    except:
                        pass
                
                chapters.append({
                    'number': chapter_num,
                    'title': chapter_title,
                    'page_ref': page_ref,
                    'source_page': page_num
                })
    
    return chapters

def categorize_chapters(chapters):
    """根据标题对章节进行分类"""
    categories = {
        'authentication': {'keywords': ['API Key', '认证', '鉴权', 'Access', 'Token'], 'chapters': []},
        'endpoints': {'keywords': ['API', '接口', 'Endpoint', 'URL', '对话', 'Chat', 'Completion'], 'chapters': []},
        'models': {'keywords': ['模型', 'Model', '参数', 'Parameter'], 'chapters': []},
        'error_handling': {'keywords': ['错误', 'Error', '状态码', 'Status Code'], 'chapters': []},
        'usage_examples': {'keywords': ['示例', 'Example', '使用', 'Usage'], 'chapters': []},
        'sdk': {'keywords': ['SDK', '客户端', 'Client'], 'chapters': []},
        'other': {'keywords': [], 'chapters': []}
    }
    
    for chapter in chapters:
        if not chapter['title']:
            categories['other']['chapters'].append(chapter)
            continue
            
        title_lower = chapter['title'].lower()
        
        categorized = False
        for cat_name, cat_info in categories.items():
            if cat_name == 'other':
                continue
                
            for keyword in cat_info['keywords']:
                if keyword.lower() in title_lower:
                    categories[cat_name]['chapters'].append(chapter)
                    categorized = True
                    break
            if categorized:
                break
        
        if not categorized:
            categories['other']['chapters'].append(chapter)
    
    return categories

def main():
    if len(sys.argv) < 2:
        print("用法: python simple-pdf-toc.py <pdf文件路径>")
        print("示例: python simple-pdf-toc.py volcengine-api-reference.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not Path(pdf_path).exists():
        print(f"错误: 文件不存在: {pdf_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("火山引擎PDF目录提取分析")
    print("=" * 60)
    
    # 1. 提取目录
    pdf_reader, toc_pages, toc_content = extract_toc_from_pdf(pdf_path)
    
    if not toc_content:
        print("未找到目录页")
        sys.exit(1)
    
    print(f"找到 {len(toc_pages)} 个目录页: {toc_pages}")
    
    # 2. 分析目录结构
    chapters = analyze_toc_content(toc_content)
    print(f"提取到 {len(chapters)} 个章节:")
    
    # 显示所有章节
    for i, chapter in enumerate(chapters):
        title_preview = chapter['title'][:50] + "..." if len(chapter['title']) > 50 else chapter['title']
        print(f"  {chapter['number']}: {title_preview} (页: {chapter['page_ref']})")
    
    # 3. 分类章节
    categories = categorize_chapters(chapters)
    print("\n章节分类统计:")
    for cat_name, cat_info in categories.items():
        if cat_info['chapters']:
            print(f"  {cat_name}: {len(cat_info['chapters'])} 个章节")
    
    # 4. 生成提取建议
    print("\n提取建议 (基于volcengine技能需求):")
    print("\n1. 高优先级 - 立即提取:")
    high_priority = ['authentication', 'endpoints', 'error_handling']
    for cat in high_priority:
        if categories[cat]['chapters']:
            print(f"  {cat}:")
            for chapter in categories[cat]['chapters'][:3]:  # 只显示前3个
                print(f"    - {chapter['number']}: {chapter['title']}")
    
    print("\n2. 中优先级 - 后续提取:")
    medium_priority = ['models', 'usage_examples']
    for cat in medium_priority:
        if categories[cat]['chapters']:
            print(f"  {cat}:")
            for chapter in categories[cat]['chapters'][:2]:
                print(f"    - {chapter['number']}: {chapter['title']}")
    
    print("\n3. 低优先级 - 可选:")
    low_priority = ['sdk', 'other']
    for cat in low_priority:
        if categories[cat]['chapters']:
            count = len(categories[cat]['chapters'])
            print(f"  {cat}: {count} 个章节")
    
    # 5. 保存结果
    output_data = {
        'pdf_file': pdf_path,
        'total_pages': len(pdf_reader.pages),
        'toc_pages': toc_pages,
        'chapters': chapters,
        'categories': {k: [{'title': c['title'], 'number': c['number'], 'page': c['page_ref']} for c in v['chapters']] for k, v in categories.items()}
    }
    
    output_file = Path(pdf_path).stem + '_toc_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n分析结果已保存到: {output_file}")
    
    # 6. 下一步建议
    print("\n下一步建议:")
    auth_count = len(categories['authentication']['chapters'])
    endpoint_count = len(categories['endpoints']['chapters'])
    
    if auth_count > 0 or endpoint_count > 0:
        print("1. 立即提取认证和API端点章节")
        print("2. 验证现有volcengine技能的API配置")
        print("3. 补充错误处理信息")
    
    print("\n预计工作量:")
    high_count = sum(len(categories[cat]['chapters']) for cat in high_priority)
    medium_count = sum(len(categories[cat]['chapters']) for cat in medium_priority)
    print(f"  • 高优先级: {high_count} 章 × 10-15分钟")
    print(f"  • 中优先级: {medium_count} 章 × 5-10分钟")

if __name__ == "__main__":
    main()