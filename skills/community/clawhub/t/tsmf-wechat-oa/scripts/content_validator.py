#!/usr/bin/env python3
"""
内容搜索与验证模块
确保文章内容的准确性和真实性
"""

import re
from typing import List, Dict, Tuple


class ContentValidator:
    """内容搜索与验证模块"""
    
    # 需要验证的关键词模式
    FACT_PATTERNS = [
        r'\d{4}年',  # 年份
        r'\d+\.?\d*\s*%',  # 百分比
        r'\d+\s*亿',  # 金额
        r'\d+\s*万',  # 数量
        r'据.*统计',  # 统计数据
        r'研究显示',  # 研究结论
        r'报告指出',  # 报告引用
    ]
    
    def __init__(self):
        self.search_cache = {}
    
    def identify_facts_to_verify(self, content: str) -> List[Dict]:
        """
        识别内容中需要验证的事实
        
        Returns:
            List of dicts with 'text', 'type', 'confidence'
        """
        facts = []
        
        for pattern in self.FACT_PATTERNS:
            matches = re.finditer(pattern, content)
            for match in matches:
                # 提取上下文
                start = max(0, match.start() - 20)
                end = min(len(content), match.end() + 20)
                context = content[start:end]
                
                facts.append({
                    'text': match.group(),
                    'context': context,
                    'type': self._classify_fact_type(match.group()),
                    'position': (match.start(), match.end())
                })
        
        return facts
    
    def _classify_fact_type(self, text: str) -> str:
        """分类事实类型"""
        if '年' in text:
            return 'time'
        elif '%' in text:
            return 'percentage'
        elif '亿' in text or '万' in text:
            return 'number'
        elif '统计' in text or '研究' in text or '报告' in text:
            return 'citation'
        return 'other'
    
    def verify_critical_facts(self, outline: List[Dict]) -> Tuple[List[Dict], List[str]]:
        """
        验证大纲中的关键事实
        
        Args:
            outline: 文章大纲
            
        Returns:
            (verified_outline, warnings)
        """
        warnings = []
        verified_outline = []
        
        for section in outline:
            verified_section = section.copy()
            
            # 检查每个章节的关键点
            if 'key_points' in section:
                verified_points = []
                for point in section['key_points']:
                    # 识别需要验证的事实
                    facts = self.identify_facts_to_verify(point)
                    
                    if facts:
                        # 标记需要验证
                        verified_points.append({
                            'content': point,
                            'needs_verification': True,
                            'facts': facts
                        })
                        warnings.append(f"章节 '{section.get('title', '未命名')}' 中的事实需要验证: {point[:50]}...")
                    else:
                        verified_points.append({
                            'content': point,
                            'needs_verification': False
                        })
                
                verified_section['key_points'] = verified_points
            
            verified_outline.append(verified_section)
        
        return verified_outline, warnings
    
    def generate_search_queries(self, topic: str, article_type: str) -> List[str]:
        """
        生成搜索查询
        
        Args:
            topic: 文章主题
            article_type: 文章类型 (tech/life/business等)
            
        Returns:
            List of search queries
        """
        queries = []
        
        # 基础查询
        queries.append(f"{topic} 最新")
        queries.append(f"{topic} 2024 2025")
        
        # 根据文章类型添加特定查询
        if article_type == 'tech':
            queries.extend([
                f"{topic} 技术趋势",
                f"{topic} 发展现状",
                f"{topic} 应用案例"
            ])
        elif article_type == 'business':
            queries.extend([
                f"{topic} 市场分析",
                f"{topic} 行业报告",
                f"{topic} 数据统计"
            ])
        elif article_type == 'life':
            queries.extend([
                f"{topic} 指南",
                f"{topic} 推荐",
                f"{topic} 经验"
            ])
        
        return queries
    
    def validate_content_accuracy(self, content: str, sources: List[Dict]) -> Dict:
        """
        验证内容准确性
        
        Args:
            content: 文章内容
            sources: 搜索到的来源
            
        Returns:
            Validation report
        """
        report = {
            'total_facts': 0,
            'verified_facts': 0,
            'unverified_facts': 0,
            'warnings': [],
            'suggestions': []
        }
        
        facts = self.identify_facts_to_verify(content)
        report['total_facts'] = len(facts)
        
        for fact in facts:
            # 在来源中查找验证
            verified = False
            for source in sources:
                if fact['text'] in source.get('content', ''):
                    verified = True
                    report['verified_facts'] += 1
                    break
            
            if not verified:
                report['unverified_facts'] += 1
                report['warnings'].append(
                    f"未验证的事实: {fact['context'][:60]}..."
                )
        
        # 生成建议
        if report['unverified_facts'] > 0:
            report['suggestions'].append(
                f"建议核实 {report['unverified_facts']} 个未验证的事实"
            )
        
        return report


# 便捷函数
def verify_article_facts(content: str) -> Tuple[bool, List[str]]:
    """
    快速验证文章事实
    
    Returns:
        (is_valid, warnings)
    """
    validator = ContentValidator()
    facts = validator.identify_facts_to_verify(content)
    
    if not facts:
        return True, []
    
    warnings = [f"需要验证: {f['context'][:50]}..." for f in facts]
    return False, warnings


def get_search_queries_for_topic(topic: str, style: str = 'general') -> List[str]:
    """获取主题的搜索查询"""
    validator = ContentValidator()
    return validator.generate_search_queries(topic, style)
