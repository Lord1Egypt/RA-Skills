#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图谱管理模块
使用本地JSON存储管理剧情图谱
"""

import json
import os
from typing import Dict, Optional, Any, List
from datetime import datetime


class GraphManager:
    """图谱管理器 - 本地JSON存储"""
    
    def __init__(self, storage_dir: str = None):
        """
        初始化图谱管理器
        
        Args:
            storage_dir: 存储目录，默认为 data/graphs
        """
        if storage_dir is None:
            # 默认存储在 data/graphs 目录
            self.storage_dir = os.path.join(
                os.path.dirname(__file__), 
                "..", 
                "data", 
                "graphs"
            )
        else:
            self.storage_dir = storage_dir
        
        # 确保目录存在
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # 内存缓存
        self.cache: Dict[str, Dict] = {}
    
    def _get_graph_path(self, pipeline_id: str) -> str:
        """获取图谱文件路径"""
        return os.path.join(self.storage_dir, f"{pipeline_id}.json")
    
    def _load_graph(self, pipeline_id: str) -> Dict:
        """加载图谱数据"""
        # 先检查缓存
        if pipeline_id in self.cache:
            return self.cache[pipeline_id]
        
        # 从文件加载
        graph_path = self._get_graph_path(pipeline_id)
        if os.path.exists(graph_path):
            try:
                with open(graph_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.cache[pipeline_id] = data
                    return data
            except (json.JSONDecodeError, Exception):
                pass
        
        # 返回空图谱
        return {
            "pipeline_id": pipeline_id,
            "episodes": {},
            "characters": {},
            "hooks": [],
            "scenes": {},
            "relationships": []
        }
    
    def _save_graph(self, pipeline_id: str, data: Dict):
        """保存图谱数据"""
        graph_path = self._get_graph_path(pipeline_id)
        
        # 更新缓存
        self.cache[pipeline_id] = data
        
        # 保存到文件
        with open(graph_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def query_graph(self, pipeline_id: str, episode: int) -> Dict[str, Any]:
        """
        查询图谱 - 获取指定剧集的图谱数据
        
        Args:
            pipeline_id: 管道ID
            episode: 剧集序号
            
        Returns:
            图谱数据字典
        """
        graph = self._load_graph(pipeline_id)
        
        # 获取指定剧集的内容
        episode_data = graph.get("episodes", {}).get(str(episode), {})
        
        if not episode_data:
            return {
                "success": False,
                "error": f"第{episode}集数据不存在",
                "data": None
            }
        
        # 提取未闭环的钩子
        open_hooks = [h for h in graph.get("hooks", []) if h.get("status") == "open"]
        
        return {
            "success": True,
            "episode": episode,
            "content": episode_data.get("content", ""),
            "summary": episode_data.get("summary", ""),
            "characters": self._get_episode_characters(graph, episode),
            "hooks": open_hooks,
            "scenes": episode_data.get("scenes", []),
            "relationships": graph.get("relationships", [])
        }
    
    def save_graph(
        self, 
        pipeline_id: str, 
        episode: int, 
        content: str,
        summary: str = "",
        characters: List[Dict] = None,
        hooks_created: List[Dict] = None,
        hooks_resolved: List[str] = None,
        scenes: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        存储图谱 - 保存当前剧集的完整内容
        
        在人工审核通过后调用此方法存储图谱
        
        Args:
            pipeline_id: 管道ID
            episode: 剧集序号
            content: 完整的剧集内容
            summary: 摘要
            characters: 人物列表
            hooks_created: 新增的钩子
            hooks_resolved: 闭环的钩子ID列表
            scenes: 场景列表
            
        Returns:
            存储结果
        """
        graph = self._load_graph(pipeline_id)
        
        # 保存剧集内容
        if "episodes" not in graph:
            graph["episodes"] = {}
        
        graph["episodes"][str(episode)] = {
            "content": content,
            "summary": summary,
            "characters": characters or [],
            "scenes": scenes or [],
            "timestamp": datetime.now().isoformat()
        }
        
        # 更新人物
        if characters:
            for char in characters:
                char_id = char.get("id", f"C-{char.get('name', 'unknown')}")
                graph["characters"][char_id] = {
                    **char,
                    "last_appear": episode
                }
        
        # 更新钩子
        if "hooks" not in graph:
            graph["hooks"] = []
        
        # 处理新增钩子
        if hooks_created:
            for hook in hooks_created:
                hook["id"] = hook.get("id", f"H-{len(graph['hooks']) + 1}")
                hook["created_in"] = episode
                hook["status"] = "open"
                graph["hooks"].append(hook)
        
        # 处理闭环钩子
        if hooks_resolved:
            for hook in graph["hooks"]:
                if hook.get("id") in hooks_resolved:
                    hook["status"] = "resolved"
                    hook["resolved_in"] = episode
        
        # 更新场景
        if scenes:
            for scene in scenes:
                scene_id = scene.get("id", f"S-{scene.get('name', 'unknown')}")
                if scene_id not in graph["scenes"]:
                    graph["scenes"][scene_id] = {
                        **scene,
                        "episodes": [episode]
                    }
                else:
                    if episode not in graph["scenes"][scene_id].get("episodes", []):
                        graph["scenes"][scene_id].setdefault("episodes", []).append(episode)
        
        # 保存
        self._save_graph(pipeline_id, graph)
        
        return {
            "success": True,
            "message": f"第{episode}集图谱存储成功",
            "episode": episode,
            "pipeline_id": pipeline_id
        }
    
    def get_open_hooks(self, pipeline_id: str) -> List[Dict]:
        """
        获取未闭环的钩子列表
        
        Args:
            pipeline_id: 管道ID
            
        Returns:
            未闭环钩子列表
        """
        graph = self._load_graph(pipeline_id)
        return [h for h in graph.get("hooks", []) if h.get("status") == "open"]
    
    def get_all_hooks(self, pipeline_id: str) -> List[Dict]:
        """
        获取所有钩子
        
        Args:
            pipeline_id: 管道ID
            
        Returns:
            所有钩子列表
        """
        graph = self._load_graph(pipeline_id)
        return graph.get("hooks", [])
    
    def get_characters(self, pipeline_id: str) -> Dict:
        """
        获取所有人物
        
        Args:
            pipeline_id: 管道ID
            
        Returns:
            人物字典
        """
        graph = self._load_graph(pipeline_id)
        return graph.get("characters", {})
    
    def get_full_graph(self, pipeline_id: str) -> Dict:
        """
        获取完整图谱
        
        Args:
            pipeline_id: 管道ID
            
        Returns:
            完整图谱数据
        """
        return self._load_graph(pipeline_id)
    
    def delete_graph(self, pipeline_id: str) -> Dict:
        """
        删除图谱
        
        Args:
            pipeline_id: 管道ID
            
        Returns:
            删除结果
        """
        # 清除缓存
        if pipeline_id in self.cache:
            del self.cache[pipeline_id]
        
        # 删除文件
        graph_path = self._get_graph_path(pipeline_id)
        if os.path.exists(graph_path):
            os.remove(graph_path)
            return {"success": True, "message": "图谱已删除"}
        
        return {"success": False, "error": "图谱不存在"}
    
    def _get_episode_characters(self, graph: Dict, episode: int) -> List[Dict]:
        """获取指定剧集涉及的人物"""
        episode_data = graph.get("episodes", {}).get(str(episode), {})
        char_ids = episode_data.get("characters", [])
        
        characters = []
        for char_id in char_ids:
            if isinstance(char_id, str):
                char_data = graph.get("characters", {}).get(char_id, {})
                if char_data:
                    characters.append(char_data)
            elif isinstance(char_id, dict):
                characters.append(char_id)
        
        return characters
    
    def clear_cache(self, pipeline_id: Optional[str] = None):
        """
        清除缓存
        
        Args:
            pipeline_id: 指定管道ID，为None时清除所有缓存
        """
        if pipeline_id:
            if pipeline_id in self.cache:
                del self.cache[pipeline_id]
        else:
            self.cache = {}


# 单例实例
_graph_manager = None

def get_graph_manager() -> GraphManager:
    """获取图谱管理器单例"""
    global _graph_manager
    if _graph_manager is None:
        _graph_manager = GraphManager()
    return _graph_manager