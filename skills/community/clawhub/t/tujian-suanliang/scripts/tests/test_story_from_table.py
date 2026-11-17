"""层高表反查的排序回归（真图 s9 第 5 步暴露）。

真图复现路径：`floor` 不给 --story-height-mm 时，按图名「标高7.950…」反查层高表；
该表多行只标标高、没有层高列，于是 pairs=[(7.95, None), (7.95, None)]，
旧代码 `pairs.sort()` 先比第一轮（相等）再比第二轮，抛
TypeError: '<' not supported between instances of 'NoneType' and 'float'。
修复：只按标高排序（key=lambda pair: pair[0]）。
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import qty_core  # noqa: E402

TITLES = [{"title": "层高表", "sheet": "S1", "x": 5000.0, "y": 5000.0, "refs": 3}]
SHEETS = {"S1": (0.0, 0.0, 20000.0, 20000.0)}
LABEL = "标高7.950叠合板平面图"


def _row(i: int, text: str, x: float, y: float):
    return (i, text, "TEXT", "文字", "S1", x, y)


class StoryFromTableSort(unittest.TestCase):
    def test_same_elevation_without_height_column_does_not_crash(self):
        """两行同标高、都没有层高列：旧代码在这里抛 TypeError。"""
        rows = [_row(0, "7.950", 1000.0, 1000.0), _row(1, "7.950", 1000.0, 1200.0)]
        story, info = qty_core.story_from_table(rows, SHEETS, LABEL, TITLES)
        self.assertIsNone(story)
        self.assertIn("原因", info)

    def test_missing_height_column_still_uses_elevation_gap_below(self):
        """没有层高列时仍能按「本层标高−下层标高」给出柱墙段高。"""
        rows = [_row(0, "7.950", 1000.0, 1000.0), _row(1, "3.600", 1000.0, 1200.0)]
        story, info = qty_core.story_from_table(rows, SHEETS, LABEL, TITLES)
        self.assertEqual(story, 4350)
        self.assertIn("本层标高", info.get("算法", ""))


if __name__ == "__main__":
    unittest.main(verbosity=2)
