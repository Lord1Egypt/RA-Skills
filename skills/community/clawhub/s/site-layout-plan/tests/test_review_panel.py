#!/usr/bin/env python3
"""多视角审查回归：角色映射、结论、闸门、Markdown。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.review_panel import build_panel, render_panel_markdown  # noqa: E402


def check(cid, status, name="检查", message="", action=""):
    return {"id": cid, "name": name, "status": status, "message": message,
            "action": action, "basis": "规范"}


def model(*checks):
    return {"stage": "structure", "stage_name": "主体结构阶段", "checks": list(checks)}


class ReviewPanelTest(unittest.TestCase):
    def test_fail_propagates_to_fire_and_chief(self) -> None:
        panel = build_panel(
            model(check(1, "pass"), check(5, "fail", "消火栓间距", "间距超限", "增设消火栓"),
                  check(6, "manual", "塔吊临建", "缺塔吊结果")),
            {"checks": [check("R1", "fail", "道路宽度", "3.0m < 3.5m", "加宽道路")]},
        )
        roles = {r["role"]: r for r in panel["roles"]}
        self.assertEqual(roles["fire"]["verdict"], "fail")
        self.assertEqual(roles["chief"]["verdict"], "fail")
        self.assertEqual(roles["safety"]["verdict"], "review")
        self.assertTrue(panel["gates"]["hard_fail"])
        self.assertFalse(panel["gates"]["ready_for_review"])
        actions = " ".join(roles["fire"]["top_actions"])
        self.assertIn("增设消火栓", actions)
        print("  [1/4] 消火栓 fail 传导到消防/总工；缺塔吊 → 安全 review")

    def test_all_pass(self) -> None:
        panel = build_panel(
            model(check(1, "pass"), check(9, "pass")),
            {"checks": [check("R1", "pass")]},
        )
        self.assertTrue(all(r["verdict"] == "pass" for r in panel["roles"]))
        self.assertFalse(panel["gates"]["hard_fail"])
        self.assertTrue(panel["gates"]["ready_for_review"])
        print("  [2/4] 全通过时六角色均为 pass，闸门开放")

    def test_missing_checks_do_not_crash(self) -> None:
        panel = build_panel(model(), {"checks": []})
        self.assertEqual(len(panel["roles"]), 6)
        self.assertTrue(all(r["counts"] == {"pass": 0, "fail": 0, "manual": 0}
                            for r in panel["roles"]))
        print("  [3/4] 空校核结果不崩溃，六角色计数为 0")

    def test_markdown_has_roles_and_boundary(self) -> None:
        panel = build_panel(model(check(5, "fail", "消火栓间距", "超限")),
                            {"checks": []})
        md = render_panel_markdown(panel)
        for name in ("项目总工", "安全总监", "消防/临建", "文明环保", "商务成本", "甲方/报建"):
            self.assertIn(name, md)
        self.assertIn("不替代", md)
        print("  [4/4] Markdown 含六个角色与责任边界")

    def test_final_check_always_false(self) -> None:
        panel = build_panel(model(check(1, "pass")), {"checks": []})
        self.assertFalse(panel["final_check"])
        print("  [附] final_check 恒为 false")


if __name__ == "__main__":
    unittest.main(verbosity=2)
