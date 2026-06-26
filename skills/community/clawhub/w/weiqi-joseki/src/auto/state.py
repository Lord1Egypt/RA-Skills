#!/usr/bin/env python3
"""
Auto模式状态管理模块

管理 ~/.weiqi-joseki/auto/state.json
包括配置、进度、统计信息
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union


DEFAULT_AUTO_DIR = Path.home() / ".weiqi-joseki" / "auto"
DEFAULT_STATE_FILE = DEFAULT_AUTO_DIR / "state.json"


def get_adaptive_cms_config(estimated_games: int) -> Dict[str, int]:
    """根据预估棋谱数返回自适应CMS配置
    
    Args:
        estimated_games: 预估棋谱数量
        
    Returns:
        dict: {'width': int, 'depth': int}
    """
    if estimated_games < 100_000:
        return {"width": 1_048_576, "depth": 4}   # 16MB
    elif estimated_games < 1_000_000:
        return {"width": 4_194_304, "depth": 4}   # 64MB
    else:
        return {"width": 16_777_216, "depth": 4}  # 256MB


class AutoState:
    """自动模式状态管理器
    
    管理配置和进度，所有数据持久化到 state.json
    """
    
    def __init__(self, auto_dir: Optional[Union[str, Path]] = None):
        """
        Args:
            auto_dir: auto目录路径，默认 ~/.weiqi-joseki/auto
        """
        self.auto_dir = Path(auto_dir) if auto_dir else DEFAULT_AUTO_DIR
        self.state_file = self.auto_dir / "state.json"
        self._data = self._load()
    
    def _load(self) -> dict:
        """加载状态文件，不存在则返回空结构"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._empty_state()
    
    def _save(self):
        """保存状态到文件"""
        self.auto_dir.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)
    
    def _empty_state(self) -> dict:
        """返回空状态结构（简化版）
        
        只保留config，不跟踪进度。状态完全由文件系统决定：
        - 有tar文件 = 已下载
        - 有temp文件 = 已提取
        - 有cms.pkl = 有统计
        """
        return {
            "mode": "auto",
            "config": {}
        }
    
    def init_config(self, 
                    estimated_games: int = 2_000_000,
                    first_n: int = 80,
                    distance_threshold: int = 4,
                    min_freq: int = 10,
                    global_top_k: int = 100_000,
                    rebuild_threshold_days: int = 0) -> dict:
        """初始化配置
        
        Args:
            estimated_games: 预估棋谱数，用于自适应CMS配置
            first_n: 提取前N手
            distance_threshold: 连通块距离阈值
            min_freq: 最小频率
            global_top_k: 全局Top-K定式数
            rebuild_threshold_days: 重建触发阈值（天）
            
        Returns:
            配置字典
        """
        cms_config = get_adaptive_cms_config(estimated_games)
        
        self._data["config"] = {
            "cms_width": cms_config["width"],
            "cms_depth": cms_config["depth"],
            "first_n": first_n,
            "distance_threshold": distance_threshold,
            "min_freq": min_freq,
            "global_top_k": global_top_k,
            "rebuild_threshold_days": rebuild_threshold_days
        }
        
        self._save()
        return self._data["config"]
    
    @property
    def config(self) -> dict:
        """获取当前配置"""
        return self._data.get("config", {})
    
    def is_initialized(self) -> bool:
        """检查是否已初始化（有配置）"""
        return bool(self._data.get("config"))
    
    def reset(self):
        """重置所有状态（删除state.json的效果）"""
        self._data = self._empty_state()
        if self.state_file.exists():
            self.state_file.unlink()
    
    def __repr__(self):
        return f"AutoState(dir={self.auto_dir}, initialized={self.is_initialized()})"
