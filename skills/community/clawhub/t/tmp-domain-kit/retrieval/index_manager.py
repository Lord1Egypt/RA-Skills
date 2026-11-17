"""
索引管理器 - 启动时重建，支持多级索引查询
支持 entity_type、tag、关系追溯
"""

import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, Set, List, Any, Optional, Tuple


class IndexManager:
    """知识库索引管理器"""
    
    def __init__(self, storage_path: str):
        """
        Args:
            storage_path: 存储目录路径
        """
        self.storage_path = Path(storage_path)
        self.entities_file = self.storage_path / "entities.jsonl"
        self.relations_file = self.storage_path / "relations.jsonl"
        
        # 索引结构
        self.entity_type_index: Dict[str, Set[str]] = defaultdict(set)   # entity_type → set(entity_ids)
        self.tag_index: Dict[str, Set[str]] = defaultdict(set)           # tag → set(entity_ids)
        self.relation_forward: Dict[str, List[Tuple[str, str]]] = defaultdict(list)  # from_id → [(to_id, type)]
        self.relation_backward: Dict[str, List[Tuple[str, str]]] = defaultdict(list) # to_id → [(from_id, type)]
        
        # 构建索引
        self._rebuild_indices()
    
    def _rebuild_indices(self):
        """启动时全量重建索引，保证一致性"""
        # 清空索引
        self.entity_type_index.clear()
        self.tag_index.clear()
        self.relation_forward.clear()
        self.relation_backward.clear()
        
        # 扫描 entities.jsonl
        if self.entities_file.exists():
            with open(self.entities_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    record = json.loads(line)
                    entity_id = record['id']
                    entity_type = record['entity_type']
                    tags = record.get('tags', [])
                    
                    # 更新实体类型索引
                    self.entity_type_index[entity_type].add(entity_id)
                    
                    # 更新 tag 索引
                    for tag in tags:
                        self.tag_index[tag].add(entity_id)
        
        # 扫描 relations.jsonl
        if self.relations_file.exists():
            with open(self.relations_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    rel = json.loads(line)
                    from_id = rel['from_id']
                    to_id = rel['to_id']
                    rel_type = rel['relation_type']
                    
                    # 更新正向关系索引
                    self.relation_forward[from_id].append((to_id, rel_type))
                    
                    # 更新反向关系索引
                    self.relation_backward[to_id].append((from_id, rel_type))
    
    def query_by_tags(self, tags: List[str]) -> Set[str]:
        """
        按标签查询（取并集）。
        
        Args:
            tags: 标签列表
        
        Returns:
            匹配的实体 ID 集合
        """
        candidates = set()
        for tag in tags:
            candidates.update(self.tag_index.get(tag, set()))
        return candidates
    
    def query_by_entity_type(self, entity_type: str) -> Set[str]:
        """
        按实体类型查询。
        
        Args:
            entity_type: 实体类型
        
        Returns:
            匹配的实体 ID 集合
        """
        return self.entity_type_index.get(entity_type, set())
    
    def query_by_keywords(self, keywords: Dict[str, List[str]]) -> Set[str]:
        """
        按关键词查询（多维度取并集）。
        
        Args:
            keywords: {"models": ["AM600"], "scenarios": ["输送带"], ...}
        
        Returns:
            匹配的实体 ID 集合
        """
        candidates = set()
        
        # 设备型号 → tag 索引
        for model in keywords.get('models', []):
            candidates.update(self.tag_index.get(model, set()))
        
        # 场景词 → tag 索引
        for scenario in keywords.get('scenarios', []):
            candidates.update(self.tag_index.get(scenario, set()))
        
        # 动作词 → 实体类型索引（如"生成代码" → CodeTemplate）
        for action in keywords.get('actions', []):
            if action in ['生成代码', '代码生成']:
                candidates.update(self.entity_type_index.get('CodeTemplate', set()))
            elif action in ['选型', '配置']:
                candidates.update(self.entity_type_index.get('Device', set()))
                candidates.update(self.entity_type_index.get('Constraint', set()))
        
        return candidates
    
    def get_forward_relations(self, entity_id: str) -> List[Tuple[str, str]]:
        """
        获取实体的正向关系（from_id → to_id）。
        
        Args:
            entity_id: 实体 ID
        
        Returns:
            [(to_id, relation_type), ...]
        """
        return self.relation_forward.get(entity_id, [])
    
    def get_backward_relations(self, entity_id: str) -> List[Tuple[str, str]]:
        """
        获取实体的反向关系（to_id ← from_id）。
        
        Args:
            entity_id: 实体 ID
        
        Returns:
            [(from_id, relation_type), ...]
        """
        return self.relation_backward.get(entity_id, [])
    
    def get_all_relations(self, entity_id: str) -> List[Dict[str, Any]]:
        """
        获取实体的所有关系（正向 + 反向）。
        
        Args:
            entity_id: 实体 ID
        
        Returns:
            [{"from": ..., "to": ..., "type": ..., "direction": "forward"/"backward"}, ...]
        """
        relations = []
        
        # 正向关系
        for to_id, rel_type in self.relation_forward.get(entity_id, []):
            relations.append({
                "from": entity_id,
                "to": to_id,
                "type": rel_type,
                "direction": "forward"
            })
        
        # 反向关系
        for from_id, rel_type in self.relation_backward.get(entity_id, []):
            relations.append({
                "from": from_id,
                "to": entity_id,
                "type": rel_type,
                "direction": "backward"
            })
        
        return relations
    
    def get_stats(self) -> Dict[str, Any]:
        """获取索引统计"""
        return {
            "entity_types": {k: len(v) for k, v in self.entity_type_index.items()},
            "unique_tags": len(self.tag_index),
            "forward_relations": sum(len(v) for v in self.relation_forward.values()),
            "backward_relations": sum(len(v) for v in self.relation_backward.values())
        }


if __name__ == "__main__":
    # 测试
    import sys
    import tempfile
    from pathlib import Path
    # 添加项目根目录到 path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from storage.knowledge_store import KnowledgeStore
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 先创建一些数据
        store = KnowledgeStore(tmpdir)
        store.add_entity("plc_001", "PLC", {"model": "AM600"},
                         {"source_path": "docs/manual.pdf"}, ["AM600", "PLC"])
        store.add_entity("tpl_001", "CodeTemplate", {"name": "conveyor_control"},
                         {"source_path": "templates/conveyor.st"}, ["AM600", "输送带"])
        store.add_relation("rel_001", "tpl_001", "plc_001", "depends_on")
        
        # 构建索引
        index = IndexManager(tmpdir)
        
        # 按 tag 查询
        results = index.query_by_tags(["AM600"])
        print(f"Query by tag 'AM600': {results}")
        
        # 按实体类型查询
        plc_ids = index.query_by_entity_type("PLC")
        print(f"Query by type 'PLC': {plc_ids}")
        
        # 关系追溯
        relations = index.get_all_relations("tpl_001")
        print(f"Relations for tpl_001: {relations}")
        
        # 统计
        stats = index.get_stats()
        print(f"Index stats: {stats}")
