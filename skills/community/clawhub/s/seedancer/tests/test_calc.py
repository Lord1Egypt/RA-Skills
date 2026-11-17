#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""seedancer_calc.py 单元测试（零依赖：python tests/test_calc.py）

守护点：计算器里的常量必须与 SKILL.md 的公式表一致 —— 改了任意一侧，这里就会红。
"""

import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import seedancer_calc as calc  # noqa: E402


def skill_text():
    with open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8") as fh:
        return fh.read()


class SminTable(unittest.TestCase):
    # SKILL.md「计算公式」表的逐格值
    TABLE = {
        6: (3, 4, 4), 9: (4, 5, 6), 10: (4, 6, 7),
        12: (5, 7, 8), 15: (6, 8, 10), 30: (12, 16, 20),
    }

    def test_table(self):
        for t, (o, a, f) in self.TABLE.items():
            self.assertEqual(calc.smin(t, "ordinary"), o, t)
            self.assertEqual(calc.smin(t, "action_reversal"), a, t)
            self.assertEqual(calc.smin(t, "fight"), f, t)

    def test_table_matches_skill_md(self):
        """SKILL.md 里的表行必须能被计算器复现（防两侧漂移）。"""
        rows = re.findall(r"^\|\s*(\d+)秒[^|]*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*$",
                          skill_text(), re.M)
        self.assertGreaterEqual(len(rows), 6)
        for t, o, a, f in rows:
            t = int(t)
            self.assertEqual((calc.smin(t, "ordinary"), calc.smin(t, "action_reversal"),
                              calc.smin(t, "fight")), (int(o), int(a), int(f)), t)

    def test_bad_input(self):
        with self.assertRaises(calc.UsageError):
            calc.smin(0, "ordinary")
        with self.assertRaises(calc.UsageError):
            calc.smin(10, "dance")


class ModelLimits(unittest.TestCase):
    def test_limits_match_skill_md(self):
        text = skill_text()
        for name, sec in (("Seedance 2.0", 15), ("Seedance 2.5", 30), ("Kling 3.0", 15), ("Veo 3", 8)):
            self.assertRegex(text, r"\|\s*%s\s*\|\s*%d秒" % (re.escape(name), sec))
        self.assertEqual(calc.MODEL_LIMITS["seedance-2.0"], 15)
        self.assertEqual(calc.MODEL_LIMITS["seedance-2.5"], 30)
        self.assertEqual(calc.MODEL_LIMITS["kling-3.0"], 15)
        self.assertEqual(calc.MODEL_LIMITS["veo-3"], 8)

    def test_aliases(self):
        self.assertEqual(calc.normalize_model("Seedance 2.0"), "seedance-2.0")
        self.assertEqual(calc.normalize_model("kling3"), "kling-3.0")
        self.assertEqual(calc.normalize_model("VEO-3"), "veo-3")
        with self.assertRaises(calc.UsageError):
            calc.normalize_model("sora")


class Dialogue(unittest.TestCase):
    def test_counts(self):
        c = calc.dialogue_cost("你终于来了。我等了三年……", "slow")
        self.assertEqual(c["voiced_chars"], 10)
        self.assertEqual(c["sentence_ends"], 1)
        self.assertEqual(c["long_pauses"], 1)
        # upper = 10/2.5 + 0.60 + 2.0 = 6.6；lower = 10/3.2 + 0.35 + 0.5 = 3.975
        self.assertAlmostEqual(c["min_seconds_upper"], 6.6, places=2)
        self.assertAlmostEqual(c["min_seconds_lower"], 3.98, places=2)

    def test_quotes_not_counted(self):
        a = calc.dialogue_cost("“走。”", "normal")
        b = calc.dialogue_cost("走。", "normal")
        self.assertEqual(a["voiced_chars"], b["voiced_chars"])

    def test_faster_pace_is_shorter(self):
        slow = calc.dialogue_cost("这件事你必须现在就告诉我。", "slow")
        fast = calc.dialogue_cost("这件事你必须现在就告诉我。", "fast")
        self.assertLess(fast["min_seconds_upper"], slow["min_seconds_upper"])


class Group(unittest.TestCase):
    def test_pass(self):
        r = calc.check_group("seedance-2.0", 12, "ordinary", 5, ["你来了。"], "normal", 3.0, 0.0)
        self.assertTrue(r["ok"], r)

    def test_over_model_limit(self):
        r = calc.check_group("veo-3", 10, "ordinary", 4, [], "normal", 3.0, 0.0)
        self.assertFalse(r["ok"])
        self.assertFalse(r["gates"][0]["ok"])

    def test_dialogue_overload(self):
        long_line = "我早就知道你会回来，可我没想到你会在这样一个雨夜，带着这样一个消息出现在我面前。"
        r = calc.check_group("seedance-2.0", 8, "ordinary", 4, [long_line], "slow", 3.0, 0.0)
        self.assertFalse(r["ok"])
        self.assertTrue(any("拆段" in a for a in r["advice"]))

    def test_shots_below_smin(self):
        r = calc.check_group("seedance-2.0", 15, "fight", 6, [], "normal", 3.0, 0.0)
        self.assertFalse(r["ok"])
        self.assertEqual(r["smin"], 10)


class Cli(unittest.TestCase):
    def test_exit_codes(self):
        self.assertEqual(calc.main(["smin", "12", "ordinary"]), 0)
        self.assertEqual(calc.main(["check-group", "--model", "veo-3", "--duration", "12"]), 1)
        self.assertEqual(calc.main(["check-group", "--model", "sora", "--duration", "5"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
