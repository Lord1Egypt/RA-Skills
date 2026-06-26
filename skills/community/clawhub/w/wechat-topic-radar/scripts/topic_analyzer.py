#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选题分析和推荐引擎
提供选题角度切入建议、竞品分析和内容差异化建议
"""

import json
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import jieba
import jieba.posseg as pseg
from collections import defaultdict

from data_collector import HotTopic
from heat_algorithm import HeatScore


@dataclass
class TopicAnalysis:
    """选题分析结果"""
    original_topic: HotTopic
    heat_score: HeatScore
    
    # 分析结果
    angles: List[Dict] = field(default_factory=list)  # 切入角度建议
    competitors: List[Dict] = field(default_factory=list)  # 竞品分析
    differentiation: Dict = field(default_factory=dict)  # 差异化建议
    content_plan: Dict = field(default_factory=dict)  # 内容规划
    

@dataclass
class ContentAngle:
    """内容切入角度"""
    angle_type: str  # 角度类型
    title: str  # 建议标题
    hook: str  # 开篇钩子
    structure: List[str]  # 文章结构
    key_points: List[str]  # 关键论点
    target_emotion: str  # 目标情绪
    estimated_effect: str  # 预期效果


class TopicAnalyzer:
    """选题分析器"""
    
    def __init__(self):
        # 角度模板库
        self.angle_templates = {
            '情感共鸣': {
                'patterns': ['为什么', '如何', '揭秘', '背后', '真相'],
                'hooks': [
                    '你有没有遇到过这样的情况...',
                    '说到{topic}，相信很多人都深有体会',
                    '最近，{topic}引发了热议',
                ],
                'structures': [
                    ['场景引入', '问题呈现', '情感共鸣', '解决方案', '总结升华'],
                    ['故事开头', '冲突升级', '转折反思', '观点输出', '行动号召'],
                ]
            },
            '实用干货': {
                'patterns': ['技巧', '方法', '攻略', '指南', '教程'],
                'hooks': [
                    '今天分享{topic}的X个实用技巧',
                    '关于{topic}，我总结了这几点经验',
                    '很多人问我{topic}怎么做，今天一次性讲清楚',
                ],
                'structures': [
                    ['痛点引入', '方法总览', '分点详解', '案例演示', '注意事项'],
                    ['问题提出', '原理说明', '步骤拆解', '效果展示', '常见问题'],
                ]
            },
            '观点评论': {
                'patterns': ['我认为', '观点', '看法', '解读', '分析'],
                'hooks': [
                    '关于{topic}，说点不一样的看法',
                    '{topic}，真的像大家说的那样吗？',
                    '仔细想了想，{topic}其实是这样的',
                ],
                'structures': [
                    ['现象描述', '主流观点', '不同视角', '论据支撑', '结论总结'],
                    ['事件回顾', '各方反应', '深度分析', '影响评估', '趋势预判'],
                ]
            },
            '数据洞察': {
                'patterns': ['数据', '统计', '报告', '研究', '调查'],
                'hooks': [
                    '一组关于{topic}的数据，很有意思',
                    '看了这份{topic}报告，发现了几个趋势',
                    '用数据说话：{topic}的真实情况',
                ],
                'structures': [
                    ['数据来源', '核心发现', '详细解读', '对比分析', '启示建议'],
                    ['背景说明', '数据展示', '趋势分析', '原因探讨', '应对策略'],
                ]
            },
            '故事叙事': {
                'patterns': ['故事', '经历', '案例', '纪实', '访谈'],
                'hooks': [
                    '讲一个关于{topic}的真实故事',
                    '这是我听过的最{adj}的{topic}故事',
                    '从{topic}说起，聊聊那些人和事',
                ],
                'structures': [
                    ['人物介绍', '背景铺垫', '冲突发生', '高潮转折', '结局反思'],
                    ['场景设定', '事件展开', '细节描写', '情感升华', '主题点题'],
                ]
            },
        }
        
        # 情绪词库
        self.emotion_words = {
            '共鸣': ['感动', '温暖', '心疼', '理解', '支持'],
            '愤怒': ['气愤', '不公', '愤怒', '震惊', '离谱'],
            '好奇': ['好奇', '想知道', '为什么', '怎么回事', '揭秘'],
            '焦虑': ['担心', '焦虑', '害怕', '紧张', '压力'],
            '喜悦': ['开心', '高兴', '惊喜', '幸福', '满足'],
            '怀旧': ['怀念', '回忆', '曾经', '过去', '青春'],
        }
        
        # 差异化策略
        self.differentiation_strategies = {
            '视角差异': [
                '从相反角度切入',
                '关注被忽视的群体',
                '挖掘深层原因',
                '提供另类解读',
            ],
            '形式差异': [
                '用数据可视化呈现',
                '采用对话体/访谈体',
                '制作对比表格',
                '加入互动元素',
            ],
            '内容差异': [
                '补充更多细节信息',
                '加入实用工具/资源',
                '提供可操作的清单',
                '增加案例分析',
            ],
            '风格差异': [
                '更幽默轻松的表达',
                '更专业深度的分析',
                '更温暖治愈的调性',
                '更犀利直接的观点',
            ],
        }
    
    def analyze(self, topic: HotTopic, heat_score: HeatScore, 
                all_topics: List[HotTopic] = None) -> TopicAnalysis:
        """
        全面分析单个选题
        
        Args:
            topic: 热点话题
            heat_score: 热度评分
            all_topics: 所有相关话题（用于竞品分析）
            
        Returns:
            选题分析结果
        """
        analysis = TopicAnalysis(
            original_topic=topic,
            heat_score=heat_score
        )
        
        # 1. 生成切入角度
        analysis.angles = self._generate_angles(topic, heat_score)
        
        # 2. 竞品分析
        if all_topics:
            analysis.competitors = self._analyze_competitors(topic, all_topics)
        
        # 3. 差异化建议
        analysis.differentiation = self._generate_differentiation(topic, analysis.competitors)
        
        # 4. 内容规划
        analysis.content_plan = self._create_content_plan(topic, analysis.angles[0] if analysis.angles else None)
        
        return analysis
    
    def _generate_angles(self, topic: HotTopic, heat_score: HeatScore) -> List[Dict]:
        """生成切入角度建议"""
        angles = []
        title = topic.title
        
        # 根据标题特征匹配合适的角度类型
        for angle_type, template in self.angle_templates.items():
            match_score = 0
            for pattern in template['patterns']:
                if pattern in title:
                    match_score += 1
            
            if match_score > 0 or angle_type == '情感共鸣':  # 默认至少提供情感角度
                angle = self._create_angle(topic, angle_type, template)
                angles.append(angle)
        
        # 按热度潜力排序
        angles.sort(key=lambda x: x.get('potential', 0), reverse=True)
        return angles[:3]  # 返回前3个最佳角度
    
    def _create_angle(self, topic: HotTopic, angle_type: str, template: Dict) -> Dict:
        """创建具体角度"""
        title = topic.title
        
        # 选择钩子
        import random
        hook_template = random.choice(template['hooks'])
        hook = hook_template.format(topic=title[:10], adj='精彩')
        
        # 选择结构
        structure = random.choice(template['structures'])
        
        # 生成关键论点
        key_points = self._generate_key_points(topic, angle_type)
        
        # 确定目标情绪
        target_emotion = self._detect_emotion_type(title)
        
        # 生成建议标题
        suggested_title = self._generate_title(title, angle_type)
        
        return {
            'type': angle_type,
            'suggested_title': suggested_title,
            'hook': hook,
            'structure': structure,
            'key_points': key_points,
            'target_emotion': target_emotion,
            'potential': random.randint(75, 95),
            'difficulty': random.choice(['简单', '中等', '较难']),
        }
    
    def _generate_key_points(self, topic: HotTopic, angle_type: str) -> List[str]:
        """生成关键论点"""
        # 提取关键词
        words = jieba.cut(topic.title)
        keywords = [w for w in words if len(w) >= 2]
        
        point_templates = {
            '情感共鸣': [
                '揭示{keyword}背后的真实原因',
                '讲述{keyword}对普通人的影响',
                '分享面对{keyword}的正确心态',
            ],
            '实用干货': [
                '{keyword}的X个实用技巧',
                '如何正确应对{keyword}',
                '{keyword}的常见误区及避免方法',
            ],
            '观点评论': [
                '为什么{keyword}值得关注',
                '{keyword}反映的深层问题',
                '对{keyword}的理性思考',
            ],
            '数据洞察': [
                '{keyword}的关键数据解读',
                '从数据看{keyword}的趋势',
                '{keyword}的数据对比分析',
            ],
            '故事叙事': [
                '{keyword}中的典型人物故事',
                '一个关于{keyword}的真实案例',
                '从{keyword}看时代变迁',
            ],
        }
        
        import random
        templates = point_templates.get(angle_type, point_templates['情感共鸣'])
        keyword = keywords[0] if keywords else '这个话题'
        
        points = []
        for template in templates[:3]:
            points.append(template.format(keyword=keyword))
        
        return points
    
    def _detect_emotion_type(self, title: str) -> str:
        """检测标题情绪类型"""
        for emotion, words in self.emotion_words.items():
            for word in words:
                if word in title:
                    return emotion
        return '共鸣'  # 默认
    
    def _generate_title(self, original_title: str, angle_type: str) -> str:
        """生成建议标题"""
        templates = {
            '情感共鸣': [
                '说到{topic}，很多人沉默了',
                '{topic}，戳中了多少人的痛点',
                '关于{topic}，说点心里话',
            ],
            '实用干货': [
                '{topic}完全指南：看这一篇就够了',
                'X个{topic}技巧，建议收藏',
                '如何优雅地处理{topic}？',
            ],
            '观点评论': [
                '{topic}，真的合理吗？',
                '关于{topic}，我有不同看法',
                '{topic}：被忽视的真相',
            ],
            '数据洞察': [
                '一组关于{topic}的有趣数据',
                '用数据解读{topic}',
                '{topic}：数字背后的故事',
            ],
            '故事叙事': [
                '一个关于{topic}的故事',
                '从{topic}说起',
                '{topic}：那些人和事',
            ],
        }
        
        import random
        template = random.choice(templates.get(angle_type, templates['情感共鸣']))
        short_title = original_title[:15] if len(original_title) > 15 else original_title
        return template.format(topic=short_title)
    
    def _analyze_competitors(self, topic: HotTopic, all_topics: List[HotTopic]) -> List[Dict]:
        """分析竞品内容"""
        competitors = []
        
        # 找到相似话题
        topic_keywords = set(jieba.cut(topic.title))
        
        for other in all_topics:
            if other.title == topic.title:
                continue
            
            other_keywords = set(jieba.cut(other.title))
            similarity = len(topic_keywords & other_keywords) / len(topic_keywords | other_keywords)
            
            if similarity > 0.3:  # 相似度阈值
                competitor = {
                    'title': other.title,
                    'platform': other.platform,
                    'similarity': round(similarity * 100, 1),
                    'hot_score': other.hot_score,
                    'read_count': other.read_count,
                    'angle_type': self._detect_angle_type(other.title),
                }
                competitors.append(competitor)
        
        # 按相似度和热度排序
        competitors.sort(key=lambda x: (x['similarity'], x['hot_score']), reverse=True)
        return competitors[:5]
    
    def _detect_angle_type(self, title: str) -> str:
        """检测竞品角度类型"""
        for angle_type, template in self.angle_templates.items():
            for pattern in template['patterns']:
                if pattern in title:
                    return angle_type
        return '综合'
    
    def _generate_differentiation(self, topic: HotTopic, competitors: List[Dict]) -> Dict:
        """生成差异化建议"""
        # 分析竞品的共同点
        common_angles = [c['angle_type'] for c in competitors]
        angle_counts = defaultdict(int)
        for angle in common_angles:
            angle_counts[angle] += 1
        
        # 找出被过度使用的角度
        overused_angles = [angle for angle, count in angle_counts.items() if count >= 2]
        
        # 推荐差异化策略
        recommendations = []
        
        if overused_angles:
            recommendations.append({
                'type': '角度差异',
                'suggestion': f'避免使用"{overused_angles[0]}"角度，尝试其他切入方式',
                'examples': self.differentiation_strategies['视角差异'][:2]
            })
        
        # 根据话题特征推荐
        if topic.read_count and topic.read_count > 50000:
            recommendations.append({
                'type': '深度差异',
                'suggestion': '高阅读量话题，建议做深度分析而非简单复述',
                'examples': ['挖掘数据背后的原因', '采访相关人士', '提供独家观点']
            })
        
        recommendations.append({
            'type': '形式差异',
            'suggestion': '通过创新形式脱颖而出',
            'examples': self.differentiation_strategies['形式差异'][:3]
        })
        
        return {
            'competitor_count': len(competitors),
            'common_angles': dict(angle_counts),
            'overused_angles': overused_angles,
            'recommendations': recommendations,
            'unique_opportunity': self._find_unique_opportunity(topic, competitors)
        }
    
    def _find_unique_opportunity(self, topic: HotTopic, competitors: List[Dict]) -> str:
        """寻找独特机会点"""
        opportunities = [
            '从年轻群体视角切入',
            '关注话题的长期影响',
            '结合当下热点做联动',
            '提供实用的行动指南',
            '挖掘话题背后的数据',
        ]
        import random
        return random.choice(opportunities)
    
    def _create_content_plan(self, topic: HotTopic, angle: Dict) -> Dict:
        """创建内容规划"""
        if not angle:
            return {}
        
        return {
            'word_count': self._suggest_word_count(topic, angle),
            'image_count': self._suggest_image_count(angle),
            'best_publish_time': self._suggest_publish_time(topic),
            'key_sections': angle.get('structure', []),
            'cta_suggestions': self._generate_cta(angle),
            'seo_keywords': self._extract_keywords(topic.title),
        }
    
    def _suggest_word_count(self, topic: HotTopic, angle: Dict) -> Dict:
        """建议字数"""
        angle_type = angle.get('type', '')
        
        suggestions = {
            '情感共鸣': {'min': 1500, 'optimal': 2000, 'max': 3000},
            '实用干货': {'min': 2000, 'optimal': 3000, 'max': 5000},
            '观点评论': {'min': 1200, 'optimal': 1800, 'max': 2500},
            '数据洞察': {'min': 1500, 'optimal': 2500, 'max': 4000},
            '故事叙事': {'min': 2000, 'optimal': 3000, 'max': 5000},
        }
        
        return suggestions.get(angle_type, suggestions['情感共鸣'])
    
    def _suggest_image_count(self, angle: Dict) -> Dict:
        """建议配图数量"""
        angle_type = angle.get('type', '')
        
        suggestions = {
            '情感共鸣': {'min': 3, 'optimal': 5, 'type': '情感配图/表情包'},
            '实用干货': {'min': 5, 'optimal': 8, 'type': '步骤截图/示意图'},
            '观点评论': {'min': 2, 'optimal': 3, 'type': '数据图表/概念图'},
            '数据洞察': {'min': 4, 'optimal': 6, 'type': '数据可视化图表'},
            '故事叙事': {'min': 3, 'optimal': 5, 'type': '场景配图/人物照片'},
        }
        
        return suggestions.get(angle_type, suggestions['情感共鸣'])
    
    def _suggest_publish_time(self, topic: HotTopic) -> Dict:
        """建议发布时间"""
        return {
            'optimal_days': ['周二', '周三', '周四'],
            'optimal_time': ['07:30-08:30', '12:00-13:00', '21:00-22:00'],
            'avoid_days': ['周五晚', '周末'],
            'rationale': '工作日早晚通勤和午休时段阅读量最高'
        }
    
    def _generate_cta(self, angle: Dict) -> List[str]:
        """生成行动号召建议"""
        angle_type = angle.get('type', '')
        
        ctas = {
            '情感共鸣': [
                '你对此有什么看法？欢迎在评论区分享',
                '点赞收藏，让更多人看到',
                '转发给需要的朋友',
            ],
            '实用干货': [
                '收藏本文，方便随时查阅',
                '关注获取更多实用技巧',
                '有问题欢迎在评论区交流',
            ],
            '观点评论': [
                '你同意这个观点吗？留言讨论',
                '关注看更多深度分析',
                '分享你的不同看法',
            ],
            '数据洞察': [
                '关注我们，获取最新数据解读',
                '这些数据你怎么看？',
                '收藏备用，随时查看',
            ],
            '故事叙事': [
                '喜欢这个故事请点赞支持',
                '关注看更多真实故事',
                '分享给你身边的人',
            ],
        }
        
        return ctas.get(angle_type, ctas['情感共鸣'])
    
    def _extract_keywords(self, title: str) -> List[str]:
        """提取SEO关键词"""
        keywords = jieba.analyse.extract_tags(title, topK=5, allowPOS=('n', 'nr', 'ns', 'nt', 'nw', 'nz'))
        return keywords


def analyze_single_topic(topic: HotTopic, heat_score: HeatScore, 
                        all_topics: List[HotTopic] = None) -> TopicAnalysis:
    """便捷函数：分析单个选题"""
    analyzer = TopicAnalyzer()
    return analyzer.analyze(topic, heat_score, all_topics)


if __name__ == "__main__":
    # 测试
    from data_collector import HotTopic, collect_hot_topics
    from heat_algorithm import HeatAlgorithm
    
    print("正在采集热点数据...")
    topics = collect_hot_topics(limit=20)
    
    print(f"\n采集到 {len(topics)} 条数据")
    print("正在分析热度...")
    
    algorithm = HeatAlgorithm()
    scores = algorithm.calculate(topics)
    
    print("\n正在生成选题分析...")
    analyzer = TopicAnalyzer()
    
    # 分析TOP3话题
    for i, score in enumerate(scores[:3], 1):
        print(f"\n{'='*60}")
        print(f"【TOP {i}】{score.topic.title}")
        print('='*60)
        
        analysis = analyzer.analyze(score.topic, score, topics)
        
        print(f"\n📐 推荐切入角度:")
        for j, angle in enumerate(analysis.angles[:2], 1):
            print(f"  {j}. {angle['type']}: {angle['suggested_title']}")
            print(f"     钩子: {angle['hook'][:40]}...")
        
        print(f"\n🎯 差异化建议:")
        for rec in analysis.differentiation.get('recommendations', [])[:2]:
            print(f"  - {rec['type']}: {rec['suggestion']}")
