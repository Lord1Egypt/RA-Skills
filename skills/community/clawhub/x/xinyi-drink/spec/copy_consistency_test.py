"""活动文案一致性测试。

`build_response.ACTIVITY_RULE_LINES` 与 `LEAD_CAPTURE_COPY` 是脚本运行时输出的真源。
所有面向用户/Agent 的文档同样需要展示这些文案；本测试守护脚本与文档不漂移：
任何一处档位、券名或留资措辞调整时，缺漏会立即被发现。
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import build_response


def _strip_label_and_period(line: str) -> str:
    """从 `小龙虾贴纸：到任意门店…。` 这种结构里取出"：" 后、句末"。" 前的核心文案。"""
    return line.split("：", 1)[-1].rstrip("。")


# 派生自 build_response，确保运行时与测试用同一份真源。
ACTIVITY_RULE_FRAGMENTS = tuple(
    _strip_label_and_period(line) for line in build_response.ACTIVITY_RULE_LINES[1:]
)


class CanonicalCopyConsistencyTest(unittest.TestCase):
    SKILL_ROOT = Path(__file__).resolve().parents[1]
    REPO_ROOT = SKILL_ROOT.parent

    DOCS_WITH_ACTIVITY_RULES = (
        SKILL_ROOT / "SKILL.md",
        REPO_ROOT / "README.md",
        SKILL_ROOT / "references" / "activity-flow.md",
        SKILL_ROOT / "references" / "response-guidelines.md",
        SKILL_ROOT / "references" / "response-examples.md",
    )
    DOCS_WITH_LEAD_CAPTURE = (
        SKILL_ROOT / "SKILL.md",
        SKILL_ROOT / "references" / "activity-flow.md",
        SKILL_ROOT / "references" / "response-guidelines.md",
        SKILL_ROOT / "references" / "response-examples.md",
    )

    def test_runtime_rule_lines_provide_three_substantive_fragments(self) -> None:
        """`ACTIVITY_RULE_LINES` 应包含「活动规则：」标题 + 三条具体规则；防止误删。"""
        self.assertEqual(build_response.ACTIVITY_RULE_LINES[0], "活动规则：")
        self.assertEqual(len(build_response.ACTIVITY_RULE_LINES), 4)
        self.assertEqual(len(ACTIVITY_RULE_FRAGMENTS), 3)
        for fragment in ACTIVITY_RULE_FRAGMENTS:
            self.assertTrue(fragment, "rule fragment must not be empty")

    def test_each_documented_doc_uses_canonical_activity_rule_fragments(self) -> None:
        for doc in self.DOCS_WITH_ACTIVITY_RULES:
            content = doc.read_text(encoding="utf-8")
            for fragment in ACTIVITY_RULE_FRAGMENTS:
                with self.subTest(doc=str(doc.relative_to(self.REPO_ROOT)), fragment=fragment):
                    self.assertIn(
                        fragment,
                        content,
                        msg=(
                            f"{doc} 缺少 ACTIVITY_RULE_LINES 派生的核心文案：{fragment!r}。"
                            " 业务文案变更时请同步 build_response.ACTIVITY_RULE_LINES 与所有相关文档。"
                        ),
                    )

    def test_each_documented_doc_uses_canonical_lead_capture_copy(self) -> None:
        canonical = build_response.LEAD_CAPTURE_COPY
        for doc in self.DOCS_WITH_LEAD_CAPTURE:
            content = doc.read_text(encoding="utf-8")
            with self.subTest(doc=str(doc.relative_to(self.REPO_ROOT))):
                self.assertIn(
                    canonical,
                    content,
                    msg=(
                        f"{doc} 缺少 build_response.LEAD_CAPTURE_COPY 文案：{canonical!r}。"
                        " 留资措辞变更时请同步常量与所有相关文档。"
                    ),
                )

    def test_persistent_local_cache_is_not_documented_as_current_session(self) -> None:
        docs = (
            self.SKILL_ROOT / "SKILL.md",
            self.REPO_ROOT / "README.md",
            self.SKILL_ROOT / "skill.json",
            self.SKILL_ROOT / "references" / "activity-flow.md",
            self.SKILL_ROOT / "references" / "privacy-boundaries.md",
            self.SKILL_ROOT / "references" / "gotchas.md",
        )
        for doc in docs:
            content = doc.read_text(encoding="utf-8")
            with self.subTest(doc=str(doc.relative_to(self.REPO_ROOT))):
                self.assertNotIn("当前会话已确认领取成功", content)
                self.assertNotIn("同一 Agent 会话已确认领取", content)
                self.assertIn("本机缓存", content)


if __name__ == "__main__":
    unittest.main()
