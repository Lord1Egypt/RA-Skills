#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标签推荐器 - 根据主题推荐热门标签
"""

import json
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class TagRecommendation:
    """标签推荐结果"""
    tag: str
    category: str  # hot/precise/longtail
    score: float  # 推荐分数 0-1
    reason: str  # 推荐理由


class TagRecommender:
    """标签推荐器"""
    
    def __init__(self):
        # 热门标签库（实际应该从 API 获取）
        self.hot_tags = {
            "xiaohongshu": [
                "小红书", "种草", "好物分享", "生活记录", "日常",
                "干货", "技巧", "学习", "成长", "自律",
                "治愈", "心情", "穿搭", "美妆", "护肤",
                "美食", "旅行", "读书", "电影", "音乐"
            ],
            "douyin": [
                "抖音", "热门", "推荐", "搞笑", "娱乐",
                "音乐", "舞蹈", "美食", "旅行", "生活",
                "技巧", "干货", "教程", "挑战", "同款"
            ],
            "wechat": [
                "公众号", "深度", "思考", "观点", "干货",
                "职场", "成长", "学习", "创业", "投资",
                "科技", "互联网", "生活", "情感", "文化"
            ],
            "zhihu": [
                "知乎", "专业", "科普", "经验", "分享",
                "职场", "学习", "成长", "生活", "情感",
                "科技", "数码", "电影", "书籍", "游戏"
            ]
        }
        
        # 主题 - 标签映射
        self.topic_mapping = {
            "AI": ["人工智能", "AI 工具", "效率", "科技", "未来"],
            "写作": ["写作技巧", "文案", "创作", "文字", "表达"],
            "赚钱": ["副业", "收入", "理财", "投资", "搞钱"],
            "学习": ["学习方法", "自我提升", "知识", "成长", "进步"],
            "生活": ["生活方式", "日常", "记录", "感悟", "治愈"],
            "职场": ["职场经验", "工作", "面试", "升职", "同事"],
            "美妆": ["化妆", "护肤", "彩妆", "美容", "变美"],
            "穿搭": ["穿搭技巧", "时尚", "搭配", "服装", "风格"],
            "美食": ["美食分享", "食谱", "做饭", "探店", "吃货"],
            "旅行": ["旅行攻略", "旅游", "景点", "拍照", "风景"],
        }
    
    def recommend(self, topic: str, platform: str, count: int = 10) -> List[TagRecommendation]:
        """
        推荐标签
        
        Args:
            topic: 主题
            platform: 平台
            count: 推荐数量
            
        Returns:
            标签推荐列表
        """
        recommendations = []
        
        # 1. 热门标签
        platform_tags = self.hot_tags.get(platform, [])
        for tag in platform_tags[:5]:
            recommendations.append(TagRecommendation(
                tag=tag,
                category="hot",
                score=0.8,
                reason="平台热门标签"
            ))
        
        # 2. 精准匹配
        for key, tags in self.topic_mapping.items():
            if key in topic or topic in key:
                for tag in tags:
                    recommendations.append(TagRecommendation(
                        tag=tag,
                        category="precise",
                        score=0.9,
                        reason=f"与主题\"{topic}\"精准匹配"
                    ))
                break
        
        # 3. 长尾标签（主题 + 细分）
        longtail_patterns = [
            f"{topic}技巧",
            f"{topic}教程",
            f"{topic}分享",
            f"{topic}心得",
            f"{topic}推荐",
        ]
        for tag in longtail_patterns[:3]:
            recommendations.append(TagRecommendation(
                tag=tag,
                category="longtail",
                score=0.7,
                reason="长尾关键词，竞争小"
            ))
        
        # 去重并排序
        seen = set()
        unique_recs = []
        for rec in recommendations:
            if rec.tag not in seen:
                seen.add(rec.tag)
                unique_recs.append(rec)
        
        # 按分数排序
        unique_recs.sort(key=lambda x: x.score, reverse=True)
        
        return unique_recs[:count]
    
    def format_tags(self, recommendations: List[TagRecommendation], 
                    platform: str) -> str:
        """
        格式化标签输出
        
        Args:
            recommendations: 推荐列表
            platform: 平台
            
        Returns:
            格式化后的标签字符串
        """
        tags = [rec.tag for rec in recommendations]
        
        if platform == "xiaohongshu":
            # 小红书格式：#标签 1 #标签 2
            return " ".join([f"#{tag}" for tag in tags])
        elif platform == "douyin":
            # 抖音格式：#标签 1#标签 2
            return "".join([f"#{tag}" for tag in tags])
        elif platform == "wechat":
            # 公众号：通常不用标签
            return ""
        elif platform == "zhihu":
            # 知乎：话题形式
            return ", ".join(tags)
        
        return " ".join(tags)


# 命令行测试
if __name__ == "__main__":
    recommender = TagRecommender()
    
    topic = "AI 写作"
    platform = "xiaohongshu"
    
    print(f"🏷️  为\"{topic}\"推荐{platform}标签：\n")
    
    recs = recommender.recommend(topic, platform, count=10)
    
    for rec in recs:
        print(f"[{rec.category}] #{rec.tag} (score: {rec.score})")
        print(f"  理由：{rec.reason}\n")
    
    print("\n📝 格式化输出:")
    print(recommender.format_tags(recs, platform))
