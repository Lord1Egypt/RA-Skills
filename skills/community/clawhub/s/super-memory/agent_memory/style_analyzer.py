from __future__ import annotations
"""
style_analyzer.py - 风格分析模块

v8.0: 个人风格 Agent
- 从内容中提取风格特征
- 视频内容风格分析
- 博主风格识别
- 风格量化评估
"""

import json
import re
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class StyleAnalyzer:
    """风格分析器"""
    
    def __init__(self):
        self.style_patterns = {
            "speaking_style": {
                "technical": ["专业", "技术", "架构", "优化", "代码", "系统", "算法", "性能"],
                "user_oriented": ["用户", "体验", "产品", "设计", "需求", "界面", "交互"],
                "creative": ["创意", "故事", "艺术", "想象", "灵感", "创作", "表达"],
                "strategic": ["战略", "商业", "市场", "团队", "领导", "管理", "目标"]
            },
            "emotional_tone": {
                "positive": ["积极", "创新", "机遇", "成长", "成功", "希望", "活力"],
                "negative": ["挑战", "风险", "问题", "困难", "失败", "危机", "压力"],
                "neutral": ["客观", "分析", "数据", "事实", "逻辑", "理性", "平衡"]
            },
            "cognitive_pattern": {
                "analytical": ["分析", "思考", "推理", "逻辑", "证据", "数据", "论证"],
                "intuitive": ["直觉", "感觉", "灵感", "创意", "想象", "体验", "感受"],
                "risk_seeking": ["冒险", "挑战", "创新", "突破", "尝试", "探索", "实验"],
                "risk_averse": ["安全", "稳定", "保守", "可靠", "传统", "经验", "验证"],
                "complexity_seeking": ["复杂", "系统", "全面", "深度", "细节", "综合", "整合"],
                "simplicity_seeking": ["简单", "清晰", "直接", "简洁", "明了", "基础", "核心"]
            }
        }
    
    def analyze(self, content: str) -> Dict[str, Any]:
        """分析文本内容的风格
        
        Args:
            content: 文本内容
        
        Returns:
            风格分析结果
        """
        content_lower = content.lower()
        
        # 分析说话风格
        speaking_style = self._analyze_speaking_style(content_lower)
        
        # 分析情感基调
        emotional_tone = self._analyze_emotional_tone(content_lower)
        
        # 分析认知模式
        cognitive_patterns = self._analyze_cognitive_patterns(content_lower)
        
        return {
            "speaking_style": speaking_style,
            "emotional_tone": emotional_tone,
            "cognitive_patterns": cognitive_patterns,
            "confidence": self._calculate_confidence(content)
        }
    
    def _analyze_speaking_style(self, content: str) -> str:
        """分析说话风格"""
        scores = {}
        for style, keywords in self.style_patterns["speaking_style"].items():
            scores[style] = sum(1 for keyword in keywords if keyword in content)
        
        if not scores or max(scores.values()) == 0:
            return "中性"
        
        dominant_style = max(scores, key=scores.get)
        style_mapping = {
            "technical": "专业、技术导向",
            "user_oriented": "用户导向、产品思维",
            "creative": "创意、富有想象力",
            "strategic": "战略性、领导力"
        }
        return style_mapping.get(dominant_style, "中性")
    
    def _analyze_emotional_tone(self, content: str) -> str:
        """分析情感基调"""
        scores = {}
        for tone, keywords in self.style_patterns["emotional_tone"].items():
            scores[tone] = sum(1 for keyword in keywords if keyword in content)
        
        if not scores:
            return "平衡、客观"
        
        dominant_tone = max(scores, key=scores.get)
        tone_mapping = {
            "positive": "积极、乐观",
            "negative": "谨慎、现实",
            "neutral": "平衡、客观"
        }
        return tone_mapping.get(dominant_tone, "平衡、客观")
    
    def _analyze_cognitive_patterns(self, content: str) -> Dict[str, float]:
        """分析认知模式"""
        patterns = {
            "reflective_depth": 0.5,
            "intuition_bias": 0.5,
            "risk_tolerance": 0.5,
            "complexity_preference": 0.5
        }
        
        # 分析反思深度
        analytical_score = sum(1 for keyword in self.style_patterns["cognitive_pattern"]["analytical"] if keyword in content)
        intuitive_score = sum(1 for keyword in self.style_patterns["cognitive_pattern"]["intuitive"] if keyword in content)
        total = analytical_score + intuitive_score
        if total > 0:
            patterns["reflective_depth"] = min(1.0, analytical_score / total)
            patterns["intuition_bias"] = min(1.0, intuitive_score / total)
        
        # 分析风险容忍度
        risk_seeking_score = sum(1 for keyword in self.style_patterns["cognitive_pattern"]["risk_seeking"] if keyword in content)
        risk_averse_score = sum(1 for keyword in self.style_patterns["cognitive_pattern"]["risk_averse"] if keyword in content)
        total_risk = risk_seeking_score + risk_averse_score
        if total_risk > 0:
            patterns["risk_tolerance"] = min(1.0, risk_seeking_score / total_risk)
        
        # 分析复杂度偏好
        complexity_score = sum(1 for keyword in self.style_patterns["cognitive_pattern"]["complexity_seeking"] if keyword in content)
        simplicity_score = sum(1 for keyword in self.style_patterns["cognitive_pattern"]["simplicity_seeking"] if keyword in content)
        total_complexity = complexity_score + simplicity_score
        if total_complexity > 0:
            patterns["complexity_preference"] = min(1.0, complexity_score / total_complexity)
        
        return patterns
    
    def _calculate_confidence(self, content: str) -> float:
        """计算分析置信度"""
        # 基于内容长度和关键词密度计算置信度
        content_length = len(content)
        if content_length < 50:
            return 0.3
        elif content_length < 200:
            return 0.6
        else:
            return 0.9
    
    def analyze_creator_style(self, videos: List[str]) -> Dict[str, Any]:
        """分析创作者的风格
        
        Args:
            videos: 视频内容列表
        
        Returns:
            创作者风格分析结果
        """
        if not videos:
            return {}
        
        # 合并所有视频内容
        combined_content = " ".join(videos)
        
        # 分析整体风格
        style = self.analyze(combined_content)
        
        # 提取主题偏好
        topic_preferences = self._extract_topic_preferences(combined_content)
        
        return {
            **style,
            "topic_preferences": topic_preferences,
            "video_count": len(videos)
        }
    
    def _extract_topic_preferences(self, content: str) -> List[str]:
        """提取主题偏好"""
        # 简化实现，实际应该使用更复杂的主题提取
        topics = {
            "技术": ["编程", "代码", "技术", "软件", "硬件", "网络", "算法"],
            "产品": ["产品", "设计", "用户", "体验", "界面", "功能", "需求"],
            "商业": ["商业", "市场", "营销", "销售", "创业", "投资", "管理"],
            "创意": ["创意", "设计", "艺术", "音乐", "视频", "写作", "创作"],
            "生活": ["生活", "健康", "美食", "旅行", "时尚", "娱乐", "运动"],
            "教育": ["教育", "学习", "知识", "技能", "考试", "培训", "课程"]
        }
        
        topic_scores = {}
        for topic, keywords in topics.items():
            topic_scores[topic] = sum(1 for keyword in keywords if keyword in content)
        
        # 排序并返回前3个主题
        sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
        return [topic for topic, score in sorted_topics if score > 0][:3]
    
    def compare_styles(self, style1: Dict[str, Any], style2: Dict[str, Any]) -> float:
        """比较两种风格的相似度
        
        Args:
            style1: 风格1
            style2: 风格2
        
        Returns:
            相似度 (0-1)
        """
        if not style1 or not style2:
            return 0.0
        
        # 比较认知模式
        cognitive1 = style1.get("cognitive_patterns", {})
        cognitive2 = style2.get("cognitive_patterns", {})
        
        similarity = 0.0
        count = 0
        
        for key in set(cognitive1.keys()) & set(cognitive2.keys()):
            similarity += 1 - abs(cognitive1[key] - cognitive2[key])
            count += 1
        
        if count > 0:
            similarity /= count
        
        # 比较说话风格和情感基调
        if style1.get("speaking_style") == style2.get("speaking_style"):
            similarity += 0.1
        if style1.get("emotional_tone") == style2.get("emotional_tone"):
            similarity += 0.1
        
        return min(1.0, similarity)


def extract_style_from_video(video_content: Dict[str, Any]) -> Dict[str, Any]:
    """从视频内容中提取风格
    
    Args:
        video_content: 视频内容，包含 transcript 和 description
    
    Returns:
        风格分析结果
    """
    analyzer = StyleAnalyzer()
    
    # 合并视频内容
    content_parts = []
    if video_content.get("transcript"):
        content_parts.append(video_content["transcript"])
    if video_content.get("description"):
        content_parts.append(video_content["description"])
    
    combined_content = " ".join(content_parts)
    
    # 分析风格
    return analyzer.analyze(combined_content)


def create_role_from_style(style: Dict[str, Any], name: str) -> Dict[str, Any]:
    """根据风格创建角色模板
    
    Args:
        style: 风格分析结果
        name: 角色名称
    
    Returns:
        角色模板数据
    """
    prompt_template = f"你是一位风格为{style.get('speaking_style', '中性')}的{name}，{style.get('emotional_tone', '平衡客观')}。"
    
    return {
        "name": name,
        "prompt_template": prompt_template,
        "personality_traits": style.get("cognitive_patterns", {}),
        "speaking_style": style.get("speaking_style", "中性"),
        "topic_preferences": style.get("topic_preferences", []),
        "emotional_tone": style.get("emotional_tone", "平衡、客观"),
        "source": "extracted",
        "version": "1.0"
    }
