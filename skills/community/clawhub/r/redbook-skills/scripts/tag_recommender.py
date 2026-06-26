# -*- coding: utf-8 -*-
# 小红书标签推荐系统
# 热门标签推荐、标签组合优化、竞品分析

import argparse
import random
import json
from datetime import datetime
from collections import Counter

class TagRecommender:
    """小红书标签推荐器"""
    
    def __init__(self):
        # 标签库
        self.tag_database = {
            # 大类目标签
            'category': {
                '科技': ['#科技', '#数码', '#互联网', '#科技创新', '#科技资讯'],
                '学习': ['#学习', '#教育', '#知识', '#校园', '#学习日常'],
                '生活': ['#生活', '#日常', '#记录生活', '#生活碎片', '#生活方式'],
                '职场': ['#职场', '#工作', '#打工人', '#职场日常', '#职场干货'],
                '效率': ['#效率', '#时间管理', '#自我管理', '#成长', '#提升'],
            },
            
            # 细分领域标签
            'niche': {
                '效率工具': ['#效率工具', '#软件推荐', '#神器', '#APP 推荐', '#工具分享'],
                'AI 技术': ['#AI', '#人工智能', '#机器学习', '#深度学习', '#AIGC'],
                '编程开发': ['#编程', '#代码', '#开发者', '#程序员', '#软件开发'],
                '数码评测': ['#数码评测', '#产品评测', '#开箱', '#测评', '#种草'],
                '学习心得': ['#学习心得', '#经验分享', '#干货分享', '#笔记', '#总结'],
            },
            
            # 热门标签（流量大）
            'hot': [
                '#小红书成长笔记', '#日常', '#分享', '#推荐', '#必看',
                '#收藏', '#实用', '#免费', '#平替', '#学生党',
                '#宝藏', '#安利', '#好物分享', '#干货', '#教程'
            ],
            
            # 长尾标签（竞争小）
            'longtail': {
                '效率工具': ['#打工人必备', '#办公神器', '#效率提升', '#工作技巧', '#职场技能'],
                'AI 技术': ['#AI 工具', '#AI 应用', '#AI 教程', '#AI 学习', '#AI 资源'],
                '编程开发': ['#编程学习', '#代码技巧', '#开发工具', '#技术分享', '#项目实战'],
            }
        }
    
    def recommend_tags(self, topic, content_type='skill', count=15, strategy='balanced'):
        """
        推荐标签
        
        Args:
            topic: 主题/话题
            content_type: 内容类型
            count: 标签数量
            strategy: 推荐策略 (balanced=平衡，aggressive=激进，conservative=保守)
        """
        tags = []
        
        # 1. 添加大类目标签（2-3 个）
        category_tags = self._match_category(topic)
        tags.extend(category_tags[:3])
        
        # 2. 添加细分领域标签（3-5 个）
        niche_tags = self._match_niche(topic)
        tags.extend(niche_tags[:5])
        
        # 3. 添加热门标签（根据策略调整数量）
        if strategy == 'aggressive':
            hot_count = 7  # 激进：多用热门标签
        elif strategy == 'conservative':
            hot_count = 3  # 保守：少用热门标签
        else:
            hot_count = 5  # 平衡
        
        tags.extend(random.sample(self.tag_database['hot'], min(hot_count, count - len(tags))))
        
        # 4. 添加长尾标签（2-3 个）
        longtail_tags = self._match_longtail(topic)
        tags.extend(longtail_tags[:3])
        
        # 5. 添加自定义话题标签
        if f'#{topic}' not in tags:
            tags.append(f'#{topic}')
        
        # 去重并限制数量
        tags = list(dict.fromkeys(tags))[:count]
        
        return tags
    
    def _match_category(self, topic):
        """匹配大类目标签"""
        for category, tag_list in self.tag_database['category'].items():
            if category in topic:
                return tag_list
        return ['#分享', '#日常', '#记录']
    
    def _match_niche(self, topic):
        """匹配细分领域标签"""
        for niche, tag_list in self.tag_database['niche'].items():
            if niche in topic:
                return tag_list
        return ['#干货', '#实用', '#推荐']
    
    def _match_longtail(self, topic):
        """匹配长尾标签"""
        for niche, tag_list in self.tag_database['longtail'].items():
            if niche in topic:
                return tag_list
        return ['#必备', '#小技巧', '#经验分享']
    
    def analyze_competitor_tags(self, competitor_notes):
        """分析竞品笔记标签"""
        all_tags = []
        
        for note in competitor_notes:
            tags = note.get('tags', [])
            all_tags.extend(tags)
        
        # 统计标签频率
        tag_counts = Counter(all_tags)
        
        # 返回最常用的标签
        return tag_counts.most_common(20)
    
    def generate_tag_combinations(self, topic, count=5):
        """生成标签组合方案"""
        combinations = []
        
        for i in range(count):
            tags = self.recommend_tags(topic, strategy=random.choice(['balanced', 'aggressive', 'conservative']))
            combinations.append({
                '方案': i + 1,
                '策略': random.choice(['平衡', '激进', '保守']),
                '标签': tags
            })
        
        return combinations
    
    def export_tags(self, tags, output_file='tags.txt'):
        """导出标签到文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(' '.join(tags))
        print(f"✅ 标签已导出到：{output_file}")


def main():
    parser = argparse.ArgumentParser(description='小红书标签推荐器')
    parser.add_argument('--topic', type=str, required=True, help='主题/话题')
    parser.add_argument('--type', type=str, default='skill', help='内容类型')
    parser.add_argument('--count', type=int, default=15, help='标签数量')
    parser.add_argument('--strategy', type=str, default='balanced',
                       choices=['balanced', 'aggressive', 'conservative'],
                       help='推荐策略')
    parser.add_argument('--output', type=str, help='导出文件')
    parser.add_argument('--analyze', type=str, help='分析模式（trending/competitor）')
    
    args = parser.parse_args()
    
    recommender = TagRecommender()
    
    if args.analyze:
        # 分析模式
        if args.analyze == 'trending':
            print("🔥 热门标签分析：")
            print(' '.join(random.sample(recommender.tag_database['hot'], 10)))
        else:
            print("分析功能需要竞品数据，暂不支持")
    else:
        # 推荐模式
        tags = recommender.recommend_tags(
            topic=args.topic,
            content_type=args.type,
            count=args.count,
            strategy=args.strategy
        )
        
        print("\n" + "="*50)
        print(f"🏷️ 标签推荐（主题：{args.topic}）")
        print("="*50)
        print(f"策略：{args.strategy}")
        print(f"数量：{len(tags)}个")
        print("\n推荐标签：")
        print(' '.join(tags))
        print("="*50)
        
        # 导出
        if args.output:
            recommender.export_tags(tags, args.output)


if __name__ == '__main__':
    main()
