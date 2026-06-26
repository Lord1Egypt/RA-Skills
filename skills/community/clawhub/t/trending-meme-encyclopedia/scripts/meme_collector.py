#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热梗收集与整理辅助脚本
用于整理和分析收集到的热梗数据
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class MemeType(Enum):
    """热梗类型"""
    QUOTE = "语录梗"
    BGM = "BGM梗"
    CHALLENGE = "挑战梗"
    GUICHU = "鬼畜梗"
    EMOTION = "表情梗"
    PLOT = "剧情梗"
    KNOWLEDGE = "知识梗"
    SOCIAL = "社会梗"
    HOMOPHONE = "谐音梗"
    OTHER = "其他"


class Platform(Enum):
    """平台"""
    BILIBILI = "B站"
    DOUYIN = "抖音"
    WEIBO = "微博"
    XIAOHONGSHU = "小红书"
    ZHIHU = "知乎"
    OTHER = "其他"


@dataclass
class MemeSource:
    """热梗来源信息"""
    original_title: str  # 原始内容标题
    creator: str  # 创作者
    platform: Platform  # 平台
    publish_time: str  # 发布时间
    original_url: str  # 原始链接
    content_id: str = ""  # 内容ID (BV号等)
    background_story: str = ""  # 背景故事


@dataclass
class MemeVideo:
    """相关视频信息"""
    title: str
    creator: str
    platform: Platform
    views: str = ""  # 播放量
    likes: str = ""  # 点赞数
    url: str = ""


@dataclass
class MemeEntry:
    """热梗条目"""
    name: str  # 梗名称
    heat_index: int  # 热度指数 (1-5)
    emerge_time: str  # 兴起时间
    platforms: List[Platform]  # 主要平台
    meme_type: MemeType  # 梗类型
    emotion: str  # 情感色彩
    
    source: MemeSource  # 来源信息
    literal_meaning: str = ""  # 字面意思
    internet_meaning: str = ""  # 网络含义
    usage_scenarios: List[str] = None  # 使用场景
    classic_quotes: List[str] = None  # 经典台词
    usage_examples: List[str] = None  # 使用示例
    variations: List[str] = None  # 常见变体
    videos: List[MemeVideo] = None  # 相关视频
    related_memes: List[str] = None  # 相关梗
    
    def __post_init__(self):
        if self.usage_scenarios is None:
            self.usage_scenarios = []
        if self.classic_quotes is None:
            self.classic_quotes = []
        if self.usage_examples is None:
            self.usage_examples = []
        if self.variations is None:
            self.variations = []
        if self.videos is None:
            self.videos = []
        if self.related_memes is None:
            self.related_memes = []
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


class MemeEncyclopedia:
    """热梗百科"""
    
    def __init__(self, date: str = None):
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.memes: List[MemeEntry] = []
        self.statistics = {
            "total_count": 0,
            "type_distribution": {},
            "platform_distribution": {}
        }
    
    def add_meme(self, meme: MemeEntry):
        """添加热梗"""
        self.memes.append(meme)
        self._update_statistics()
    
    def _update_statistics(self):
        """更新统计数据"""
        self.statistics["total_count"] = len(self.memes)
        
        # 类型分布
        type_dist = {}
        for meme in self.memes:
            t = meme.meme_type.value
            type_dist[t] = type_dist.get(t, 0) + 1
        self.statistics["type_distribution"] = type_dist
        
        # 平台分布
        platform_dist = {}
        for meme in self.memes:
            for p in meme.platforms:
                platform_dist[p.value] = platform_dist.get(p.value, 0) + 1
        self.statistics["platform_distribution"] = platform_dist
    
    def get_top_memes(self, n: int = 5) -> List[MemeEntry]:
        """获取热度最高的N个梗"""
        return sorted(self.memes, key=lambda x: x.heat_index, reverse=True)[:n]
    
    def get_memes_by_type(self, meme_type: MemeType) -> List[MemeEntry]:
        """按类型获取梗"""
        return [m for m in self.memes if m.meme_type == meme_type]
    
    def get_memes_by_platform(self, platform: Platform) -> List[MemeEntry]:
        """按平台获取梗"""
        return [m for m in self.memes if platform in m.platforms]
    
    def export_to_json(self, filepath: str):
        """导出为JSON"""
        data = {
            "date": self.date,
            "statistics": self.statistics,
            "memes": [m.to_dict() for m in self.memes],
            "exported_at": datetime.now().isoformat()
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已导出到: {filepath}")
    
    def generate_markdown(self) -> str:
        """生成Markdown格式的百科"""
        lines = [
            f"# {self.date} 热梗百科",
            "",
            f"> 📅 **统计时间**：{datetime.now().strftime('%Y年%m月%d日 %H:%M')}",
            f"> 🔢 **收录数量**：{self.statistics['total_count']}个热梗",
            "",
            "---",
            "",
            "## 📊 数据统计",
            "",
            "### 类型分布",
            ""
        ]
        
        # 类型分布表格
        lines.append("| 类型 | 数量 | 占比 |")
        lines.append("|------|------|------|")
        total = self.statistics['total_count']
        for t, count in sorted(self.statistics['type_distribution'].items(), 
                               key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            lines.append(f"| {t} | {count} | {percentage:.1f}% |")
        
        lines.extend(["", "### 平台分布", ""])
        lines.append("| 平台 | 数量 | 占比 |")
        lines.append("|------|------|------|")
        for p, count in sorted(self.statistics['platform_distribution'].items(),
                               key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            lines.append(f"| {p} | {count} | {percentage:.1f}% |")
        
        lines.extend(["", "---", "", "## 🔥 热梗榜单", ""])
        
        # 热梗列表
        for i, meme in enumerate(self.get_top_memes(10), 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}")
            stars = "⭐" * meme.heat_index + "☆" * (5 - meme.heat_index)
            platforms = ", ".join([p.value for p in meme.platforms])
            
            lines.append(f"### {medal} {meme.name}")
            lines.append("")
            lines.append(f"**热度**：{stars}")
            lines.append(f"**类型**：{meme.meme_type.value}")
            lines.append(f"**平台**：{platforms}")
            lines.append(f"**来源**：{meme.source.creator} @ {meme.source.platform.value}")
            lines.append("")
            
            if meme.internet_meaning:
                lines.append(f"**含义**：{meme.internet_meaning[:100]}...")
                lines.append("")
            
            lines.append(f"[查看详情](#{meme.name})")
            lines.append("")
        
        lines.extend(["---", "", "## 📖 热梗详解", ""])
        
        # 详细内容
        for meme in self.memes:
            lines.extend(self._generate_meme_detail(meme))
        
        return "\n".join(lines)
    
    def _generate_meme_detail(self, meme: MemeEntry) -> List[str]:
        """生成单个梗的详细内容"""
        lines = [
            f"### {meme.name}",
            "",
            "#### 基本信息",
            "",
            f"- **热度指数**：{'⭐' * meme.heat_index}{'☆' * (5 - meme.heat_index)}",
            f"- **兴起时间**：{meme.emerge_time}",
            f"- **主要平台**：{", ".join([p.value for p in meme.platforms])}",
            f"- **梗类型**：{meme.meme_type.value}",
            f"- **情感色彩**：{meme.emotion}",
            "",
            "#### 来源追溯",
            "",
            f"- **原始出处**：{meme.source.original_title}",
            f"- **创作者**：{meme.source.creator}",
            f"- **平台**：{meme.source.platform.value}",
            f"- **发布时间**：{meme.source.publish_time}",
        ]
        
        if meme.source.original_url:
            lines.append(f"- **原始链接**：[点击查看]({meme.source.original_url})")
        
        if meme.source.background_story:
            lines.extend([
                "",
                "**背景故事**：",
                f"> {meme.source.background_story}",
            ])
        
        lines.append("")
        
        if meme.literal_meaning or meme.internet_meaning:
            lines.extend([
                "#### 含义解释",
                "",
            ])
            
            if meme.literal_meaning:
                lines.extend([
                    "**字面意思**：",
                    f"> {meme.literal_meaning}",
                    "",
                ])
            
            if meme.internet_meaning:
                lines.extend([
                    "**网络含义**：",
                    f"> {meme.internet_meaning}",
                    "",
                ])
        
        if meme.usage_scenarios:
            lines.extend([
                "**使用场景**：",
            ])
            for scenario in meme.usage_scenarios:
                lines.append(f"- {scenario}")
            lines.append("")
        
        if meme.classic_quotes:
            lines.extend([
                "**经典台词**：",
                "",
            ])
            for quote in meme.classic_quotes:
                lines.append(f"> {quote}")
            lines.append("")
        
        if meme.videos:
            lines.extend([
                "#### 相关视频",
                "",
                "| 平台 | 视频标题 | 创作者 | 链接 |",
                "|------|----------|--------|------|",
            ])
            for video in meme.videos[:5]:  # 最多显示5个
                lines.append(f"| {video.platform.value} | {video.title} | {video.creator} | [观看]({video.url}) |")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        
        return lines


class MemeSearcher:
    """热梗搜索辅助"""
    
    # 搜索关键词模板
    SEARCH_TEMPLATES = {
        "bilibili": [
            "B站热梗 {time}",
            "bilibili热门梗 合集",
            "鬼畜 热门 {time}",
            "弹幕热词 梗",
            "梗指南 更新",
        ],
        "douyin": [
            "抖音热梗 {time}",
            "抖音挑战 热门",
            "抖音BGM 梗",
            "抖音热门话题",
        ],
        "general": [
            "网络热梗 {time}",
            "互联网热词 梗",
            "梗百科 更新",
        ]
    }
    
    @classmethod
    def get_search_keywords(cls, platform: str = "general", time_range: str = "当天") -> List[str]:
        """获取搜索关键词"""
        templates = cls.SEARCH_TEMPLATES.get(platform, cls.SEARCH_TEMPLATES["general"])
        return [t.format(time=time_range) for t in templates]
    
    @classmethod
    def get_source_tracing_keywords(cls, meme_name: str) -> List[str]:
        """获取来源追溯关键词"""
        return [
            f"{meme_name} 出处",
            f"{meme_name} 来源",
            f"{meme_name} 原版",
            f"{meme_name} 梗百科",
            f"{meme_name} 是什么意思",
        ]


class MemeHeatCalculator:
    """热度计算器"""
    
    @staticmethod
    def calculate_heat(
        search_volume: int = 0,  # 搜索量
        video_views: int = 0,    # 视频播放量
        discussion_count: int = 0,  # 讨论数
        cross_platform: int = 1,    # 跨平台数
        duration_days: int = 1      # 持续天数
    ) -> int:
        """
        计算热度指数 (1-5)
        
        评分标准：
        - 5星：现象级，全平台爆发
        - 4星：高热，多平台热门
        - 3星：中热，单一平台热门
        - 2星：低热，小众传播
        - 1星：微热，刚兴起
        """
        score = 0
        
        # 搜索量评分
        if search_volume > 1000000:
            score += 2
        elif search_volume > 100000:
            score += 1
        
        # 播放量评分
        if video_views > 10000000:
            score += 2
        elif video_views > 1000000:
            score += 1
        
        # 讨论数评分
        if discussion_count > 100000:
            score += 1
        
        # 跨平台评分
        score += min(cross_platform - 1, 1)
        
        # 持续时间评分
        if duration_days >= 7:
            score += 1
        
        return min(max(score, 1), 5)


# 使用示例
if __name__ == "__main__":
    # 创建百科实例
    encyclopedia = MemeEncyclopedia("2024-01-15")
    
    # 创建示例热梗
    meme = MemeEntry(
        name="示例梗",
        heat_index=4,
        emerge_time="2024-01-10",
        platforms=[Platform.BILIBILI, Platform.DOUYIN],
        meme_type=MemeType.QUOTE,
        emotion="搞笑",
        source=MemeSource(
            original_title="示例视频标题",
            creator="示例UP主",
            platform=Platform.BILIBILI,
            publish_time="2024-01-10",
            original_url="https://example.com",
            background_story="这是一个示例梗的背景故事"
        ),
        literal_meaning="字面意思",
        internet_meaning="网络含义",
        usage_scenarios=["场景1", "场景2"],
        classic_quotes=["经典台词1"],
    )
    
    # 添加视频
    meme.videos.append(MemeVideo(
        title="示例视频",
        creator="示例UP主",
        platform=Platform.BILIBILI,
        views="100万",
        likes="10万",
        url="https://example.com"
    ))
    
    # 添加到百科
    encyclopedia.add_meme(meme)
    
    # 生成Markdown
    markdown = encyclopedia.generate_markdown()
    print(markdown)
    
    # 导出JSON
    encyclopedia.export_to_json("meme_encyclopedia.json")
    
    # 获取搜索关键词
    keywords = MemeSearcher.get_search_keywords("bilibili", "本周")
    print("\n搜索关键词：")
    for kw in keywords:
        print(f"  - {kw}")
