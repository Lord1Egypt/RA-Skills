"""
WorkBuddy 智能学习系统 - 反馈收集与处理模块
功能：收集用户反馈、自动归类、触发学习机制
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
import uuid


class FeedbackCollector:
    """反馈收集器 - 收集和管理用户反馈"""

    def __init__(self, workspace_root: str):
        self.workspace = Path(workspace_root)
        self.feedback_dir = self.workspace / ".workbuddy" / "memory" / "feedback"
        self.feedback_dir.mkdir(parents=True, exist_ok=True)

    def record_feedback(
        self,
        task_id: str,
        rating: str,  # "good" | "bad" | "neutral"
        tags: list[str] = None,
        note: str = None,
        context_hash: str = None,
        feedback_type: str = "explicit"
    ) -> dict:
        """
        记录一条反馈
        """
        feedback = {
            "feedback_id": str(uuid.uuid4()),
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "type": feedback_type,
            "rating": rating,
            "tags": tags or [],
            "note": note,
            "context_hash": context_hash,
            "learned": False
        }

        # 写入当月反馈文件
        month_key = datetime.now().strftime("%Y-%m")
        feedback_file = self.feedback_dir / f"feedback_{month_key}.json"

        existing = []
        if feedback_file.exists():
            with open(feedback_file, "r", encoding="utf-8") as f:
                existing = json.load(f)

        existing.append(feedback)

        with open(feedback_file, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

        return feedback

    def get_recent_feedback(self, days: int = 7) -> list[dict]:
        """获取最近N天的反馈"""
        feedbacks = []
        for f in self.feedback_dir.glob("feedback_*.json"):
            with open(f, "r", encoding="utf-8") as file:
                data = json.load(file)
                cutoff = datetime.now().timestamp() - (days * 86400)
                feedbacks.extend([
                    fb for fb in data
                    if datetime.fromisoformat(fb["timestamp"]).timestamp() > cutoff
                ])
        return feedbacks

    def get_unsatisfied_patterns(self) -> dict:
        """分析不满意反馈，提取问题模式"""
        recent = self.get_recent_feedback(30)
        bad_feedback = [fb for fb in recent if fb["rating"] == "bad"]

        patterns = {"by_tag": {}, "total": len(bad_feedback)}

        for fb in bad_feedback:
            for tag in fb.get("tags", []):
                patterns["by_tag"][tag] = patterns["by_tag"].get(tag, 0) + 1

        return patterns


def generate_feedback_prompt(last_task_summary: str = None) -> str:
    """
    生成反馈收集提示（供AI在任务结束时调用）
    """
    prompt = """
## 任务反馈收集

请评估本次任务执行的质量：

**评分标准**：
- 👍 满意：结果直接可用，符合预期
- 👎 不满意：需要修正或重新执行
- ✏️ 有建议：有具体改进意见

**快速反馈格式**：
```
反馈：[👍/👎/✏️]
标签：任务类型标签（可选）
备注：改进建议（可选）
```

**当前任务摘要**：
""" + (last_task_summary or "（无）")

    return prompt


if __name__ == "__main__":
    # 测试代码
    collector = FeedbackCollector("c:/Users/Administrator/WorkBuddy/20260412210819")

    # 模拟记录反馈
    test_feedback = collector.record_feedback(
        task_id="test-001",
        rating="good",
        tags=["文件整理", "记忆系统"],
        note="结构清晰，格式正确"
    )
    print(f"✓ 反馈已记录: {test_feedback['feedback_id']}")

    # 获取近期反馈
    recent = collector.get_recent_feedback()
    print(f"✓ 最近7天反馈数: {len(recent)}")
