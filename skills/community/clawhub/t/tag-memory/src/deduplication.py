#!/usr/bin/env python3
"""
TagMemory - 数据去重模块
处理 TagMemory 与 LCM 之间的数据重复问题
"""

import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Set
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database import MemoryDatabase, Memory


class DeduplicationManager:
    """
    数据去重管理器
    
    职责：
    1. 检测 TagMemory 与 LCM 之间的重复内容
    2. 避免重复存储相似内容
    3. 提供存储前的重复检查
    """
    
    def __init__(self, db: MemoryDatabase = None):
        self.db = db or MemoryDatabase()
        
        # 简单哈希集合，用于快速检测
        self._content_hash_cache: Set[str] = set()
        self._load_existing_hashes()
    
    def _load_existing_hashes(self):
        """加载现有记忆的哈希到缓存"""
        memories = self.db.get_all(limit=1000)
        for m in memories:
            h = self._hash_content(m.content)
            self._content_hash_cache.add(h)
    
    def _hash_content(self, content: str) -> str:
        """生成内容哈希"""
        # 简化：取前100字符的MD5
        normalized = content[:100].strip().lower()
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def _normalize_for_comparison(self, content: str) -> str:
        """标准化内容用于比较"""
        # 移除多余空格、转小写
        return " ".join(content.split()).lower()
    
    def is_duplicate(self, content: str, threshold: float = 0.8) -> Dict:
        """
        检查内容是否重复
        
        Args:
            content: 要检查的内容
            threshold: 相似度阈值 (0-1)
        
        Returns:
            {
                "is_duplicate": bool,
                "similar_memories": [...],
                "best_match": {...}
            }
        """
        normalized = self._normalize_for_comparison(content)
        normalized_hash = self._hash_content(content)
        
        # 检查完全匹配
        if normalized_hash in self._content_hash_cache:
            return {
                "is_duplicate": True,
                "reason": "exact_match",
                "similar_memories": [],
                "best_match": None
            }
        
        # 检查相似内容
        all_memories = self.db.get_all(limit=100)
        best_match = None
        best_score = 0.0
        
        for m in all_memories:
            if m.verified:
                # 只检查已确认的记忆，避免重复存储
                similarity = self._calculate_similarity(normalized, m.content)
                if similarity > best_score:
                    best_score = similarity
                    best_match = {
                        "id": m.id,
                        "content": m.content,
                        "similarity": similarity,
                        "verified": m.verified
                    }
        
        if best_score >= threshold:
            return {
                "is_duplicate": True,
                "reason": f"similar ({best_score:.1%})",
                "similar_memories": [best_match] if best_match else [],
                "best_match": best_match
            }
        
        return {
            "is_duplicate": False,
            "reason": None,
            "similar_memories": [],
            "best_match": None
        }
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的相似度
        使用简单的词集合重叠率
        """
        # 分词
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        # Jaccard 相似度
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def should_store(self, content: str, tags: List[str] = None,
                    force: bool = False) -> Dict:
        """
        判断是否应该存储
        
        规则：
        1. 已确认的记忆不重复存储
        2. 未确认的记忆可以覆盖
        3. force=True 时强制存储
        """
        if force:
            return {
                "should_store": True,
                "reason": "force",
                "action": "store"
            }
        
        dup_check = self.is_duplicate(content)
        
        if dup_check["is_duplicate"]:
            if dup_check["reason"] == "exact_match":
                return {
                    "should_store": False,
                    "reason": "完全匹配，已存在",
                    "existing_memory": dup_check["best_match"],
                    "action": "skip"
                }
            else:
                # 高度相似但不完全相同
                return {
                    "should_store": True,
                    "reason": f"相似但有新内容 ({dup_check['best_match']['similarity']:.1%})",
                    "existing_memory": dup_check["best_match"],
                    "action": "update"
                }
        
        return {
            "should_store": True,
            "reason": "新内容",
            "existing_memory": None,
            "action": "store"
        }
    
    def smart_store(self, content: str, tags: List[str] = None,
                   time_label: str = None, source: str = "dialogue",
                   force: bool = False) -> Dict:
        """
        智能存储 - 自动处理去重
        """
        # 先检查是否应该存储
        should = self.should_store(content, tags, force)
        
        if not should["should_store"] and not force:
            return {
                "success": True,
                "stored": False,
                "action": should["action"],
                "message": f"⏭️ {should['reason']}，跳过存储",
                "existing_memory": should.get("existing_memory")
            }
        
        # 如果是更新，先删除旧的
        if should["action"] == "update" and should.get("existing_memory"):
            old_id = should["existing_memory"]["id"]
            self.db.delete(old_id)
        
        # 存储新内容
        memory = Memory(
            id="",
            content=content,
            tags=tags or [],
            time_label=time_label or datetime.now().strftime("%Y-%m"),
            source=source
        )
        
        memory_id = self.db.insert(memory)
        
        # 更新缓存
        h = self._hash_content(content)
        self._content_hash_cache.add(h)
        
        return {
            "success": True,
            "stored": True,
            "action": "stored" if should["action"] == "store" else "updated",
            "memory_id": memory_id,
            "message": f"✅ 记忆{'更新' if should['action'] == 'update' else '存储'}成功",
            "was_similar_to": should.get("existing_memory")
        }
    
    def get_storage_stats(self) -> Dict:
        """获取存储统计"""
        all_memories = self.db.get_all(limit=1000)
        
        verified = sum(1 for m in all_memories if m.verified)
        unverified = len(all_memories) - verified
        
        # 按标签统计
        tag_counts = {}
        for m in all_memories:
            for tag in m.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        return {
            "total": len(all_memories),
            "verified": verified,
            "unverified": unverified,
            "tag_distribution": tag_counts
        }


# ==================== 与 LCM 协同 ====================

class LCMIntegration:
    """
    LCM 协同模块
    
    目的：避免 TagMemory 和 LCM 存储完全相同的内容
    
    原理：
    - LCM 自动压缩对话存储
    - TagMemory 只存储用户标记的重要信息
    - 用户说"记住..."时，只存 TagMemory，不存 LCM 的摘要里
    """
    
    def __init__(self, db: MemoryDatabase = None):
        self.db = db or MemoryDatabase()
        self.dedup = DeduplicationManager(db)
    
    def extract_user_intent_to_remember(self, user_message: str) -> Optional[str]:
        """
        从用户消息中提取需要记忆的内容
        
        检测模式：
        - "记住..." 
        - "我一直..."
        - "我偏好..."
        - "我决定..."
        """
        message = user_message.strip()
        
        # 明确的记忆请求
        patterns = [
            (r"记住[，,](.+)", "direct"),
            (r"我一直(.+)", "ongoing"),
            (r"我偏好(.+)", "preference"),
            (r"我决定(.+)", "decision"),
            (r"我喜欢(.+)", "preference"),
            (r"我选择(.+)", "decision"),
        ]
        
        for pattern, intent_type in patterns:
            import re
            match = re.search(pattern, message)
            if match:
                content = match.group(1).strip()
                return content
        
        return None
    
    def auto_tag(self, content: str) -> List[str]:
        """
        自动为内容打标签
        
        简单规则匹配
        """
        tags = []
        
        # 偏好相关
        preference_keywords = ["喜欢", "偏好", "习惯", "一直", "总是", "从不"]
        if any(kw in content for kw in preference_keywords):
            tags.append("#偏好")
        
        # 决定相关
        decision_keywords = ["决定", "选择", "选了", "要用", "采用", "采用"]
        if any(kw in content for kw in decision_keywords):
            tags.append("#决定")
        
        # 项目相关
        project_keywords = ["项目", "在做", "开发", "正在", "项目是"]
        if any(kw in content for kw in project_keywords):
            tags.append("#项目")
        
        # 人相关
        person_keywords = ["是张三", "李四", "王五", "经理", "同事", "老板"]
        if any(kw in content for kw in person_keywords):
            tags.append("#人")
        
        # 事件相关
        event_keywords = ["发生了", "上次", "昨天", "那天", "之前"]
        if any(kw in content for kw in event_keywords):
            tags.append("#事件")
        
        # 知识相关
        knowledge_keywords = ["学会了", "学到", "知道了", "明白了", "理解"]
        if any(kw in content for kw in knowledge_keywords):
            tags.append("#知识")
        
        # 错误相关
        error_keywords = ["错了", "不对", "失败", "后悔", "不应该"]
        if any(kw in content for kw in error_keywords):
            tags.append("#错误")
        
        # 默认标签
        if not tags:
            tags.append("#其他")
        
        return tags


if __name__ == "__main__":
    dedup = DeduplicationManager()
    
    print("🔍 TagMemory 去重测试")
    print("=" * 40)
    
    # 测试重复检测
    print("\n📝 测试 1: 完全重复")
    result = dedup.is_duplicate("用户选择了 PostgreSQL 而不是 MongoDB")
    print(f"结果: {result}")
    
    print("\n📝 测试 2: 相似内容")
    result = dedup.is_duplicate("用户选了 PostgreSQL 而不是 MongoDB，因为性能好")
    print(f"结果: {result}")
    
    print("\n📝 测试 3: 新内容")
    result = dedup.is_duplicate("用户喜欢用 tabs 缩进")
    print(f"结果: {result}")
    
    # 测试智能存储
    print("\n📝 测试 4: 智能存储")
    result = dedup.smart_store(
        "用户喜欢用 tabs 缩进",
        tags=["#偏好"],
        force=False
    )
    print(f"结果: {result}")
    
    # 测试 LCM 协同
    print("\n📝 测试 5: LCM 协同 - 提取记忆意图")
    lcm = LCMIntegration()
    
    test_messages = [
        "记住，我喜欢用 tabs 缩进",
        "我决定使用 PostgreSQL 数据库",
        "我一直用 Docker 开发",
        "今天天气不错",
    ]
    
    for msg in test_messages:
        intent = lcm.extract_user_intent_to_remember(msg)
        if intent:
            tags = lcm.auto_tag(intent)
            print(f"  '{msg}' → 记忆: '{intent}' | 标签: {tags}")
        else:
            print(f"  '{msg}' → 不需要记忆")
