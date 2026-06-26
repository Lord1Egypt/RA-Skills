#!/usr/bin/env python3
"""
yaoyao-memory Memory Engine v5.0
统一记忆调度引擎 - 替代原有111个散落脚本
"""

import json
import time
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime

# 内部模块
from .search.search_engine import SearchEngine
from .storage.sqlite_store import SQLiteStore
from .engine.capture_engine import CaptureEngine
from .engine.recall_engine import RecallEngine
from .engine.sync_engine import SyncEngine
from .engine.backup_engine import BackupEngine
from .engine.analytics_engine import AnalyticsEngine


class MemoryEngine:
    """
    统一记忆调度引擎
    所有记忆操作通过此引擎统一入口
    """
    
    VERSION = "5.0.0"
    
    def __init__(self, config_path: Optional[Path] = None):
        self.start_time = time.time()
        
        # 初始化存储层
        self.store = SQLiteStore()
        
        # 初始化搜索引擎
        self.search = SearchEngine()
        
        # 初始化引擎
        self.engines = {
            "capture": CaptureEngine(),
            "recall": RecallEngine(),
            "sync": SyncEngine(),
            "backup": BackupEngine(),
            "analytics": AnalyticsEngine(),
        }
        
        # 加载配置
        self.config = self._load_config(config_path)
        
        # 状态
        self._stats = {
            "queries": 0,
            "captures": 0,
            "errors": 0,
            "uptime_start": self.start_time,
        }
    
    def _load_config(self, config_path: Optional[Path]) -> Dict:
        """加载配置"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "unified_config.json"
        
        if config_path.exists():
            return json.loads(config_path.read_text())
        return {}
    
    # ========== 核心操作 ==========
    
    def search_memory(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索记忆"""
        self._stats["queries"] += 1
        return self.search.query(query, limit=limit)
    
    def capture(self, content: str, metadata: Optional[Dict] = None) -> Dict:
        """捕获新记忆"""
        self._stats["captures"] += 1
        return self.engines["capture"].run(content, metadata)
    
    def recall(self, query: str, context: Optional[Dict] = None) -> List[Dict]:
        """召回相关记忆"""
        return self.engines["recall"].run(query, context)
    
    def sync(self, target: str = "ima") -> Dict:
        """同步到云端"""
        return self.engines["sync"].run(target)
    
    def backup(self, target: str = "local") -> Dict:
        """备份"""
        return self.engines["backup"].run(target)
    
    def analyze(self) -> Dict:
        """分析记忆统计"""
        return self.engines["analytics"].run()
    
    # ========== 状态接口 ==========
    
    def stats(self) -> Dict:
        """获取引擎统计"""
        return {
            **self._stats,
            "uptime": time.time() - self.start_time,
            "version": self.VERSION,
        }
    
    def health(self) -> Dict:
        """健康检查"""
        return {
            "status": "healthy",
            "engines": {k: "ok" for k in self.engines},
            "store": self.store.health(),
            "search": self.search.health(),
        }


# 便捷函数
_engine_instance: Optional[MemoryEngine] = None


def get_engine() -> MemoryEngine:
    """获取引擎单例"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = MemoryEngine()
    return _engine_instance


def search(query: str, limit: int = 10) -> List[Dict]:
    """快捷搜索"""
    return get_engine().search_memory(query, limit)


def capture(content: str, metadata: Optional[Dict] = None) -> Dict:
    """快捷捕获"""
    return get_engine().capture(content, metadata)
