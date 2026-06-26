#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公众号爆款选题雷达 - 主控模块
整合数据采集、热度分析、选题建议、报告生成
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import List, Optional

# 使用增强版数据源 (支持20+平台，自动故障转移)
from enhanced_collector import EnhancedCollector, collect_hot_topics, HotTopic
from heat_algorithm import HeatAlgorithm, analyze_topics, HeatScore
from topic_analyzer import TopicAnalyzer, analyze_single_topic, TopicAnalysis
from report_generator import ReportGenerator


class WechatTopicRadar:
    """公众号爆款选题雷达主类"""
    
    def __init__(self, config_path: str = None):
        """
        初始化雷达
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        # 使用增强版数据采集器 (支持20+平台，多源备份)
        self.data_collector = EnhancedCollector()
        self.heat_algorithm = HeatAlgorithm()
        self.topic_analyzer = TopicAnalyzer()
        self.report_generator = ReportGenerator(
            output_dir=self.config.get('report_dir', './data/reports')
        )
        
    def _load_config(self, config_path: str) -> dict:
        """加载配置"""
        default_config = {
            # 增强版采集器支持的平台 (20+平台，自动故障转移):
            # 国内热点: 百度, 微博, 知乎, 今日头条, 抖音, B站热搜/日榜
            # 技术社区: 掘金, CSDN, GitHub, V2EX, HackerNews
            # 新闻资讯: 网易新闻, 少数派, 爱范儿
            'platforms': ['百度', '微博', '知乎', '今日头条', '抖音', 'B站热搜'],
            'limit_per_platform': 50,
            'min_heat_score': 50,
            'top_n_recommendations': 10,
            'report_dir': './data/reports',
            'data_dir': './data',
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                import yaml
                user_config = yaml.safe_load(f)
                default_config.update(user_config)
        
        return default_config
    
    def scan(self, platforms: List[str] = None, limit: int = None) -> dict:
        """
        执行一次完整的选题扫描
        
        Args:
            platforms: 指定平台列表
            limit: 每个平台采集数量
            
        Returns:
            扫描结果字典
        """
        platforms = platforms or self.config['platforms']
        limit = limit or self.config['limit_per_platform']
        
        print("=" * 60)
        print("[热门] 公众号爆款选题雷达 - 开始扫描")
        print("=" * 60)
        print(f"[手机] 扫描平台: {', '.join(platforms)}")
        print(f"[图表] 每平台采集: {limit} 条")
        print(f"[时间] 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        # Step 1: 数据采集
        print("\n[步骤1] Step 1: 多平台数据采集...")
        topics = self.data_collector.collect_merged(platforms, limit)
        print(f"   [OK] 共采集 {len(topics)} 条热点数据")
        
        # Step 2: 热度计算
        print("\n[步骤2] Step 2: 综合热度计算...")
        scores = self.heat_algorithm.calculate(topics)
        valid_scores = [s for s in scores if s.total_score >= self.config['min_heat_score']]
        print(f"   [OK] 计算完成，{len(valid_scores)} 条达到热度阈值")
        
        # Step 3: 趋势分析
        print("\n[步骤3] Step 3: 热点趋势分析...")
        trends = self.heat_algorithm.detect_trends(valid_scores)
        keywords = self.heat_algorithm.analyze_keywords(topics)
        recommendations = self.heat_algorithm.get_recommendations(
            valid_scores, 
            self.config['top_n_recommendations']
        )
        print(f"   [OK] 提取 {len(keywords)} 个关键词")
        print(f"   [OK] 识别 {len(trends['rising_topics'])} 个上升话题")
        
        # Step 4: 选题深度分析
        print("\n[步骤4] Step 4: 选题深度分析...")
        analyses = []
        for score in valid_scores[:self.config['top_n_recommendations']]:
            analysis = self.topic_analyzer.analyze(score.topic, score, topics)
            analyses.append(analysis)
        print(f"   [OK] 完成 {len(analyses)} 个选题深度分析")
        
        # Step 5: 生成报告
        print("\n[步骤5] Step 5: 生成分析报告...")
        report_file = self.report_generator.generate_full_report(
            valid_scores, analyses, trends, keywords, recommendations
        )
        json_file = self.report_generator.export_json(valid_scores, analyses)
        print(f"   [OK] HTML报告: {report_file}")
        print(f"   [OK] JSON数据: {json_file}")
        
        # 汇总
        print("\n" + "=" * 60)
        print("[完成] 扫描完成!")
        print("=" * 60)
        print(f"[图表] 数据概览:")
        print(f"   - 采集热点: {len(topics)} 条")
        print(f"   - 有效选题: {len(valid_scores)} 条")
        print(f"   - 深度分析: {len(analyses)} 条")
        print(f"\n[奖杯] TOP 5 热门选题:")
        for i, score in enumerate(valid_scores[:5], 1):
            print(f"   {i}. [{score.topic.platform}] {score.topic.title[:30]}... (热度: {score.total_score})")
        
        print(f"\n[文件] 输出文件:")
        print(f"   - {report_file}")
        print(f"   - {json_file}")
        print("=" * 60)
        
        return {
            'topics': topics,
            'scores': valid_scores,
            'analyses': analyses,
            'trends': trends,
            'keywords': keywords,
            'recommendations': recommendations,
            'report_file': report_file,
            'json_file': json_file,
        }
    
    def quick_scan(self, keyword: str = None) -> dict:
        """
        快速扫描 - 获取当前热点概览
        
        Args:
            keyword: 可选的关键词筛选
            
        Returns:
            简化版扫描结果
        """
        print("[闪电] 快速扫描模式")
        
        # 快速扫描主要平台: 百度 + 微博 + 今日头条 + B站
        topics = self.data_collector.collect_merged(['百度', '微博', '今日头条', 'B站热搜'], 30)
        
        if keyword:
            topics = [t for t in topics if keyword in t.title]
        
        scores = self.heat_algorithm.calculate(topics)
        
        return {
            'hot_topics': scores[:10],
            'keywords': self.heat_algorithm.analyze_keywords(topics, top_k=10),
        }
    
    def analyze_topic(self, title: str, platform: str = "自定义") -> Optional[TopicAnalysis]:
        """
        分析单个选题
        
        Args:
            title: 选题标题
            platform: 平台来源
            
        Returns:
            选题分析结果
        """
        from enhanced_collector import HotTopic
        
        # 创建临时话题对象
        topic = HotTopic(
            platform=platform,
            title=title,
            url="",
            hot_score=50.0
        )
        
        # 计算热度
        scores = self.heat_algorithm.calculate([topic])
        if not scores:
            return None
        
        # 深度分析
        analysis = self.topic_analyzer.analyze(topic, scores[0])
        
        return analysis
    
    def compare_topics(self, titles: List[str]) -> dict:
        """
        对比多个选题
        
        Args:
            titles: 选题标题列表
            
        Returns:
            对比结果
        """
        from enhanced_collector import HotTopic
        
        topics = []
        for title in titles:
            topics.append(HotTopic(
                platform="对比分析",
                title=title,
                url="",
                hot_score=50.0
            ))
        
        scores = self.heat_algorithm.calculate(topics)
        
        return {
            'comparison': [
                {
                    'title': s.topic.title,
                    'total_score': s.total_score,
                    'potential_score': s.potential_score,
                    'quality_score': s.quality_score,
                }
                for s in sorted(scores, key=lambda x: x.total_score, reverse=True)
            ]
        }


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='公众号爆款选题雷达 - 智能发现爆款选题',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 完整扫描
  python radar_main.py scan
  
  # 快速扫描
  python radar_main.py quick
  
  # 分析单个选题
  python radar_main.py analyze "为什么年轻人都不结婚了？"
  
  # 对比多个选题
  python radar_main.py compare "标题1" "标题2" "标题3"
        """
    )
    
    parser.add_argument(
        'command',
        choices=['scan', 'quick', 'analyze', 'compare'],
        help='执行命令'
    )
    
    parser.add_argument(
        '--config', '-c',
        help='配置文件路径'
    )
    
    parser.add_argument(
        '--platforms', '-p',
        nargs='+',
        default=['百度', '微博', '知乎', '今日头条', '抖音', 'B站热搜'],
        help='指定扫描平台 (可选: 百度, 微博, 知乎, 今日头条, 抖音, B站热搜/B站日榜, 掘金, CSDN, GitHub, V2EX, HackerNews, 网易新闻, 少数派)'
    )
    
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=50,
        help='每平台采集数量'
    )
    
    parser.add_argument(
        '--keyword', '-k',
        help='关键词筛选'
    )
    
    parser.add_argument(
        'titles',
        nargs='*',
        help='选题标题（用于analyze/compare命令）'
    )
    
    args = parser.parse_args()
    
    # 初始化雷达
    radar = WechatTopicRadar(args.config)
    
    # 执行命令
    if args.command == 'scan':
        result = radar.scan(args.platforms, args.limit)
        
    elif args.command == 'quick':
        result = radar.quick_scan(args.keyword)
        print("\n[闪电] 快速扫描结果:")
        print("-" * 60)
        for i, score in enumerate(result['hot_topics'][:5], 1):
            print(f"{i}. [{score.topic.platform}] {score.topic.title}")
            print(f"   热度: {score.total_score} | 潜力: {score.potential_score}")
        
        print("\n[热门] 热门关键词:")
        for word, weight in result['keywords'][:10]:
            print(f"  - {word}: {weight:.3f}")
            
    elif args.command == 'analyze':
        if not args.titles:
            print("[X] 请提供选题标题")
            sys.exit(1)
        
        title = ' '.join(args.titles)
        analysis = radar.analyze_topic(title)
        
        if analysis:
            print(f"\n[图表] 选题分析: {title}")
            print("=" * 60)
            print(f"\n[温度计] 热度评分: {analysis.heat_score.total_score}")
            print(f"   平台分: {analysis.heat_score.platform_score}")
            print(f"   互动分: {analysis.heat_score.interaction_score}")
            print(f"   潜力分: {analysis.heat_score.potential_score}")
            
            print(f"\n[目标] 推荐切入角度:")
            for i, angle in enumerate(analysis.angles[:3], 1):
                print(f"\n  {i}. {angle['type']}")
                print(f"     标题: {angle['suggested_title']}")
                print(f"     钩子: {angle['hook']}")
                print(f"     结构: {' -> '.join(angle['structure'])}")
        
    elif args.command == 'compare':
        if len(args.titles) < 2:
            print("[X] 请提供至少2个选题进行对比")
            sys.exit(1)
        
        result = radar.compare_topics(args.titles)
        
        print("\n[图表] 选题对比结果")
        print("=" * 60)
        for item in result['comparison']:
            print(f"\n{item['title'][:40]}")
            print(f"  综合热度: {item['total_score']}")
            print(f"  爆款潜力: {item['potential_score']}")
            print(f"  内容质量: {item['quality_score']}")


if __name__ == "__main__":
    main()
