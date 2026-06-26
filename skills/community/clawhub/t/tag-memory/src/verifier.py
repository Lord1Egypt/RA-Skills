#!/usr/bin/env python3
"""
TagMemory - 闲时核对模块
定期检查存储的记忆，主动向用户确认
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database import MemoryDatabase, Memory


@dataclass
class VerificationResult:
    memory_id: str
    memory_content: str
    verification_type: str  # "recent_store" / "periodic" / "search_result"
    status: str  # "pending" / "confirmed" / "corrected" / "deleted"
    corrected_content: Optional[str] = None
    verified_at: Optional[str] = None


class MemoryVerifier:
    """
    闲时核对模块
    
    职责：
    1. 新存储后核对 - 隔一段时间询问是否正确
    2. 搜索结果核对 - 检查返回结果是否相关
    3. 周期审核 - 每周全面检查所有记忆
    """
    
    def __init__(self, db: MemoryDatabase = None):
        self.db = db or MemoryDatabase()
        
        # 核对配置
        self.config = {
            "verify_after_store_delay": 300,  # 存储后 5 分钟询问
            "verify_sample_ratio": 0.1,  # 每次审核 10% 的记忆
            "verify_min_interval": 3600,  # 同一记忆至少隔 1 小时再问
            "max_verifications_per_session": 3,  # 每次最多问 3 个
        }
        
        # 上次核对时间记录 (memory_id -> timestamp)
        self._last_verification = {}
    
    def should_verify(self, memory: Memory) -> bool:
        """
        判断是否应该核对某条记忆
        """
        memory_id = memory.id
        
        # 如果从未核对过，需要核对
        if memory_id not in self._last_verification:
            return True
        
        # 检查是否过了最小间隔
        last_time = self._last_verification[memory_id]
        last_dt = datetime.fromisoformat(last_time) if isinstance(last_time, str) else last_time
        
        if (datetime.now() - last_dt).total_seconds() < self.config["verify_min_interval"]:
            return False
        
        # 随机采样（避免每次都问）
        if random.random() > self.config["verify_sample_ratio"]:
            return False
        
        return True
    
    def get_unverified_memories(self, limit: int = 10) -> List[Memory]:
        """
        获取未确认的记忆（用于核对）
        """
        all_memories = self.db.get_all(limit=100)
        
        candidates = []
        for m in all_memories:
            if not m.verified and self.should_verify(m):
                candidates.append(m)
        
        return candidates[:limit]
    
    def get_recent_stored_memories(self, hours: int = 24) -> List[Memory]:
        """
        获取最近存储的记忆（优先核对）
        """
        all_memories = self.db.get_all(limit=100)
        recent_threshold = datetime.now() - timedelta(hours=hours)
        
        recent = []
        for m in all_memories:
            created = datetime.fromisoformat(m.created_at)
            if created > recent_threshold:
                recent.append(m)
        
        return recent
    
    def generate_verification_question(self, memory: Memory) -> str:
        """
        为记忆生成核对问题
        """
        # 根据标签生成不同的问题模板
        tags = memory.tags
        
        if "#偏好" in tags:
            templates = [
                f"刚才我记录了「{memory.content[:50]}...」，这对吗？",
                f"我记下说你{memory.content[:30]}...，对吗？",
            ]
        elif "#决定" in tags:
            templates = [
                f"我记得你{memory.content[:40]}...，确认一下？",
                f"关于{memory.content[:30]}...，这个决定还正确吗？",
            ]
        elif "#项目" in tags:
            templates = [
                f"关于{memory.content[:40]}...，情况有变化吗？",
                f"我记录说{memory.content[:30]}...，项目进展如何？",
            ]
        else:
            templates = [
                f"我记录了「{memory.content[:50]}...」，这对吗？",
                f"你之前说过{memory.content[:40]}...，现在还这样吗？",
            ]
        
        return random.choice(templates)
    
    def get_pending_verifications(self, max_count: int = 3) -> List[Dict]:
        """
        获取待核对的列表（用于展示给用户）
        
        Returns:
            List of {
                "memory_id": str,
                "question": str,
                "content": str,
                "tags": List[str],
                "time_label": str
            }
        """
        # 优先检查最近存储的
        recent = self.get_recent_stored_memories(hours=24)
        candidates = recent[:max_count]
        
        # 如果不够，用随机采样补充
        if len(candidates) < max_count:
            unverified = self.get_unverified_memories(limit=max_count - len(candidates))
            for m in unverified:
                if m not in candidates:
                    candidates.append(m)
        
        results = []
        for m in candidates[:max_count]:
            self._last_verification[m.id] = datetime.now().isoformat()
            results.append({
                "memory_id": m.id,
                "question": self.generate_verification_question(m),
                "content": m.content,
                "tags": m.tags,
                "time_label": m.time_label,
                "created_at": m.created_at
            })
        
        return results
    
    def record_verification_result(self, memory_id: str, result: str, 
                                   correction: str = None) -> Dict:
        """
        记录核对结果
        
        Args:
            memory_id: 记忆 ID
            result: "confirm" / "correct" / "delete"
            correction: 修正内容（如果是 correct）
        """
        if result == "confirm":
            self.db.update(memory_id, {
                "verified": True,
                "verified_at": datetime.now().isoformat()
            })
            return {
                "success": True,
                "message": "✅ 已确认，这条记忆正确"
            }
        
        elif result == "correct":
            if not correction:
                return {"success": False, "error": "修正内容不能为空"}
            
            self.db.update(memory_id, {
                "content": correction,
                "verified": False,
                "updated_at": datetime.now().isoformat()
            })
            return {
                "success": True,
                "message": f"✏️ 已修正记忆"
            }
        
        elif result == "delete":
            self.db.delete(memory_id)
            return {
                "success": True,
                "message": "🗑️ 已删除记忆"
            }
        
        else:
            return {"success": False, "error": f"未知结果: {result}"}
    
    def periodic_audit(self) -> Dict:
        """
        执行周期性审核
        返回审核报告
        """
        all_memories = self.db.get_all(limit=1000)
        total = len(all_memories)
        verified = sum(1 for m in all_memories if m.verified)
        unverified = total - verified
        
        # 需要核对的记忆
        needs_verification = [m for m in all_memories if not m.verified]
        
        # 按标签统计
        tag_stats = {}
        for m in all_memories:
            for tag in m.tags:
                tag_stats[tag] = tag_stats.get(tag, 0) + 1
        
        return {
            "success": True,
            "report": {
                "total_memories": total,
                "verified": verified,
                "unverified": unverified,
                "verification_rate": f"{verified/total*100:.1f}%" if total > 0 else "0%",
                "needs_verification": len(needs_verification),
                "tag_distribution": tag_stats,
                "audit_time": datetime.now().isoformat()
            },
            "message": self._format_audit_report(total, verified, unverified, tag_stats)
        }
    
    def _format_audit_report(self, total: int, verified: int, 
                            unverified: int, tag_stats: Dict) -> str:
        """格式化审核报告"""
        lines = [
            "📊 **闲时审核报告**",
            "",
            f"- 总记忆数: {total}",
            f"- ✅ 已确认: {verified} ({verified/total*100:.1f}%" if total > 0 else "- ✅ 已确认: 0",
            f"- ❓ 待确认: {unverified}",
            "",
        ]
        
        if tag_stats:
            lines.append("🏷️ **标签分布:**")
            for tag, count in sorted(tag_stats.items(), key=lambda x: -x[1])[:5]:
                lines.append(f"  - {tag}: {count}")
        
        if unverified > 0:
            lines.append("")
            lines.append(f"💡 有 {unverified} 条记忆待确认，可以让我帮你核对吗？")
        
        return "\n".join(lines)
    
    def verify_search_relevance(self, memory_id: str, query: str, 
                               search_score: float) -> bool:
        """
        验证搜索结果是否相关
        这个用于后台检查，不需要用户参与
        """
        memory = self.db.get(memory_id)
        if not memory:
            return False
        
        # 简单规则：如果 BM25 score > 0，认为相关
        # 更复杂的可以用 LLM 判断
        return search_score > 0


# ==================== CLI 入口 ====================

if __name__ == "__main__":
    verifier = MemoryVerifier()
    
    print("🔍 TagMemory 闲时核对模块")
    print("=" * 40)
    
    # 周期性审核
    print("\n📊 执行周期性审核...\n")
    result = verifier.periodic_audit()
    print(result["message"])
    
    # 待核对列表
    print("\n❓ 待核对记忆:")
    pending = verifier.get_pending_verifications(max_count=3)
    if pending:
        for i, p in enumerate(pending, 1):
            print(f"\n{i}. {p['question']}")
            print(f"   内容: {p['content'][:60]}...")
    else:
        print("  暂无待核对记忆 ✅")
    
    # 模拟确认
    if pending:
        print(f"\n📝 模拟确认第 1 条...")
        result = verifier.record_verification_result(
            pending[0]["memory_id"], 
            "confirm"
        )
        print(result["message"])
