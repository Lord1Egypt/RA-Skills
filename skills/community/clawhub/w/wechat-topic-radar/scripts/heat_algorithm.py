#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合热度算法引擎
计算多维度热度评分，识别真正的爆款潜力选题
"""

import math
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict
import jieba
import jieba.analyse

from data_collector import HotTopic


@dataclass
class HeatScore:
    """热度评分结果"""
    topic: HotTopic
    total_score: float  # 总热度分 (0-100)
    platform_score: float  # 平台热度分
    interaction_score: float  # 互动热度分
    trend_score: float  # 趋势热度分
    quality_score: float  # 内容质量分
    potential_score: float  # 爆款潜力分
    factors: Dict[str, float]  # 各因子得分详情
    
    
class HeatAlgorithm:
    """综合热度算法"""
    
    def __init__(self):
        # 权重配置
        self.weights = {
            'platform': 0.20,      # 平台热度权重
            'interaction': 0.25,   # 互动数据权重
            'trend': 0.20,         # 趋势增长权重
            'quality': 0.15,       # 内容质量权重
            'potential': 0.20,     # 爆款潜力权重
        }
        
        # 平台热度基准值
        self.platform_baseline = {
            '知乎': 10000,
            '微博': 1000000,
            '小红书': 5000,
            '公众号': 50000,
        }
        
        # 互动权重
        self.interaction_weights = {
            'read': 0.1,      # 阅读
            'like': 0.25,     # 点赞
            'comment': 0.35,  # 评论
            'share': 0.30,    # 分享
        }
    
    def calculate(self, topics: List[HotTopic]) -> List[HeatScore]:
        """
        计算所有话题的综合热度
        
        Args:
            topics: 热点话题列表
            
        Returns:
            热度评分结果列表
        """
        scores = []
        
        for topic in topics:
            try:
                score = self._calculate_single(topic)
                scores.append(score)
            except Exception as e:
                print(f"计算热度失败: {topic.title}, 错误: {e}")
                continue
        
        # 按总热度排序
        scores.sort(key=lambda x: x.total_score, reverse=True)
        return scores
    
    def _calculate_single(self, topic: HotTopic) -> HeatScore:
        """计算单个话题的热度"""
        
        # 1. 平台热度分 (0-100)
        platform_score = self._calc_platform_score(topic)
        
        # 2. 互动热度分 (0-100)
        interaction_score = self._calc_interaction_score(topic)
        
        # 3. 趋势热度分 (0-100)
        trend_score = self._calc_trend_score(topic)
        
        # 4. 内容质量分 (0-100)
        quality_score = self._calc_quality_score(topic)
        
        # 5. 爆款潜力分 (0-100)
        potential_score = self._calc_potential_score(topic)
        
        # 计算总分
        total_score = (
            platform_score * self.weights['platform'] +
            interaction_score * self.weights['interaction'] +
            trend_score * self.weights['trend'] +
            quality_score * self.weights['quality'] +
            potential_score * self.weights['potential']
        )
        
        # 各因子详情
        factors = {
            'platform_raw': topic.hot_score,
            'read_count': topic.read_count or 0,
            'like_count': topic.like_count or 0,
            'comment_count': topic.comment_count or 0,
            'share_count': topic.share_count or 0,
            'title_length': len(topic.title),
            'has_category': 1 if topic.category else 0,
        }
        
        return HeatScore(
            topic=topic,
            total_score=round(total_score, 2),
            platform_score=round(platform_score, 2),
            interaction_score=round(interaction_score, 2),
            trend_score=round(trend_score, 2),
            quality_score=round(quality_score, 2),
            potential_score=round(potential_score, 2),
            factors=factors
        )
    
    def _calc_platform_score(self, topic: HotTopic) -> float:
        """计算平台热度分"""
        baseline = self.platform_baseline.get(topic.platform, 10000)
        
        # 归一化到 0-100
        if baseline > 0:
            score = min(100, (topic.hot_score / baseline) * 100)
        else:
            score = 50
        
        # 平台加成
        platform_bonus = {
            '知乎': 1.0,
            '微博': 1.1,
            '小红书': 1.2,
            '公众号': 1.3,
        }
        
        score *= platform_bonus.get(topic.platform, 1.0)
        return min(100, score)
    
    def _calc_interaction_score(self, topic: HotTopic) -> float:
        """计算互动热度分"""
        # 获取各项数据
        read = topic.read_count or 0
        like = topic.like_count or 0
        comment = topic.comment_count or 0
        share = topic.share_count or 0
        
        # 计算互动率
        if read > 0:
            like_rate = like / read
            comment_rate = comment / read
            share_rate = share / read
        else:
            like_rate = comment_rate = share_rate = 0
        
        # 加权得分
        score = (
            like_rate * 100 * self.interaction_weights['like'] +
            comment_rate * 100 * self.interaction_weights['comment'] +
            share_rate * 100 * self.interaction_weights['share']
        )
        
        # 绝对数量加成
        volume_score = min(30, math.log10(max(10, like + comment + share)) * 5)
        
        return min(100, score + volume_score)
    
    def _calc_trend_score(self, topic: HotTopic) -> float:
        """计算趋势热度分"""
        # 基于发布时间计算新鲜度
        if topic.publish_time:
            try:
                # 处理字符串格式的发布时间
                if isinstance(topic.publish_time, str):
                    publish_dt = datetime.strptime(topic.publish_time, '%Y-%m-%d %H:%M:%S')
                else:
                    publish_dt = topic.publish_time
                hours_ago = (datetime.now() - publish_dt).total_seconds() / 3600
                # 24小时内满分，之后衰减
                freshness = max(0, 100 - hours_ago * 2)
            except:
                freshness = 70  # 解析失败使用默认值
        else:
            freshness = 70  # 默认中等新鲜度
        
        # 热度增长趋势（基于当前热度值）
        if topic.hot_score > 100000:
            growth_trend = 95
        elif topic.hot_score > 50000:
            growth_trend = 85
        elif topic.hot_score > 10000:
            growth_trend = 75
        elif topic.hot_score > 1000:
            growth_trend = 65
        else:
            growth_trend = 50
        
        return freshness * 0.6 + growth_trend * 0.4
    
    def _calc_quality_score(self, topic: HotTopic) -> float:
        """计算内容质量分"""
        score = 50  # 基础分
        
        # 标题长度适中 (15-30字最佳)
        title_len = len(topic.title)
        if 15 <= title_len <= 30:
            score += 20
        elif 10 <= title_len < 15 or 30 < title_len <= 40:
            score += 10
        
        # 有分类标签加分
        if topic.category:
            score += 10
        
        # 有作者信息加分
        if topic.author:
            score += 10
        
        # 标题包含数字加分（数字标题通常更吸引人）
        if any(c.isdigit() for c in topic.title):
            score += 10
        
        # 标题包含热点词汇加分
        hot_words = ['爆', '火', '热搜', '热门', '最新', '重磅', '揭秘', '独家']
        if any(word in topic.title for word in hot_words):
            score += 10
        
        return min(100, score)
    
    def _calc_potential_score(self, topic: HotTopic) -> float:
        """计算爆款潜力分"""
        score = 50  # 基础分
        
        title = topic.title
        
        # 情绪词加分
        emotion_words = {
            'high': ['震惊', '绝了', '炸裂', '泪目', '破防', '燃爆', '神作'],
            'medium': ['为什么', '如何', '什么', '揭秘', '真相', '背后']
        }
        
        for word in emotion_words['high']:
            if word in title:
                score += 15
                break
        
        for word in emotion_words['medium']:
            if word in title:
                score += 8
                break
        
        # 数字+对比结构加分
        if any(c.isdigit() for c in title) and ('vs' in title.lower() or '对比' in title or '差距' in title):
            score += 15
        
        # 疑问句加分
        if '?' in title or '？' in title or title.startswith(('为什么', '怎么', '什么', '如何')):
            score += 10
        
        # 人群定位加分
        target_words = ['年轻人', '90后', '00后', '职场', '宝妈', '学生', '打工人']
        for word in target_words:
            if word in title:
                score += 10
                break
        
        # 平台热度加成
        if topic.hot_score > 50000:
            score += 15
        elif topic.hot_score > 10000:
            score += 10
        
        return min(100, score)
    
    def analyze_keywords(self, topics: List[HotTopic], top_k: int = 20) -> List[Tuple[str, float]]:
        """
        分析热点关键词
        
        Args:
            topics: 热点话题列表
            top_k: 返回前K个关键词
            
        Returns:
            关键词及其权重列表
        """
        # 合并所有标题
        text = ' '.join([t.title for t in topics])
        
        # 使用jieba提取关键词
        keywords = jieba.analyse.extract_tags(
            text, 
            topK=top_k,
            withWeight=True,
            allowPOS=('n', 'nr', 'ns', 'nt', 'nw', 'nz', 'v', 'vd', 'vn')
        )
        
        return keywords
    
    def detect_trends(self, scores: List[HeatScore], time_window: int = 24) -> Dict:
        """
        检测趋势变化
        
        Args:
            scores: 热度评分列表
            time_window: 时间窗口（小时）
            
        Returns:
            趋势分析结果
        """
        # 按平台分组
        platform_groups = defaultdict(list)
        for score in scores:
            platform_groups[score.topic.platform].append(score)
        
        trends = {
            'rising_topics': [],  # 上升话题
            'stable_topics': [],  # 稳定话题
            'falling_topics': [], # 下降话题
            'platform_distribution': {},  # 平台分布
            'category_distribution': {},  # 分类分布
        }
        
        # 分析平台分布
        for platform, items in platform_groups.items():
            trends['platform_distribution'][platform] = {
                'count': len(items),
                'avg_score': np.mean([s.total_score for s in items]) if items else 0,
                'top_score': max([s.total_score for s in items]) if items else 0,
            }
        
        # 分析分类分布
        category_groups = defaultdict(list)
        for score in scores:
            cat = score.topic.category or '未分类'
            category_groups[cat].append(score)
        
        for cat, items in category_groups.items():
            trends['category_distribution'][cat] = len(items)
        
        # 按热度分级
        for score in scores:
            if score.total_score >= 80:
                trends['rising_topics'].append(score)
            elif score.total_score >= 60:
                trends['stable_topics'].append(score)
            else:
                trends['falling_topics'].append(score)
        
        return trends
    
    def get_recommendations(self, scores: List[HeatScore], top_n: int = 10) -> Dict:
        """
        生成选题推荐
        
        Args:
            scores: 热度评分列表
            top_n: 推荐数量
            
        Returns:
            推荐结果
        """
        recommendations = {
            'hot_now': [],      # 当下最热
            'high_potential': [], # 高潜力
            'undervalued': [],  # 被低估
            'cross_platform': [], # 多平台热点
        }
        
        # 当下最热（总热度最高）
        recommendations['hot_now'] = scores[:top_n]
        
        # 高潜力（潜力分高但总分中等）
        high_potential = [s for s in scores if s.potential_score >= 75 and s.total_score < 75]
        high_potential.sort(key=lambda x: x.potential_score, reverse=True)
        recommendations['high_potential'] = high_potential[:top_n]
        
        # 被低估（互动分高但平台分低）
        undervalued = [s for s in scores if s.interaction_score >= 70 and s.platform_score < 60]
        undervalued.sort(key=lambda x: x.interaction_score, reverse=True)
        recommendations['undervalued'] = undervalued[:top_n]
        
        # 多平台热点（同一话题在多平台出现）
        title_platforms = defaultdict(set)
        for score in scores:
            # 简化标题用于匹配
            simple_title = score.topic.title[:10]
            title_platforms[simple_title].add(score.topic.platform)
        
        cross_platform = [s for s in scores if len(title_platforms.get(s.topic.title[:10], [])) >= 2]
        cross_platform.sort(key=lambda x: x.total_score, reverse=True)
        recommendations['cross_platform'] = cross_platform[:top_n]
        
        return recommendations


def analyze_topics(topics: List[HotTopic]) -> Dict:
    """
    便捷函数：全面分析热点话题
    
    Args:
        topics: 热点话题列表
        
    Returns:
        完整分析结果
    """
    algorithm = HeatAlgorithm()
    
    # 计算热度
    scores = algorithm.calculate(topics)
    
    # 提取关键词
    keywords = algorithm.analyze_keywords(topics)
    
    # 检测趋势
    trends = algorithm.detect_trends(scores)
    
    # 生成推荐
    recommendations = algorithm.get_recommendations(scores)
    
    return {
        'scores': scores,
        'keywords': keywords,
        'trends': trends,
        'recommendations': recommendations,
    }


if __name__ == "__main__":
    # 测试
    from data_collector import collect_hot_topics
    
    print("正在采集热点数据...")
    topics = collect_hot_topics(limit=30)
    
    print(f"\n采集到 {len(topics)} 条数据，开始分析...")
    result = analyze_topics(topics)
    
    print("\n" + "="*60)
    print("TOP 10 热门选题")
    print("="*60)
    for i, score in enumerate(result['scores'][:10], 1):
        print(f"{i}. {score.topic.title[:40]}")
        print(f"   平台: {score.topic.platform} | 总分: {score.total_score} | 潜力: {score.potential_score}")
    
    print("\n" + "="*60)
    print("热门关键词")
    print("="*60)
    for word, weight in result['keywords'][:10]:
        print(f"- {word}: {weight:.3f}")
