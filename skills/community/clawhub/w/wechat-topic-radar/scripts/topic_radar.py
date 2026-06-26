#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公众号爆款选题雷达 - 主控程序
整合数据采集、热度分析、选题推荐、报告生成
"""

import argparse
import json
import sys
import os
from typing import List, Dict, Optional
from datetime import datetime

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_collector import DataCollector, collect_hot_topics
from heat_algorithm import HeatAlgorithm, analyze_topics
from topic_analyzer import TopicAnalyzer, analyze_single_topic
from report_generator import ReportGenerator


class TopicRadar:
    """选题雷达主控类"""
    
    VERSION = "1.0.0"
    
    def __init__(self, config_path: str = None):
        """
        初始化选题雷达
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.collector = DataCollector()
        self.algorithm = HeatAlgorithm()
        self.analyzer = TopicAnalyzer()
        self.report_gen = ReportGenerator(
            output_dir=self.config.get('report_dir', './data/reports')
        )
        
        print(f"🚀 公众号爆款选题雷达 v{self.VERSION}")
        print("=" * 60)
    
    def _load_config(self, config_path: str = None) -> Dict:
        """加载配置"""
        default_config = {
            'platforms': ['zhihu', 'weibo', 'xiaohongshu', 'wechat'],
            'limit_per_platform': 50,
            'min_heat_score': 50,
            'top_n': 10,
            'report_dir': './data/reports',
            'data_dir': './data',
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"⚠️  配置文件加载失败: {e}，使用默认配置")
        
        return default_config
    
    def scan(self, platforms: List[str] = None, limit: int = None) -> Dict:
        """
        执行选题扫描
        
        Args:
            platforms: 指定平台列表
            limit: 每平台采集数量
            
        Returns:
            完整分析结果
        """
        platforms = platforms or self.config['platforms']
        limit = limit or self.config['limit_per_platform']
        
        print(f"\n📡 开始扫描 {len(platforms)} 个平台...")
        print(f"   平台: {', '.join(platforms)}")
        print(f"   每平台采集: {limit} 条")
        print("-" * 60)
        
        # 1. 数据采集
        print("\n[1/4] 正在采集热点数据...")
        topics = collect_hot_topics(platforms, limit)
        print(f"✅ 共采集 {len(topics)} 条热点数据")
        
        if not topics:
            print("❌ 未采集到数据，请检查网络连接")
            return {}
        
        # 2. 热度分析
        print("\n[2/4] 正在计算综合热度...")
        result = analyze_topics(topics)
        scores = result['scores']
        print(f"✅ 完成 {len(scores)} 条数据的热度计算")
        
        # 3. 选题分析
        print("\n[3/4] 正在生成选题建议...")
        analyses = []
        for score in scores[:self.config['top_n']]:
            analysis = self.analyzer.analyze(score.topic, score, topics)
            analyses.append(analysis)
        print(f"✅ 完成 TOP {len(analyses)} 选题的深度分析")
        
        # 4. 生成报告
        print("\n[4/4] 正在生成报告...")
        report_file = self.report_gen.generate_full_report(
            scores=scores,
            analyses=analyses,
            trends=result['trends'],
            keywords=result['keywords'],
            recommendations=result['recommendations']
        )
        print(f"✅ 报告已生成: {report_file}")
        
        # 同时导出JSON
        json_file = self.report_gen.export_json(scores, analyses)
        print(f"✅ 数据已导出: {json_file}")
        
        # 汇总结果
        result.update({
            'report_file': report_file,
            'json_file': json_file,
            'analyses': analyses,
        })
        
        return result
    
    def quick_scan(self, keyword: str = None) -> List[Dict]:
        """
        快速扫描，返回简洁结果
        
        Args:
            keyword: 关键词筛选
            
        Returns:
            简洁的选题列表
        """
        print(f"\n⚡ 快速扫描模式")
        
        # 采集
        topics = collect_hot_topics(limit=30)
        
        # 筛选
        if keyword:
            topics = [t for t in topics if keyword.lower() in t.title.lower()]
        
        # 分析
        scores = self.algorithm.calculate(topics)
        
        # 生成简洁结果
        results = []
        for score in scores[:10]:
            results.append({
                'title': score.topic.title,
                'platform': score.topic.platform,
                'heat_score': score.total_score,
                'potential': score.potential_score,
                'url': score.topic.url,
            })
        
        return results
    
    def analyze_topic(self, title: str, platform: str = "custom") -> Optional[TopicAnalysis]:
        """
        分析单个选题
        
        Args:
            title: 选题标题
            platform: 平台
            
        Returns:
            选题分析结果
        """
        from data_collector import HotTopic
        
        # 创建临时话题
        topic = HotTopic(
            platform=platform,
            title=title,
            url="",
            hot_score=50.0
        )
        
        # 计算热度
        scores = self.algorithm.calculate([topic])
        if not scores:
            return None
        
        # 分析
        analysis = self.analyzer.analyze(topic, scores[0])
        
        return analysis
    
    def watch(self, keywords: List[str], interval: int = 3600):
        """
        持续监控指定关键词
        
        Args:
            keywords: 监控关键词列表
            interval: 检查间隔（秒）
        """
        import time
        
        print(f"\n👀 开始监控关键词: {', '.join(keywords)}")
        print(f"   检查间隔: {interval}秒")
        print("-" * 60)
        
        while True:
            try:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 执行检查...")
                
                # 采集
                topics = collect_hot_topics(limit=100)
                
                # 筛选匹配的话题
                matched = []
                for topic in topics:
                    for keyword in keywords:
                        if keyword.lower() in topic.title.lower():
                            matched.append(topic)
                            break
                
                if matched:
                    print(f"🎯 发现 {len(matched)} 个匹配话题:")
                    for topic in matched[:5]:
                        print(f"   - {topic.title[:40]} ({topic.platform})")
                else:
                    print("   暂无匹配话题")
                
                print(f"   下次检查: {interval}秒后")
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n\n👋 监控已停止")
                break
            except Exception as e:
                print(f"❌ 检查出错: {e}")
                time.sleep(60)
    
    def print_summary(self, result: Dict):
        """打印结果摘要"""
        if not result:
            return
        
        scores = result.get('scores', [])
        keywords = result.get('keywords', [])
        recommendations = result.get('recommendations', {})
        
        print("\n" + "=" * 60)
        print("📊 扫描结果摘要")
        print("=" * 60)
        
        # TOP 5 热门
        print("\n🔥 TOP 5 热门选题:")
        for i, score in enumerate(scores[:5], 1):
            print(f"   {i}. [{score.topic.platform}] {score.topic.title[:35]}")
            print(f"      热度: {score.total_score} | 潜力: {score.potential_score}")
        
        # 热门关键词
        print("\n📌 热门关键词:")
        for word, weight in keywords[:8]:
            print(f"   - {word}: {weight:.3f}")
        
        # 推荐
        hot_now = recommendations.get('hot_now', [])
        if hot_now:
            print("\n⭐ 立即跟进:")
            for score in hot_now[:3]:
                print(f"   - {score.topic.title[:40]}")
        
        print("\n" + "=" * 60)
        print(f"📄 详细报告: {result.get('report_file', 'N/A')}")
        print("=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='公众号爆款选题雷达 - 智能发现热门选题',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 完整扫描
  python topic_radar.py scan
  
  # 快速扫描
  python topic_radar.py quick
  
  # 分析特定选题
  python topic_radar.py analyze "为什么年轻人都不结婚了？"
  
  # 监控关键词
  python topic_radar.py watch "AI 人工智能 大模型"
        """
    )
    
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('-c', '--config', help='配置文件路径')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # scan 命令
    scan_parser = subparsers.add_parser('scan', help='执行完整扫描')
    scan_parser.add_argument('-p', '--platforms', nargs='+', 
                           choices=['zhihu', 'weibo', 'xiaohongshu', 'wechat'],
                           help='指定平台')
    scan_parser.add_argument('-l', '--limit', type=int, default=50,
                           help='每平台采集数量')
    
    # quick 命令
    quick_parser = subparsers.add_parser('quick', help='快速扫描')
    quick_parser.add_argument('-k', '--keyword', help='关键词筛选')
    
    # analyze 命令
    analyze_parser = subparsers.add_parser('analyze', help='分析单个选题')
    analyze_parser.add_argument('title', help='选题标题')
    analyze_parser.add_argument('-p', '--platform', default='custom',
                              help='平台')
    
    # watch 命令
    watch_parser = subparsers.add_parser('watch', help='持续监控关键词')
    watch_parser.add_argument('keywords', nargs='+', help='监控关键词')
    watch_parser.add_argument('-i', '--interval', type=int, default=3600,
                            help='检查间隔（秒）')
    
    args = parser.parse_args()
    
    # 初始化雷达
    radar = TopicRadar(config_path=args.config)
    
    # 执行命令
    if args.command == 'scan':
        result = radar.scan(
            platforms=args.platforms,
            limit=args.limit
        )
        radar.print_summary(result)
        
    elif args.command == 'quick':
        results = radar.quick_scan(keyword=args.keyword)
        print("\n⚡ 快速扫描结果:")
        print("-" * 60)
        for i, item in enumerate(results, 1):
            print(f"{i}. [{item['platform']}] {item['title']}")
            print(f"   热度: {item['heat_score']} | 潜力: {item['potential']}")
        
    elif args.command == 'analyze':
        analysis = radar.analyze_topic(args.title, args.platform)
        if analysis:
            print("\n📋 选题分析报告")
            print("=" * 60)
            print(f"标题: {analysis.original_topic.title}")
            print(f"热度: {analysis.heat_score.total_score}")
            print(f"\n🎯 切入角度:")
            for i, angle in enumerate(analysis.angles[:3], 1):
                print(f"\n  {i}. {angle['type']}: {angle['suggested_title']}")
                print(f"     钩子: {angle['hook']}")
                print(f"     结构: {' → '.join(angle['structure'])}")
        else:
            print("❌ 分析失败")
            
    elif args.command == 'watch':
        radar.watch(args.keywords, args.interval)
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
