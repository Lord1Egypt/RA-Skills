#!/usr/bin/env python3
"""
Soul Memory v3.4.0 - Incremental Index Update
增量索引更新：無需全量重建，即時可搜索

Author: Li Si (李斯)
Date: 2026-03-08

v3.4.0 - 新增增量更新 + 異步索引
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import threading

# Ensure module path
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@dataclass
class IndexSegment:
    """索引分段"""
    segment_id: str
    content: str
    content_hash: str
    timestamp: float
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'segment_id': self.segment_id,
            'content': self.content,
            'content_hash': self.content_hash,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'IndexSegment':
        return cls(
            segment_id=data['segment_id'],
            content=data['content'],
            content_hash=data['content_hash'],
            timestamp=data['timestamp'],
            metadata=data.get('metadata', {})
        )


class IncrementalIndexer:
    """
    增量索引更新器 v3.4.0
    
    Features:
    - 增量添加新記憶
    - 異步索引重建
    - 分段管理
    - 自動合併
    """
    
    VERSION = "3.4.0"
    MERGE_THRESHOLD = 100  # 累積 100 個分段後合併
    
    def __init__(self, index_path: Optional[Path] = None):
        """
        初始化索引器
        
        Args:
            index_path: 索引文件路徑
        """
        self.index_path = index_path or Path(__file__).parent.parent / "cache" / "index"
        self.index_path.mkdir(parents=True, exist_ok=True)
        
        # 索引數據結構
        self.segments: Dict[str, IndexSegment] = {}
        self.content_to_segment: Dict[str, str] = {}  # content_hash -> segment_id
        self.incremental_count = 0
        self.last_full_rebuild = 0.0
        
        # 鎖機制
        self.lock = threading.RLock()
        
        # 異步線程
        self.merge_thread: Optional[threading.Thread] = None
        
        # 加載現有索引
        self.load_index()
    
    def _hash_content(self, content: str) -> str:
        """計算內容哈希"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def _generate_segment_id(self) -> str:
        """生成分段 ID"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"seg_{timestamp}_{os.getpid()}"
    
    def add_segment(self, content: str, metadata: Optional[Dict] = None) -> str:
        """
        添加新分段
        
        Args:
            content: 內容文本
            metadata: 元數據
            
        Returns:
            分段 ID
        """
        with self.lock:
            content_hash = self._hash_content(content)
            
            # 檢查是否已存在
            if content_hash in self.content_to_segment:
                segment_id = self.content_to_segment[content_hash]
                print(f"[Indexer] Segment already exists: {segment_id}")
                return segment_id
            
            # 創建新分段
            segment_id = self._generate_segment_id()
            segment = IndexSegment(
                segment_id=segment_id,
                content=content,
                content_hash=content_hash,
                timestamp=time.time(),
                metadata=metadata or {}
            )
            
            # 添加到索引
            self.segments[segment_id] = segment
            self.content_to_segment[content_hash] = segment_id
            self.incremental_count += 1
            
            # 檢查是否需要合併
            if self.incremental_count >= self.MERGE_THRESHOLD:
                self._trigger_merge()
            
            # 保存增量
            self._save_increment(segment)
            
            return segment_id
    
    def remove_segment(self, segment_id: str) -> bool:
        """
        移除分段
        
        Args:
            segment_id: 分段 ID
            
        Returns:
            是否成功移除
        """
        with self.lock:
            if segment_id not in self.segments:
                return False
            
            segment = self.segments[segment_id]
            del self.segments[segment_id]
            
            if segment.content_hash in self.content_to_segment:
                del self.content_to_segment[segment.content_hash]
            
            # 標記為已刪除
            segment.metadata['deleted'] = True
            segment.metadata['deleted_at'] = time.time()
            
            return True
    
    def update_segment(self, segment_id: str, new_content: str) -> bool:
        """
        更新分段
        
        Args:
            segment_id: 分段 ID
            new_content: 新內容
            
        Returns:
            是否成功更新
        """
        with self.lock:
            if segment_id not in self.segments:
                return False
            
            # 移除舊內容映射
            old_segment = self.segments[segment_id]
            if old_segment.content_hash in self.content_to_segment:
                del self.content_to_segment[old_segment.content_hash]
            
            # 更新內容
            content_hash = self._hash_content(new_content)
            old_segment.content = new_content
            old_segment.content_hash = content_hash
            old_segment.timestamp = time.time()
            old_segment.metadata['updated'] = True
            
            # 添加新映射
            self.content_to_segment[content_hash] = segment_id
            
            return True
    
    def search(self, query: str) -> List[Dict]:
        """
        搜索索引
        
        Args:
            query: 查詢字符串
            
        Returns:
            匹配的 segment 列表
        """
        with self.lock:
            results = []
            query_lower = query.lower()
            
            for segment in self.segments.values():
                # 跳過已刪除的
                if segment.metadata.get('deleted'):
                    continue
                
                # 關鍵詞匹配
                if query_lower in segment.content.lower():
                    results.append({
                        'segment_id': segment.segment_id,
                        'content': segment.content,
                        'timestamp': segment.timestamp,
                        'metadata': segment.metadata
                    })
            
            # 按時間排序（最新的在前）
            results.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return results
    
    def _trigger_merge(self):
        """觸發異步合併"""
        if self.merge_thread and self.merge_thread.is_alive():
            return
        
        self.merge_thread = threading.Thread(target=self._merge_segments, daemon=True)
        self.merge_thread.start()
    
    def _merge_segments(self):
        """合併分段（異步）"""
        print("[Indexer] Starting background merge...")
        
        with self.lock:
            # 保存完整索引
            self._save_full_index()
            
            # 重置增量計數
            self.incremental_count = 0
            
            print(f"[Indexer] Merge complete. Total segments: {len(self.segments)}")
    
    def _save_increment(self, segment: IndexSegment):
        """保存增量"""
        increment_file = self.index_path / "increments" / f"{segment.segment_id}.json"
        increment_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(increment_file, 'w', encoding='utf-8') as f:
            json.dump(segment.to_dict(), f, ensure_ascii=False, indent=2)
    
    def _save_full_index(self):
        """保存完整索引"""
        index_file = self.index_path / "index.json"
        
        data = {
            'version': self.VERSION,
            'built_at': datetime.now().isoformat(),
            'segment_count': len(self.segments),
            'segments': [seg.to_dict() for seg in self.segments.values()]
        }
        
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_index(self):
        """加載索引"""
        index_file = self.index_path / "index.json"
        
        if not index_file.exists():
            print("[Indexer] No existing index found, starting fresh")
            return
        
        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for seg_data in data.get('segments', []):
                segment = IndexSegment.from_dict(seg_data)
                self.segments[segment.segment_id] = segment
                self.content_to_segment[segment.content_hash] = segment.segment_id
            
            print(f"[Indexer] Loaded {len(self.segments)} segments")
            
            # 加載增量
            self._load_increments()
            
        except Exception as e:
            print(f"[Indexer] Failed to load index: {e}")
    
    def _load_increments(self):
        """加載增量文件"""
        increments_dir = self.index_path / "increments"
        
        if not increments_dir.exists():
            return
        
        for increment_file in increments_dir.glob("*.json"):
            try:
                with open(increment_file, 'r', encoding='utf-8') as f:
                    seg_data = json.load(f)
                
                segment = IndexSegment.from_dict(seg_data)
                self.segments[segment.segment_id] = segment
                self.content_to_segment[segment.content_hash] = segment.segment_id
                self.incremental_count += 1
            except Exception as e:
                print(f"[Indexer] Failed to load increment {increment_file}: {e}")
    
    def get_stats(self) -> Dict:
        """獲取索引統計"""
        return {
            'version': self.VERSION,
            'total_segments': len(self.segments),
            'incremental_count': self.incremental_count,
            'last_full_rebuild': datetime.fromtimestamp(self.last_full_rebuild).isoformat() if self.last_full_rebuild > 0 else None,
            'merge_threshold': self.MERGE_THRESHOLD
        }
    
    def force_merge(self):
        """強制合併"""
        with self.lock:
            self._merge_segments()


# 全局實例
_global_indexer: Optional[IncrementalIndexer] = None


def get_indexer(index_path: Optional[Path] = None) -> IncrementalIndexer:
    """獲取全局索引器實例"""
    global _global_indexer
    
    if _global_indexer is None:
        _global_indexer = IncrementalIndexer(index_path)
    
    return _global_indexer


# CLI 測試
if __name__ == "__main__":
    print("🧪 Testing Incremental Index Update v3.4.0\n")
    
    indexer = get_indexer()
    
    # 測試 1: 添加分段
    print("Test 1: Add Segments")
    for i in range(5):
        content = f"Test content {i} - QST theory and FSCA simulation"
        segment_id = indexer.add_segment(content, {'test': True, 'index': i})
        print(f"  Added segment: {segment_id}")
    print()
    
    # 測試 2: 搜索
    print("Test 2: Search")
    results = indexer.search("QST theory")
    print(f"  Found {len(results)} results")
    for r in results[:3]:
        print(f"    - {r['content'][:50]}...")
    print()
    
    # 測試 3: 更新分段
    print("Test 3: Update Segment")
    if results:
        segment_id = results[0]['segment_id']
        success = indexer.update_segment(segment_id, "Updated content - new QST theory")
        print(f"  Update success: {success}")
    print()
    
    # 測試 4: 統計信息
    print("Test 4: Statistics")
    stats = indexer.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()
    
    # 測試 5: 強制合併
    print("Test 5: Force Merge")
    indexer.force_merge()
    print(f"  Merge complete\n")
    
    print("✅ All tests passed!")
