"""
荞麦饼 Skills - 八层记忆系统 (OctoMemory)
从瞬时到永恒的完整记忆架构
"""

import time
import json
import hashlib
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from collections import OrderedDict
import threading


@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    content: Any
    layer: int  # 1-8
    timestamp: float
    access_count: int = 0
    last_access: float = field(default_factory=time.time)
    importance: float = 0.5  # 0-1
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoryEntry':
        return cls(**data)


class MemoryLayer:
    """记忆层基类"""
    
    def __init__(self, layer_id: int, name: str, capacity: int, ttl: Optional[float] = None):
        self.layer_id = layer_id
        self.name = name
        self.capacity = capacity
        self.ttl = ttl  # 生存时间（秒）
        self.memories: OrderedDict[str, MemoryEntry] = OrderedDict()
        self.lock = threading.RLock()
    
    def store(self, entry: MemoryEntry) -> bool:
        """存储记忆"""
        with self.lock:
            # 检查容量
            if len(self.memories) >= self.capacity:
                self._evict()
            
            self.memories[entry.id] = entry
            return True
    
    def retrieve(self, memory_id: str) -> Optional[MemoryEntry]:
        """检索记忆"""
        with self.lock:
            entry = self.memories.get(memory_id)
            if entry:
                # 检查TTL
                if self.ttl and time.time() - entry.timestamp > self.ttl:
                    del self.memories[memory_id]
                    return None
                
                # 更新访问信息
                entry.access_count += 1
                entry.last_access = time.time()
                
                # 移动到最近使用
                self.memories.move_to_end(memory_id)
                
                return entry
            return None
    
    def search(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        """搜索记忆（简单关键词匹配）"""
        results = []
        query_lower = query.lower()
        
        with self.lock:
            for entry in self.memories.values():
                # 检查TTL
                if self.ttl and time.time() - entry.timestamp > self.ttl:
                    continue
                
                content_str = str(entry.content).lower()
                if query_lower in content_str:
                    score = self._calculate_relevance(entry, query)
                    results.append((score, entry))
        
        # 按相关度排序
        results.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in results[:top_k]]
    
    def _calculate_relevance(self, entry: MemoryEntry, query: str) -> float:
        """计算相关度分数"""
        score = 0.0
        
        # 访问频率
        score += min(entry.access_count * 0.1, 1.0)
        
        # 重要性
        score += entry.importance
        
        # 时效性（越新越好）
        age = time.time() - entry.timestamp
        freshness = max(0, 1 - age / (7 * 24 * 3600))  # 一周内
        score += freshness * 0.5
        
        return score
    
    def _evict(self):
        """淘汰策略（LRU）"""
        if self.memories:
            # 移除最久未使用的
            self.memories.popitem(last=False)
    
    def clear(self):
        """清空层"""
        with self.lock:
            self.memories.clear()
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        with self.lock:
            return {
                "layer_id": self.layer_id,
                "name": self.name,
                "count": len(self.memories),
                "capacity": self.capacity,
                "utilization": len(self.memories) / self.capacity
            }


class OctoMemorySystem:
    """八层记忆系统"""
    
    LAYER_CONFIG = {
        8: {"name": "instant", "capacity": 10, "ttl": 1},        # 瞬时记忆 - 1秒
        7: {"name": "working", "capacity": 20, "ttl": 60},       # 工作记忆 - 1分钟
        6: {"name": "short", "capacity": 100, "ttl": 3600},      # 短期记忆 - 1小时
        5: {"name": "session", "capacity": 500, "ttl": 86400},   # 会话记忆 - 1天
        4: {"name": "context", "capacity": 1000, "ttl": 604800}, # 上下文记忆 - 7天
        3: {"name": "long", "capacity": 5000, "ttl": None},      # 长期记忆 - 永久
        2: {"name": "skill", "capacity": 2000, "ttl": None},     # 技能记忆 - 永久
        1: {"name": "expert", "capacity": 1000, "ttl": None},    # 专家记忆 - 永久
    }
    
    def __init__(self):
        self.layers: Dict[int, MemoryLayer] = {}
        self._init_layers()
        self.promotion_threshold = 3  # 访问次数阈值，用于晋升
    
    def _init_layers(self):
        """初始化各层"""
        for layer_id, config in self.LAYER_CONFIG.items():
            self.layers[layer_id] = MemoryLayer(
                layer_id=layer_id,
                name=config["name"],
                capacity=config["capacity"],
                ttl=config["ttl"]
            )
    
    def store(self, content: Any, layer: int = 5, importance: float = 0.5, 
              tags: List[str] = None, metadata: Dict = None) -> str:
        """
        存储记忆
        
        Args:
            content: 记忆内容
            layer: 存储层 (1-8)，默认5（会话记忆）
            importance: 重要性 (0-1)
            tags: 标签列表
            metadata: 元数据
        
        Returns:
            memory_id: 记忆ID
        """
        layer = max(1, min(8, layer))
        
        # 生成唯一ID
        content_hash = hashlib.md5(
            f"{content}{time.time()}".encode()
        ).hexdigest()[:12]
        memory_id = f"mem_{self.LAYER_CONFIG[layer]['name']}_{content_hash}"
        
        entry = MemoryEntry(
            id=memory_id,
            content=content,
            layer=layer,
            timestamp=time.time(),
            importance=importance,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        self.layers[layer].store(entry)
        return memory_id
    
    def retrieve(self, memory_id: str) -> Optional[MemoryEntry]:
        """检索记忆（跨层搜索）"""
        # 从高层到低层搜索
        for layer_id in range(8, 0, -1):
            entry = self.layers[layer_id].retrieve(memory_id)
            if entry:
                # 考虑晋升
                self._consider_promotion(entry)
                return entry
        return None
    
    def search(self, query: str, top_k: int = 10, layers: List[int] = None) -> List[Tuple[int, MemoryEntry]]:
        """
        跨层搜索记忆
        
        Args:
            query: 搜索关键词
            top_k: 返回结果数量
            layers: 指定搜索层，默认全部
        
        Returns:
            [(layer_id, entry), ...]
        """
        layers = layers or range(8, 0, -1)
        all_results = []
        
        for layer_id in layers:
            results = self.layers[layer_id].search(query, top_k)
            for entry in results:
                all_results.append((layer_id, entry))
        
        # 按相关度排序
        all_results.sort(
            key=lambda x: self._calculate_total_score(x[1]),
            reverse=True
        )
        
        return all_results[:top_k]
    
    def _calculate_total_score(self, entry: MemoryEntry) -> float:
        """计算总分"""
        base_score = entry.importance
        
        # 访问频率加成
        base_score += min(entry.access_count * 0.05, 0.5)
        
        # 时效性加成
        age = time.time() - entry.timestamp
        if age < 3600:  # 1小时内
            base_score += 0.3
        elif age < 86400:  # 1天内
            base_score += 0.2
        
        return base_score
    
    def _consider_promotion(self, entry: MemoryEntry):
        """考虑晋升到更高层"""
        if entry.access_count >= self.promotion_threshold and entry.layer < 8:
            # 晋升到上一层
            new_layer = entry.layer + 1
            entry.layer = new_layer
            self.layers[new_layer].store(entry)
    
    def consolidate(self):
        """记忆整合（将重要短期记忆转为长期）"""
        # 从短期记忆层提取高重要性记忆
        short_layer = self.layers[6]
        long_layer = self.layers[3]
        
        with short_layer.lock:
            for memory_id, entry in list(short_layer.memories.items()):
                if entry.importance > 0.7 or entry.access_count > 5:
                    # 晋升到长期记忆
                    entry.layer = 3
                    long_layer.store(entry)
    
    def get_memory_flow(self, memory_id: str) -> List[Dict]:
        """获取记忆流动轨迹"""
        flow = []
        
        for layer_id in range(1, 9):
            entry = self.layers[layer_id].retrieve(memory_id)
            if entry:
                flow.append({
                    "layer": layer_id,
                    "name": self.LAYER_CONFIG[layer_id]["name"],
                    "timestamp": entry.timestamp,
                    "access_count": entry.access_count
                })
        
        return flow
    
    def get_stats(self) -> Dict:
        """获取系统统计"""
        total_memories = sum(
            layer.get_stats()["count"] 
            for layer in self.layers.values()
        )
        
        return {
            "total_memories": total_memories,
            "layers": {
                layer_id: layer.get_stats()
                for layer_id, layer in self.layers.items()
            },
            "utilization": sum(
                layer.get_stats()["utilization"]
                for layer in self.layers.values()
            ) / 8
        }
    
    def export_layer(self, layer: int) -> List[Dict]:
        """导出指定层的记忆"""
        if layer not in self.layers:
            return []
        
        return [
            entry.to_dict()
            for entry in self.layers[layer].memories.values()
        ]
    
    def import_layer(self, layer: int, memories: List[Dict]):
        """导入记忆到指定层"""
        if layer not in self.layers:
            return
        
        for mem_data in memories:
            entry = MemoryEntry.from_dict(mem_data)
            self.layers[layer].store(entry)
    
    def clear_layer(self, layer: int):
        """清空指定层"""
        if layer in self.layers:
            self.layers[layer].clear()
    
    def clear_all(self):
        """清空所有记忆"""
        for layer in self.layers.values():
            layer.clear()


class MemorySync:
    """记忆同步器"""
    
    def __init__(self, memory_system: OctoMemorySystem):
        self.memory = memory_system
        self.sync_history: List[Dict] = []
    
    def sync_to_external(self, target: str, layer_filter: List[int] = None) -> Dict:
        """同步到外部系统"""
        layer_filter = layer_filter or [3, 2, 1]  # 只同步长期记忆
        
        exported = {}
        for layer_id in layer_filter:
            exported[layer_id] = self.memory.export_layer(layer_id)
        
        sync_record = {
            "timestamp": time.time(),
            "target": target,
            "layers": layer_filter,
            "count": sum(len(mems) for mems in exported.values())
        }
        self.sync_history.append(sync_record)
        
        return {
            "success": True,
            "exported": exported,
            "record": sync_record
        }
    
    def sync_from_external(self, source: str, data: Dict) -> Dict:
        """从外部系统同步"""
        imported_count = 0
        
        for layer_id, memories in data.items():
            layer_id = int(layer_id)
            self.memory.import_layer(layer_id, memories)
            imported_count += len(memories)
        
        return {
            "success": True,
            "imported": imported_count,
            "source": source
        }
    
    def get_sync_history(self) -> List[Dict]:
        """获取同步历史"""
        return self.sync_history


# 便捷函数
def create_memory_system() -> OctoMemorySystem:
    """创建记忆系统"""
    return OctoMemorySystem()


def quick_store(content: Any, importance: float = 0.5) -> str:
    """快速存储"""
    mem = OctoMemorySystem()
    return mem.store(content, importance=importance)


def quick_search(query: str, top_k: int = 5) -> List[Tuple[int, MemoryEntry]]:
    """快速搜索"""
    mem = OctoMemorySystem()
    return mem.search(query, top_k)


if __name__ == "__main__":
    # 测试
    mem = OctoMemorySystem()
    
    # 存储记忆
    id1 = mem.store("AI发展趋势研究", layer=5, importance=0.8, tags=["AI", "研究"])
    id2 = mem.store("Python编程技巧", layer=3, importance=0.6, tags=["编程", "Python"])
    id3 = mem.store("会议纪要", layer=6, importance=0.4, tags=["会议"])
    
    print(f"存储记忆: {id1}, {id2}, {id3}")
    
    # 搜索
    results = mem.search("AI")
    print(f"\n搜索结果 ({len(results)} 条):")
    for layer, entry in results:
        print(f"  [{mem.LAYER_CONFIG[layer]['name']}] {entry.content}")
    
    # 统计
    print("\n系统统计:")
    print(mem.get_stats())
