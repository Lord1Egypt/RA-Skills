"""
AI 智能总结模块
使用 AI 生成文章内容摘要
"""

import json
import sys
from typing import Dict, List


class AISummarizer:
    """AI 总结器"""
    
    def __init__(self):
        self.max_summary_length = 300
        self.max_key_points = 5
    
    def summarize(self, content: str, title: str = '', platform: str = '') -> Dict:
        """
        生成文章总结
        
        Args:
            content: 文章内容
            title: 文章标题
            platform: 平台名称
        
        Returns:
            包含总结的字典
        """
        if not content:
            return {
                'success': False,
                'error': '内容为空'
            }
        
        # 分段
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        if not paragraphs:
            return {
                'success': False,
                'error': '无法分段'
            }
        
        # 提取关键段落（通常第一段和最后一段最重要）
        key_paragraphs = []
        if len(paragraphs) >= 1:
            key_paragraphs.append(paragraphs[0])  # 第一段
        if len(paragraphs) >= 2:
            key_paragraphs.append(paragraphs[-1])  # 最后一段
        if len(paragraphs) > 2:
            # 中间段落选最长的 3 段
            middle = paragraphs[1:-1]
            middle_sorted = sorted(middle, key=len, reverse=True)
            key_paragraphs.extend(middle_sorted[:3])
        
        # 生成一句话概述
        overview = self._generate_overview(title, key_paragraphs[0] if key_paragraphs else '')
        
        # 提取关键点
        key_points = self._extract_key_points(content)
        
        # 生成摘要
        summary = self._generate_summary(key_paragraphs)
        
        # 评估文章价值
        value_assessment = self._assess_value(content, platform)
        
        return {
            'success': True,
            'overview': overview,
            'key_points': key_points,
            'summary': summary,
            'word_count': len(content),
            'reading_time': max(1, len(content) // 300),
            'value_assessment': value_assessment
        }
    
    def _generate_overview(self, title: str, first_paragraph: str) -> str:
        """生成一句话概述"""
        if title:
            # 从标题提取关键信息
            overview = f"本文标题为\"{title}\""
            if first_paragraph:
                # 结合第一段
                first_sentence = first_paragraph.split('。')[0]
                if len(first_sentence) < 100:
                    overview += f"，{first_sentence}"
            return overview + "。"
        else:
            # 没有标题，直接用第一段
            if first_paragraph:
                first_sentence = first_paragraph.split('。')[0]
                return first_sentence + "。"
            return "文章内容概述。"
    
    def _extract_key_points(self, content: str) -> List[str]:
        """提取关键点"""
        key_points = []
        
        # 按句号分段
        sentences = [s.strip() for s in content.replace('！', '。').replace('？', '。').split('。') if s.strip()]
        
        # 筛选重要句子（包含数字、关键词等）
        important_keywords = ['重要', '关键', '首先', '其次', '最后', '总结', '因此', '所以', '但是', '然而']
        
        for sentence in sentences:
            score = 0
            
            # 包含数字（数据、统计）
            if any(c.isdigit() for c in sentence):
                score += 1
            
            # 包含关键词
            for keyword in important_keywords:
                if keyword in sentence:
                    score += 1
                    break
            
            # 句子长度适中
            if 20 < len(sentence) < 100:
                score += 1
            
            if score >= 2:
                key_points.append(sentence + '。')
            
            if len(key_points) >= self.max_key_points:
                break
        
        return key_points
    
    def _generate_summary(self, paragraphs: List[str]) -> str:
        """生成摘要"""
        if not paragraphs:
            return ''
        
        # 连接关键段落
        summary_parts = []
        total_length = 0
        
        for p in paragraphs:
            if total_length + len(p) <= self.max_summary_length:
                summary_parts.append(p)
                total_length += len(p)
            else:
                # 截断
                remaining = self.max_summary_length - total_length
                if remaining > 20:
                    summary_parts.append(p[:remaining] + '...')
                break
        
        return ' '.join(summary_parts)
    
    def _assess_value(self, content: str, platform: str) -> Dict:
        """评估文章价值"""
        assessment = {
            'credibility': '中等',  # 可信度
            'timeliness': '未知',   # 时效性
            'reference_value': '中等',  # 参考价值
            'recommendation': ''    # 推荐建议
        }
        
        # 根据平台评估可信度
        platform_credibility = {
            '今日头条': '中等',
            '微信公众号': '中等',
            '知乎': '较高',
            '雪球': '较高',
        }
        assessment['credibility'] = platform_credibility.get(platform, '中等')
        
        # 评估内容质量
        word_count = len(content)
        if word_count > 2000:
            assessment['reference_value'] = '较高'
            assessment['recommendation'] = '值得仔细阅读'
        elif word_count > 500:
            assessment['reference_value'] = '中等'
            assessment['recommendation'] = '快速浏览即可'
        else:
            assessment['reference_value'] = '较低'
            assessment['recommendation'] = '仅供参考'
        
        return assessment


def main():
    """测试"""
    test_content = """
    这是一篇测试文章的第一段，介绍了文章的背景和主题。
    第二段包含了一些重要的数据和统计信息，显示增长达到了 50%。
    第三段讨论了关键问题和挑战。
    第四段提出了解决方案和建议。
    最后一段总结了全文的主要观点。
    """
    
    summarizer = AISummarizer()
    result = summarizer.summarize(test_content, "测试文章标题", "今日头条")
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
