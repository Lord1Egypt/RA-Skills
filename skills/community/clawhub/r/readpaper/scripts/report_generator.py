#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文内容提取器 - v7.0 简化版
提取论文结构化内容，供AI直接生成中文报告

提取内容：
1. 论文基本信息（标题、期刊、作者、发表时间、DOI）
2. 摘要
3. 研究背景
4. 研究方法
5. 图表信息
6. 研究结果
7. 结论
"""

import os
import re
from datetime import datetime
from pathlib import Path


class PaperReportGenerator:
    """论文内容提取器 - 提取结构化内容供AI分析"""
    
    def __init__(self):
        # 期刊名称中英文对照
        self.journal_translations = {
            'Nature': '自然',
            'Science': '科学',
            'PNAS': '美国科学院院刊',
            'Nature Climate Change': '自然·气候变化',
            'Nature Communications': '自然·通讯',
            'Geoscientific Model Development': '地球科学模型发展',
            'Atmospheric Chemistry and Physics': '大气化学与物理',
            'Journal of Climate': '气候期刊',
            'Journal of Geophysical Research': '地球物理研究期刊',
            'Environmental Research Letters': '环境研究快报',
            'Earth System Dynamics': '地球系统动力学',
            'Acta Oceanologica Sinica': '海洋学报（英文版）',
            'Science Advances': '科学进展',
            'Nature Geoscience': '自然·地球科学',
            'Nature Reviews Earth & Environment': '自然·综述：地球与环境',
        }
    
    def extract_paper_metadata(self, content):
        """提取论文元数据"""
        metadata = {
            'title': '',
            'authors': '',
            'affiliation': '',
            'journal': '',
            'journal_cn': '',
            'year': '',
            'doi': ''
        }
        
        if not content:
            return metadata
        
        lines = content.split('\n')
        clean_lines = [l.strip() for l in lines if l.strip()]
        
        # 提取DOI
        doi_match = re.search(r'10\.\d{4,}/[^\s\n]{5,}', content)
        if doi_match:
            metadata['doi'] = doi_match.group(0)
        
        # 提取年份
        year_patterns = [
            r'Published[:\s]+(\d{1,2}\s+\w+\s+(\d{4}))',
            r'Published[:\s]+(\d{4})',
            r'Accepted[:\s]+\d{1,2}\s+\w+\s+(\d{4})',
            r'©\s*(\d{4})',
        ]
        for pattern in year_patterns:
            match = re.search(pattern, content[:10000])
            if match:
                year = match.group(1) if match.lastindex == 1 else match.group(2)
                if year and len(year) == 4:
                    metadata['year'] = year
                    break
        
        if not metadata['year']:
            years = re.findall(r'\b(20\d{2})\b', content[:5000])
            if years:
                metadata['year'] = max(years)
        
        # 提取期刊名称
        journal_list = [
            'Nature Reviews Earth & Environment',
            'Nature Geoscience',
            'Geoscientific Model Development',
            'Atmospheric Chemistry and Physics',
            'Nature', 'Science', 'Science Advances', 'PNAS',
            'Nature Climate Change', 'Nature Communications',
            'Journal of Climate', 'Journal of Geophysical Research',
            'Environmental Research Letters', 'Earth System Dynamics',
            'Acta Oceanologica Sinica',
        ]
        for journal in journal_list:
            if journal.lower() in content[:8000].lower():
                metadata['journal'] = journal
                metadata['journal_cn'] = self.journal_translations.get(journal, journal)
                break
        
        # 提取标题
        abstract_pos = content.lower().find('abstract')
        if abstract_pos > 0:
            pre_abstract = content[:abstract_pos]
            pre_lines = [l.strip() for l in pre_abstract.split('\n') if l.strip()]
            
            title_candidates = []
            current_title = []
            
            for i, line in enumerate(pre_lines[-20:]):
                skip_keywords = ['abstract', 'author', 'received', 'published', 'doi', 'http', 
                               'correspondence', 'keywords', 'introduction', '©', 'creative commons',
                               'creativecommons', 'this work', 'distribution']
                if any(kw in line.lower() for kw in skip_keywords):
                    if current_title:
                        title_candidates.append(' '.join(current_title))
                        current_title = []
                    continue
                
                if 20 < len(line) < 200 and (line[0].isupper() or '\u4e00' <= line[0] <= '\u9fff'):
                    if not re.search(r'[0-9]{4,}', line) and '@' not in line:
                        current_title.append(line)
                elif current_title:
                    title_candidates.append(' '.join(current_title))
                    current_title = []
            
            if current_title:
                title_candidates.append(' '.join(current_title))
            
            if title_candidates:
                valid_titles = [t for t in title_candidates if len(t) > 30 and '©' not in t]
                if valid_titles:
                    metadata['title'] = max(valid_titles, key=len)[:200]
        
        # 提取作者
        author_patterns = [
            r'([A-Z][a-z]+\s+[A-Z]\.?\s+[A-Z][a-z]+(?:\d,?\d?)?(?:\s*,\s*[A-Z][a-z]+\s+[A-Z]\.?\s+[A-Z][a-z]+(?:\d,?\d?)?)*)',
            r'([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+(?:\s*,\s*[A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+)*)',
        ]
        
        for pattern in author_patterns:
            matches = re.findall(pattern, content[:3000])
            for match in matches:
                names = re.findall(r'[A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+', match)
                if len(names) >= 2:
                    clean_authors = re.sub(r'\d', '', match).strip()
                    clean_authors = re.sub(r'\s+', ' ', clean_authors)
                    if len(clean_authors) > 20 and len(clean_authors) < 300:
                        metadata['authors'] = clean_authors[:200]
                        break
            if metadata['authors']:
                break
        
        # 提取作者单位
        affiliation_keywords = ['university', 'institute', 'laboratory', 'center', 'centre', 
                               'college', 'school', 'department', 'division', 'csiro', 'bureau']
        
        for line in clean_lines[5:50]:
            if any(kw in line.lower() for kw in affiliation_keywords):
                if len(line) > 20 and len(line) < 250:
                    affil = re.sub(r'^\d+\s*', '', line).strip()
                    if affil[0].isupper():
                        metadata['affiliation'] = affil[:200]
                        break
        
        return metadata
    
    def extract_abstract(self, content):
        """提取摘要"""
        if not content:
            return None
        
        patterns = [
            r'Abstract[.\s]*\n(.+?)(?=\n\s*(?:1\.?\s+|Introduction|Keywords|1\s+Introduction))',
            r'ABSTRACT[.\s]*\n(.+?)(?=\n\s*(?:1\.?\s+|INTRODUCTION|KEYWORDS))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                abstract = match.group(1).strip()
                abstract = re.sub(r'\s+', ' ', abstract)
                return abstract[:3000]
        
        lines = content.split('\n')
        for i, line in enumerate(lines[:80]):
            if 'abstract' in line.lower():
                abstract_lines = []
                for j in range(i+1, min(i+30, len(lines))):
                    text = lines[j].strip()
                    if text and 'introduction' not in text.lower() and 'keywords' not in text.lower():
                        abstract_lines.append(text)
                    elif len(' '.join(abstract_lines)) > 200:
                        break
                if abstract_lines:
                    return ' '.join(abstract_lines)[:3000]
        
        return None
    
    def extract_background(self, content):
        """提取背景信息"""
        if not content:
            return None
        
        patterns = [
            r'(?:1\.?\s+)?Introduction[.\s]*\n(.+?)(?=\n\s*(?:2\.?\s+|Methods?|Methodology|Data))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                intro = match.group(1).strip()
                paragraphs = [p.strip() for p in intro.split('\n\n') if len(p.strip()) > 80]
                return paragraphs[:8]
        
        return None
    
    def extract_methodology(self, content):
        """提取方法介绍"""
        if not content:
            return None
        
        patterns = [
            r'(?:2\.?\s+)?(?:Methods?|Methodology|Data and methods)[.\s]*\n(.+?)(?=\n\s*(?:3\.?\s+|Results?|Discussion))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                methods_text = match.group(1).strip()
                return methods_text[:3000]
        
        return None
    
    def extract_figures_and_tables(self, content):
        """提取图表信息 - 改进版，能更好地识别所有图表"""
        if not content:
            return []
        
        items = []
        seen = set()  # 用于去重
        
        # 提取Figure - 改进的正则，更好地匹配图表标题
        fig_pattern = r'(?:Figure|Fig\.?)\s*(\d+)[.:]?\s*\n?\s*([^\n]+(?:\n(?![A-Z][a-z]+\s*\d|[Ff]ig|[Tt]able)[^\n]*)*)'
        for match in re.finditer(fig_pattern, content, re.IGNORECASE):
            fig_num = match.group(1)
            caption = match.group(2).strip()
            caption = re.sub(r'\s+', ' ', caption)[:600]
            
            # 去重：同一图表只保留一次
            key = f"fig_{fig_num}"
            if key not in seen and len(caption) > 10:
                seen.add(key)
                items.append({
                    'type': '图',
                    'number': fig_num,
                    'caption': caption
                })
        
        # 提取Table
        table_pattern = r'(?:Table)\s*(\d+)[.:]?\s*\n?\s*([^\n]+(?:\n(?![A-Z][a-z]+\s*\d|[Ff]ig|[Tt]able)[^\n]*)*)'
        for match in re.finditer(table_pattern, content, re.IGNORECASE):
            table_num = match.group(1)
            caption = match.group(2).strip()
            caption = re.sub(r'\s+', ' ', caption)[:600]
            
            key = f"table_{table_num}"
            if key not in seen and len(caption) > 10:
                seen.add(key)
                items.append({
                    'type': '表',
                    'number': table_num,
                    'caption': caption
                })
        
        # 按类型和编号排序
        items.sort(key=lambda x: (0 if x['type'] == '图' else 1, int(x['number'])))
        
        return items[:20]
    
    def extract_results(self, content):
        """提取研究结果"""
        if not content:
            return None
        
        patterns = [
            r'(?:3\.?\s+)?(?:Results?)[.\s]*\n(.+?)(?=\n\s*(?:4\.?\s+|Discussion|Conclusions?))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:3000]
        
        return None
    
    def extract_conclusion(self, content):
        """提取结论"""
        if not content:
            return None
        
        patterns = [
            r'(?:Conclusions?|Summary)[.\s]*\n(.+?)(?=\n\s*(?:Acknowledgments?|References?|Appendix|\Z))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()[:2500]
        
        return None
    
    def extract_all_content(self, pdf_path, content):
        """提取所有论文内容，返回结构化数据"""
        
        metadata = self.extract_paper_metadata(content)
        abstract = self.extract_abstract(content)
        background = self.extract_background(content)
        methods = self.extract_methodology(content)
        figures_tables = self.extract_figures_and_tables(content)
        results = self.extract_results(content)
        conclusion = self.extract_conclusion(content)
        
        return {
            'metadata': metadata,
            'abstract': abstract,
            'background': background,
            'methods': methods,
            'figures_tables': figures_tables,
            'results': results,
            'conclusion': conclusion,
            'raw_content': content[:8000]  # 保留部分原始内容供参考
        }


def generate_filename(pdf_path, output_dir="."):
    """根据PDF文件名生成报告文件名"""
    filename = os.path.basename(pdf_path)
    base_name = os.path.splitext(filename)[0]
    
    clean_name = re.sub(r'[<>:"/\\|?*]', '', base_name)
    if len(clean_name) > 120:
        clean_name = clean_name[:120].strip()
    
    return os.path.join(output_dir, f"{clean_name}_报告.md")


def save_report(report_content, pdf_path, output_dir="."):
    """保存报告到文件"""
    report_file = generate_filename(pdf_path, output_dir)
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        return report_file
    except Exception as e:
        print(f"保存报告失败: {e}")
        return None


if __name__ == "__main__":
    print("论文内容提取器 v7.0（简化版）")
    print("=" * 60)
    print("功能：提取论文结构化内容，供AI生成中文报告")
