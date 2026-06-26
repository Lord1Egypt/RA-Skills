"""
Obsidian Knowledge Base Skill
与Obsidian知识库交互，支持创建笔记、语义搜索、笔记管理
"""

import requests
import json
from datetime import datetime
import os

class ObsidianKB:
    """Obsidian知识库操作类"""
    
    def __init__(self, api_url="http://192.168.18.15:5000"):
        self.api_url = api_url
        self.base_url = f"{api_url}/api"
    
    def check_health(self):
        """检查API服务健康状态"""
        try:
            response = requests.get(f"{self.api_url}/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def health_check(self):
        """检查API服务健康状态"""
        try:
            response = requests.get(f"{self.api_url}/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def create_note(self, title, content, tags=None, folder=None):
        """创建笔记"""
        try:
            data = {
                "title": title,
                "content": content,
                "tags": tags or []
            }
            if folder:
                data["folder"] = folder
            
            response = requests.post(f"{self.base_url}/note", 
                                   json=data, 
                                   headers={"Content-Type": "application/json"})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def search_notes(self, query, limit=10):
        """语义搜索笔记"""
        try:
            data = {"query": query, "limit": limit}
            response = requests.post(f"{self.base_url}/search", 
                                   json=data, 
                                   headers={"Content-Type": "application/json"})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_note(self, file_path):
        """获取单个笔记"""
        try:
            response = requests.get(f"{self.base_url}/note", 
                                  params={"file": file_path})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def list_notes(self, folder=None):
        """列出所有笔记"""
        try:
            params = {}
            if folder:
                params["folder"] = folder
            
            response = requests.get(f"{self.base_url}/notes", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_stats(self):
        """获取统计信息"""
        try:
            response = requests.get(f"{self.base_url}/stats")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def rebuild_index(self):
        """重建索引"""
        try:
            response = requests.post(f"{self.base_url}/build")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def save_experience(self, title, content, category, tags=None):
        """保存工作经验（包装方法）"""
        # 自动添加身份标识
        host = "4090服务器 (192.168.18.15)"
        agent = "nanobot-001"
        created = datetime.now().strftime("%Y-%m-%d")
        
        frontmatter = f"""---
host: {host}
agent: {agent}
created: {created}
updated: {created}
---

{content}"""
        
        # 确定文件夹
        folder_map = {
            "工作日志": "claw_daily",
            "项目经验": "project_lessons", 
            "运维经验": "openclaw_ops",
            "执行规范": "wf_overview",
            "工作流": "wf_composite",
            "系统配置": "_system"
        }
        
        folder = folder_map.get(category, "claw_memory")
        
        return self.create_note(title, frontmatter, tags, folder)

def check_health():
    """检查健康状态的便捷函数"""
    kb = ObsidianKB()
    return kb.health_check()

def create_note(title, content, tags=None, folder=None):
    """创建笔记的便捷函数"""
    kb = ObsidianKB()
    return kb.create_note(title, content, tags, folder)

def search_notes(query, limit=10):
    """搜索笔记的便捷函数"""
    kb = ObsidianKB()
    return kb.search_notes(query, limit)

def save_experience(title, content, category, tags=None):
    """保存工作经验的便捷函数"""
    kb = ObsidianKB()
    return kb.save_experience(title, content, category, tags)