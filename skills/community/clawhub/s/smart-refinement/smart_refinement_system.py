"""
Smart Refinement System - 集成提示词优化和向量优化的智能系统
集成模块：
1. Prompt Refinement Module - 提示词优化
2. Vector Optimizer - 向量化技能匹配
3. Context Manager - 上下文集成
"""

import re
import json
import math
from typing import Optional, Dict, List, Tuple, Any
from datetime import datetime
from collections import Counter


class SmartRefinementSystem:
    """智能提示词优化与向量匹配系统"""
    
    def __init__(self, config_path: Optional[str] = None):
        # 初始化提示词优化器
        self.prompt_refiner = PromptRefiner()
        
        # 初始化向量优化器
        self.vector_optimizer = VectorOptimizer()
        
        # 上下文管理器
        self.context_manager = ContextManager()
        
        # 技能数据库
        self.skills_database = self._load_skills_database()
        
        # 配置
        self.config = self._load_config(config_path)
        
        # 性能统计
        self.stats = {
            "refinements": 0,
            "vector_matches": 0,
            "success_rate": 0.0,
            "avg_processing_time": 0.0
        }
    
    def _load_skills_database(self) -> Dict:
        """加载技能数据库"""
        return {
            "code_generation": {
                "keywords": ["code", "script", "function", "write", "generate", "implement", "debug", "optimize"],
                "description": "代码生成和优化",
                "required_tools": ["exec", "write", "read"],
                "suggested_actions": [
                    "确认编程语言",
                    "添加必要的注释和错误处理",
                    "考虑代码可读性和模块化"
                ]
            },
            "file_operation": {
                "keywords": ["file", "save", "open", "read", "write", "create", "delete", "modify", "edit"],
                "description": "文件操作",
                "required_tools": ["read", "write", "edit"],
                "suggested_actions": [
                    "确认文件路径和格式",
                    "检查文件权限",
                    "备份重要文件"
                ]
            },
            "web_search": {
                "keywords": ["find", "search", "check", "retrieve", "look for", "google", "browse"],
                "description": "网络搜索",
                "required_tools": ["autoglm-websearch", "browser", "web_fetch"],
                "suggested_actions": [
                    "确定搜索关键词",
                    "选择搜索范围（本地/网络/数据库）",
                    "验证信息来源可靠性"
                ]
            },
            "data_analysis": {
                "keywords": ["analyze", "process", "calculate", "statistics", "report", "chart", "graph"],
                "description": "数据分析",
                "required_tools": ["exec", "read", "write"],
                "suggested_actions": [
                    "明确分析目标和指标",
                    "确定数据源和格式",
                    "选择合适的分析方法"
                ]
            },
            "documentation": {
                "keywords": ["document", "write", "create", "edit", "format", "organize", "summarize"],
                "description": "文档编写",
                "required_tools": ["write", "edit", "read"],
                "suggested_actions": [
                    "确定文档类型和结构",
                    "收集必要信息",
                    "遵循格式规范"
                ]
            },
            "system_operation": {
                "keywords": ["run", "execute", "install", "configure", "setup", "monitor", "manage"],
                "description": "系统操作",
                "required_tools": ["exec", "process", "nodes"],
                "suggested_actions": [
                    "确认系统环境和权限",
                    "检查依赖和配置",
                    "测试操作结果"
                ]
            }
        }
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置"""
        default_config = {
            "refinement_threshold": 0.3,  # 优化阈值
            "vector_match_threshold": 0.5,  # 向量匹配阈值
            "enable_context_integration": True,
            "enable_skill_suggestion": True,
            "enable_performance_tracking": True,
            "language": "auto",  # auto, zh, en
            "output_format": "structured"  # structured, simple, detailed
        }
        
        if config_path:
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"Warning: Failed to load config from {config_path}: {e}")
        
        return default_config
    
    def process_message(self, message: str, context: Optional[Dict] = None) -> Dict:
        """
        处理用户消息，集成优化和向量匹配
        
        Args:
            message: 用户消息
            context: 上下文信息
            
        Returns:
            处理结果字典
        """
        start_time = datetime.now()
        
        # 1. 检查是否需要优化
        needs_refine, confidence = self.prompt_refiner.needs_refinement(message)
        
        # 2. 提取意图和实体
        intent = self.prompt_refiner.infer_intent(message)
        entities = self.prompt_refiner.extract_entities(message)
        
        # 3. 向量化技能匹配
        skill_matches = self.vector_optimizer.match_skills(
            message, 
            self.skills_database
        )
        
        # 4. 生成优化提示（如果需要）
        if needs_refine:
            refined_prompt = self.prompt_refiner.generate_refined_prompt(
                message, 
                context
            )
        else:
            refined_prompt = message
        
        # 5. 集成上下文
        if self.config["enable_context_integration"] and context:
            integrated_context = self.context_manager.integrate_context(
                message, 
                context
            )
        else:
            integrated_context = context or {}
        
        # 6. 生成建议动作
        suggested_actions = self._generate_suggested_actions(
            intent, 
            skill_matches, 
            entities
        )
        
        # 7. 生成执行指南
        execution_guide = self._generate_execution_guide(
            intent, 
            skill_matches, 
            suggested_actions
        )
        
        # 8. 更新统计
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        self._update_stats(needs_refine, processing_time)
        
        # 9. 构建结果
        result = {
            "original_message": message,
            "needs_refinement": needs_refine,
            "refinement_confidence": confidence,
            "refined_prompt": refined_prompt,
            "intent": intent,
            "entities": entities,
            "skill_matches": skill_matches,
            "suggested_actions": suggested_actions,
            "execution_guide": execution_guide,
            "integrated_context": integrated_context,
            "processing_time_ms": processing_time,
            "system_stats": self.stats.copy()
        }
        
        return result
    
    def _generate_suggested_actions(self, intent: Dict, 
                                   skill_matches: List[Dict], 
                                   entities: Dict) -> List[str]:
        """生成建议动作"""
        actions = []
        
        # 添加意图相关动作
        if intent.get('suggested_actions'):
            actions.extend(intent['suggested_actions'])
        
        # 添加技能匹配相关动作
        for match in skill_matches[:3]:  # 取前3个匹配
            skill_info = self.skills_database.get(match['skill_type'], {})
            if skill_info.get('suggested_actions'):
                actions.extend(skill_info['suggested_actions'])
        
        # 添加实体相关动作
        if entities.get('file_paths'):
            actions.append(f"读取文件: {entities['file_paths'][0]}")
        if entities.get('urls'):
            actions.append(f"访问URL: {entities['urls'][0]}")
        
        # 去重并限制数量
        unique_actions = []
        seen = set()
        for action in actions:
            if action not in seen:
                unique_actions.append(action)
                seen.add(action)
        
        return unique_actions[:5]  # 最多5个动作
    
    def _generate_execution_guide(self, intent: Dict, 
                                 skill_matches: List[Dict], 
                                 suggested_actions: List[str]) -> str:
        """生成执行指南"""
        guide_parts = []
        
        # 基本指南
        guide_parts.append("## 执行指南")
        guide_parts.append("")
        guide_parts.append("### 步骤建议:")
        for i, action in enumerate(suggested_actions, 1):
            guide_parts.append(f"{i}. {action}")
        
        guide_parts.append("")
        guide_parts.append("### 注意事项:")
        guide_parts.append("- 按建议步骤顺序执行")
        guide_parts.append("- 每个步骤完成后验证结果")
        guide_parts.append("- 遇到问题及时询问用户澄清")
        guide_parts.append("- 重要操作记录到上下文管理器")
        
        # 技能相关指南
        if skill_matches:
            guide_parts.append("")
            guide_parts.append("### 推荐技能:")
            for match in skill_matches[:2]:
                skill_info = self.skills_database.get(match['skill_type'], {})
                guide_parts.append(f"- **{match['skill_type']}** ({match['match_score']:.1%}): {skill_info.get('description', '')}")
        
        return "\n".join(guide_parts)
    
    def _update_stats(self, needs_refine: bool, processing_time: float):
        """更新统计信息"""
        self.stats["refinements"] += 1 if needs_refine else 0
        self.stats["vector_matches"] += 1
        
        # 更新平均处理时间
        total_refinements = self.stats["refinements"]
        if total_refinements > 0:
            old_avg = self.stats["avg_processing_time"]
            self.stats["avg_processing_time"] = (
                old_avg * (total_refinements - 1) + processing_time
            ) / total_refinements
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.stats.copy()
    
    def save_config(self, config_path: str):
        """保存配置"""
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def export_skill_data(self) -> Dict:
        """导出技能数据"""
        return {
            "skills_database": self.skills_database,
            "config": self.config,
            "stats": self.stats,
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        }


class PromptRefiner:
    """提示词优化器（从原模块移植）"""
    
    def __init__(self):
        # 模糊关键词
        self.vague_keywords = [
            "that", "this", "the previous", "just now",
            "help me", "look at", "check", "handle", "process",
            "那个", "这个", "刚才", "之前", "帮我", "看看", "检查", "处理"
        ]
        
        # 更多关键词分类...
        # （这里省略详细实现，使用原prompt_refinement.py的核心逻辑）
    
    def needs_refinement(self, message: str) -> Tuple[bool, float]:
        """检查是否需要优化"""
        message_lower = message.lower()
        score = 0.0
        
        # 检查模糊关键词
        for keyword in self.vague_keywords:
            if keyword in message_lower:
                score += 0.1
        
        # 检查是否缺少具体信息
        if len(message.split()) < 4:
            score += 0.2
        
        return score > 0.3, min(score, 1.0)
    
    def infer_intent(self, message: str) -> Dict:
        """推断意图"""
        # 简化实现
        message_lower = message.lower()
        
        intents = []
        if any(kw in message_lower for kw in ["code", "script", "function"]):
            intents.append("code_generation")
        if any(kw in message_lower for kw in ["file", "save", "read"]):
            intents.append("file_operation")
        if any(kw in message_lower for kw in ["search", "find", "look"]):
            intents.append("web_search")
        
        return {
            "intent_type": intents[0] if intents else "general",
            "confidence": 0.8 if intents else 0.3,
            "detected_keywords": [],
            "suggested_actions": []
        }
    
    def extract_entities(self, message: str) -> Dict:
        """提取实体"""
        # 简化实现
        file_paths = re.findall(r'[A-Za-z]:\\[^\\].*?\.[a-zA-Z0-9]+|\./[^ ]+\.[a-zA-Z0-9]+', message)
        urls = re.findall(r'https?://[^\s]+', message)
        
        return {
            "file_paths": file_paths,
            "urls": urls,
            "code_snippets": []
        }
    
    def generate_refined_prompt(self, message: str, context: Optional[Dict] = None) -> str:
        """生成优化提示"""
        intent = self.infer_intent(message)
        
        parts = []
        parts.append("# 任务类型: " + intent["intent_type"])
        parts.append("")
        
        if context:
            parts.append("## 上下文:")
            for key, value in context.items():
                parts.append(f"- {key}: {value}")
            parts.append("")
        
        parts.append("## 用户请求:")
        parts.append(message)
        parts.append("")
        
        parts.append("## 建议动作:")
        parts.append("1. 确认具体需求和约束条件")
        parts.append("2. 分步骤执行任务")
        parts.append("3. 验证每个步骤的结果")
        parts.append("")
        
        parts.append("## 执行指南:")
        parts.append("- 按建议步骤顺序执行")
        parts.append("- 遇到问题及时询问澄清")
        parts.append("- 记录重要操作到上下文")
        
        return "\n".join(parts)


class VectorOptimizer:
    """向量优化器（从原模块移植）"""
    
    def __init__(self):
        self.tfidf_weights = {}
        self.skill_vectors = {}
    
    def match_skills(self, message: str, skills_database: Dict) -> List[Dict]:
        """匹配技能"""
        message_tokens = message.lower().split()
        
        matches = []
        for skill_type, skill_info in skills_database.items():
            keywords = skill_info.get("keywords", [])
            
            # 计算匹配分数
            match_count = sum(1 for token in message_tokens 
                            if any(kw in token for kw in keywords))
            total_keywords = len(keywords)
            
            if total_keywords > 0:
                score = match_count / total_keywords
                if score > 0:
                    matches.append({
                        "skill_type": skill_type,
                        "match_score": score,
                        "matched_keywords": [kw for kw in keywords 
                                           if any(kw in token for token in message_tokens)],
                        "description": skill_info.get("description", "")
                    })
        
        # 按分数排序
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        return matches


class ContextManager:
    """上下文管理器"""
    
    def __init__(self):
        self.context_cache = {}
    
    def integrate_context(self, message: str, context: Dict) -> Dict:
        """集成上下文"""
        integrated = context.copy()
        
        # 添加消息相关信息
        integrated["message_length"] = len(message)
        integrated["word_count"] = len(message.split())
        integrated["processed_at"] = datetime.now().isoformat()
        
        # 缓存上下文
        self.context_cache["last_message"] = message
        self.context_cache["last_context"] = context
        
        return integrated
    
    def get_context(self, key: str) -> Any:
        """获取上下文"""
        return self.context_cache.get(key)


# 简化接口函数
def refine_prompt(message: str, context: Optional[Dict] = None) -> str:
    """简化接口：优化提示词"""
    system = SmartRefinementSystem()
    result = system.process_message(message, context)
    return result["refined_prompt"]


def match_skills(message: str) -> List[Dict]:
    """简化接口：匹配技能"""
    system = SmartRefinementSystem()
    result = system.process_message(message)
    return result["skill_matches"]


if __name__ == "__main__":
    # 测试代码
    system = SmartRefinementSystem()
    
    test_messages = [
        "Help me process that file",
        "Write a Python script to analyze data",
        "Search for information about AI trends"
    ]
    
    for msg in test_messages:
        print(f"\n{'='*60}")
        print(f"测试消息: {msg}")
        print(f"{'='*60}")
        
        result = system.process_message(msg)
        
        print(f"需要优化: {result['needs_refinement']}")
        print(f"优化置信度: {result['refinement_confidence']:.1%}")
        print(f"意图类型: {result['intent']['intent_type']}")
        
        if result['skill_matches']:
            print(f"\n技能匹配:")
            for match in result['skill_matches'][:2]:
                print(f"  - {match['skill_type']}: {match['match_score']:.1%}")