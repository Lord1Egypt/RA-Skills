"""Skill memory system — EXPERIMENTAL."""
from __future__ import annotations
"""
记忆系统 Skill
为OpenClaw提供强大的记忆管理能力
EXPERIMENTAL — 此模块尚未稳定，API 可能随时变更。
"""

import sys
from pathlib import Path

# 添加插件目录到路径
plugin_dir = Path(__file__).parent.parent
sys.path.insert(0, str(plugin_dir))

from agent_memory_service import get_memory_service

class MemorySkill:
    """记忆系统Skill类"""
    
    def __init__(self):
        """初始化记忆系统Skill"""
        self.memory_service = get_memory_service()
        self.name = "memory-system"
        self.description = "强大的记忆管理系统"
        self.version = "9.1.0"
        
    def remember(self, content: str, importance: str = "medium", topics: list = None) -> dict:
        """记住信息
        
        示例: "记住我的生日是1月1日"
        
        Args:
            content: 记忆内容
            importance: 重要度 (high/medium/low)
            topics: 主题列表
            
        Returns:
            写入结果
        """
        result = self.memory_service.remember(content, importance, topics)
        return {
            "success": result.get("written", False),
            "content": content,
            "result": result,
            "message": "我已经记住了！" if result.get("written", False) else "抱歉，记忆写入失败了"
        }
    
    def recall(self, query: str, limit: int = 10) -> dict:
        """检索记忆
        
        示例: "回忆我之前说过什么"
        
        Args:
            query: 查询内容
            limit: 返回条数
            
        Returns:
            检索结果
        """
        results = self.memory_service.recall(query, limit)
        return {
            "success": len(results) > 0,
            "query": query,
            "results": results,
            "message": f"找到了 {len(results)} 条相关记忆" if results else "抱歉，没有找到相关记忆"
        }
    
    def build_context(self, query: str, max_tokens: int = 800) -> dict:
        """构建上下文
        
        示例: "帮我构建关于这个话题的上下文"
        
        Args:
            query: 查询内容
            max_tokens: 最大token数
            
        Returns:
            上下文字符串
        """
        context = self.memory_service.build_context(query, max_tokens)
        return {
            "success": bool(context),
            "query": query,
            "context": context,
            "message": "已为您构建了相关上下文" if context else "未能构建上下文"
        }
    
    def get_persona(self) -> dict:
        """获取人格画像
        
        示例: "获取我的人格画像"
        
        Returns:
            人格画像字典
        """
        persona = self.memory_service.get_persona()
        return {
            "success": bool(persona),
            "persona": persona,
            "message": "这是您的人格画像" if persona else "还没有人格画像"
        }
    
    def build_persona(self) -> dict:
        """构建人格画像
        
        示例: "帮我构建人格画像"
        
        Returns:
            人格画像字典
        """
        persona = self.memory_service.build_persona()
        return {
            "success": bool(persona),
            "persona": persona,
            "message": "人格画像构建成功" if persona else "人格画像构建失败"
        }
    
    def apply_role(self, role_id: str, weight: float = 0.4) -> dict:
        """应用角色风格
        
        示例: "使用技术专家风格"
        
        Args:
            role_id: 角色ID (tech_expert, product_manager, creative_writer, business_leader等)
            weight: 角色权重 (0-1)
            
        Returns:
            风格混合结果
        """
        style = self.memory_service.apply_role(role_id, weight)
        return {
            "success": bool(style),
            "role_id": role_id,
            "weight": weight,
            "style": style,
            "message": f"已应用 {role_id} 角色风格" if style else "角色风格应用失败"
        }
    
    def list_roles(self) -> dict:
        """列出所有角色
        
        示例: "列出所有可用角色"
        
        Returns:
            角色列表
        """
        roles = self.memory_service.list_roles()
        return {
            "success": True,
            "roles": roles,
            "message": f"共有 {len(roles)} 个可用角色"
        }
    
    def close(self):
        """关闭资源"""
        self.memory_service.close()

# 全局skill实例
_memory_skill = None

def get_memory_skill():
    """获取记忆系统Skill实例
    
    Returns:
        MemorySkill实例
    """
    global _memory_skill
    if _memory_skill is None:
        _memory_skill = MemorySkill()
    return _memory_skill
