"""
任务解析器（模型无关）
让任何大模型都能更准确地理解任务、更规范地回答
"""

import re
from typing import Dict, List
from enum import Enum


class TaskIntent(Enum):
    """任务意图"""
    GREETING = "greeting"      # 问候
    QUERY = "query"           # 查询
    COMMAND = "command"       # 命令/请求
    ANALYSIS = "analysis"     # 分析
    CHAT = "chat"            # 闲聊


class TaskComplexity(Enum):
    """任务复杂度"""
    SIMPLE = "simple"         # 简单
    MEDIUM = "medium"         # 中等
    COMPLEX = "complex"       # 复杂


class TaskParser:
    """任务解析器"""
    
    def __init__(self):
        # 意图识别规则
        self.intent_patterns = {
            TaskIntent.GREETING: [
                r"^(你好|hi|hello|嗨|早上好|晚上好|再见|谢谢|感谢)",
            ],
            TaskIntent.QUERY: [
                r"(什么|哪里|为什么|怎么|如何|是否|能否)",
                r"(查询|查看|显示|告诉我)",
            ],
            TaskIntent.COMMAND: [
                r"(帮我|请|能不能|可以|麻烦)",
                r"(创建|生成|写|做|执行|运行)",
            ],
            TaskIntent.ANALYSIS: [
                r"(分析|评估|对比|比较|总结|归纳)",
                r"(优缺点|区别|差异)",
            ],
        }
        
        # 复杂度判断规则
        self.complexity_keywords = {
            "simple": ["问候", "查询", "是什么", "在哪", "什么时候"],
            "complex": ["分析", "设计", "实现", "优化", "重构", "对比", "评估"]
        }
    
    def parse(self, message: str, context: Dict = None) -> Dict:
        """
        解析任务
        
        Args:
            message: 用户消息
            context: 上下文（可选）
        
        Returns:
            解析结果
        """
        return {
            "intent": self._detect_intent(message),
            "complexity": self._judge_complexity(message, context),
            "entities": self._extract_entities(message),
            "needs_context": self._check_context_needed(message),
            "enhanced_prompt": self._enhance_prompt(message, context)
        }
    
    def _detect_intent(self, message: str) -> TaskIntent:
        """检测意图"""
        message_lower = message.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        return TaskIntent.CHAT
    
    def _judge_complexity(self, message: str, context: Dict = None) -> TaskComplexity:
        """判断复杂度"""
        # 简单任务关键词
        if any(kw in message for kw in self.complexity_keywords["simple"]):
            return TaskComplexity.SIMPLE
        
        # 复杂任务关键词
        if any(kw in message for kw in self.complexity_keywords["complex"]):
            return TaskComplexity.COMPLEX
        
        # 根据长度判断
        if len(message) > 200:
            return TaskComplexity.COMPLEX
        elif len(message) > 50:
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.SIMPLE
    
    def _extract_entities(self, message: str) -> Dict:
        """提取实体（简单版）"""
        entities = {
            "time": [],
            "location": [],
            "person": [],
            "number": []
        }
        
        # 提取时间
        time_patterns = [
            r"(明天|今天|昨天|下周|上周)",
            r"(\d{1,2}点|\d{1,2}:\d{2})",
            r"(\d{4}年\d{1,2}月\d{1,2}日)"
        ]
        for pattern in time_patterns:
            matches = re.findall(pattern, message)
            entities["time"].extend(matches)
        
        # 提取数字
        numbers = re.findall(r"\d+", message)
        entities["number"] = numbers
        
        return entities
    
    def _check_context_needed(self, message: str) -> bool:
        """检查是否需要上下文"""
        context_keywords = [
            "刚才", "之前", "上次", "继续", "那个", "这个",
            "它", "他", "她", "它们"
        ]
        return any(kw in message for kw in context_keywords)
    
    def _enhance_prompt(self, message: str, context: Dict = None) -> str:
        """增强 Prompt（结构化）"""
        intent = self._detect_intent(message)
        complexity = self._judge_complexity(message, context)
        
        # 基础 Prompt
        enhanced = message
        
        # 根据意图添加引导
        if intent == TaskIntent.QUERY:
            enhanced += "\n\n【要求】请直接回答问题，简洁明了。"
        
        elif intent == TaskIntent.COMMAND:
            enhanced += "\n\n【要求】\n1. 给出具体步骤\n2. 说明预期结果\n3. 标注风险点（如有）"
        
        elif intent == TaskIntent.ANALYSIS:
            enhanced += "\n\n【要求】\n1. 结构化分析\n2. 列出关键点\n3. 给出结论"
        
        # 根据复杂度添加约束
        if complexity == TaskComplexity.SIMPLE:
            enhanced += "\n\n【约束】回复控制在 200 字以内。"
        
        return enhanced


class ResponseValidator:
    """回复验证器（防止乱回答）"""
    
    def validate(self, response: str, message: str, parsed: Dict) -> Dict:
        """
        验证回复质量
        
        Returns:
            {
                "valid": bool,
                "issues": List[str],
                "confidence": float,
                "suggestion": str
            }
        """
        issues = []
        
        # 1. 检测空回复
        if not response or len(response.strip()) < 10:
            issues.append("回复过短")
        
        # 2. 检测无关回复
        if self._is_irrelevant(response, message):
            issues.append("回复与问题可能无关")
        
        # 3. 检测重复内容
        if self._has_repetition(response):
            issues.append("回复内容重复")
        
        # 4. 检测格式问题
        intent = parsed.get("intent")
        if intent == TaskIntent.COMMAND and not self._has_structure(response):
            issues.append("命令类任务缺少结构化回复")
        
        # 5. 检测不确定性
        if self._is_uncertain(response):
            issues.append("回复包含不确定表述")
        
        # 计算置信度
        confidence = 1.0 - (len(issues) * 0.2)
        confidence = max(0.0, min(1.0, confidence))
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "confidence": confidence,
            "suggestion": self._generate_suggestion(issues)
        }
    
    def _is_irrelevant(self, response: str, message: str) -> bool:
        """检测无关回复（简单版）"""
        # 提取关键词（简单分词）
        message_words = set(re.findall(r"[\w]+", message))
        response_words = set(re.findall(r"[\w]+", response))
        
        # 计算重叠度
        if not message_words:
            return False
        
        overlap = len(message_words & response_words)
        overlap_ratio = overlap / len(message_words)
        
        return overlap_ratio < 0.1  # 重叠度低于 10%
    
    def _has_repetition(self, response: str) -> bool:
        """检测重复内容"""
        sentences = [s.strip() for s in response.split("。") if s.strip()]
        if len(sentences) < 2:
            return False
        
        # 检查是否有完全相同的句子
        return len(sentences) != len(set(sentences))
    
    def _has_structure(self, response: str) -> bool:
        """检测结构化"""
        structure_patterns = [
            r"\d+[\.\、]",  # 数字列表
            r"[-*•]",       # 无序列表
            r"步骤|首先|其次|最后",  # 步骤词
        ]
        return any(re.search(p, response) for p in structure_patterns)
    
    def _is_uncertain(self, response: str) -> bool:
        """检测不确定性"""
        uncertain_phrases = [
            "可能", "也许", "大概", "应该", "似乎",
            "不太确定", "不太清楚", "我猜"
        ]
        return any(phrase in response for phrase in uncertain_phrases)
    
    def _generate_suggestion(self, issues: List[str]) -> str:
        """生成改进建议"""
        if not issues:
            return ""
        
        suggestions = {
            "回复过短": "建议补充更多细节",
            "回复与问题可能无关": "建议重新理解问题",
            "回复内容重复": "建议删除重复内容",
            "命令类任务缺少结构化回复": "建议使用列表或步骤格式",
            "回复包含不确定表述": "建议明确表达或说明不确定的原因"
        }
        
        return "；".join([suggestions.get(issue, issue) for issue in issues])


# 使用示例
if __name__ == "__main__":
    parser = TaskParser()
    validator = ResponseValidator()
    
    # 测试1：简单查询
    message1 = "Python 是什么？"
    parsed1 = parser.parse(message1)
    print(f"消息: {message1}")
    print(f"意图: {parsed1['intent']}")
    print(f"复杂度: {parsed1['complexity']}")
    print(f"增强 Prompt: {parsed1['enhanced_prompt']}")
    print()
    
    # 测试2：命令任务
    message2 = "帮我分析一下这个项目的架构"
    parsed2 = parser.parse(message2)
    print(f"消息: {message2}")
    print(f"意图: {parsed2['intent']}")
    print(f"复杂度: {parsed2['complexity']}")
    print()
    
    # 测试3：回复验证
    response = "Python 是一种编程语言。Python 是一种编程语言。"
    validation = validator.validate(response, message1, parsed1)
    print(f"回复: {response}")
    print(f"验证结果: {validation}")
