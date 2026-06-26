#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
lib/utils.py
火种·灵魂 v2.0 - 工具函数库

提供化石管理、文件操作、ID生成等通用工具函数。
"""

import os
import json
import hashlib
import datetime
from typing import List, Dict, Optional
from pathlib import Path

from .extractor import Fossil


def generate_fossil_id(dimension: int) -> str:
    """
    生成唯一化石ID
    
    格式: FOSSIL-{timestamp}-{suffix}
    
    参数:
        dimension: 维度编号
        
    返回:
        唯一ID字符串
    """
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    suffix = hashlib.md5(
        f"{timestamp}{dimension}{os.getpid()}".encode()
    ).hexdigest()[:6]
    return f"FOSSIL-{timestamp}-{suffix}"


def save_fossil(fossil: Fossil, storage_path: str = "user-data/fossils/") -> str:
    """
    保存化石到文件
    
    参数:
        fossil: 化石对象
        storage_path: 存储路径
        
    返回:
        文件路径
    """
    path = Path(storage_path)
    path.mkdir(parents=True, exist_ok=True)
    
    file_path = path / f"{fossil.id}.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fossil.to_json())
    
    return str(file_path)


def load_fossil(file_path: str) -> Optional[Fossil]:
    """
    从文件加载化石
    
    参数:
        file_path: 文件路径
        
    返回:
        化石对象，失败返回 None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return Fossil(**data)
    except Exception as e:
        print(f"加载化石失败: {e}")
        return None


def load_all_fossils(storage_path: str = "user-data/fossils/") -> List[Fossil]:
    """
    加载目录下所有化石
    
    参数:
        storage_path: 存储路径
        
    返回:
        化石列表
    """
    path = Path(storage_path)
    if not path.exists():
        return []
    
    fossils = []
    for file_path in path.glob("*.json"):
        fossil = load_fossil(str(file_path))
        if fossil:
            fossils.append(fossil)
    
    return fossils


def backup_fossils(storage_path: str = "user-data/fossils/",
                  backup_path: str = "user-data/backups/") -> str:
    """
    备份化石数据
    
    参数:
        storage_path: 源路径
        backup_path: 备份路径
        
    返回:
        备份目录路径
    """
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(backup_path) / f"backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    source = Path(storage_path)
    if source.exists():
        import shutil
        for file_path in source.glob("*.json"):
            shutil.copy2(file_path, backup_dir / file_path.name)
    
    return str(backup_dir)


def clean_old_backups(backup_path: str = "user-data/backups/",
                     retention_days: int = 30) -> int:
    """
    清理旧备份
    
    参数:
        backup_path: 备份路径
        retention_days: 保留天数
        
    返回:
        删除的备份数量
    """
    path = Path(backup_path)
    if not path.exists():
        return 0
    
    cutoff = datetime.datetime.now() - datetime.timedelta(days=retention_days)
    deleted = 0
    
    for backup_dir in path.glob("backup_*"):
        # 从目录名提取时间戳
        try:
            timestamp_str = backup_dir.name.replace("backup_", "")
            backup_time = datetime.datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            
            if backup_time < cutoff:
                import shutil
                shutil.rmtree(backup_dir)
                deleted += 1
        except ValueError:
            continue
    
    return deleted


def export_fossils_to_csv(fossils: List[Fossil], output_path: str) -> str:
    """
    导出化石为 CSV 格式
    
    参数:
        fossils: 化石列表
        output_path: 输出文件路径
        
    返回:
        输出文件路径
    """
    import csv
    
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # 写入表头
        writer.writerow([
            "ID", "Dimension", "Subdimension", "Content",
            "Timestamp", "Confidence", "Tags"
        ])
        
        # 写入数据
        for fossil in fossils:
            writer.writerow([
                fossil.id,
                fossil.dimension,
                fossil.subdimension,
                fossil.content,
                fossil.timestamp,
                fossil.confidence,
                ", ".join(fossil.tags)
            ])
    
    return output_path


def get_storage_stats(storage_path: str = "user-data/fossils/") -> Dict:
    """
    获取存储统计信息
    
    参数:
        storage_path: 存储路径
        
    返回:
        统计信息字典
    """
    path = Path(storage_path)
    if not path.exists():
        return {
            "total_fossils": 0,
            "dimensions": {},
            "avg_confidence": 0.0,
            "storage_size_mb": 0.0
        }
    
    fossils = load_all_fossils(storage_path)
    
    # 按维度统计
    dim_counts = {}
    for fossil in fossils:
        dim_name = f"dimension_{fossil.dimension}"
        dim_counts[dim_name] = dim_counts.get(dim_name, 0) + 1
    
    # 平均置信度
    avg_confidence = (
        sum(f.confidence for f in fossils) / len(fossils)
        if fossils else 0.0
    )
    
    # 存储空间
    total_size = sum(f.stat().st_size for f in path.glob("*.json"))
    storage_size_mb = total_size / (1024 * 1024)
    
    return {
        "total_fossils": len(fossils),
        "dimensions": dim_counts,
        "avg_confidence": round(avg_confidence, 2),
        "storage_size_mb": round(storage_size_mb, 2)
    }


def validate_fossil_structure(data: Dict) -> bool:
    """
    验证化石数据结构是否完整
    
    参数:
        data: 化石数据字典
        
    返回:
        是否有效
    """
    required_fields = [
        "id", "dimension", "subdimension", "content",
        "timestamp", "confidence"
    ]
    
    for field in required_fields:
        if field not in data:
            return False
    
    # 类型检查
    if not isinstance(data["dimension"], int):
        return False
    
    if not (0.0 <= data["confidence"] <= 1.0):
        return False
    
    return True
