#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强对话钩子 v3.0
作者: zcg007
日期: 2026-03-15

智能检测对话意图，自动触发记忆检索和工作准备
"""

import re
import json
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging
from collections import defaultdict

from task_detector import TaskDetector
from memory_retriever import MemoryRetriever
from config_loader import config_loader

logger = logging.getLogger(__name__)


class ConversationHook:
    """增强对话钩子"""
    
    def __init__(self, config=None):
        """
        初始化对话钩子
        
        Args:
            config: 配置字典
        """
        if config is None:
            self.config = config_loader.load_config()
        else:
            self.config = config
        
        # 初始化组件
        self.task_detector = TaskDetector(self.config.get("detection_config", {}))
        self.memory_retriever = MemoryRetriever(self.config.get("retrieval_config", {}))
        
        # 对话历史
        self.conversation_history = []
        self.max_history_size = 20
        
        # 状态跟踪
        self.last_trigger_time = None
        self.trigger_count = 0
        self.trigger_types = defaultdict(int)
        
        # 触发条件配置
        self.trigger_conditions = {
            "new_task": {
                "keywords": ["制作", "创建", "生成", "处理", "安装", "开发", "实现"],
                "patterns": [r"请.*(?:制作|创建|处理).*", r"帮我.*(?:做|弄|搞).*"],
                "min_length": 5,
                "cooldown_seconds": 60,
            },
            "question": {
                "keywords": ["什么", "如何", "怎么", "为什么", "是否", "能否", "有没有"],
                "patterns": [r".*[?？].*", r".*吗.*", r".*呢.*"],
                "min_length": 3,
                "cooldown_seconds": 30,
            },
            "problem": {
                "keywords": ["错误", "问题", "故障", "失败", "不行", "不能", "无法"],
                "patterns": [r".*错误.*", r".*问题.*", r".*怎么办.*"],
                "min_length": 5,
                "cooldown_seconds": 45,
            },
            "memory_request": {
                "keywords": ["回忆", "记忆", "经验", "总结", "之前", "以前", "历史"],
                "patterns": [r".*回忆.*", r".*记忆.*", r".*经验.*"],
                "min_length": 4,
                "cooldown_seconds": 30,
            },
            "skill_reminder": {
                "keywords": ["@skill", "workbuddy-add-memory", "技能", "忘记", "又忘了", "没用"],
                "patterns": [r".*@skill.*", r".*workbuddy.*memory.*", r".*忘了.*技能.*"],
                "min_length": 3,
                "cooldown_seconds": 30,
            },
        }
        
        # 响应模板
        self.response_templates = {
            "new_task": {
                "title": "🎯 检测到新任务启动",
                "template": """检测到您正在开始新的任务：**{task_description}**

**相关记忆检索结果：**
{memory_results}

**智能建议：**
{suggestions}

**下一步操作：**
1. {action1}
2. {action2}
3. {action3}

需要我立即开始执行吗？""",
            },
            "question": {
                "title": "❓ 检测到问题咨询",
                "template": """检测到您的问题：**{query}**

**相关解答参考：**
{memory_results}

**详细解答：**
{detailed_answer}

**扩展知识：**
{extended_info}

**参考链接：**
{references}

还有其它问题吗？""",
            },
            "problem": {
                "title": "⚠️ 检测到问题报告",
                "template": """检测到您遇到的问题：**{problem_description}**

**类似问题解决方案：**
{memory_results}

**问题分析：**
{problem_analysis}

**解决步骤：**
1. {step1}
2. {step2}
3. {step3}

**预防措施：**
{prevention_tips}

需要我帮您解决这个问题吗？""",
            },
            "memory_request": {
                "title": "📚 记忆检索结果",
                "template": """根据您的要求，检索相关记忆：

**检索关键词：** {keywords}

**检索结果（{result_count}条）：**
{memory_results}

**记忆分类统计：**
{category_stats}

**重要性分布：**
{importance_stats}

**时间范围：** {time_range}

需要进一步筛选或查找特定记忆吗？""",
            },
            "skill_reminder": {
                "title": "⚠️ 技能使用提醒检测",
                "template": """检测到您提醒我使用workbuddy-add-memory技能！

**问题分析：**
{problem_analysis}

**我的错误原因：**
{skill_error_analysis}

**根本解决方案：**
{skill_solution}

**立即纠正步骤：**
1. {action1}
2. {action2}
3. {action3}

**长期预防措施：**
{skill_prevention}

**核心承诺：**
{skill_commitment}

请确认我是否正确理解了您的提醒！""",
            },
        }
        
        # 加载记忆库
        self._load_memory_library()
    
    def _load_memory_library(self) -> bool:
        """加载记忆库"""
        try:
            memory_sources = config_loader.get_memory_sources()
            loaded_count = self.memory_retriever.load_memories(memory_sources)
            
            if loaded_count > 0:
                self.memory_retriever.build_index()
                logger.info(f"记忆库加载完成: {loaded_count} 个记忆")
                return True
            else:
                logger.warning("记忆库加载失败或为空")
                return False
                
        except Exception as e:
            logger.error(f"加载记忆库失败: {e}")
            return False
    
    def process_message(self, message: str, user_id: str = "default", 
                       context: List[str] = None) -> Dict[str, Any]:
        """
        处理用户消息，检测是否需要触发记忆检索
        
        Args:
            message: 用户消息
            user_id: 用户ID
            context: 上下文历史
            
        Returns:
            处理结果字典
        """
        # 记录对话历史
        self._add_to_history({
            "user_id": user_id,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "context": context,
        })
        
        # 检测触发条件
        trigger_result = self._detect_trigger(message, context)
        
        response = {
            "message": message,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "trigger_detected": trigger_result["triggered"],
            "trigger_type": trigger_result["type"],
            "confidence": trigger_result["confidence"],
            "should_respond": False,
            "response": None,
            "memories_retrieved": [],
            "suggestions": [],
            "actions": [],
        }
        
        # 如果触发，生成响应
        if trigger_result["triggered"]:
            response_data = self._generate_response(
                message, 
                trigger_result["type"],
                context
            )
            
            response.update({
                "should_respond": True,
                "response": response_data["response"],
                "memories_retrieved": response_data["memories"],
                "suggestions": response_data["suggestions"],
                "actions": response_data["actions"],
            })
            
            # 更新统计
            self.trigger_count += 1
            self.trigger_types[trigger_result["type"]] += 1
            self.last_trigger_time = datetime.now()
        
        return response
    
    def _detect_trigger(self, message: str, context: List[str] = None) -> Dict[str, Any]:
        """
        检测是否触发记忆检索
        
        Args:
            message: 用户消息
            context: 上下文
            
        Returns:
            触发检测结果
        """
        message_lower = message.lower()
        message_length = len(message.strip())
        
        # 检查冷却时间
        if self.last_trigger_time:
            elapsed = (datetime.now() - self.last_trigger_time).total_seconds()
            
            # 根据最后触发类型获取冷却时间
            last_type = max(self.trigger_types.items(), key=lambda x: x[1])[0] if self.trigger_types else None
            if last_type:
                cooldown = self.trigger_conditions.get(last_type, {}).get("cooldown_seconds", 30)
                if elapsed < cooldown:
                    return {
                        "triggered": False,
                        "type": None,
                        "confidence": 0.0,
                        "reason": f"冷却时间中 ({elapsed:.1f}/{cooldown}秒)",
                    }
        
        # 多条件检测
        trigger_scores = defaultdict(float)
        trigger_reasons = {}
        
        for trigger_type, condition in self.trigger_conditions.items():
            score = 0.0
            reasons = []
            
            # 检查消息长度
            if message_length < condition["min_length"]:
                continue
            
            # 关键词匹配
            keyword_matches = 0
            for keyword in condition["keywords"]:
                if keyword in message_lower:
                    keyword_matches += 1
            
            if keyword_matches > 0:
                score += keyword_matches * 0.2
                reasons.append(f"关键词匹配({keyword_matches}个)")
            
            # 模式匹配
            pattern_matches = 0
            for pattern in condition["patterns"]:
                if re.search(pattern, message, re.IGNORECASE):
                    pattern_matches += 1
            
            if pattern_matches > 0:
                score += pattern_matches * 0.3
                reasons.append(f"模式匹配({pattern_matches}个)")
            
            # 任务检测器增强
            task_result = self.task_detector.detect_task(message, context)
            if task_result["primary_task"]:
                score += task_result["confidence"] * 0.3
                reasons.append(f"任务检测({task_result['primary_task']})")
            
            # 上下文增强
            if context and len(context) > 0:
                # 检查是否是新话题
                if self._is_new_topic(message, context):
                    score += 0.2
                    reasons.append("新话题检测")
            
            # 记录分数和原因
            if score > 0:
                trigger_scores[trigger_type] = score
                trigger_reasons[trigger_type] = reasons
        
        # 确定最高分数
        if trigger_scores:
            best_trigger = max(trigger_scores.items(), key=lambda x: x[1])
            best_type = best_trigger[0]
            best_score = best_trigger[1]
            
            # 设置阈值
            threshold = 0.4
            
            if best_score >= threshold:
                return {
                    "triggered": True,
                    "type": best_type,
                    "confidence": min(best_score, 1.0),
                    "reason": f"综合检测: {', '.join(trigger_reasons[best_type])}",
                }
        
        return {
            "triggered": False,
            "type": None,
            "confidence": 0.0,
            "reason": "未达到触发阈值",
        }
    
    def _is_new_topic(self, message: str, context: List[str]) -> bool:
        """检测是否是新话题"""
        if not context:
            return True
        
        # 简单检测：检查关键词重叠
        message_words = set(re.findall(r'\w+', message.lower()))
        
        topic_changed = True
        for context_message in context[-3:]:  # 检查最近3条上下文
            context_words = set(re.findall(r'\w+', context_message.lower()))
            
            # 计算重叠度
            overlap = len(message_words & context_words)
            total_unique = len(message_words | context_words)
            
            if total_unique > 0:
                overlap_ratio = overlap / total_unique
                if overlap_ratio > 0.3:  # 30%重叠认为相关
                    topic_changed = False
                    break
        
        return topic_changed
    
    def _generate_response(self, message: str, trigger_type: str, 
                          context: List[str] = None) -> Dict[str, Any]:
        """
        生成响应
        
        Args:
            message: 原始消息
            trigger_type: 触发类型
            context: 上下文
            
        Returns:
            响应数据
        """
        # 检索相关记忆
        memories = self.memory_retriever.search(message, top_k=5)
        
        # 任务检测
        task_result = self.task_detector.detect_task(message, context)
        
        # 获取模板
        template_info = self.response_templates.get(trigger_type, {})
        
        # 格式化记忆结果
        formatted_memories = self._format_memories(memories)
        
        # 生成建议
        suggestions = task_result.get("suggested_actions", [])
        if not suggestions:
            suggestions = self._generate_default_suggestions(trigger_type, memories)
        
        # 生成操作
        actions = self._generate_actions(trigger_type, task_result, memories)
        
        # 填充模板
        template_data = {
            "task_description": message[:100],
            "query": message,
            "problem_description": message,
            "keywords": self._extract_keywords(message),
            "memory_results": formatted_memories,
            "result_count": len(memories),
            "suggestions": "\n".join(f"- {s}" for s in suggestions[:3]),
            "detailed_answer": self._generate_detailed_answer(memories),
            "problem_analysis": self._analyze_problem(message, memories),
            "action1": actions[0] if len(actions) > 0 else "分析任务需求",
            "action2": actions[1] if len(actions) > 1 else "准备相关资源",
            "action3": actions[2] if len(actions) > 2 else "开始执行操作",
            "step1": actions[0] if len(actions) > 0 else "确认问题现象",
            "step2": actions[1] if len(actions) > 1 else "分析问题原因",
            "step3": actions[2] if len(actions) > 2 else "实施解决方案",
            "prevention_tips": self._generate_prevention_tips(memories),
            "extended_info": self._generate_extended_info(memories),
            "references": self._generate_references(memories),
            "category_stats": self._generate_category_stats(memories),
            "importance_stats": self._generate_importance_stats(memories),
            "time_range": self._generate_time_range(memories),
        }
        
        # 如果是技能提醒类型，添加特定数据
        if trigger_type == "skill_reminder":
            template_data.update({
                "skill_error_analysis": self._analyze_skill_error(message, memories),
                "skill_solution": self._generate_skill_solution(memories),
                "skill_prevention": self._generate_skill_prevention(memories),
                "skill_commitment": self._generate_skill_commitment(),
            })
        
        response_text = self._fill_template(
            template_info.get("template", ""),
            template_data
        )
        
        # 添加标题
        if template_info.get("title"):
            response_text = f"## {template_info['title']}\n\n{response_text}"
        
        return {
            "response": response_text,
            "memories": memories,
            "suggestions": suggestions,
            "actions": actions,
            "trigger_type": trigger_type,
            "task_type": task_result.get("primary_task"),
        }
    
    def _format_memories(self, memories: List[Dict]) -> str:
        """格式化记忆结果"""
        if not memories:
            return "暂无相关记忆。"
        
        formatted = []
        for i, memory in enumerate(memories, 1):
            title = memory.get("title", "无标题")
            relevance = memory.get("relevance_score", 0)
            category = memory.get("category", "general")
            importance = memory.get("importance", "normal")
            
            # 截断内容
            content = memory.get("content", "")[:150]
            if len(memory.get("content", "")) > 150:
                content += "..."
            
            formatted.append(
                f"{i}. **{title}** (相关性: {relevance:.3f})\n"
                f"   类别: {category}, 重要性: {importance}\n"
                f"   {content}\n"
            )
        
        return "\n".join(formatted)
    
    def _extract_keywords(self, text: str) -> str:
        """提取关键词"""
        # 简单关键词提取
        words = re.findall(r'[\u4e00-\u9fff]{2,5}|\b[a-z]{3,15}\b', text.lower())
        
        # 去重并限制数量
        unique_words = list(set(words))[:10]
        
        return "、".join(unique_words) if unique_words else "无明确关键词"
    
    def _generate_default_suggestions(self, trigger_type: str, memories: List[Dict]) -> List[str]:
        """生成默认建议"""
        suggestions = []
        
        if trigger_type == "new_task":
            suggestions.extend([
                "建议先分析任务的具体要求",
                "查阅相关文档和最佳实践",
                "制定详细的工作计划",
            ])
        elif trigger_type == "question":
            suggestions.extend([
                "建议查阅官方文档",
                "参考类似问题的解决方案",
                "如有疑问可进一步询问",
            ])
        elif trigger_type == "problem":
            suggestions.extend([
                "建议先确认问题复现步骤",
                "检查相关配置和依赖",
                "查看错误日志和堆栈信息",
            ])
        elif trigger_type == "memory_request":
            suggestions.extend([
                "建议使用更具体的关键词",
                "可以按时间或类别筛选",
                "如需特定记忆可进一步描述",
            ])
        
        return suggestions
    
    def _generate_actions(self, trigger_type: str, task_result: Dict, 
                         memories: List[Dict]) -> List[str]:
        """生成操作建议"""
        actions = []
        
        if trigger_type == "new_task":
            task_type = task_result.get("primary_task")
            
            if task_type == "excel":
                actions.extend([
                    "检查Excel文件结构和格式",
                    "分析数据内容和业务逻辑",
                    "制定处理方案和验证方法",
                ])
            elif task_type == "skill":
                actions.extend([
                    "通过SkillHub搜索相关技能",
                    "检查技能依赖和兼容性",
                    "制定安装和测试计划",
                ])
            else:
                actions.extend([
                    "分析任务需求和约束条件",
                    "准备必要资源和工具",
                    "设计执行方案和验证标准",
                ])
        
        elif trigger_type == "problem":
            actions.extend([
                "收集问题详细信息和现象",
                "分析可能的原因和影响因素",
                "制定解决方案和验证步骤",
            ])
        
        return actions
    
    def _generate_detailed_answer(self, memories: List[Dict]) -> str:
        """生成详细解答"""
        if not memories:
            return "目前没有找到详细的解答信息，建议查阅相关文档或进一步描述问题。"
        
        # 使用第一个高相关性的记忆作为主要解答
        best_memory = memories[0]
        content = best_memory.get("content", "")
        
        # 提取核心内容（前500字）
        if len(content) > 500:
            content = content[:497] + "..."
        
        return content
    
    def _analyze_problem(self, problem: str, memories: List[Dict]) -> str:
        """分析问题"""
        if not memories:
            return f"问题分析：'{problem}'。目前没有找到类似问题的解决方案，建议收集更多信息或尝试通用排查方法。"
        
        # 分析常见问题和解决方案
        common_causes = []
        for memory in memories[:3]:
            title = memory.get("title", "")
            if "错误" in title or "问题" in title or "故障" in title:
                common_causes.append(f"- {title}")
        
        if common_causes:
            causes_text = "\n".join(common_causes)
            return f"问题分析：'{problem}'。可能的原因包括：\n{causes_text}"
        else:
            return f"问题分析：'{problem}'。找到了一些相关经验，但未明确匹配具体问题原因。"
    
    def _generate_prevention_tips(self, memories: List[Dict]) -> str:
        """生成预防措施"""
        tips = []
        
        for memory in memories[:3]:
            content = memory.get("content", "")
            # 提取包含"建议"、"应该"、"避免"等词的句子
            sentences = re.findall(r'[^。！？]*[建议|应该|避免|注意|防止][^。！？]*[。！？]', content)
            tips.extend(sentences[:2])
        
        if tips:
            return "\n".join(f"- {tip}" for tip in tips[:5])
        else:
            return "- 定期备份重要数据\n- 遵循最佳实践和规范\n- 及时更新相关依赖"
    
    def _generate_extended_info(self, memories: List[Dict]) -> str:
        """生成扩展信息"""
        if not memories:
            return "暂无扩展信息。"
        
        # 提取相关主题
        topics = set()
        for memory in memories[:3]:
            category = memory.get("category", "")
            if category:
                topics.add(category)
        
        if topics:
            return f"相关主题：{', '.join(topics)}"
        else:
            return "相关主题：通用知识"
    
    def _generate_references(self, memories: List[Dict]) -> str:
        """生成参考链接"""
        references = []
        
        for memory in memories[:3]:
            source = memory.get("source", "")
            if source and ("http://" in source or "https://" in source):
                references.append(f"- {source}")
        
        if references:
            return "\n".join(references[:3])
        else:
            return "- 官方文档\n- 社区论坛\n- 最佳实践指南"
    
    def _generate_category_stats(self, memories: List[Dict]) -> str:
        """生成类别统计"""
        if not memories:
            return "无类别统计信息。"
        
        categories = defaultdict(int)
        for memory in memories:
            category = memory.get("category", "unknown")
            categories[category] += 1
        
        stats = []
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            stats.append(f"{category}: {count}")
        
        return "，".join(stats)
    
    def _generate_importance_stats(self, memories: List[Dict]) -> str:
        """生成重要性统计"""
        if not memories:
            return "无重要性统计信息。"
        
        importance_levels = defaultdict(int)
        for memory in memories:
            importance = memory.get("importance", "normal")
            importance_levels[importance] += 1
        
        stats = []
        for level, count in sorted(importance_levels.items(), key=lambda x: x[1], reverse=True):
            stats.append(f"{level}: {count}")
        
        return "，".join(stats)
    
    def _generate_time_range(self, memories: List[Dict]) -> str:
        """生成时间范围"""
        if not memories:
            return "无时间信息。"
        
        # 提取修改时间
        times = []
        for memory in memories:
            metadata = memory.get("metadata", {})
            if "modified_time" in metadata:
                try:
                    time_str = metadata["modified_time"]
                    if isinstance(time_str, str):
                        # 尝试解析时间
                        dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                        times.append(dt)
                except:
                    pass
        
        if times:
            oldest = min(times)
            newest = max(times)
            return f"{oldest.strftime('%Y-%m-%d')} 至 {newest.strftime('%Y-%m-%d')}"
        else:
            return "时间信息不可用"
    
    def _analyze_skill_error(self, message: str, memories: List[Dict]) -> str:
        """分析技能使用错误"""
        error_patterns = [
            {
                "pattern": "忘了.*技能",
                "analysis": "习惯性思维导致忘记使用技能",
                "solution": "建立自动化检查机制"
            },
            {
                "pattern": "没用.*技能",
                "analysis": "没有按照标准流程工作",
                "solution": "严格执行技能使用流程"
            },
            {
                "pattern": "@skill",
                "analysis": "看到技能标签但没有立即使用",
                "solution": "看到@skill标签就立即调用use_skill"
            },
        ]
        
        for pattern_info in error_patterns:
            if re.search(pattern_info["pattern"], message, re.IGNORECASE):
                return f"**错误类型**：{pattern_info['analysis']}\n**根本原因**：习惯性思维战胜了新指令要求\n**影响**：无法正确回忆相关经验，工作质量下降"
        
        return "**错误类型**：未正确使用workbuddy-add-memory技能\n**根本原因**：习惯性思维导致忘记遵循标准流程\n**影响**：无法充分利用记忆系统优势"
    
    def _generate_skill_solution(self, memories: List[Dict]) -> str:
        """生成技能使用解决方案"""
        solutions = [
            "**立即纠正**：看到@skill://workbuddy-add-memory就立即调用use_skill",
            "**标准流程**：use_skill → start_work.py → 读取报告 → 基于记忆行动",
            "**技术防御**：完善钩子脚本，自动检测和提醒技能使用",
            "**流程强化**：每次任务开始前强制检查技能使用情况"
        ]
        
        return "\n".join(f"- {solution}" for solution in solutions)
    
    def _generate_skill_prevention(self, memories: List[Dict]) -> str:
        """生成技能使用预防措施"""
        prevention_measures = [
            "**自动化检查**：在conversation_hook中增加技能使用检查",
            "**强制提醒**：检测到相关任务时自动提醒使用技能",
            "**历史分析**：记录技能使用情况，分析错误模式",
            "**肌肉记忆训练**：通过重复正确操作形成本能反应",
            "**三层防御**：认知防御 + 技术防御 + 流程防御"
        ]
        
        return "\n".join(f"- {measure}" for measure in prevention_measures)
    
    def _generate_skill_commitment(self) -> str:
        """生成技能使用承诺"""
        return "**我绝对承诺**：\n1. 🚫 绝不忘记使用workbuddy-add-memory技能\n2. ✅ 看到@skill标签就立即使用\n3. 📋 严格按照标准流程工作\n4. 💪 让做什么就做什么，不添加不减少"
    
    def _fill_template(self, template: str, data: Dict[str, Any]) -> str:
        """填充模板"""
        result = template
        
        for key, value in data.items():
            placeholder = f"{{{key}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        
        return result
    
    def _add_to_history(self, entry: Dict[str, Any]) -> None:
        """添加到对话历史"""
        self.conversation_history.append(entry)
        
        # 限制历史大小
        if len(self.conversation_history) > self.max_history_size:
            self.conversation_history = self.conversation_history[-self.max_history_size:]
    
    def get_conversation_summary(self) -> str:
        """获取对话摘要"""
        if not self.conversation_history:
            return "对话历史为空。"
        
        summary = []
        summary.append(f"对话历史 ({len(self.conversation_history)} 条消息):")
        
        for i, entry in enumerate(self.conversation_history[-5:], 1):
            message = entry.get("message", "")
            timestamp = entry.get("timestamp", "")
            
            # 截断长消息
            if len(message) > 50:
                message = message[:47] + "..."
            
            # 格式化时间
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    time_str = dt.strftime("%H:%M")
                except:
                    time_str = timestamp
            else:
                time_str = "未知时间"
            
            summary.append(f"{i}. [{time_str}] {message}")
        
        # 添加触发统计
        summary.append(f"\n触发统计:")
        summary.append(f"- 总触发次数: {self.trigger_count}")
        for trigger_type, count in self.trigger_types.items():
            summary.append(f"- {trigger_type}: {count}次")
        
        return "\n".join(summary)
    
    def clear_history(self) -> None:
        """清除对话历史"""
        self.conversation_history = []
        self.trigger_count = 0
        self.trigger_types.clear()
        logger.info("对话历史已清除")


# 全局对话钩子实例
conversation_hook = ConversationHook()


if __name__ == "__main__":
    # 测试对话钩子
    import logging
    
    logging.basicConfig(level=logging.INFO)
    
    hook = ConversationHook()
    
    # 测试消息
    test_messages = [
        "请帮我制作一个Excel预算表",
        "如何安装新的技能？",
        "我遇到了Excel处理错误",
        "回忆一下之前的记忆管理经验",
        "今天天气怎么样？",  # 不应该触发
    ]
    
    print("=== 对话钩子测试 ===")
    for message in test_messages:
        print(f"\n{'='*50}")
        print(f"用户消息: {message}")
        
        result = hook.process_message(message)
        
        if result["trigger_detected"]:
            print(f"触发类型: {result['trigger_type']}")
            print(f"置信度: {result['confidence']:.2f}")
            print(f"是否需要响应: {result['should_respond']}")
            
            if result["should_respond"]:
                print(f"\n响应内容:")
                print(result["response"][:500] + "..." if len(result["response"]) > 500 else result["response"])
        else:
            print("未触发记忆检索")
    
    # 显示对话摘要
    print(f"\n{'='*50}")
    print("对话摘要:")
    print(hook.get_conversation_summary())