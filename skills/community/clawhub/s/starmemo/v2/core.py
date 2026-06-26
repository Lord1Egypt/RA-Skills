#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
starmemo v2.0 - 核心引擎
整合存储、AI处理、召回系统
"""
import os
import sys
from pathlib import Path

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from storage import MemoryStorage
from ai_processor import AIProcessor, ConfigManager, MessageCleaner, LLM_PRESET
from recall import HeuristicRecall


class StarMemoEngine:
    """starmemo 核心引擎"""
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.base_dir = Path(base_dir)
        self.config_path = self.base_dir / ".skill_config"
        
        # 初始化各模块
        self.storage = MemoryStorage(self.base_dir)
        self.config = ConfigManager(str(self.config_path))
        self.ai = AIProcessor(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            model=self.config.model,
            enable_ai=self.config.enable_ai,
            temperature=self.config.temperature
        )
        self.recall = HeuristicRecall(self.storage, self.ai)
    
    def process(self, text: str, auto_save: bool = True) -> dict:
        """
        处理输入文本
        
        Args:
            text: 输入文本
            auto_save: 是否自动保存
        
        Returns:
            dict: {
                "action": "saved" | "recalled" | "clarified" | "answered",
                "memory": str,
                "response": str
            }
        """
        result = {
            "action": "none",
            "memory": "",
            "response": ""
        }
        
        # 清洗文本
        text = MessageCleaner.clean(text)
        if not text:
            return result
        
        # 检查是否为配置指令
        if MessageCleaner.is_config_command(text):
            result["action"] = "config"
            result["response"] = self._handle_config(text)
            return result
        
        # 1. 尝试召回
        recall_result = self.recall.recall(text)
        
        if recall_result["should_recall"] and recall_result["combined_memory"]:
            # 有相关记忆
            memory = recall_result["combined_memory"]
            result["memory"] = memory
            
            # 判断记忆是否足够
            if self._is_memory_enough(text, memory):
                # 直接回答
                result["action"] = "answered"
                result["response"] = self.ai.answer_with_memory(text, memory)
            else:
                # 需要澄清
                result["action"] = "clarified"
                result["response"] = self.ai.clarify(text, memory)
            
            return result
        
        # 2. 无相关记忆，保存新记忆
        if auto_save:
            structured = self.ai.extract_structured(text)
            
            self.storage.save_daily(
                cause=structured.get("cause", text[:100]),
                change=structured.get("change", text[:200]),
                todo=structured.get("todo", ""),
                topic=structured.get("topic", "")
            )
            
            # 提取知识点
            knowledge_list = self.ai.extract_knowledge(text)
            for k in knowledge_list:
                if k.get("key") and k.get("content"):
                    self.storage.save_knowledge(
                        key=k["key"],
                        content=k["content"],
                        source="对话提取"
                    )
            
            result["action"] = "saved"
            result["response"] = f"✅ 已保存记忆：{structured.get('topic', '日常记录')}"
        
        return result
    
    def _is_memory_enough(self, query: str, memory: str) -> bool:
        """判断记忆是否足够回答问题"""
        # 简单判断：记忆长度和关键词重叠
        if len(memory) < 30:
            return False
        
        query_words = set(query)
        memory_words = set(memory)
        
        overlap = len(query_words & memory_words) / max(1, len(query_words))
        
        return overlap >= 0.2
    
    def _handle_config(self, text: str) -> str:
        """处理配置指令"""
        text = text.replace("记忆配置", "").strip()
        
        params = {}
        for part in text.split():
            if "=" in part:
                k, v = part.split("=", 1)
                params[k.strip()] = v.strip()
        
        if params.get("llm") and params["llm"] in LLM_PRESET:
            self.config.set_llm(params["llm"], params.get("key"))
            # 重新初始化 AI
            self.ai = AIProcessor(
                api_key=self.config.api_key,
                base_url=self.config.base_url,
                model=self.config.model,
                enable_ai=True,
                temperature=self.config.temperature
            )
        
        if "persist" in params:
            self.config.persist_key = params["persist"].lower() == "true"
        
        if "web" in params:
            self.config.allow_web_fetch = params["web"].lower() == "true"
        
        self.config.save()
        
        return "✅ 配置已更新"
    
    # ========== 直接调用接口 ==========
    
    def save(self, cause: str, change: str, todo: str = "", topic: str = ""):
        """直接保存记忆"""
        return self.storage.save_daily(cause, change, todo, topic)
    
    def save_text(self, text: str):
        """保存文本（自动提取结构）"""
        structured = self.ai.extract_structured(text)
        return self.storage.save_daily(
            cause=structured.get("cause", text[:100]),
            change=structured.get("change", text[:200]),
            todo=structured.get("todo", ""),
            topic=structured.get("topic", "")
        )
    
    def save_knowledge(self, key: str, content: str, source: str = "手动添加"):
        """保存知识点"""
        return self.storage.save_knowledge(key, content, source)
    
    def search(self, keyword: str):
        """搜索记忆和知识"""
        daily = self.storage.search_daily(keyword)
        knowledge = self.storage.search_knowledge(keyword)
        return {"daily": daily, "knowledge": knowledge}
    
    def get_today(self) -> str:
        """获取今日记忆"""
        return self.storage.get_today()
    
    def get_status(self) -> dict:
        """获取状态"""
        files = self.storage.list_files()
        return {
            "config": {
                "model": self.config.model,
                "enable_ai": self.config.enable_ai,
                "persist_key": self.config.persist_key,
                "allow_web_fetch": self.config.allow_web_fetch
            },
            "files": files
        }


# 单例
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = StarMemoEngine()
    return _engine
