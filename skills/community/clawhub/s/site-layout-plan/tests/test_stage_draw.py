#!/usr/bin/env python3
"""site-layout-plan 0.6.7 · 尺寸标注失败与文字排版回归。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.bootstrap import ensure_runtime  # noqa: E402

ensure_runtime(__file__)

from site_layout.annotate import Box, TextPlacer, summarize, verify  # noqa: E402
from site_layout.stage_draw import (  # noqa: E402
    _base_layers, _create_doc, _ensure_dimstyle, _render_dimensions, _selfcheck,
)


class DimensionFailureTest(unittest.TestCase):
    def test_render_failure_is_recorded_not_silently_skipped(self) -> None:
        doc = _create_doc([("DIM-尺寸", 2, "Continuous")])
        _ensure_dimstyle(doc, 100.0)
        msp = doc.modelspace()
        good = {
            "kind": "road_width", "text": "道路宽4.50m",
            "p1": [0.0, 0.0], "p2": [4500.0, 0.0], "offset": 120.0,
            "refs": ["F-ROAD-01"],
        }
        bad = {
            "kind": "elevator_offset", "text": "距结构边0.00m",
            "p1": [1000.0, 1000.0], "p2": [1000.0, 1000.0], "offset": 120.0,
            "refs": ["F-LIFT-01"],
        }
        rendered, failures = _render_dimensions(msp, [good, bad])
        self.assertEqual([item["kind"] for item in rendered], ["road_width"])
        self.assertEqual(len(failures), 1)
        self.assertEqual(failures[0]["kind"], "elevator_offset")
        self.assertEqual(failures[0]["refs"], ["F-LIFT-01"])
        self.assertIn("ZeroDivisionError", failures[0]["reason"])
        self.assertEqual(len(list(msp.query("DIMENSION"))), 1)
        print("  [1/5] DIMENSION 渲染异常被记录为 failures，不静默跳过")


class TextPlacerTest(unittest.TestCase):
    def test_same_anchor_labels_do_not_overlap(self) -> None:
        placer = TextPlacer(Box(0, 0, 1000, 600))
        first = placer.place("塔吊 TC-01", (500, 300), 40, ref="tc")
        second = placer.place("施工电梯 SC-01", (500, 300), 40, ref="lift")
        self.assertNotEqual(first.level, "unplaced")
        self.assertNotEqual(second.level, "unplaced")
        self.assertEqual(summarize([first, second])["overlaps"], 0)
        self.assertEqual(verify([first, second]), [])
        print("  [2/5] 同一锚点两条标签自动避让，无矩形重叠")

    def test_label_avoids_road_segment(self) -> None:
        placer = TextPlacer(Box(0, 0, 1000, 600))
        placer.add_segment((0, 300), (1000, 300), "road:1")
        placement = placer.place("中心点", (500, 300), 40, ref="center")
        self.assertNotEqual(placement.level, "unplaced")
        self.assertFalse(placement.box.overlap_area(Box(0, 299, 1000, 301)) > 0)
        self.assertGreater(placement.box.y0, 301)
        print("  [3/5] 标签避开道路线段，必要时引线外移")

    def test_shrink_then_unplaced(self) -> None:
        tight = TextPlacer(Box(0, 0, 1000, 300))
        shrunk = tight.place("LONG-LABEL-ABCDEFGHIJ", (500, 150), 100,
                             ref="tight", short="")
        self.assertEqual(shrunk.level, "shrunk")
        self.assertLess(shrunk.height, 100)
        too_small = TextPlacer(Box(0, 0, 100, 50))
        unplaced = too_small.place("LONG-LABEL-ABCDEFGHIJ", (50, 25), 20, ref="tiny")
        self.assertEqual(unplaced.level, "unplaced")
        stats = summarize([shrunk, unplaced])
        self.assertEqual(stats["unplaced_count"], 1)
        print("  [4/5] 空间不足先缩字，再不足记 unplaced，不硬塞")

    def test_selfcheck_11_fails_on_overlap_and_unplaced(self) -> None:
        model = {
            "stage": "structure", "coord_unit": "mm", "redline_closed": True,
            "redline_area_m2": 100.0, "facilities": [], "cranes": [],
            "checks": [], "summary": {"pass": 0, "fail": 0, "manual": 0},
            "road_summary": {}, "context_summary": {},
        }
        doc = _create_doc(_base_layers(model))
        title = {"stage": "structure", "draft": "DRAFT"}
        png_info = {"font_status": "ok", "font_path": "test"}
        base_annotations = {
            "dimension_kinds": [], "applicable": [], "blocked": [], "skipped": [],
            "dimension_failures": [], "dimension_rendered": 0, "dimension_count": 0,
            "coordinate_csv_rows": 1, "coordinate_rows": 1, "coordinate_model_rows": 1,
            "coordinate_csv": "x.csv", "north_arrow": True, "scale_bar_m": 20.0,
            "legend_sections": ["设施", "线型", "标注", "说明"],
        }
        good = dict(base_annotations)
        good["text_layout"] = summarize([
            TextPlacer(Box(0, 0, 1000, 600)).place("A", (100, 100), 20, ref="a")])
        good["dxf_label_overlaps"] = []
        self.assertEqual(_selfcheck(model, doc, title, png_info, "DRAFT", good)["items"][10]["status"],
                         "pass")
        bad = dict(base_annotations)
        bad["text_layout"] = {"total": 2, "overlaps": 1, "problems": [{"a": "x", "b": "y"}],
                              "unplaced": [{"ref": "z", "text": "无处放"}],
                              "unplaced_count": 1, "index_entries": []}
        bad["dxf_label_overlaps"] = [{"a": "x", "b": "y"}]
        result = _selfcheck(model, doc, title, png_info, "DRAFT", bad)
        self.assertEqual(result["items"][10]["status"], "fail")
        self.assertEqual(result["exit_code"], 5)
        self.assertIn("无文字重叠", result["items"][10]["name"])
        print("  [5/5] 自检第 11 条对重叠/未放置判 fail，并写证据")


if __name__ == "__main__":
    unittest.main(verbosity=2)
