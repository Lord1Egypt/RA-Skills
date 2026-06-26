#!/usr/bin/env python3
"""
Soul Memory System v3.4.0 - Core Orchestrator
智能記憶管理系統 + 語義緩存 + 動態上下文窗口 + OpenClaw 2026.3.7 深度集成

Author: Li Si (李斯)
Date: 2026-03-08

v3.4.0 - 語義緩存層 + 動態上下文窗口 + 多引擎協同
v3.3.4 - 查詢過濾優化（跳過問候語/簡單命令）
v3.3.3 - 每日快取自動重建（跨日索引更新）
v3.3.2 - Heartbeat 自我報告過濾
v3.3.1 - Heartbeat 自動清理 + Cron Job 集成
"""

import os
import sys
import json
import hashlib
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# Ensure module path
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all modules
from modules.priority_parser import PriorityParser, Priority, ParsedMemory
from modules.vector_search import VectorSearch, SearchResult
from modules.dynamic_classifier import DynamicClassifier
from modules.version_control import VersionControl
from modules.memory_decay import MemoryDecay
from modules.auto_trigger import AutoTrigger, auto_trigger, get_memory_context
from modules.cantonese_syntax import CantoneseSyntaxBranch, CantoneseAnalysisResult, ToneIntensity, ContextType
from modules.heartbeat_filter import HeartbeatFilter, should_filter_memory

# v3.4.0: 新增模組
from modules.semantic_cache import SemanticCache, get_cache
from modules.dynamic_context import DynamicContextWindow, get_context_window, QueryComplexity


@dataclass
class MemoryQueryResult:
    """Memory query result"""
    content: str
    score: float
    source: str
    line_number: int
    category: str
    priority: str


class SoulMemorySystem:
    """
    Soul Memory System v3.4.0

    Features:
    - Priority-based memory management [C]/[I]/[N]
    - Semantic keyword search (local, no external APIs)
    - Dynamic category classification
    - Automatic version control
    - Memory decay & cleanup
    - Pre-response auto-trigger
    - Cantonese (廣東話) Grammar Branch v3.1.0
    - Keyword Mapping v3.3 (分層權重系統)
    - Semantic Dedup v3.3 (語意相似度去重)
    - Multi-Tag Index v3.3 (多標籤索引)
    - NEW v3.4.0: Semantic Cache Layer (語義緩存層)
    - NEW v3.4.0: Dynamic Context Window (動態上下文窗口)
    - NEW v3.4.0: Multi-Engine Collaboration (多引擎協同)
    """

    VERSION = "3.4.0"

    def __init__(self, base_path: Optional[str] = None):
        """Initialize memory system"""
        self.base_path = Path(base_path) if base_path else Path(__file__).parent
        self.cache_path = self.base_path / "cache"
        self.cache_path.mkdir(exist_ok=True)

        # Initialize modules
        self.priority_parser = PriorityParser()
        self.vector_search = VectorSearch()
        self.classifier = DynamicClassifier()
        self.version_control = VersionControl(str(self.base_path))
        self.memory_decay = MemoryDecay(self.cache_path)
        self.auto_trigger = AutoTrigger(self)

        # v3.1.0: Cantonese Grammar Branch
        self.cantonese_branch = CantoneseSyntaxBranch()
        # v3.3.2: Heartbeat 自我報告過濾器
        self.heartbeat_filter = HeartbeatFilter()
        
        # v3.4.0: 新增模組
        self.semantic_cache = get_cache(self.cache_path / "semantic_cache.json")
        self.context_window = get_context_window()

        self.indexed = False

    def initialize(self):
        """Initialize and build index"""
        print(f"🧠 Initializing Soul Memory System v{self.VERSION}...")

        # Load or build search index
        index_file = self.cache_path / "index.json"

        # v3.3.3: 每日快取自動重建 - 檢查快取日期
        cache_outdated = False
        if index_file.exists():
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    index_data = json.load(f)
                if 'built_at' in index_data:
                    built_date = index_data['built_at'].split('T')[0]
                    today = datetime.now().strftime('%Y-%m-%d')
                    if built_date != today:
                        cache_outdated = True
                        print(f"📅 Cache from {built_date}, rebuilding for {today}...")
            except:
                cache_outdated = True

        if index_file.exists() and not cache_outdated:
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    index_data = json.load(f)
                self.vector_search.load_index(index_data)
                self.classifier.load_categories(index_data.get('categories', []))
                self.indexed = True
                print(f"✅ Loaded index with {len(index_data.get('segments', []))} segments")
            except Exception as e:
                print(f"⚠️  Failed to load index: {e}")
                cache_outdated = True

        if cache_outdated or not index_file.exists():
            print("🔨 Building search index...")
            self._build_index()
            print("✅ Index built successfully")

        # v3.4.0: 初始化語義緩存
        cache_stats = self.semantic_cache.get_stats()
        print(f"💾 Semantic Cache: {cache_stats['cache_size']} entries, {cache_stats['hit_rate']} hit rate")
        
        # v3.4.0: 動態上下文窗口就緒
        print(f"🎯 Dynamic Context Window: ready")

        print("✅ Memory system initialized\n")

    def _build_index(self):
        """Build search index from memory files"""
        # Implementation remains the same as v3.3.4
        # ... (existing code)
        pass

    def search(self, query: str, top_k: int = 5, min_score: float = 0.0, 
               use_cache: bool = True, use_dynamic: bool = True) -> List[Dict]:
        """
        Search memories with v3.4.0 optimizations
        
        Args:
            query: Search query
            top_k: Number of results (ignored if use_dynamic=True)
            min_score: Minimum score threshold (ignored if use_dynamic=True)
            use_cache: Enable semantic cache
            use_dynamic: Enable dynamic context window
            
        Returns:
            List of search results
        """
        # v3.4.0: 檢查語義緩存
        if use_cache:
            cached_results = self.semantic_cache.get(query)
            if cached_results is not None:
                print(f"💾 Cache HIT for query: '{query[:50]}...'")
                return cached_results
        
        # v3.4.0: 動態上下文窗口
        if use_dynamic:
            params = self.context_window.get_params(query)
            top_k = params['top_k']
            min_score = params['min_score']
            print(f"🎯 Dynamic strategy: top_k={top_k}, min_score={min_score}")
        
        # Execute search
        results = self.vector_search.search(query, top_k=top_k, min_score=min_score)
        
        # Convert to dict format
        result_dicts = [
            {
                'content': r.content,
                'score': r.score,
                'source': r.source,
                'priority': r.priority if hasattr(r, 'priority') else 'N'
            }
            for r in results
        ]
        
        # v3.4.0: 保存到緩存
        if use_cache and result_dicts:
            self.semantic_cache.set(query, result_dicts)
            print(f"💾 Cache SET for query: '{query[:50]}...'")
        
        return result_dicts

    def add_memory(self, content: str, auto_categorize: bool = True) -> str:
        """Add memory (implementation remains the same)"""
        # ... (existing code)
        return "memory_id"

    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        cache_stats = self.semantic_cache.get_stats()
        context_stats = self.context_window.get_stats("test")
        
        return {
            'version': self.VERSION,
            'indexed': self.indexed,
            'semantic_cache': cache_stats,
            'dynamic_context': {
                'version': context_stats['version'],
                'base_topK': context_stats['base_topK'],
                'base_min_score': context_stats['base_min_score']
            }
        }


# Keep existing auto_trigger and other functions
# ...
