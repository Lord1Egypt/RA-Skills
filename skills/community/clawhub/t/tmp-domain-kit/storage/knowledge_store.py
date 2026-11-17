"""
知识库存储模块 - JSONL 增量追加写入
支持 entities.jsonl 和 relations.jsonl 的读写
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class KnowledgeStore:
    """知识库存储管理器"""
    
    def __init__(self, storage_path: str):
        """
        Args:
            storage_path: 存储目录路径
        """
        self.storage_path = Path(storage_path)
        self.entities_file = self.storage_path / "entities.jsonl"
        self.relations_file = self.storage_path / "relations.jsonl"
        
        # 确保存储目录存在
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def add_entity(self, entity_id: str, entity_type: str, entity: Dict[str, Any],
                   provenance: Dict[str, Any], tags: List[str]) -> bool:
        """
        添加实体（增量追加）。
        
        Returns:
            True 如果新增，False 如果已存在（幂等）
        """
        # 检查是否已存在
        existing = self.get_entity(entity_id)
        if existing:
            return False
        
        record = {
            "id": entity_id,
            "entity_type": entity_type,
            "entity": entity,
            "provenance": provenance,
            "tags": tags,
            "created_at": datetime.now().isoformat(),
            "version": 1
        }
        
        with open(self.entities_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        return True
    
    def add_relation(self, relation_id: str, from_id: str, to_id: str,
                     relation_type: str, confidence: float = 1.0,
                     provenance: Optional[Dict[str, Any]] = None) -> bool:
        """
        添加关系（增量追加）。
        
        Returns:
            True 如果新增，False 如果已存在（幂等）
        """
        # 检查是否已存在
        existing = self.get_relation(relation_id)
        if existing:
            return False
        
        record = {
            "id": relation_id,
            "from_id": from_id,
            "to_id": to_id,
            "relation_type": relation_type,
            "confidence": confidence,
            "provenance": provenance or {},
            "created_at": datetime.now().isoformat()
        }
        
        with open(self.relations_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        return True
    
    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """根据 ID 获取实体"""
        if not self.entities_file.exists():
            return None
        
        with open(self.entities_file, 'r', encoding='utf-8') as f:
            for line in f:
                record = json.loads(line.strip())
                if record.get('id') == entity_id:
                    return record
        return None
    
    def get_relation(self, relation_id: str) -> Optional[Dict[str, Any]]:
        """根据 ID 获取关系"""
        if not self.relations_file.exists():
            return None
        
        with open(self.relations_file, 'r', encoding='utf-8') as f:
            for line in f:
                record = json.loads(line.strip())
                if record.get('id') == relation_id:
                    return record
        return None
    
    def get_all_entities(self, entity_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取所有实体（可按类型过滤）"""
        if not self.entities_file.exists():
            return []
        
        results = []
        with open(self.entities_file, 'r', encoding='utf-8') as f:
            for line in f:
                record = json.loads(line.strip())
                if entity_type is None or record.get('entity_type') == entity_type:
                    results.append(record)
        return results
    
    def get_all_relations(self, from_id: Optional[str] = None,
                          to_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取所有关系（可按 from_id 或 to_id 过滤）"""
        if not self.relations_file.exists():
            return []
        
        results = []
        with open(self.relations_file, 'r', encoding='utf-8') as f:
            for line in f:
                record = json.loads(line.strip())
                if from_id and record.get('from_id') != from_id:
                    continue
                if to_id and record.get('to_id') != to_id:
                    continue
                results.append(record)
        return results
    
    def get_stats(self) -> Dict[str, int]:
        """获取知识库统计"""
        entity_count = 0
        relation_count = 0
        entity_types = {}
        
        if self.entities_file.exists():
            with open(self.entities_file, 'r', encoding='utf-8') as f:
                for line in f:
                    entity_count += 1
                    record = json.loads(line.strip())
                    etype = record.get('entity_type', 'unknown')
                    entity_types[etype] = entity_types.get(etype, 0) + 1
        
        if self.relations_file.exists():
            with open(self.relations_file, 'r', encoding='utf-8') as f:
                for line in f:
                    relation_count += 1
        
        return {
            "entity_count": entity_count,
            "relation_count": relation_count,
            "entity_types": entity_types
        }


if __name__ == "__main__":
    # 测试
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        store = KnowledgeStore(tmpdir)
        
        # 添加实体
        added1 = store.add_entity(
            entity_id="test_plc_001",
            entity_type="PLC",
            entity={"model": "AM600", "cpu_type": "ARM Cortex-A9"},
            provenance={"source_path": "docs/AM600_manual.pdf"},
            tags=["AM600", "PLC"]
        )
        print(f"Added entity (first time): {added1}")
        
        # 重复添加（幂等）
        added2 = store.add_entity(
            entity_id="test_plc_001",
            entity_type="PLC",
            entity={"model": "AM600", "cpu_type": "ARM Cortex-A9"},
            provenance={"source_path": "docs/AM600_manual.pdf"},
            tags=["AM600", "PLC"]
        )
        print(f"Added entity (duplicate): {added2}")
        
        # 添加关系
        rel_added = store.add_relation(
            relation_id="test_rel_001",
            from_id="test_plc_001",
            to_id="modbus_tcp",
            relation_type="compatible_with"
        )
        print(f"Added relation: {rel_added}")
        
        # 统计
        stats = store.get_stats()
        print(f"Stats: {stats}")
