#!/usr/bin/env python3
"""
论文润色脚本
提供学术论文语言润色和格式规范检查功能
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class PaperPolisher:
    """学术论文润色工具"""
    
    def __init__(self):
        # 口语化词汇 -> 学术化词汇映射
        self.word_upgrades = {
            r'\blook at\b': 'examine',
            r'\bfind out\b': 'determine',
            r'\buse\b': 'utilize',
            r'\bget\b': 'obtain',
            r'\ba lot of\b': 'numerous',
            r'\bvery\b': 'significantly',
            r'\bbig\b': 'substantial',
            r'\bsmall\b': 'minimal',
            r'\bthing\b': 'aspect',
            r'\bshow\b': 'demonstrate',
            r'\btry\b': 'attempt',
            r'\bhelp\b': 'facilitate',
        }
        
        # 过度绝对化词汇
        self.absolute_words = [
            'prove', 'always', 'never', 'all', 'none',
            'definitely', 'obviously', 'certainly'
        ]
        
        # 学术连接词
        self.transition_words = {
            'addition': ['furthermore', 'moreover', 'additionally', 'in addition'],
            'contrast': ['however', 'nevertheless', 'conversely', 'on the other hand'],
            'cause': ['therefore', 'consequently', 'as a result', 'hence'],
            'example': ['for instance', 'specifically', 'notably', 'in particular'],
        }
    
    def check_grammar_issues(self, text: str) -> List[Dict]:
        """检查常见语法问题"""
        issues = []
        
        # 检查句子长度
        sentences = re.split(r'[.!?]+', text)
        for i, sent in enumerate(sentences):
            word_count = len(sent.split())
            if word_count > 30:
                issues.append({
                    'type': '长句',
                    'sentence': sent.strip()[:50] + '...',
                    'suggestion': f'句子过长({word_count}词)，建议拆分',
                    'line': i + 1
                })
        
        # 检查悬垂修饰语（简化版）
        dangling_pattern = r'\b(ing|ed)\b.*?,\s*[A-Z]'
        matches = re.finditer(dangling_pattern, text)
        for match in matches:
            issues.append({
                'type': '可能的悬垂修饰语',
                'text': match.group(),
                'suggestion': '检查修饰语逻辑主语是否一致'
            })
        
        # 检查被动语态使用（方法部分应多用）
        passive_count = len(re.findall(r'\b(was|were|is|are)\s+\w+ed\b', text))
        active_count = len(re.findall(r'\b(we|I)\s+\w+\b', text))
        
        return issues
    
    def check_academic_style(self, text: str) -> List[Dict]:
        """检查学术写作风格"""
        suggestions = []
        text_lower = text.lower()
        
        # 检查口语化表达
        for pattern, replacement in self.word_upgrades.items():
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                suggestions.append({
                    'type': '词汇升级',
                    'original': match.group(),
                    'suggested': replacement,
                    'message': f'建议将"{match.group()}"替换为"{replacement}"'
                })
        
        # 检查绝对化词汇
        for word in self.absolute_words:
            if re.search(rf'\b{word}\b', text_lower):
                suggestions.append({
                    'type': '过度绝对',
                    'word': word,
                    'message': f'避免使用绝对化词汇"{word}"，考虑使用更谨慎的表达'
                })
        
        return suggestions
    
    def check_citation_format(self, text: str) -> List[Dict]:
        """检查引用格式"""
        issues = []
        
        # 检测常见引用格式
        apa_pattern = r'\([A-Z][a-z]+,?\s*\d{4}\)'
        ieee_pattern = r'\[\d+\]'
        mla_pattern = r'\([A-Z][a-z]+\s+\d+\)'
        
        apa_citations = re.findall(apa_pattern, text)
        ieee_citations = re.findall(ieee_pattern, text)
        mla_citations = re.findall(mla_pattern, text)
        
        formats_found = []
        if apa_citations:
            formats_found.append('APA')
        if ieee_citations:
            formats_found.append('IEEE')
        if mla_citations:
            formats_found.append('MLA')
        
        if len(formats_found) > 1:
            issues.append({
                'type': '引用格式混乱',
                'formats': formats_found,
                'message': f'检测到多种引用格式：{", ".join(formats_found)}，建议统一'
            })
        
        return issues
    
    def analyze_text(self, text: str) -> Dict:
        """综合分析文本"""
        results = {
            'grammar': self.check_grammar_issues(text),
            'style': self.check_academic_style(text),
            'citations': self.check_citation_format(text),
            'statistics': {
                'word_count': len(text.split()),
                'sentence_count': len(re.split(r'[.!?]+', text)),
                'paragraph_count': len(text.split('\n\n')),
            }
        }
        
        return results
    
    def generate_report(self, analysis: Dict) -> str:
        """生成润色报告"""
        report = []
        report.append("=" * 60)
        report.append("学术论文润色分析报告")
        report.append("=" * 60)
        
        # 基本统计
        stats = analysis['statistics']
        report.append(f"\n【文本统计】")
        report.append(f"词数: {stats['word_count']}")
        report.append(f"句数: {stats['sentence_count']}")
        report.append(f"段落数: {stats['paragraph_count']}")
        
        # 语法问题
        if analysis['grammar']:
            report.append(f"\n【语法问题】({len(analysis['grammar'])}项)")
            for i, issue in enumerate(analysis['grammar'][:5], 1):
                report.append(f"{i}. {issue['type']}: {issue['suggestion']}")
        
        # 风格建议
        if analysis['style']:
            report.append(f"\n【风格优化建议】({len(analysis['style'])}项)")
            for i, sugg in enumerate(analysis['style'][:5], 1):
                report.append(f"{i}. {sugg['message']}")
        
        # 引用格式
        if analysis['citations']:
            report.append(f"\n【引用格式检查】")
            for issue in analysis['citations']:
                report.append(f"- {issue['message']}")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python polish_paper.py <文本文件>")
        print("示例: python polish_paper.py paper.txt")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"错误: 文件不存在 {file_path}")
        sys.exit(1)
    
    text = file_path.read_text(encoding='utf-8')
    polisher = PaperPolisher()
    analysis = polisher.analyze_text(text)
    report = polisher.generate_report(analysis)
    
    print(report)
    
    # 保存报告
    report_path = file_path.with_suffix('.polish_report.txt')
    report_path.write_text(report, encoding='utf-8')
    print(f"\n报告已保存至: {report_path}")


if __name__ == '__main__':
    main()
