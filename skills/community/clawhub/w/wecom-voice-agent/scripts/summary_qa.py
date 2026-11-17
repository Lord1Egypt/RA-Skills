#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
summary_qa.py — 通话摘要质检（v2.8）

功能：
1. 三要素完整度评分：决策事项 / 待办事项 / 时间节点（加权 0-100）
2. 达标判定：≥ 80 分才交付使用；未达标回炉重新生成
3. 人工抽检队列：达标摘要随机 5% 进入人工复核（可调）
4. 纠错回流：人工修正结果写入反馈记录，驱动摘要 Prompt 迭代

评分权重：
- 决策事项 40 分（有无结论、是否明确）
- 待办事项 35 分（责任人 + 具体动作）
- 时间节点 25 分（截止时间是否具体）

降级策略（规则 9）：
- 数据库异常时返回内存态结果，不阻断摘要交付流程
- 任何单要素识别失败按 0 分计，不影响其他要素评分

依赖：纯 Python 标准库（re + sqlite3 + random）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-09-20)
"""

import os
import re
import json
import random
import sqlite3
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

# ==========================================
# 配置
# ==========================================

DB_PATH = os.path.join(os.path.expanduser("~"), ".wecom_voice", "summary_qa.db")

# 达标线
PASS_THRESHOLD = 80

# 人工抽检概率（达标摘要的 5%）
SPOT_CHECK_RATE = 0.05

# 三要素权重
WEIGHTS = {"decision": 0.40, "todo": 0.35, "time": 0.25}

# 要素识别规则（正则 + 关键词，纯规则零依赖）
DECISION_KEYWORDS = [
    "决定", "确定", "确认", "同意", "结论", "通过", "采纳", "批准", "否决",
    "暂缓", "明确", "敲定", "定了", "就这么办", "没问题",
]
DECISION_NEGATIVE = ["再考虑", "再商量", "再讨论", "暂不", "还没定", "不确定"]

TODO_KEYWORDS = [
    "待办", "需要", "负责", "跟进", "完成", "提交", "落实", "安排", "务必",
    "记得", "尽快", "限期", "督办", "落地", "执行",
]
OWNER_PATTERNS = [
    r"[一-龥]{2,4}(?:负责|牵头|对接|跟进|落实|执行)",
    r"由[一-龥]{2,4}",
    r"[一-龥]{2,4}(?:部门|团队|小组|组)",
]

TIME_PATTERNS = [
    r"\d{4}\s*年", r"\d{1,2}\s*月\s*\d{1,2}\s*[日号]",
    r"[今明后]\s*[天日]", r"下\s*周[一二三四五六日天]?",
    r"本\s*周[一二三四五六日天]?", r"周[一二三四五六日天]",
    r"\d{1,2}\s*[点时]\s*(?:\d{1,2}\s*分?)?", r"\d{1,2}\s*:\s*\d{2}",
    r"截止", r"之?前", r"底前", r"期?限",
    r"\d+\s*(?:个)?\s*(?:小时|分钟|秒|天|周|月)(?![一-龥])",
]
TIME_VAGUE = ["尽快", "近期", "过两天", "有时间", "抽空", "稍后"]


# ==========================================
# 摘要质检器
# ==========================================

class SummaryQA:
    """
    通话摘要质检器

    使用方式：
        qa = SummaryQA()
        result = qa.review("会议决定下周三前由张三提交方案。", summary_id="call_001")
        # result: {"score": 92, "passed": True, "elements": {...}, "suggestions": []}
        if result["passed"]:
            qa.maybe_enqueue_spot_check("call_001", summary_text)
    """

    def __init__(self, db_path: str = DB_PATH, pass_threshold: int = PASS_THRESHOLD,
                 spot_check_rate: float = SPOT_CHECK_RATE):
        self.db_path = db_path
        self.pass_threshold = pass_threshold
        self.spot_check_rate = spot_check_rate
        self._db_ok = True
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self._init_db()
        except Exception as e:
            # 降级：数据库不可用时仅内存评分，不阻断流程（规则 9）
            self._db_ok = False
            logger.warning(f"质检数据库初始化失败，降级为内存模式: {e}")

    def _init_db(self):
        """初始化质检与抽检队列表"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS summary_reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    summary_id TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    passed INTEGER NOT NULL,
                    elements_json TEXT DEFAULT '',
                    source TEXT DEFAULT 'auto',
                    created_at TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS spot_check_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    review_id INTEGER NOT NULL,
                    summary_id TEXT NOT NULL,
                    summary_text TEXT DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'pending',
                    correction TEXT DEFAULT '',
                    corrected_summary TEXT DEFAULT '',
                    reviewer TEXT DEFAULT '',
                    created_at TEXT NOT NULL,
                    reviewed_at TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_spot_check_status
                ON spot_check_queue(status)
            """)

    # ---------- 三要素评分 ----------

    def _score_decision(self, text: str) -> Dict[str, Any]:
        """决策事项评分（0-100）"""
        hits = [kw for kw in DECISION_KEYWORDS if kw in text]
        vague = [kw for kw in DECISION_NEGATIVE if kw in text]
        if hits and not vague:
            score = 100
        elif hits and vague:
            score = 60  # 有结论词但含犹豫表述
        elif vague:
            score = 20
        else:
            score = 0
        return {"score": score, "found": bool(hits), "hits": hits, "vague": vague}

    def _score_todo(self, text: str) -> Dict[str, Any]:
        """待办事项评分（0-100）：关键词 + 责任人 + 动作"""
        hits = [kw for kw in TODO_KEYWORDS if kw in text]
        owners = []
        for pattern in OWNER_PATTERNS:
            owners.extend(re.findall(pattern, text))
        if hits and owners:
            score = 100
        elif hits:
            score = 60  # 有待办无责任人
        elif owners:
            score = 40  # 有责任人无待办关键词
        else:
            score = 0
        return {"score": score, "found": bool(hits), "hits": hits, "owners": owners[:5]}

    def _score_time(self, text: str) -> Dict[str, Any]:
        """时间节点评分（0-100）：具体时间模式优先，模糊表述降分"""
        hits = []
        for pattern in TIME_PATTERNS:
            hits.extend(re.findall(pattern, text))
        vague = [kw for kw in TIME_VAGUE if kw in text]
        # 仅有模糊词（尽快/近期）且无具体时间 → 低分
        if hits and not vague:
            score = 100
        elif hits and vague:
            score = 70
        elif vague:
            score = 20
        else:
            score = 0
        return {"score": score, "found": bool(hits), "hits": hits[:8], "vague": vague}

    # ---------- 综合评审 ----------

    def review(self, summary_text: str, summary_id: str = "", source: str = "auto") -> Dict[str, Any]:
        """
        评审摘要质量

        Args:
            summary_text: 摘要文本
            summary_id: 关联通话 ID
            source: 来源标识

        Returns:
            {
                "score": int (0-100),
                "passed": bool,
                "elements": {"decision": {...}, "todo": {...}, "time": {...}},
                "suggestions": [str, ...]   # 中文改进建议
            }
        """
        text = (summary_text or "").strip()

        if not text:
            elements = {
                "decision": {"score": 0, "found": False, "hits": []},
                "todo": {"score": 0, "found": False, "hits": []},
                "time": {"score": 0, "found": False, "hits": []},
            }
            score = 0
            passed = False
            suggestions = ["摘要内容为空，请重新生成。"]
        else:
            elements = {
                "decision": self._score_decision(text),
                "todo": self._score_todo(text),
                "time": self._score_time(text),
            }
            total = sum(elements[k]["score"] * WEIGHTS[k] for k in WEIGHTS)
            score = int(round(total))
            passed = score >= self.pass_threshold

            suggestions = []
            if elements["decision"]["score"] < 60:
                suggestions.append("补充明确的决策结论（如：会议决定/双方同意……）")
            if elements["todo"]["score"] < 60:
                suggestions.append("补充待办事项及责任人（如：由张三负责提交方案）")
            if elements["time"]["score"] < 60:
                suggestions.append("补充具体时间节点（如：下周三 18:00 前，避免使用「尽快」等模糊表述）")

        result = {
            "score": score,
            "passed": passed,
            "elements": elements,
            "suggestions": suggestions,
        }

        # 持久化评审记录（空摘要同样记录，便于追踪摘要生成质量问题；
        # 数据库不可用时静默跳过，不影响结果返回——规则 9）
        if self._db_ok and summary_id:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("""
                        INSERT INTO summary_reviews (summary_id, score, passed, elements_json, source, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (summary_id, score, 1 if passed else 0,
                          json.dumps(elements, ensure_ascii=False), source,
                          datetime.now().isoformat()))
            except Exception as e:
                logger.warning(f"评审记录写入失败（不影响结果）: {e}")

        return result

    # ---------- 人工抽检队列 ----------

    def maybe_enqueue_spot_check(self, summary_id: str, summary_text: str) -> bool:
        """
        达标摘要按 5% 概率进入人工抽检队列

        Returns:
            True=已入队；False=未入队
        """
        if not self._db_ok:
            return False
        if random.random() >= self.spot_check_rate:
            return False
        try:
            with sqlite3.connect(self.db_path) as conn:
                # 取最近一条评审记录关联
                row = conn.execute(
                    "SELECT id FROM summary_reviews WHERE summary_id = ? ORDER BY id DESC LIMIT 1",
                    (summary_id,)
                ).fetchone()
                review_id = row[0] if row else 0
                conn.execute("""
                    INSERT INTO spot_check_queue (review_id, summary_id, summary_text, status, created_at)
                    VALUES (?, ?, ?, 'pending', ?)
                """, (review_id, summary_id, summary_text, datetime.now().isoformat()))
            logger.info(f"摘要 {summary_id} 进入人工抽检队列")
            return True
        except Exception as e:
            logger.warning(f"抽检入队失败: {e}")
            return False

    def list_review_queue(self, status: str = "pending") -> List[Dict[str, Any]]:
        """列出抽检队列"""
        if not self._db_ok:
            return []
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    "SELECT * FROM spot_check_queue WHERE status = ? ORDER BY created_at DESC",
                    (status,)
                ).fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            logger.warning(f"查询抽检队列失败: {e}")
            return []

    def submit_correction(self, review_id: int, corrected_summary: str,
                          reviewer: str = "", comment: str = "") -> Dict[str, Any]:
        """
        提交人工纠错（回流驱动 Prompt 迭代）

        Returns:
            {"ok": True, ...} 或 {"ok": False, "reason": ...}
        """
        if not corrected_summary or not corrected_summary.strip():
            return {"ok": False, "reason": "修正后的摘要不能为空"}
        if not self._db_ok:
            return {"ok": False, "reason": "质检数据库不可用"}
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.execute("""
                    UPDATE spot_check_queue
                    SET status = 'reviewed', correction = ?, corrected_summary = ?,
                        reviewer = ?, reviewed_at = ?
                    WHERE id = ? AND status = 'pending'
                """, (comment, corrected_summary.strip(), reviewer,
                      datetime.now().isoformat(), review_id))
                if cur.rowcount == 0:
                    return {"ok": False, "reason": "抽检记录不存在或已处理"}
            logger.info(f"人工纠错已回流: review_id={review_id}, 复核人={reviewer or '(未署名)'}")
            return {"ok": True, "review_id": review_id, "reviewer": reviewer}
        except Exception as e:
            logger.warning(f"纠错提交失败: {e}")
            return {"ok": False, "reason": f"纠错提交失败: {e}"}

    def get_prompt_feedback(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        获取人工纠错记录（供摘要 Prompt 迭代使用）

        Returns:
            最近的纠错列表（含原始摘要与修正摘要对照）
        """
        if not self._db_ok:
            return []
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute("""
                    SELECT id, summary_id, summary_text, corrected_summary, correction, reviewer, reviewed_at
                    FROM spot_check_queue
                    WHERE status = 'reviewed' AND corrected_summary != ''
                    ORDER BY reviewed_at DESC LIMIT ?
                """, (limit,)).fetchall()
            return [dict(r) for r in rows]
        except Exception as e:
            logger.warning(f"获取纠错记录失败: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """质检统计（通过率 / 平均分 / 待抽检数）"""
        if not self._db_ok:
            return {"total": 0, "passed": 0, "pass_rate": 0.0, "avg_score": 0, "pending_spot_checks": 0}
        try:
            with sqlite3.connect(self.db_path) as conn:
                total = conn.execute("SELECT COUNT(*) FROM summary_reviews").fetchone()[0]
                passed = conn.execute("SELECT COUNT(*) FROM summary_reviews WHERE passed = 1").fetchone()[0]
                avg = conn.execute("SELECT AVG(score) FROM summary_reviews").fetchone()[0] or 0
                pending = conn.execute(
                    "SELECT COUNT(*) FROM spot_check_queue WHERE status = 'pending'").fetchone()[0]
            return {
                "total": total,
                "passed": passed,
                "pass_rate": round(passed / total, 4) if total else 0.0,
                "avg_score": int(round(avg)),
                "pending_spot_checks": pending,
            }
        except Exception as e:
            logger.warning(f"质检统计失败: {e}")
            return {"total": 0, "passed": 0, "pass_rate": 0.0, "avg_score": 0, "pending_spot_checks": 0}


# ==========================================
# 便捷函数
# ==========================================

_qa_instance: Optional[SummaryQA] = None


def get_qa() -> SummaryQA:
    """获取质检器单例"""
    global _qa_instance
    if _qa_instance is None:
        _qa_instance = SummaryQA()
    return _qa_instance


def review_summary(summary_text: str, summary_id: str = "") -> Dict[str, Any]:
    """便捷函数：评审摘要质量"""
    return get_qa().review(summary_text, summary_id)


# ==========================================
# 命令行入口
# ==========================================

def _print_encoding_safe(text: str):
    """GBK 终端安全输出"""
    try:
        import sys
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print(text)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="通话摘要质检（v2.8）")
    sub = parser.add_subparsers(dest="command")

    p_review = sub.add_parser("review", help="评审一段摘要")
    p_review.add_argument("--text", required=True, help="摘要文本")
    p_review.add_argument("--id", default="", help="关联通话 ID")

    sub.add_parser("queue", help="查看人工抽检队列")
    sub.add_parser("feedback", help="查看纠错回流记录（Prompt 迭代用）")
    sub.add_parser("stats", help="质检统计")
    sub.add_parser("selftest", help="运行自测")

    args = parser.parse_args()
    qa = get_qa()

    if args.command == "review":
        result = qa.review(args.text, args.id)
        _print_encoding_safe(f"综合得分: {result['score']} / 100")
        _print_encoding_safe(f"是否达标(≥{qa.pass_threshold}): {'是' if result['passed'] else '否'}")
        for name, label in [("decision", "决策事项"), ("todo", "待办事项"), ("time", "时间节点")]:
            el = result["elements"][name]
            _print_encoding_safe(f"  {label}: {el['score']} 分{'（命中: ' + '、'.join(el.get('hits', [])[:5]) + '）' if el.get('hits') else ''}")
        if result["suggestions"]:
            _print_encoding_safe("改进建议:")
            for s in result["suggestions"]:
                _print_encoding_safe(f"  - {s}")
    elif args.command == "queue":
        items = qa.list_review_queue()
        if not items:
            _print_encoding_safe("抽检队列为空。")
        for it in items:
            _print_encoding_safe(f"  [{it['id']}] {it['summary_id']}: {it['summary_text'][:50]}")
    elif args.command == "feedback":
        items = qa.get_prompt_feedback()
        if not items:
            _print_encoding_safe("暂无纠错回流记录。")
        for it in items:
            _print_encoding_safe(f"  [{it['id']}] {it['summary_id']}")
            _print_encoding_safe(f"    原摘要: {it['summary_text'][:60]}")
            _print_encoding_safe(f"    修正后: {it['corrected_summary'][:60]}")
            if it.get("correction"):
                _print_encoding_safe(f"    纠错说明: {it['correction']}")
    elif args.command == "stats":
        stats = qa.get_stats()
        _print_encoding_safe(f"评审总数: {stats['total']}  通过: {stats['passed']}  "
                             f"通过率: {stats['pass_rate'] * 100:.1f}%  平均分: {stats['avg_score']}")
        _print_encoding_safe(f"待人工抽检: {stats['pending_spot_checks']}")
    elif args.command == "selftest":
        run_self_test()
    else:
        parser.print_help()


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行摘要质检自测（使用临时数据库，不触碰真实数据）"""
    import tempfile

    _print_encoding_safe("=" * 60)
    _print_encoding_safe("summary_qa.py — 自测模式")
    _print_encoding_safe("=" * 60)

    tmp_dir = tempfile.mkdtemp(prefix="summary_qa_test_")
    qa = SummaryQA(db_path=os.path.join(tmp_dir, "test_qa.db"))

    # 测试 1: 三要素齐全 → 高分通过
    _print_encoding_safe("\n[测试 1] 三要素齐全")
    r1 = qa.review("会议决定：下周三18点前由张三负责提交修订方案，双方确认无异议。",
                   summary_id="call_001")
    _print_encoding_safe(f"  得分: {r1['score']}  通过: {r1['passed']}")
    assert r1["score"] >= qa.pass_threshold, f"三要素齐全应通过，实际 {r1['score']}"
    assert r1["elements"]["decision"]["score"] == 100
    assert r1["elements"]["todo"]["score"] == 100
    assert r1["elements"]["time"]["score"] == 100
    _print_encoding_safe("  ✅ 通过")

    # 测试 2: 缺时间要素 → 不通过
    _print_encoding_safe("\n[测试 2] 缺时间节点")
    r2 = qa.review("会议决定由张三负责提交方案。", summary_id="call_002")
    _print_encoding_safe(f"  得分: {r2['score']}  通过: {r2['passed']}")
    assert r2["elements"]["time"]["score"] == 0
    assert r2["score"] < qa.pass_threshold
    assert any("时间" in s for s in r2["suggestions"])
    _print_encoding_safe("  ✅ 未通过且给出中文建议")

    # 测试 3: 模糊时间降分
    _print_encoding_safe("\n[测试 3] 模糊时间降分")
    r3 = qa.review("会议决定尽快由张三完成整改。", summary_id="call_003")
    _print_encoding_safe(f"  时间要素得分: {r3['elements']['time']['score']}")
    assert r3["elements"]["time"]["score"] == 20, "仅模糊词应低分"
    _print_encoding_safe("  ✅ 「尽快」仅得 20 分")

    # 测试 4: 空摘要
    _print_encoding_safe("\n[测试 4] 空摘要")
    r4 = qa.review("", summary_id="call_004")
    assert r4["score"] == 0 and r4["passed"] is False
    assert r4["suggestions"]
    _print_encoding_safe(f"  得分: {r4['score']}  建议: {r4['suggestions'][0]} ✅")

    # 测试 5: 抽检概率（打桩 random 保证确定性）
    _print_encoding_safe("\n[测试 5] 5% 抽检概率")
    old_random = random.random
    try:
        random.random = lambda: 0.01   # < 0.05 → 入队
        assert qa.maybe_enqueue_spot_check("call_001", "测试摘要") is True
        random.random = lambda: 0.99   # > 0.05 → 不入队
        assert qa.maybe_enqueue_spot_check("call_002", "测试摘要") is False
    finally:
        random.random = old_random
    queue = qa.list_review_queue()
    assert len(queue) == 1 and queue[0]["status"] == "pending"
    _print_encoding_safe("  入队/跳过均符合预期 ✅")

    # 测试 6: 纠错回流
    _print_encoding_safe("\n[测试 6] 纠错回流驱动 Prompt 迭代")
    r6 = qa.submit_correction(queue[0]["id"], "会议决定：下周三前张三提交方案（已补充截止时间）",
                              reviewer="admin", comment="补充了缺失的时间要素")
    assert r6["ok"] is True
    feedback = qa.get_prompt_feedback()
    assert len(feedback) == 1
    assert feedback[0]["corrected_summary"].startswith("会议决定")
    assert feedback[0]["correction"] == "补充了缺失的时间要素"
    # 重复提交应被拒绝（已处理）
    r6b = qa.submit_correction(queue[0]["id"], "再次提交")
    assert r6b["ok"] is False
    _print_encoding_safe("  纠错写入/查询/防重复 ✅")

    # 测试 7: 空修正拒绝
    _print_encoding_safe("\n[测试 7] 空修正拒绝")
    r7 = qa.submit_correction(999, "   ")
    assert r7["ok"] is False and "不能为空" in r7["reason"]
    _print_encoding_safe("  ✅")

    # 测试 8: 统计
    _print_encoding_safe("\n[测试 8] 质检统计")
    stats = qa.get_stats()
    _print_encoding_safe(f"  总数: {stats['total']}  通过: {stats['passed']}  待抽检: {stats['pending_spot_checks']}")
    assert stats["total"] == 4  # 测试1-4 共 4 条评审记录（含空摘要）
    assert stats["passed"] == 2  # 测试1（100分）与测试3（80分）达标
    assert stats["pending_spot_checks"] == 0  # 唯一入队项已被处理
    _print_encoding_safe("  ✅")

    import shutil
    shutil.rmtree(tmp_dir, ignore_errors=True)

    _print_encoding_safe(f"\n{'='*60}")
    _print_encoding_safe("所有自测通过 ✓")
    _print_encoding_safe("=" * 60)


if __name__ == "__main__":
    main()
