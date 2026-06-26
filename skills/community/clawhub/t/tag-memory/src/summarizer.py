#!/usr/bin/env python3
"""
TagMemory - 定期归纳模块
分析对话内容，生成结构化总结，主动询问用户确认
"""

import json
import re
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from database import MemoryDatabase, Memory


@dataclass
class SummaryDraft:
    """总结草稿"""
    period: str  # 时间段，如 "2026-03-23 ~ 2026-03-30"
    decisions: List[str]  # 决定
    preferences: List[str]  # 偏好
    projects: List[str]  # 项目
    learned: List[str]  # 学到的
    events: List[str]  # 事件
    issues: List[str]  # 问题/错误
    other: List[str]  # 其他
    verified: bool = False
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        d = asdict(self)
        d['verified'] = self.verified
        return d
    
    def format_for_display(self) -> str:
        """格式化展示给用户"""
        lines = [
            f"📊 **阶段性总结** ({self.period})",
            "",
        ]
        
        if self.decisions:
            lines.append("### ✅ 决定")
            for d in self.decisions:
                lines.append(f"- {d}")
            lines.append("")
        
        if self.preferences:
            lines.append("### 💡 偏好")
            for p in self.preferences:
                lines.append(f"- {p}")
            lines.append("")
        
        if self.projects:
            lines.append("### 📁 项目")
            for p in self.projects:
                lines.append(f"- {p}")
            lines.append("")
        
        if self.learned:
            lines.append("### 📚 学到的")
            for l in self.learned:
                lines.append(f"- {l}")
            lines.append("")
        
        if self.events:
            lines.append("### 📅 事件")
            for e in self.events:
                lines.append(f"- {e}")
            lines.append("")
        
        if self.issues:
            lines.append("### ⚠️ 问题/错误")
            for i in self.issues:
                lines.append(f"- {i}")
            lines.append("")
        
        if self.other:
            lines.append("### 📝 其他")
            for o in self.other:
                lines.append(f"- {o}")
            lines.append("")
        
        lines.append("---")
        lines.append("这对吗？回复「确认」存档，或告诉我需要修改的地方。")
        
        return "\n".join(lines)


class MemorySummarizer:
    """
    定期归纳模块
    
    职责：
    1. 分析近期对话/记忆
    2. 按标签分类整理
    3. 生成结构化总结
    4. 询问用户确认
    5. 确认后存档为新记忆
    """
    
    # 标签到分类的映射
    TAG_CATEGORY_MAP = {
        "#决定": "decisions",
        "#偏好": "preferences",
        "#项目": "projects",
        "#知识": "learned",
        "#事件": "events",
        "#错误": "issues",
    }
    
    def __init__(self, db: MemoryDatabase = None):
        self.db = db or MemoryDatabase()
    
    def get_memories_for_period(self, start_date: str, end_date: str = None) -> List[Memory]:
        """
        获取指定时间段的记忆
        
        Args:
            start_date: 开始日期 YYYY-MM-DD
            end_date: 结束日期 YYYY-MM-DD，默认今天
        """
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        # 转换为 YYYY-MM 格式用于查询
        start_month = start_date[:7]
        end_month = end_date[:7]
        
        all_memories = self.db.get_all(limit=500)
        
        # 按时间过滤
        filtered = []
        for m in all_memories:
            time_label = m.time_label  # YYYY-MM 格式
            if start_month <= time_label <= end_month:
                filtered.append(m)
        
        return filtered
    
    def analyze_memories(self, memories: List[Memory]) -> SummaryDraft:
        """
        分析记忆列表，生成总结草稿
        
        Args:
            memories: 记忆列表
        
        Returns:
            SummaryDraft: 结构化总结
        """
        if not memories:
            return SummaryDraft(
                period="无记忆",
                decisions=[],
                preferences=[],
                projects=[],
                learned=[],
                events=[],
                issues=[],
                other=[]
            )
        
        # 按标签分类
        categorized = {
            "decisions": [],
            "preferences": [],
            "projects": [],
            "learned": [],
            "events": [],
            "issues": [],
            "other": []
        }
        
        for m in memories:
            if not m.content:
                continue
            
            # 分配到类别
            assigned = False
            for tag, category in self.TAG_CATEGORY_MAP.items():
                if tag in m.tags:
                    categorized[category].append(m.content)
                    assigned = True
                    break
            
            if not assigned:
                categorized["other"].append(m.content)
        
        # 去重（简单去重，保留第一次出现的）
        for key in categorized:
            seen = set()
            unique = []
            for item in categorized[key]:
                # 简化比较：取前50字符
                key_part = item[:50].lower()
                if key_part not in seen:
                    seen.add(key_part)
                    unique.append(item)
            categorized[key] = unique
        
        # 生成时间段
        if memories:
            dates = [m.time_label for m in memories if m.time_label]
            if dates:
                period = f"{min(dates)} ~ {max(dates)}"
            else:
                period = datetime.now().strftime("%Y-%m")
        else:
            period = datetime.now().strftime("%Y-%m")
        
        return SummaryDraft(
            period=period,
            decisions=categorized["decisions"],
            preferences=categorized["preferences"],
            projects=categorized["projects"],
            learned=categorized["learned"],
            events=categorized["events"],
            issues=categorized["issues"],
            other=categorized["other"]
        )
    
    def generate_summary_draft(self, days: int = 7) -> SummaryDraft:
        """
        生成过去 N 天的总结草稿
        
        Args:
            days: 天数，默认 7 天
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        memories = self.get_memories_for_period(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        
        return self.analyze_memories(memories)
    
    def parse_user_feedback(self, feedback: str, current_summary: SummaryDraft) -> Dict:
        """
        解析用户反馈
        
        Args:
            feedback: 用户回复
            current_summary: 当前总结
        
        Returns:
            {
                "action": "confirm" / "correct" / "cancel",
                "corrections": {...},  # 如果是 correct
                "message": str
            }
        """
        feedback = feedback.strip().lower()
        
        # 确认关键词
        confirm_keywords = ["对", "ok", "yes", "确认", "是的", "没问题", "对的"]
        
        # 取消关键词
        cancel_keywords = ["取消", "不要", "算了", "cancel", "no"]
        
        # 检查是否确认
        if any(k in feedback for k in confirm_keywords):
            return {
                "action": "confirm",
                "message": "✅ 总结已确认存档"
            }
        
        # 检查是否取消
        if any(k in feedback for k in cancel_keywords):
            return {
                "action": "cancel",
                "message": "❌ 总结已取消"
            }
        
        # 否则认为是修改
        return {
            "action": "correct",
            "feedback": feedback,
            "message": "✏️ 收到修改意见，我会更新总结"
        }
    
    def archive_summary(self, summary: SummaryDraft) -> List[str]:
        """
        存档总结
        
        将总结中的每条信息存为独立记忆
        
        Returns:
            存档的记忆 ID 列表
        """
        archived_ids = []
        
        categories = {
            "decisions": "#决定",
            "preferences": "#偏好",
            "projects": "#项目",
            "learned": "#知识",
            "events": "#事件",
            "issues": "#错误",
        }
        
        for category, tag in categories.items():
            items = getattr(summary, category, [])
            for item in items:
                memory = Memory(
                    id="",
                    content=item,
                    summary=f"[总结] {summary.period}",
                    tags=[tag, "#总结"],
                    time_label=summary.period[:7] if len(summary.period) > 7 else summary.period,
                    source="summary",
                    verified=True
                )
                memory_id = self.db.insert(memory)
                archived_ids.append(memory_id)
        
        return archived_ids
    
    def save_draft(self, summary: SummaryDraft, filepath: str = None) -> str:
        """
        保存草稿到文件
        """
        if not filepath:
            filepath = Path(__file__).parent.parent / "data" / "pending_summary.json"
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(summary.to_dict(), f, ensure_ascii=False, indent=2)
        
        return str(filepath)
    
    def load_draft(self, filepath: str = None) -> Optional[SummaryDraft]:
        """
        加载草稿
        """
        if not filepath:
            filepath = Path(__file__).parent.parent / "data" / "pending_summary.json"
        
        if not Path(filepath).exists():
            return None
        
        with open(filepath, encoding="utf-8") as f:
            d = json.load(f)
        
        return SummaryDraft(**d)
    
    def clear_draft(self, filepath: str = None) -> bool:
        """
        清除草稿
        """
        if not filepath:
            filepath = Path(__file__).parent.parent / "data" / "pending_summary.json"
        
        if Path(filepath).exists():
            Path(filepath).unlink()
            return True
        return False


# ==================== CLI 入口 ====================

if __name__ == "__main__":
    summarizer = MemorySummarizer()
    
    print("📊 TagMemory 定期归纳模块")
    print("=" * 40)
    
    # 生成过去 7 天的总结
    print("\n📝 生成过去 7 天的总结...\n")
    summary = summarizer.generate_summary_draft(days=7)
    
    print(summary.format_for_display())
    
    # 保存草稿
    draft_path = summarizer.save_draft(summary)
    print(f"\n💾 草稿已保存: {draft_path}")
    
    # 模拟用户确认
    print("\n" + "=" * 40)
    print("📝 模拟用户反馈...")
    
    feedback = "确认"
    result = summarizer.parse_user_feedback(feedback, summary)
    print(f"反馈「{feedback}」: {result['message']}")
    
    if result["action"] == "confirm":
        archived = summarizer.archive_summary(summary)
        print(f"✅ 已存档 {len(archived)} 条记忆")
        summarizer.clear_draft()
        print("🗑️ 草稿已清除")
