#!/usr/bin/env python3
"""
火山引擎PDF目录提取脚本
提取PDF的目录结构、章节概览，帮助决定重点提取内容
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
        
        # 如果没有找到明确的目录页，检查前5页中类似目录的结构
        if not toc_pages:
            print("未找到明确的目录页，检查前5页中的结构...")
            for page_num in range(min(5, total_pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # 检查是否有章节编号模式（如 "1. ", "2.1 ", "3.2.1 "）
                lines = text.split('\n')
                chapter_lines = []
                
                for line in lines:
                    line = line.strip()
                    # 匹配章节编号模式
                    if re.match(r'^\d+(\.\d+)*[\s\.].+', line):
                        chapter_lines.append(line)
                
                if len(chapter_lines) > 3:  # 至少有3个章节行
                    toc_pages.append(page_num + 1)
                    toc_content.append({
                        'page': page_num + 1,
                        'text': text
                    })
                    print(f"发现疑似目录结构: 第 {page_num + 1} 页")
        
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
                    page_ref = int(page_match.group(1))
                    # 从标题中移除页号
                    chapter_title = re.sub(r'\s*\d+$', '', chapter_title)
                
                chapters.append({
                    'number': chapter_num,
                    'title': chapter_title,
                    'page_ref': page_ref,
                    'source_page': page_num
                })
            
            # 匹配非编号的标题（如 "附录"、"参考文献"）
            elif line and len(line) > 2 and not line[0].isdigit():
                # 检查是否是重要的非编号章节
                important_keywords = ['附录', '参考文献', '索引', '术语表', 'API', 'SDK', '认证', '配置']
                if any(keyword in line for keyword in important_keywords):
                    chapters.append({
                        'number': None,
                        'title': line,
                        'page_ref': None,
                        'source_page': page_num
                    })
    
    return chapters

def extract_chapter_previews(pdf_reader, chapters, preview_lines=10):
    """提取每个章节的预览内容"""
    chapter_details = []
    
    for chapter in chapters:
        # 如果有页号参考，提取该页的预览
        if chapter['page_ref'] and chapter['page_ref'] <= len(pdf_reader.pages):
            try:
                page_idx = chapter['page_ref'] - 1  # 转换为0-based索引
                page = pdf_reader.pages[page_idx]
                text = page.extract_text()
                
                if text:
                    lines = text.split('\n')
                    preview = '\n'.join(lines[:preview_lines])
                    
                    chapter_details.append({
                        'chapter': chapter,
                        'preview_page': chapter['page_ref'],
                        'preview_content': preview,
                        'preview_length': len(text)
                    })
            except Exception as e:
                print(f"提取章节 {chapter['number']} 预览时出错: {e}")
    
    return chapter_details

def categorize_chapters(chapters):
    """根据标题对章节进行分类，识别对volcengine技能重要的部分"""
    categories = {
        'authentication': {'keywords': ['API Key', '认证', '鉴权', 'Access', 'Token'], 'chapters': []},
        'endpoints': {'keywords': ['API', '接口', 'Endpoint', 'URL', '对话', 'Chat', 'Completion'], 'chapters': []},
        'models': {'keywords': ['模型', 'Model', '参数', 'Parameter', '配置', 'Configuration'], 'chapters': []},
        'error_handling': {'keywords': ['错误', 'Error', '状态码', 'Status Code', '异常', 'Exception'], 'chapters': []},
        'usage_examples': {'keywords': ['示例', 'Example', '使用', 'Usage', '最佳实践', 'Best Practice'], 'chapters': []},
        'sdk': {'keywords': ['SDK', '客户端', 'Client', '库', 'Library'], 'chapters': []},
        'other': {'keywords': [], 'chapters': []}
    }
    
    for chapter in chapters:
        title = chapter['title'].lower() if chapter['title'] else ''
        
        categorized = False
        for cat_name, cat_info in categories.items():
            if cat_name == 'other':
                continue
                
            for keyword in cat_info['keywords']:
                if keyword.lower() in title:
                    categories[cat_name]['chapters'].append(chapter)
                    categorized = True
                    break
            if categorized:
                break
        
        if not categorized:
            categories['other']['chapters'].append(chapter)
    
    return categories

def generate_extraction_plan(categories, total_pages):
    """根据分类生成提取计划"""
    plan = {
        'priority_high': [],
        'priority_medium': [],
        'priority_low': []
    }
    
    # 高优先级：认证、端点、错误处理
    high_priority_cats = ['authentication', 'endpoints', 'error_handling']
    for cat in high_priority_cats:
        for chapter in categories[cat]['chapters']:
            plan['priority_high'].append({
                'chapter': chapter,
                'reason': f"关键配置信息: {cat}"
            })
    
    # 中优先级：模型、使用示例
    medium_priority_cats = ['models', 'usage_examples']
    for cat in medium_priority_cats:
        for chapter in categories[cat]['chapters']:
            plan['priority_medium'].append({
                'chapter': chapter,
                'reason': f"重要参考信息: {cat}"
            })
    
    # 低优先级：SDK、其他
    low_priority_cats = ['sdk', 'other']
    for cat in low_priority_cats:
        for chapter in categories[cat]['chapters']:
            plan['priority_low'].append({
                'chapter': chapter,
                'reason': f"补充信息: {cat}"
            })
    
    return plan

def main():
    if len(sys.argv) < 2:
        print("用法: python extract-pdf-toc.py <pdf文件路径>")
        print("示例: python extract-pdf-toc.py volcengine-api-reference.pdf")
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
        print("\n⚠️  未找到目录页，将分析前20页的内容结构...")
        # 提取前20页的文本进行简单分析
        preview_pages = min(20, len(pdf_reader.pages))
        all_text = ""
        for i in range(preview_pages):
            page = pdf_reader.pages[i]
            text = page.extract_text()
            if text:
                all_text += f"\n--- 第 {i+1} 页 ---\n{text[:500]}"
        
        print(f"\n前{preview_pages}页预览:")
        print(all_text[:2000] + "..." if len(all_text) > 2000 else all_text)
        return
    
    print(f"\n✅ 找到 {len(toc_pages)} 个目录页: {toc_pages}")
    
    # 2. 分析目录结构
    chapters = analyze_toc_content(toc_content)
    print(f"\n✅ 提取到 {len(chapters)} 个章节:")
    for i, chapter in enumerate(chapters[:20]):  # 只显示前20个
        print(f"  {chapter['number'] or 'N/A'}: {chapter['title'][:50]}{'...' if len(chapter['title']) > 50 else ''} (页: {chapter['page_ref']})")
    
    if len(chapters) > 20:
        print(f"  ... 还有 {len(chapters) - 20} 个章节")
    
    # 3. 提取章节预览
    chapter_details = extract_chapter_previews(pdf_reader, chapters, preview_lines=5)
    print(f"\n✅ 提取了 {len(chapter_details)} 个章节的预览")
    
    # 4. 分类章节
    categories = categorize_chapters(chapters)
    print("\n📊 章节分类统计:")
    for cat_name, cat_info in categories.items():
        if cat_info['chapters']:
            print(f"  {cat_name}: {len(cat_info['chapters'])} 个章节")
    
    # 5. 生成提取计划
    plan = generate_extraction_plan(categories, len(pdf_reader.pages))
    
    print("\n🎯 提取计划建议:")
    print("\n高优先级 (立即提取):")
    for item in plan['priority_high'][:5]:  # 只显示前5个
        chapter = item['chapter']
        print(f"  • {chapter['number']}: {chapter['title'][:40]} - {item['reason']}")
    
    print("\n中优先级 (后续提取):")
    for item in plan['priority_medium'][:5]:
        chapter = item['chapter']
        print(f"  • {chapter['number']}: {chapter['title'][:40]} - {item['reason']}")
    
    print("\n低优先级 (可选提取):")
    for item in plan['priority_low'][:3]:
        chapter = item['chapter']
        print(f"  • {chapter['number']}: {chapter['title'][:40]} - {item['reason']}")
    
    # 6. 保存分析结果
    output_data = {
        'pdf_file': pdf_path,
        'total_pages': len(pdf_reader.pages),
        'toc_pages': toc_pages,
        'chapters': chapters,
        'categories': {k: [c['title'] for c in v['chapters']] for k, v in categories.items()},
        'extraction_plan': plan
    }
    
    output_file = Path(pdf_path).stem + '_toc_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 分析结果已保存到: {output_file}")
    
    # 7. 提取建议
    print("\n📋 下一步建议:")
    if plan['priority_high']:
        print("1. 立即提取高优先级章节（认证、API端点、错误处理）")
        print("2. 验证现有volcengine技能的准确性")
        print("3. 补充缺失的关键配置信息")
    
    print("\n⏱️  预计工作量:")
    print(f"  • 高优先级: {len(plan['priority_high'])} 章 × 10-15分钟 ≈ {len(plan['priority_high']) * 15} 分钟")
    print(f"  • 中优先级: {len(plan['priority_medium'])} 章 × 5-10分钟 ≈ {len(plan['priority_medium']) * 10} 分钟")
    print(f"  • 低优先级: {len(plan['priority_low'])} 章 × 2-5分钟 ≈ {len(plan['priority_low']) * 5} 分钟")

if __name__ == "__main__":
    main()