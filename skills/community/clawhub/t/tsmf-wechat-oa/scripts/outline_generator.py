#!/usr/bin/env python3
"""
大纲生成模块
根据主题自动生成文章结构
"""

from typing import List, Dict, Tuple
import re


class OutlineGenerator:
    """文章大纲生成器"""
    
    # 文章类型模板
    TEMPLATES = {
        'tech': {
            'name': '技术文章',
            'structure': [
                {'title': '引言', 'type': 'intro', 'ratio': 0.10},
                {'title': '背景介绍', 'type': 'background', 'ratio': 0.15},
                {'title': '核心内容', 'type': 'main', 'ratio': 0.40},
                {'title': '实践案例', 'type': 'example', 'ratio': 0.20},
                {'title': '总结与展望', 'type': 'conclusion', 'ratio': 0.15},
            ]
        },
        'business': {
            'name': '商业分析',
            'structure': [
                {'title': '现象描述', 'type': 'intro', 'ratio': 0.10},
                {'title': '背景分析', 'type': 'background', 'ratio': 0.20},
                {'title': '深度解读', 'type': 'analysis', 'ratio': 0.35},
                {'title': '案例支撑', 'type': 'case', 'ratio': 0.20},
                {'title': '趋势判断', 'type': 'conclusion', 'ratio': 0.15},
            ]
        },
        'life': {
            'name': '生活方式',
            'structure': [
                {'title': '开篇引入', 'type': 'intro', 'ratio': 0.10},
                {'title': '个人经历/观察', 'type': 'story', 'ratio': 0.25},
                {'title': '深入探讨', 'type': 'main', 'ratio': 0.35},
                {'title': '实用建议', 'type': 'tips', 'ratio': 0.20},
                {'title': '结语感悟', 'type': 'conclusion', 'ratio': 0.10},
            ]
        },
        'tutorial': {
            'name': '教程指南',
            'structure': [
                {'title': '教程简介', 'type': 'intro', 'ratio': 0.10},
                {'title': '准备工作', 'type': 'prerequisite', 'ratio': 0.15},
                {'title': '步骤详解', 'type': 'steps', 'ratio': 0.50},
                {'title': '常见问题', 'type': 'faq', 'ratio': 0.15},
                {'title': '总结', 'type': 'conclusion', 'ratio': 0.10},
            ]
        },
        'review': {
            'name': '评测评论',
            'structure': [
                {'title': '产品/服务介绍', 'type': 'intro', 'ratio': 0.10},
                {'title': '外观/第一印象', 'type': 'appearance', 'ratio': 0.15},
                {'title': '核心体验', 'type': 'experience', 'ratio': 0.40},
                {'title': '优缺点分析', 'type': 'analysis', 'ratio': 0.20},
                {'title': '购买建议', 'type': 'conclusion', 'ratio': 0.15},
            ]
        }
    }
    
    # 主题关键词映射
    TOPIC_KEYWORDS = {
        'tech': ['技术', '编程', '代码', '开发', 'AI', '人工智能', '算法', '系统', '架构', '工具', '软件', 'Python', 'JavaScript', '前端', '后端'],
        'business': ['商业', '市场', '行业', '企业', '创业', '投资', '经济', '战略', '管理', '分析', '趋势', '报告'],
        'life': ['生活', '日常', '情感', '读书', '旅行', '美食', '咖啡', '随笔', '感悟', '故事'],
        'tutorial': ['教程', '指南', '如何', '怎么', '步骤', '方法', '入门', '新手', '攻略'],
        'review': ['评测', '测评', '体验', '试用', '推荐', '对比', '哪个好', '值得买']
    }
    
    def __init__(self):
        pass
    
    def analyze_topic(self, topic: str) -> Tuple[str, float]:
        """
        分析话题类型
        
        Returns:
            (article_type, confidence)
        """
        topic_lower = topic.lower()
        scores = {}
        
        for article_type, keywords in self.TOPIC_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                if keyword in topic_lower:
                    score += 1
            scores[article_type] = score
        
        # 找最高分
        if max(scores.values()) == 0:
            return 'life', 0.5  # 默认生活方式
        
        best_type = max(scores, key=scores.get)
        confidence = scores[best_type] / sum(scores.values())
        
        return best_type, confidence
    
    def generate_outline(self, topic: str, word_count: int = 1500, style: str = None) -> Dict:
        """
        生成文章大纲
        
        Args:
            topic: 文章主题
            word_count: 目标字数
            style: 指定风格（可选）
            
        Returns:
            完整大纲字典
        """
        # 分析话题类型
        article_type, confidence = self.analyze_topic(topic)
        if style:
            article_type = style
        
        # 获取模板
        template = self.TEMPLATES.get(article_type, self.TEMPLATES['life'])
        
        # 构建大纲
        outline = {
            'topic': topic,
            'type': article_type,
            'type_name': template['name'],
            'word_count': word_count,
            'confidence': confidence,
            'sections': []
        }
        
        # 生成各章节
        for section_template in template['structure']:
            section_words = int(word_count * section_template['ratio'])
            section = {
                'title': section_template['title'],
                'type': section_template['type'],
                'word_count': section_words,
                'key_points': self._generate_key_points(section_template['type'], topic),
                'content': ''  # 待填充
            }
            outline['sections'].append(section)
        
        return outline
    
    def _generate_key_points(self, section_type: str, topic: str) -> List[str]:
        """生成章节关键点提示"""
        prompts = {
            'intro': [
                f'引出{topic}话题',
                '吸引读者兴趣',
                '点明文章价值'
            ],
            'background': [
                f'{topic}的发展背景',
                '相关概念解释',
                '现状概述'
            ],
            'main': [
                f'{topic}的核心内容',
                '深入分析',
                '关键要点'
            ],
            'example': [
                f'{topic}的实际应用',
                '具体案例',
                '效果展示'
            ],
            'conclusion': [
                '总结要点',
                '未来展望',
                '行动建议'
            ],
            'analysis': [
                '深度分析',
                '数据支撑',
                '逻辑论证'
            ],
            'case': [
                '典型案例',
                '成功/失败经验',
                '启示总结'
            ],
            'story': [
                '个人经历',
                '真实感受',
                '情感共鸣'
            ],
            'tips': [
                '实用技巧',
                '操作建议',
                '注意事项'
            ],
            'steps': [
                '详细步骤',
                '操作说明',
                '图文配合'
            ],
            'experience': [
                '使用体验',
                '优缺点',
                '对比分析'
            ]
        }
        
        return prompts.get(section_type, ['内容要点'])
    
    def adjust_outline(self, outline: Dict, adjustments: Dict) -> Dict:
        """
        根据用户反馈调整大纲
        
        Args:
            outline: 原大纲
            adjustments: 调整指令
            
        Returns:
            调整后的大纲
        """
        adjusted = outline.copy()
        
        # 调整字数
        if 'word_count' in adjustments:
            new_count = adjustments['word_count']
            ratio = new_count / outline['word_count']
            for section in adjusted['sections']:
                section['word_count'] = int(section['word_count'] * ratio)
            adjusted['word_count'] = new_count
        
        # 调整章节
        if 'sections' in adjustments:
            # 添加、删除或修改章节
            pass
        
        return adjusted
    
    def outline_to_text(self, outline: Dict) -> str:
        """将大纲转换为可读文本"""
        lines = []
        lines.append(f"# {outline['topic']}")
        lines.append(f"类型：{outline['type_name']} | 目标字数：{outline['word_count']}字")
        lines.append('')
        
        for i, section in enumerate(outline['sections'], 1):
            lines.append(f"## {i}. {section['title']} ({section['word_count']}字)")
            for point in section['key_points']:
                lines.append(f"- {point}")
            lines.append('')
        
        return '\n'.join(lines)


# 便捷函数
def quick_outline(topic: str, word_count: int = 1500) -> Dict:
    """快速生成大纲"""
    generator = OutlineGenerator()
    return generator.generate_outline(topic, word_count)


def analyze_article_type(topic: str) -> str:
    """分析文章类型"""
    generator = OutlineGenerator()
    article_type, _ = generator.analyze_topic(topic)
    return article_type
