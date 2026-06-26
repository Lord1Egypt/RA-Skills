#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能任务检测器 v3.0
作者: zcg007
日期: 2026-03-15

使用多层级检测算法识别任务类型和意图
"""

import re
import json
from typing import Dict, List, Tuple, Optional, Any
import logging
from collections import defaultdict
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)


class TaskDetector:
    """智能任务检测器"""
    
    def __init__(self, config=None):
        """
        初始化任务检测器
        
        Args:
            config: 配置字典，如果为None则使用默认配置
        """
        if config is None:
            from config_loader import config_loader
            self.config = config_loader.get_detection_config()
        else:
            self.config = config
        
        # 任务关键词词典
        self.task_keywords = self.config.get("task_keywords", {})
        
        # 通用任务模式
        self.task_patterns = {
            "excel": [
                r"(?:制作|创建|生成|处理).*?(?:excel|表格|报表|预算|财务)",
                r"(?:分析|统计).*?(?:数据|报表)",
                r"(?:合并|清洗|整理).*?(?:表格|数据)",
            ],
            "skill": [
                r"(?:安装|下载|创建|制作|开发).*?(?:技能|skill)",
                r"(?:更新|升级).*?(?:版本)",
                r"(?:测试|验证).*?(?:技能|功能)",
            ],
            "memory": [
                r"(?:回忆|检索|查找|搜索).*?(?:记忆|经验|总结)",
                r"(?:记录|保存|存储).*?(?:记忆|经验)",
                r"(?:学习|了解).*?(?:方法|技巧)",
            ],
            "workflow": [
                r"(?:自动化|优化|改进).*?(?:工作流|流程)",
                r"(?:创建|设计).*?(?:流程|步骤)",
                r"(?:执行|运行).*?(?:任务|操作)",
            ],
            "analysis": [
                r"(?:分析|评估|研究).*?(?:问题|情况)",
                r"(?:总结|报告).*?(?:结果|发现)",
                r"(?:统计|计算).*?(?:数据|指标)",
            ],
        }
        
        # 意图关键词
        self.intent_keywords = {
            "instruction": ["制作", "创建", "生成", "处理", "安装", "下载", "运行"],
            "question": ["什么", "如何", "怎么", "为什么", "是否", "能否", "有没有"],
            "request": ["请", "帮忙", "帮助", "协助", "需要", "想要", "希望"],
            "confirmation": ["确认", "验证", "检查", "测试", "确保", "核对"],
            "explanation": ["解释", "说明", "介绍", "描述", "讲述"],
        }
        
        # 上下文管理器
        self.context_history = []
        self.max_context_size = self.config.get("context_window", 5)
        
        # 任务类型权重
        self.task_weights = {
            "excel": 1.0,
            "skill": 0.9,
            "memory": 0.8,
            "workflow": 0.7,
            "analysis": 0.6,
        }
        
        # 缓存检测结果
        self.detection_cache = {}
    
    def detect_task(self, text: str, context: List[str] = None) -> Dict[str, Any]:
        """
        检测任务类型和意图
        
        Args:
            text: 输入文本
            context: 上下文历史（可选）
            
        Returns:
            检测结果字典
        """
        # 检查缓存
        cache_key = f"{text}_{hash(str(context)) if context else 0}"
        if cache_key in self.detection_cache:
            return self.detection_cache[cache_key]
        
        # 更新上下文
        self._update_context(text, context)
        
        # 多层级检测
        detection_result = {
            "text": text,
            "timestamp": datetime.now().isoformat(),
            "task_types": [],
            "primary_task": None,
            "confidence": 0.0,
            "intent": None,
            "keywords_found": [],
            "suggested_actions": [],
            "context_used": len(self.context_history),
        }
        
        # 1. 关键词检测
        keyword_results = self._detect_by_keywords(text)
        detection_result["keywords_found"] = keyword_results["keywords"]
        
        # 2. 模式匹配检测
        pattern_results = self._detect_by_patterns(text)
        
        # 3. 意图分析
        intent_result = self._detect_intent(text)
        detection_result["intent"] = intent_result["intent"]
        
        # 4. 上下文增强检测
        context_results = self._detect_with_context(text)
        
        # 5. 合并检测结果
        all_task_scores = defaultdict(float)
        
        # 合并关键词检测结果
        for task_type, score in keyword_results["scores"].items():
            all_task_scores[task_type] += score * 0.4
        
        # 合并模式匹配结果
        for task_type, score in pattern_results["scores"].items():
            all_task_scores[task_type] += score * 0.3
        
        # 合并上下文结果
        for task_type, score in context_results["scores"].items():
            all_task_scores[task_type] += score * 0.3
        
        # 6. 应用权重
        for task_type in list(all_task_scores.keys()):
            weight = self.task_weights.get(task_type, 0.5)
            all_task_scores[task_type] *= weight
        
        # 7. 排序和选择
        if all_task_scores:
            sorted_tasks = sorted(
                all_task_scores.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            detection_result["task_types"] = [
                {"type": task_type, "score": score}
                for task_type, score in sorted_tasks
                if score >= self.config.get("min_confidence", 0.3)
            ]
            
            if detection_result["task_types"]:
                detection_result["primary_task"] = detection_result["task_types"][0]["type"]
                detection_result["confidence"] = detection_result["task_types"][0]["score"]
        
        # 8. 生成建议操作
        detection_result["suggested_actions"] = self._generate_suggestions(
            detection_result["primary_task"],
            detection_result["intent"],
            keyword_results["keywords"]
        )
        
        # 缓存结果
        self.detection_cache[cache_key] = detection_result
        
        # 清理缓存（保持大小）
        if len(self.detection_cache) > 100:
            self._clean_cache()
        
        logger.debug(f"任务检测完成: {detection_result['primary_task']} (置信度: {detection_result['confidence']:.2f})")
        return detection_result
    
    def _detect_by_keywords(self, text: str) -> Dict[str, Any]:
        """基于关键词检测任务类型"""
        text_lower = text.lower()
        keywords_found = []
        task_scores = defaultdict(float)
        
        for task_type, keyword_list in self.task_keywords.items():
            for keyword in keyword_list:
                keyword_lower = keyword.lower()
                if keyword_lower in text_lower:
                    keywords_found.append({
                        "keyword": keyword,
                        "task_type": task_type,
                        "position": text_lower.find(keyword_lower)
                    })
                    
                    # 计算关键词分数
                    # 关键词在文本中的位置越靠前，分数越高
                    position_score = 1.0 - (text_lower.find(keyword_lower) / len(text_lower))
                    task_scores[task_type] += position_score * 0.1
        
        return {
            "keywords": keywords_found,
            "scores": dict(task_scores)
        }
    
    def _detect_by_patterns(self, text: str) -> Dict[str, Any]:
        """基于正则表达式模式检测任务类型"""
        task_scores = defaultdict(float)
        
        for task_type, patterns in self.task_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    # 模式匹配成功，增加分数
                    task_scores[task_type] += 0.2
        
        return {"scores": dict(task_scores)}
    
    def _detect_intent(self, text: str) -> Dict[str, Any]:
        """检测用户意图"""
        text_lower = text.lower()
        intent_scores = defaultdict(float)
        
        for intent_type, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    intent_scores[intent_type] += 0.1
        
        # 确定主要意图
        if intent_scores:
            primary_intent = max(intent_scores.items(), key=lambda x: x[1])[0]
        else:
            primary_intent = "unknown"
        
        # 根据文本特征进一步判断
        if any(word in text_lower for word in ["?", "？", "什么", "如何", "怎么"]):
            primary_intent = "question"
        elif any(word in text_lower for word in ["请", "帮忙", "帮助"]):
            primary_intent = "request"
        
        return {
            "intent": primary_intent,
            "scores": dict(intent_scores)
        }
    
    def _detect_with_context(self, text: str) -> Dict[str, Any]:
        """结合上下文进行检测"""
        if not self.context_history:
            return {"scores": {}}
        
        task_scores = defaultdict(float)
        
        # 分析最近上下文中的任务类型
        recent_context = self.context_history[-3:]  # 最近3条上下文
        
        for context_text in recent_context:
            # 直接分析上下文文本，避免递归调用detect_task
            # 使用简单的关键词匹配而不是完整的任务检测
            context_lower = context_text.lower()
            
            for task_type, keyword_list in self.task_keywords.items():
                for keyword in keyword_list:
                    if keyword.lower() in context_lower:
                        # 上下文匹配分数
                        task_scores[task_type] += 0.1
            
            # 检查模式匹配
            for task_type, patterns in self.task_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, context_text, re.IGNORECASE):
                        task_scores[task_type] += 0.15
        
        return {"scores": dict(task_scores)}
    
    def _update_context(self, text: str, context: List[str] = None) -> None:
        """更新上下文历史"""
        if context:
            self.context_history.extend(context)
        else:
            self.context_history.append(text)
        
        # 保持上下文大小
        if len(self.context_history) > self.max_context_size:
            self.context_history = self.context_history[-self.max_context_size:]
    
    def _generate_suggestions(self, task_type: str, intent: str, keywords: List[Dict]) -> List[str]:
        """根据检测结果生成建议操作"""
        suggestions = []
        
        if not task_type:
            return ["请提供更多任务描述以便我更好地理解您的需求"]
        
        # 根据任务类型生成建议
        if task_type == "excel":
            suggestions.extend([
                "建议先检查现有Excel文件的格式和结构",
                "是否需要我帮助分析Excel数据？",
                "建议创建数据清洗和验证流程",
            ])
        elif task_type == "skill":
            suggestions.extend([
                "建议先通过SkillHub搜索相关技能",
                "是否需要我帮助安装或测试技能？",
                "建议记录技能安装过程中的关键经验",
            ])
        elif task_type == "memory":
            suggestions.extend([
                "建议检索相关记忆和经验",
                "是否需要记录新的学习经验？",
                "建议整理和分类记忆文件",
            ])
        elif task_type == "workflow":
            suggestions.extend([
                "建议分析当前工作流程的瓶颈",
                "是否需要自动化某些重复任务？",
                "建议创建标准化操作流程",
            ])
        
        # 根据意图生成建议
        if intent == "question":
            suggestions.append("我将为您提供详细的解答和指导")
        elif intent == "request":
            suggestions.append("我将立即开始处理您的请求")
        elif intent == "instruction":
            suggestions.append("我将按照您的指示执行操作")
        
        # 根据关键词生成具体建议
        for keyword_info in keywords:
            keyword = keyword_info["keyword"]
            if keyword in ["预算", "财务"]:
                suggestions.append("建议创建带公式的动态预算表")
            elif keyword in ["合并", "清洗"]:
                suggestions.append("建议保留原始公式和数据完整性")
            elif keyword in ["安装", "下载"]:
                suggestions.append("建议通过SkillHub官方渠道安装")
        
        return suggestions
    
    def _clean_cache(self) -> None:
        """清理过期的缓存"""
        # 简单策略：删除一半最旧的缓存
        if len(self.detection_cache) > 100:
            keys_to_remove = list(self.detection_cache.keys())[:50]
            for key in keys_to_remove:
                del self.detection_cache[key]
    
    def get_context_summary(self) -> str:
        """获取上下文摘要"""
        if not self.context_history:
            return "无上下文历史"
        
        summary = []
        for i, text in enumerate(self.context_history[-3:], 1):
            # 截断长文本
            if len(text) > 50:
                text = text[:47] + "..."
            summary.append(f"{i}. {text}")
        
        return "\n".join(summary)
    
    def clear_context(self) -> None:
        """清除上下文历史"""
        self.context_history = []
        logger.info("上下文历史已清除")


# 全局任务检测器实例
task_detector = TaskDetector()


if __name__ == "__main__":
    # 测试任务检测器
    detector = TaskDetector()
    
    test_texts = [
        "请帮我制作一个Excel预算表",
        "如何安装新的技能？",
        "帮我回忆一下之前的Excel处理经验",
        "创建工作流自动化方案",
        "这是什么意思？",
    ]
    
    print("=== 任务检测器测试 ===")
    for text in test_texts:
        result = detector.detect_task(text)
        print(f"\n文本: {text}")
        print(f"主要任务: {result['primary_task']}")
        print(f"置信度: {result['confidence']:.2f}")
        print(f"意图: {result['intent']}")
        print(f"关键词: {[k['keyword'] for k in result['keywords_found']]}")
        print(f"建议操作: {result['suggested_actions'][:2]}")
    
    print("\n=== 上下文测试 ===")
    detector.clear_context()
    
    # 模拟对话流程
    detector.detect_task("我想学习Excel处理")
    detector.detect_task("具体是制作预算表")
    detector.detect_task("请帮我创建带公式的预算表")
    
    print("上下文摘要:")
    print(detector.get_context_summary())