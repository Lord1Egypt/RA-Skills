#!/usr/bin/env python3
"""
文献矩阵生成工具
帮助整理和分析学术文献
"""

import csv
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class Literature:
    """文献数据结构"""
    id: str
    authors: str
    year: str
    title: str
    journal: str
    research_question: str = ""
    methodology: str = ""
    sample_size: str = ""
    key_findings: str = ""
    limitations: str = ""
    quality_score: int = 0
    relevance: str = "medium"  # high, medium, low
    notes: str = ""


class LiteratureMatrix:
    """文献矩阵管理器"""
    
    def __init__(self):
        self.literatures: List[Literature] = []
    
    def add_literature(self, lit: Literature) -> None:
        """添加文献"""
        self.literatures.append(lit)
    
    def load_from_csv(self, file_path: Path) -> None:
        """从CSV加载文献"""
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lit = Literature(
                    id=row.get('id', ''),
                    authors=row.get('authors', ''),
                    year=row.get('year', ''),
                    title=row.get('title', ''),
                    journal=row.get('journal', ''),
                    research_question=row.get('research_question', ''),
                    methodology=row.get('methodology', ''),
                    sample_size=row.get('sample_size', ''),
                    key_findings=row.get('key_findings', ''),
                    limitations=row.get('limitations', ''),
                    quality_score=int(row.get('quality_score', 0)),
                    relevance=row.get('relevance', 'medium'),
                    notes=row.get('notes', '')
                )
                self.literatures.append(lit)
    
    def save_to_csv(self, file_path: Path) -> None:
        """保存为CSV"""
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['id', 'authors', 'year', 'title', 'journal',
                         'research_question', 'methodology', 'sample_size',
                         'key_findings', 'limitations', 'quality_score',
                         'relevance', 'notes']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for lit in self.literatures:
                writer.writerow(asdict(lit))
    
    def save_to_json(self, file_path: Path) -> None:
        """保存为JSON"""
        data = [asdict(lit) for lit in self.literatures]
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def generate_markdown_table(self) -> str:
        """生成Markdown格式的文献表格"""
        lines = []
        
        # 表头
        headers = ['ID', '作者/年份', '标题', '研究问题', '方法', '主要发现', '质量评分']
        lines.append('| ' + ' | '.join(headers) + ' |')
        lines.append('|' + '|'.join(['---'] * len(headers)) + '|')
        
        # 数据行
        for lit in self.literatures:
            row = [
                lit.id,
                f"{lit.authors} ({lit.year})",
                lit.title[:30] + '...' if len(lit.title) > 30 else lit.title,
                lit.research_question[:20] + '...' if len(lit.research_question) > 20 else lit.research_question,
                lit.methodology[:15] + '...' if len(lit.methodology) > 15 else lit.methodology,
                lit.key_findings[:25] + '...' if len(lit.key_findings) > 25 else lit.key_findings,
                str(lit.quality_score)
            ]
            lines.append('| ' + ' | '.join(row) + ' |')
        
        return '\n'.join(lines)
    
    def generate_summary(self) -> str:
        """生成文献综述摘要"""
        summary = []
        summary.append("=" * 60)
        summary.append("文献矩阵摘要")
        summary.append("=" * 60)
        
        # 基本统计
        summary.append(f"\n文献总数: {len(self.literatures)}")
        
        # 按年份统计
        years = [lit.year for lit in self.literatures if lit.year]
        if years:
            summary.append(f"年份范围: {min(years)} - {max(years)}")
        
        # 按相关性统计
        relevance_count = {}
        for lit in self.literatures:
            relevance_count[lit.relevance] = relevance_count.get(lit.relevance, 0) + 1
        summary.append(f"相关性分布: {relevance_count}")
        
        # 高质量文献
        high_quality = [lit for lit in self.literatures if lit.quality_score >= 8]
        summary.append(f"\n高质量文献(评分≥8): {len(high_quality)}篇")
        
        if high_quality:
            summary.append("\n推荐阅读:")
            for lit in high_quality[:5]:
                summary.append(f"  - [{lit.id}] {lit.authors} ({lit.year}): {lit.title}")
        
        # 方法分布
        methods = {}
        for lit in self.literatures:
            if lit.methodology:
                method = lit.methodology.lower()
                methods[method] = methods.get(method, 0) + 1
        
        if methods:
            summary.append(f"\n研究方法分布:")
            for method, count in sorted(methods.items(), key=lambda x: x[1], reverse=True):
                summary.append(f"  - {method}: {count}篇")
        
        summary.append("\n" + "=" * 60)
        
        return '\n'.join(summary)
    
    def search(self, keyword: str) -> List[Literature]:
        """搜索文献"""
        results = []
        keyword_lower = keyword.lower()
        
        for lit in self.literatures:
            if (keyword_lower in lit.title.lower() or
                keyword_lower in lit.authors.lower() or
                keyword_lower in lit.key_findings.lower() or
                keyword_lower in lit.notes.lower()):
                results.append(lit)
        
        return results
    
    def filter_by_year(self, start_year: int, end_year: int) -> List[Literature]:
        """按年份筛选"""
        results = []
        for lit in self.literatures:
            try:
                year = int(lit.year)
                if start_year <= year <= end_year:
                    results.append(lit)
            except ValueError:
                continue
        return results
    
    def filter_by_quality(self, min_score: int) -> List[Literature]:
        """按质量评分筛选"""
        return [lit for lit in self.literatures if lit.quality_score >= min_score]


def create_template_csv(output_path: Path) -> None:
    """创建CSV模板"""
    template = Literature(
        id='001',
        authors='Smith, J. & Wang, L.',
        year='2023',
        title='Research on Example Topic',
        journal='Journal of Example',
        research_question='What is the effect of X on Y?',
        methodology='Quantitative survey',
        sample_size='500',
        key_findings='X has significant positive effect on Y',
        limitations='Sample limited to one region',
        quality_score=8,
        relevance='high',
        notes='Important for theoretical framework'
    )
    
    matrix = LiteratureMatrix()
    matrix.add_literature(template)
    matrix.save_to_csv(output_path)
    print(f"模板已创建: {output_path}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("文献矩阵生成工具")
        print("\n用法:")
        print("  生成模板: python generate_literature_matrix.py --template <输出文件>")
        print("  分析文献: python generate_literature_matrix.py <CSV文件>")
        print("  搜索文献: python generate_literature_matrix.py <CSV文件> --search <关键词>")
        print("\n示例:")
        print("  python generate_literature_matrix.py --template literature_template.csv")
        print("  python generate_literature_matrix.py literature.csv")
        print("  python generate_literature_matrix.py literature.csv --search machine learning")
        sys.exit(1)
    
    # 生成模板
    if sys.argv[1] == '--template':
        output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('literature_template.csv')
        create_template_csv(output_path)
        return
    
    # 加载并分析文献
    csv_path = Path(sys.argv[1])
    if not csv_path.exists():
        print(f"错误: 文件不存在 {csv_path}")
        sys.exit(1)
    
    matrix = LiteratureMatrix()
    matrix.load_from_csv(csv_path)
    
    # 搜索功能
    if len(sys.argv) > 2 and sys.argv[2] == '--search':
        keyword = ' '.join(sys.argv[3:])
        results = matrix.search(keyword)
        print(f"\n搜索 '{keyword}' 找到 {len(results)} 篇文献:")
        for lit in results:
            print(f"  [{lit.id}] {lit.authors} ({lit.year}): {lit.title}")
        return
    
    # 生成报告
    print(matrix.generate_summary())
    print("\n" + matrix.generate_markdown_table())
    
    # 保存结果
    output_json = csv_path.with_suffix('.json')
    matrix.save_to_json(output_json)
    print(f"\nJSON文件已保存: {output_json}")


if __name__ == '__main__':
    main()
