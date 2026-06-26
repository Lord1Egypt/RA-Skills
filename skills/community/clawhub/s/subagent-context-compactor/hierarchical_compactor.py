#!/usr/bin/env python3
"""
分层压缩策略实现
HOT/WARM/COLD三层数据管理
"""

import json
import time
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import hashlib
import re
from dataclasses import dataclass
from enum import Enum

class Tier(Enum):
    """数据分层"""
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"

class CompressionMethod(Enum):
    """压缩方法"""
    SUMMARIZATION = "summarization"
    KEYWORD_EXTRACTION = "keyword_extraction"
    ARCHIVAL = "archival"

@dataclass
class ContextItem:
    """上下文项"""
    content: str
    timestamp: str
    source: str
    importance: float = 0.5
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def id(self) -> str:
        """生成唯一ID"""
        content_hash = hashlib.md5(self.content.encode()).hexdigest()
        return f"{self.timestamp}_{content_hash[:8]}"
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "content": self.content,
            "timestamp": self.timestamp,
            "source": self.source,
            "importance": self.importance,
            "metadata": self.metadata
        }

class HierarchicalCompactor:
    """分层压缩器"""
    
    def __init__(self, config_path: str = None):
        """初始化"""
        self.config = self.load_config(config_path)
        self.db_path = "context_compactor.db"
        self.init_database()
    
    def load_config(self, config_path: str = None) -> Dict:
        """加载配置"""
        default_config = {
            "tiers": {
                "hot": {
                    "retention_days": 1,
                    "max_items": 20,
                    "importance_threshold": 0.7
                },
                "warm": {
                    "retention_days": 7,
                    "max_items": 100,
                    "importance_threshold": 0.4
                },
                "cold": {
                    "retention_days": 30,
                    "max_items": 500,
                    "importance_threshold": 0.2
                }
            },
            "compression_methods": {
                "summarization": {"max_length_ratio": 0.3},
                "keyword_extraction": {"max_keywords": 10},
                "archival": {"format": "jsonl"}
            }
        }
        
        if config_path:
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    # 合并配置
                    default_config.update(user_config)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
        
        return default_config
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建压缩历史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compaction_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                tier TEXT NOT NULL,
                trigger_type TEXT NOT NULL,
                items_before INTEGER NOT NULL,
                items_after INTEGER NOT NULL,
                tokens_before INTEGER NOT NULL,
                tokens_after INTEGER NOT NULL,
                compression_ratio REAL NOT NULL,
                details TEXT
            )
        ''')
        
        # 创建分层数据表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tiered_data (
                id TEXT PRIMARY KEY,
                tier TEXT NOT NULL,
                content TEXT NOT NULL,
                compressed_content TEXT,
                original_length INTEGER NOT NULL,
                compressed_length INTEGER,
                importance_score REAL NOT NULL,
                timestamp TEXT NOT NULL,
                source TEXT NOT NULL,
                metadata TEXT,
                created_at TEXT NOT NULL,
                last_accessed TEXT NOT NULL
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tier ON tiered_data (tier)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON tiered_data (timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_importance ON tiered_data (importance_score)')
        
        conn.commit()
        conn.close()
    
    def calculate_importance(self, item: ContextItem) -> float:
        """计算内容重要性"""
        importance = item.importance  # 基础重要性
        
        # 基于内容特征调整
        content = item.content.lower()
        
        # 决策相关
        if any(keyword in content for keyword in ["决定", "选择", "采用", "使用", "配置"]):
            importance += 0.2
        
        # 任务相关
        if any(keyword in content for keyword in ["任务", "完成", "需要", "必须", "重要"]):
            importance += 0.15
        
        # 偏好相关
        if any(keyword in content for keyword in ["喜欢", "偏好", "习惯", "通常", "总是"]):
            importance += 0.1
        
        # 错误相关
        if any(keyword in content for keyword in ["错误", "失败", "问题", "修复", "解决"]):
            importance += 0.15
        
        # 限制在0-1之间
        return max(0.0, min(1.0, importance))
    
    def assign_tier(self, item: ContextItem) -> Tier:
        """分配数据层"""
        importance = self.calculate_importance(item)
        
        tier_config = self.config["tiers"]
        
        if importance >= tier_config["hot"]["importance_threshold"]:
            return Tier.HOT
        elif importance >= tier_config["warm"]["importance_threshold"]:
            return Tier.WARM
        else:
            return Tier.COLD
    
    def compress_content(self, content: str, method: CompressionMethod) -> Tuple[str, float]:
        """压缩内容"""
        if method == CompressionMethod.SUMMARIZATION:
            return self.summarize_content(content)
        elif method == CompressionMethod.KEYWORD_EXTRACTION:
            return self.extract_keywords(content)
        elif method == CompressionMethod.ARCHIVAL:
            return content, 1.0  # 归档不压缩内容
        else:
            return content, 1.0
    
    def summarize_content(self, content: str) -> Tuple[str, float]:
        """总结内容"""
        # 简单实现：提取关键句子
        sentences = re.split(r'[。！？!?]', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= 3:
            return content, 1.0
        
        # 选择前3个句子作为总结
        summary = "。".join(sentences[:3]) + "。"
        compression_ratio = len(summary) / len(content)
        
        return summary, compression_ratio
    
    def extract_keywords(self, content: str) -> Tuple[str, float]:
        """提取关键词"""
        # 简单实现：提取高频词
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', content)
        
        if not words:
            return content, 1.0
        
        # 统计词频
        from collections import Counter
        word_counts = Counter(words)
        
        # 获取前5个关键词
        keywords = [word for word, _ in word_counts.most_common(5)]
        
        # 构建关键词摘要
        summary = f"关键词: {', '.join(keywords)}"
        
        # 添加上下文片段
        if len(content) > 50:
            summary += f" | 上下文: {content[:50]}..."
        
        compression_ratio = len(summary) / len(content)
        
        return summary, compression_ratio
    
    def process_item(self, item: ContextItem) -> Dict:
        """处理单个项"""
        tier = self.assign_tier(item)
        tier_config = self.config["tiers"][tier.value]
        
        # 确定压缩方法
        if tier == Tier.HOT:
            method = CompressionMethod.SUMMARIZATION
        elif tier == Tier.WARM:
            method = CompressionMethod.KEYWORD_EXTRACTION
        else:
            method = CompressionMethod.ARCHIVAL
        
        # 压缩内容
        compressed_content, compression_ratio = self.compress_content(
            item.content, method
        )
        
        # 准备存储数据
        result = {
            "id": item.id,
            "tier": tier.value,
            "content": item.content,
            "compressed_content": compressed_content,
            "original_length": len(item.content),
            "compressed_length": len(compressed_content),
            "importance_score": self.calculate_importance(item),
            "timestamp": item.timestamp,
            "source": item.source,
            "metadata": json.dumps(item.metadata, ensure_ascii=False),
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat()
        }
        
        return result
    
    def store_item(self, item_data: Dict):
        """存储项到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO tiered_data 
                (id, tier, content, compressed_content, original_length, 
                 compressed_length, importance_score, timestamp, source, 
                 metadata, created_at, last_accessed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item_data["id"],
                item_data["tier"],
                item_data["content"],
                item_data["compressed_content"],
                item_data["original_length"],
                item_data["compressed_length"],
                item_data["importance_score"],
                item_data["timestamp"],
                item_data["source"],
                item_data["metadata"],
                item_data["created_at"],
                item_data["last_accessed"]
            ))
            
            conn.commit()
            
        except Exception as e:
            print(f"存储项失败: {e}")
            conn.rollback()
        
        finally:
            conn.close()
    
    def cleanup_tier(self, tier: Tier):
        """清理层级数据"""
        tier_config = self.config["tiers"][tier.value]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 检查数量限制
            cursor.execute(
                'SELECT COUNT(*) FROM tiered_data WHERE tier = ?',
                (tier.value,)
            )
            count = cursor.fetchone()[0]
            
            if count > tier_config["max_items"]:
                # 按重要性排序，删除重要性最低的
                cursor.execute('''
                    SELECT id FROM tiered_data 
                    WHERE tier = ? 
                    ORDER BY importance_score ASC, timestamp ASC
                    LIMIT ?
                ''', (tier.value, count - tier_config["max_items"]))
                
                ids_to_delete = [row[0] for row in cursor.fetchall()]
                
                if ids_to_delete:
                    placeholders = ','.join(['?'] * len(ids_to_delete))
                    cursor.execute(
                        f'DELETE FROM tiered_data WHERE id IN ({placeholders})',
                        ids_to_delete
                    )
            
            # 检查时间限制
            retention_days = tier_config["retention_days"]
            cutoff_date = (datetime.now() - timedelta(days=retention_days)).isoformat()
            
            cursor.execute('''
                DELETE FROM tiered_data 
                WHERE tier = ? AND timestamp < ?
            ''', (tier.value, cutoff_date))
            
            conn.commit()
            
            deleted_count = cursor.rowcount
            if deleted_count > 0:
                print(f"清理{tier.value}层: 删除了{deleted_count}条过期数据")
            
        except Exception as e:
            print(f"清理{tier.value}层失败: {e}")
            conn.rollback()
        
        finally:
            conn.close()
    
    def compact(self, items: List[ContextItem], trigger_type: str = "manual") -> Dict:
        """执行压缩"""
        print(f"开始压缩，触发类型: {trigger_type}")
        print(f"处理项目数: {len(items)}")
        
        start_time = time.time()
        items_before = len(items)
        tokens_before = sum(len(item.content) for item in items)
        
        # 处理每个项目
        processed_items = []
        for item in items:
            item_data = self.process_item(item)
            self.store_item(item_data)
            processed_items.append(item_data)
        
        # 清理各层数据
        for tier in Tier:
            self.cleanup_tier(tier)
        
        # 计算压缩结果
        items_after = len(processed_items)
        tokens_after = sum(item["compressed_length"] for item in processed_items)
        
        if tokens_before > 0:
            compression_ratio = tokens_after / tokens_before
        else:
            compression_ratio = 1.0
        
        # 记录压缩历史
        self.record_compaction_history(
            trigger_type=trigger_type,
            items_before=items_before,
            items_after=items_after,
            tokens_before=tokens_before,
            tokens_after=tokens_after,
            compression_ratio=compression_ratio
        )
        
        processing_time = time.time() - start_time
        
        result = {
            "success": True,
            "processing_time": processing_time,
            "stats": {
                "items_before": items_before,
                "items_after": items_after,
                "tokens_before": tokens_before,
                "tokens_after": tokens_after,
                "compression_ratio": compression_ratio,
                "tokens_saved": tokens_before - tokens_after
            },
            "tier_distribution": self.get_tier_distribution(),
            "trigger_type": trigger_type
        }
        
        print(f"压缩完成，用时: {processing_time:.2f}秒")
        print(f"压缩率: {compression_ratio:.2%}")
        print(f"节省Token: {tokens_before - tokens_after}")
        
        return result
    
    def record_compaction_history(self, **kwargs):
        """记录压缩历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO compaction_history 
                (timestamp, tier, trigger_type, items_before, items_after, 
                 tokens_before, tokens_after, compression_ratio, details)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                "all",  # 记录整体压缩
                kwargs.get("trigger_type", "unknown"),
                kwargs.get("items_before", 0),
                kwargs.get("items_after", 0),
                kwargs.get("tokens_before", 0),
                kwargs.get("tokens_after", 0),
                kwargs.get("compression_ratio", 1.0),
                json.dumps(kwargs, ensure_ascii=False)
            ))
            
            conn.commit()
            
        except Exception as e:
            print(f"记录压缩历史失败: {e}")
            conn.rollback()
        
        finally:
            conn.close()
    
    def get_tier_distribution(self) -> Dict:
        """获取层级分布"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        distribution = {}
        
        try:
            cursor.execute('''
                SELECT tier, COUNT(*), AVG(importance_score), 
                       SUM(original_length), SUM(compressed_length)
                FROM tiered_data 
                GROUP BY tier
            ''')
            
            for row in cursor.fetchall():
                tier, count, avg_importance, total_original, total_compressed = row
                distribution[tier] = {
                    "count": count,
                    "avg_importance": avg_importance or 0,
                    "total_original_length": total_original or 0,
                    "total_compressed_length": total_compressed or 0
                }
        
        except Exception as e:
            print(f"获取层级分布失败: {e}")
        
        finally:
            conn.close()
        
        return distribution
    
    def get_status_report(self) -> Dict:
        """获取状态报告"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "database": {
                "path": self.db_path
            },
            "tiers": {},
            "compaction_history": {}
        }
        
        try:
            # 获取各层统计
            for tier in Tier:
                cursor.execute(
                    'SELECT COUNT(*) FROM tiered_data WHERE tier = ?',
                    (tier.value,)
                )
                count = cursor.fetchone()[0]
                
                cursor.execute('''
                    SELECT AVG(importance_score), 
                           SUM(original_length), 
                           SUM(compressed_length)
                    FROM tiered_data WHERE tier = ?
                ''', (tier.value,))
                
                row = cursor.fetchone()
                avg_importance, total_original, total_compressed = row
                
                report["tiers"][tier.value] = {
                    "count": count,
                    "avg_importance": avg_importance or 0,
                    "total_original_length": total_original or 0,
                    "total_compressed_length": total_compressed or 0
                }
            
            # 获取压缩历史
            cursor.execute('''
                SELECT COUNT(*), 
                       SUM(tokens_before - tokens_after) as total_saved,
                       AVG(compression_ratio) as avg_ratio
                FROM compaction_history
            ''')
            
            row = cursor.fetchone()
            report["compaction_history"] = {
                "total_compactions": row[0] or 0,
                "total_tokens_saved": row[1] or 0,
                "avg_compression_ratio": row[2] or 0
            }
            
            # 获取最新压缩
            cursor.execute('''
                SELECT timestamp, trigger_type, compression_ratio, tokens_before - tokens_after
                FROM compaction_history 
                ORDER