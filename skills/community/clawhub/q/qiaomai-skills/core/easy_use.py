"""
荞麦饼 Skills - 易用性模块
让复杂系统变得简单自然
"""

import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class IntentType(Enum):
    """用户意图类型"""
    RESEARCH = "research"           # 研究分析
    CODE = "code"                   # 代码开发
    WRITE = "write"                 # 写作生成
    ANALYZE = "analyze"             # 分析诊断
    SEARCH = "search"               # 搜索查询
    SUMMARIZE = "summarize"         # 总结摘要
    COMPARE = "compare"             # 对比分析
    PLAN = "plan"                   # 规划任务
    CHAT = "chat"                   # 闲聊对话
    HELP = "help"                   # 帮助请求


@dataclass
class ParsedIntent:
    """解析后的意图"""
    intent: IntentType
    confidence: float
    entities: Dict[str, Any]
    parameters: Dict[str, Any]
    suggested_action: str


class NaturalLanguageParser:
    """自然语言解析器"""
    
    # 意图关键词映射
    INTENT_PATTERNS = {
        IntentType.RESEARCH: [
            r"研究.*", r"调研.*", r"分析.*趋势", r"了解.*", 
            r"调查.*", r"探索.*", r"深入研究.*"
        ],
        IntentType.CODE: [
            r"写.*代码", r"开发.*", r"编程.*", r"实现.*",
            r"写.*程序", r"做.*软件", r"建.*系统"
        ],
        IntentType.WRITE: [
            r"写.*", r"生成.*", r"创作.*", r"撰写.*",
            r"起草.*", r"准备.*文档", r"写.*报告"
        ],
        IntentType.ANALYZE: [
            r"分析.*", r"诊断.*", r"评估.*", r"检查.*",
            r"审查.*", r"解析.*", r"解读.*"
        ],
        IntentType.SEARCH: [
            r"搜索.*", r"查找.*", r"查询.*", r"找.*",
            r"搜.*", r"查.*信息", r"获取.*"
        ],
        IntentType.SUMMARIZE: [
            r"总结.*", r"概括.*", r"摘要.*", r"提炼.*",
            r"归纳.*", r"简述.*"
        ],
        IntentType.COMPARE: [
            r"对比.*", r"比较.*", r"vs", r"区别.*",
            r"差异.*", r"优劣.*"
        ],
        IntentType.PLAN: [
            r"规划.*", r"计划.*", r"安排.*", r"制定.*",
            r"设计.*方案", r"策划.*"
        ],
        IntentType.HELP: [
            r"帮助", r"怎么用", r"如何使用", r"说明.*",
            r"教程", r"guide", r"help"
        ]
    }
    
    def parse(self, query: str) -> ParsedIntent:
        """解析用户输入"""
        query = query.strip().lower()
        
        # 匹配意图
        best_intent = IntentType.CHAT
        best_confidence = 0.0
        
        for intent, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, query):
                    confidence = self._calculate_confidence(query, pattern)
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_intent = intent
        
        # 提取实体
        entities = self._extract_entities(query)
        
        # 提取参数
        parameters = self._extract_parameters(query)
        
        # 生成建议动作
        suggested_action = self._suggest_action(best_intent, entities)
        
        return ParsedIntent(
            intent=best_intent,
            confidence=best_confidence,
            entities=entities,
            parameters=parameters,
            suggested_action=suggested_action
        )
    
    def _calculate_confidence(self, query: str, pattern: str) -> float:
        """计算匹配置信度"""
        # 简单实现：基于匹配长度
        match = re.search(pattern, query)
        if match:
            return min(0.5 + len(match.group()) / len(query) * 0.5, 1.0)
        return 0.0
    
    def _extract_entities(self, query: str) -> Dict[str, Any]:
        """提取命名实体"""
        entities = {}
        
        # 提取主题
        topic_patterns = [
            r"关于(.+?)[的|之]",
            r"(.+?)的[趋势|发展|现状]",
            r"研究(.+?)[\?|？|$]",
        ]
        for pattern in topic_patterns:
            match = re.search(pattern, query)
            if match:
                entities["topic"] = match.group(1).strip()
                break
        
        # 提取数量
        number_patterns = [
            r"(\d+)[个|条|份]",
            r"前(\d+)",
            r"(\d+)个",
        ]
        for pattern in number_patterns:
            match = re.search(pattern, query)
            if match:
                entities["count"] = int(match.group(1))
                break
        
        return entities
    
    def _extract_parameters(self, query: str) -> Dict[str, Any]:
        """提取参数"""
        params = {}
        
        # 深度参数
        if any(word in query for word in ["深入", "详细", "全面", "彻底"]):
            params["depth"] = "deep"
        elif any(word in query for word in ["快速", "简单", "大概"]):
            params["depth"] = "shallow"
        else:
            params["depth"] = "normal"
        
        # 格式参数
        if any(word in query for word in ["报告", "文档", "pdf"]):
            params["format"] = "report"
        elif any(word in query for word in ["列表", "清单", "条目"]):
            params["format"] = "list"
        else:
            params["format"] = "auto"
        
        return params
    
    def _suggest_action(self, intent: IntentType, entities: Dict) -> str:
        """建议执行动作"""
        actions = {
            IntentType.RESEARCH: "启动深度研究流程",
            IntentType.CODE: "启动代码生成任务",
            IntentType.WRITE: "启动写作助手",
            IntentType.ANALYZE: "启动分析诊断",
            IntentType.SEARCH: "执行智能搜索",
            IntentType.SUMMARIZE: "生成内容摘要",
            IntentType.COMPARE: "执行对比分析",
            IntentType.PLAN: "创建任务规划",
            IntentType.CHAT: "进入对话模式",
            IntentType.HELP: "显示帮助信息",
        }
        return actions.get(intent, "继续对话")


class OneClickSetup:
    """一键配置向导"""
    
    SCENARIOS = {
        "research": {
            "name": "研究分析",
            "description": "适合学术研究和深度分析",
            "features": ["memory", "knowledge_graph", "deep_research"],
            "default_depth": "deep",
        },
        "development": {
            "name": "软件开发",
            "description": "适合编程和系统开发",
            "features": ["code_execution", "debugging", "documentation"],
            "default_depth": "normal",
        },
        "office": {
            "name": "日常办公",
            "description": "适合文档处理和日常任务",
            "features": ["writing", "summarization", "scheduling"],
            "default_depth": "shallow",
        },
        "full": {
            "name": "全部功能",
            "description": "启用所有高级功能",
            "features": "all",
            "default_depth": "adaptive",
        }
    }
    
    def __init__(self):
        self.config = {}
    
    def interactive_setup(self) -> Dict:
        """交互式配置"""
        print("🌾 欢迎使用荞麦饼 Skills 配置向导")
        print("=" * 50)
        
        # 选择场景
        print("\n请选择您的使用场景:")
        for key, scenario in self.SCENARIOS.items():
            print(f"  [{key}] {scenario['name']} - {scenario['description']}")
        
        # 模拟用户选择（实际应为交互式输入）
        selected = "research"  # 默认值
        
        scenario = self.SCENARIOS[selected]
        self.config["scenario"] = selected
        self.config["scenario_name"] = scenario["name"]
        self.config["features"] = scenario["features"]
        self.config["default_depth"] = scenario["default_depth"]
        
        # 性能配置
        self.config["performance"] = {
            "cache_size": "1GB",
            "max_workers": 10,
            "timeout": 30
        }
        
        # 记忆配置
        self.config["memory"] = {
            "enabled": True,
            "layers": ["instant", "working", "short", "session", "context", "long", "skill", "expert"],
            "sync_interval": 300
        }
        
        print(f"\n✅ 已为您配置: {scenario['name']} 模式")
        print(f"   启用功能: {', '.join(scenario['features']) if isinstance(scenario['features'], list) else '全部'}")
        
        return self.config
    
    def quick_setup(self, scenario: str = "full") -> Dict:
        """快速配置"""
        if scenario not in self.SCENARIOS:
            scenario = "full"
        
        return self.interactive_setup()


class SmartAssistant:
    """智能助手"""
    
    def __init__(self):
        self.parser = NaturalLanguageParser()
        self.setup = OneClickSetup()
    
    def process(self, query: str) -> Dict:
        """处理用户输入"""
        # 解析意图
        intent = self.parser.parse(query)
        
        # 生成响应
        response = {
            "intent": intent.intent.value,
            "confidence": intent.confidence,
            "action": intent.suggested_action,
            "entities": intent.entities,
            "parameters": intent.parameters,
            "message": self._generate_response(intent)
        }
        
        return response
    
    def _generate_response(self, intent: ParsedIntent) -> str:
        """生成自然语言响应"""
        responses = {
            IntentType.RESEARCH: f"我将为您深入研究「{intent.entities.get('topic', '这个主题')}」，预计需要几分钟时间。",
            IntentType.CODE: "好的，我来帮您编写代码。请告诉我具体需求。",
            IntentType.WRITE: "我来帮您撰写内容。请提供更多信息。",
            IntentType.ANALYZE: "我来分析一下。请稍等。",
            IntentType.SEARCH: f"正在搜索「{intent.entities.get('topic', '相关信息')}」...",
            IntentType.SUMMARIZE: "我来为您总结要点。",
            IntentType.COMPARE: "我来对比分析一下。",
            IntentType.PLAN: "我来帮您制定计划。",
            IntentType.CHAT: "有什么我可以帮您的吗？",
            IntentType.HELP: "荞麦饼 Skills 支持：研究、编程、写作、分析等多种功能。请告诉我您想做什么？",
        }
        
        return responses.get(intent.intent, "明白了，请继续。")


# 便捷函数
def parse_query(query: str) -> ParsedIntent:
    """解析查询"""
    parser = NaturalLanguageParser()
    return parser.parse(query)


def setup_wizard() -> Dict:
    """启动配置向导"""
    setup = OneClickSetup()
    return setup.interactive_setup()


def smart_process(query: str) -> Dict:
    """智能处理"""
    assistant = SmartAssistant()
    return assistant.process(query)


if __name__ == "__main__":
    # 测试
    test_queries = [
        "帮我研究一下AI发展趋势",
        "写个Python爬虫",
        "总结一下这篇文章",
        "搜索最近的新闻",
    ]
    
    assistant = SmartAssistant()
    for query in test_queries:
        print(f"\n输入: {query}")
        result = assistant.process(query)
        print(f"意图: {result['intent']} (置信度: {result['confidence']:.2f})")
        print(f"动作: {result['action']}")
        print(f"响应: {result['message']}")
