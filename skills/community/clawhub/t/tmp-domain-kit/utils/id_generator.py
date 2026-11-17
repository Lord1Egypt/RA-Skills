"""
ID 生成器 - MD5 幂等去重
统一 ID 生成：MD5(entity_type + sorted_entity_json + source_path)
"""

import hashlib
import json
from typing import Dict, Any


def generate_entity_id(entity_type: str, entity: Dict[str, Any], source_path: str) -> str:
    """
    生成实体 ID（幂等）。
    
    同一实体来自同一来源 → 相同 ID
    同一实体来自不同来源 → 不同 ID（保留多种描述）
    
    Args:
        entity_type: 实体类型（如 PLC, CodeTemplate）
        entity: 实体数据字典
        source_path: 来源文件路径
    
    Returns:
        32 位 MD5 hash 字符串
    """
    content = {
        "entity_type": entity_type,
        "entity": entity,
        "source_path": source_path
    }
    sorted_json = json.dumps(content, sort_keys=True, ensure_ascii=False)
    return hashlib.md5(sorted_json.encode('utf-8')).hexdigest()


def generate_relation_id(from_id: str, to_id: str, relation_type: str) -> str:
    """
    生成关系 ID（幂等）。
    
    Args:
        from_id: 源实体 ID
        to_id: 目标实体 ID
        relation_type: 关系类型
    
    Returns:
        32 位 MD5 hash 字符串
    """
    content = {
        "from_id": from_id,
        "to_id": to_id,
        "relation_type": relation_type
    }
    sorted_json = json.dumps(content, sort_keys=True, ensure_ascii=False)
    return hashlib.md5(sorted_json.encode('utf-8')).hexdigest()


if __name__ == "__main__":
    # 测试
    entity1 = {"model": "AM600", "cpu_type": "ARM Cortex-A9"}
    id1 = generate_entity_id("PLC", entity1, "docs/AM600_manual.pdf")
    id2 = generate_entity_id("PLC", entity1, "docs/AM600_manual.pdf")
    id3 = generate_entity_id("PLC", entity1, "docs/AM600_manual_v2.pdf")
    
    print(f"Same entity + same source: {id1}")
    print(f"Same entity + same source: {id2}")
    print(f"Same entity + diff source: {id3}")
    print(f"ID1 == ID2 (幂等): {id1 == id2}")
    print(f"ID1 != ID3 (不同来源): {id1 != id3}")
