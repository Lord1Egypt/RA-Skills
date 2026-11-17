#!/usr/bin/env python3
"""验证 report2article Skill 的结构与核心编辑契约。"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_FILE = SKILL_DIR / "SKILL.md"


def read_text(path: Path) -> str:
    """以 UTF-8 读取文本，并在失败时保留文件路径上下文。"""
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"无法读取文件：{path}") from exc


class ReportToArticleContractTest(unittest.TestCase):
    """防止后续修改破坏 Skill 的读者型编辑契约。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_text = read_text(SKILL_FILE)

    def test_frontmatter_describes_reader_oriented_editing(self) -> None:
        """Skill 发现信息应覆盖结构、表达和配图，而非字面搬运。"""
        frontmatter = self.skill_text.split("---", 2)[1]
        self.assertIn('name: "report2article"', frontmatter)
        for concept in ("结构", "表达", "配图"):
            self.assertIn(concept, frontmatter)
        self.assertNotIn("只重组排序起标题", frontmatter)

    def test_all_references_exist(self) -> None:
        """入口文件提到的每份相对引用都必须可读取。"""
        references = set(re.findall(r"references/[A-Za-z0-9._/-]+\.md", self.skill_text))
        self.assertGreaterEqual(len(references), 6)
        missing = [reference for reference in references if not (SKILL_DIR / reference).is_file()]
        self.assertEqual([], missing)

    def test_semantic_fidelity_replaces_verbatim_freeze(self) -> None:
        """允许等义编辑，同时保留事实与证据边界。"""
        for concept in ("语义保真", "编辑自由", "判断强弱", "等义"):
            self.assertIn(concept, self.skill_text)
        for conflicting_rule in (
            "正文内容一字不动",
            "内容层一字不动",
            "不允许对研究报告的内容进行任何增、删、改",
        ):
            self.assertNotIn(conflicting_rule, self.skill_text)

    def test_visual_guidance_has_fidelity_and_fallback_rules(self) -> None:
        """配图必须降低理解成本，且不能伪造数据或执行越界操作。"""
        visual_text = read_text(SKILL_DIR / "references/visual-guidelines.md")
        for concept in ("认知负担", "原报告", "来源", "替代文本", "配图方案"):
            self.assertIn(concept, visual_text)
        self.assertIn("不得编造", visual_text)
        self.assertIn("用户明确要求", visual_text)

    def test_prose_supports_one_consistent_style(self) -> None:
        """可按场景选择文风，但整篇不能混杂多种声音。"""
        prose_text = read_text(SKILL_DIR / "references/prose-style.md")
        for style in ("专业通俗", "技术深度", "媒体叙事", "周报速读"):
            self.assertIn(style, prose_text)
        self.assertIn("整篇只选一个主风格", prose_text)

    def test_long_report_audits_atomic_information(self) -> None:
        """长文复核必须覆盖对象内部信息，不能只核对对象数量。"""
        protocol = read_text(SKILL_DIR / "references/long-report-protocol.md")
        for concept in ("原子信息", "事实", "数据", "判断", "链接", "二次派生"):
            self.assertIn(concept, protocol)
        self.assertNotIn("只证明\"文章覆盖了我提取的对象清单\"", protocol)

    def test_structure_does_not_invent_implicit_relationships(self) -> None:
        """章节组织不能把模型推断包装成报告结论。"""
        skeleton = read_text(SKILL_DIR / "references/logic-skeleton.md")
        self.assertIn("明确表达", skeleton)
        self.assertNotIn("揭示报告中**已隐含**的关联", skeleton)


if __name__ == "__main__":
    unittest.main(verbosity=2)
