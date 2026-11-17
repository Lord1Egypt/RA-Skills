#!/usr/bin/env python3
"""设施图块库：BLOCK/INSERT、形象化图元、PNG 同源与图层回归。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.bootstrap import ensure_runtime  # noqa: E402

ensure_runtime(__file__)

import ezdxf  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

from site_layout.symbols import (  # noqa: E402
    BASE, SYMBOLS, block_name, categories_in, draw_pictogram,
    ensure_symbol_blocks, insert_symbol, primitives, symbol_size,
)


def _kinds(prims):
    return [item[0] for item in prims]


class SymbolTest(unittest.TestCase):
    def test_every_category_has_block(self) -> None:
        for category, item in SYMBOLS.items():
            self.assertEqual(block_name(category), item["block"])
            self.assertGreater(symbol_size(category), 0)
            self.assertTrue(primitives(category), msg=category)
        self.assertIsNone(block_name("not_a_category"))
        print("  [1/8] 全部设施类别都有 SLP_* 图块、尺寸与图元")

    def test_ensure_blocks_idempotent(self) -> None:
        doc = ezdxf.new("R2010")
        created = ensure_symbol_blocks(doc)
        self.assertEqual(len(created), len(SYMBOLS))
        again = ensure_symbol_blocks(doc)
        self.assertEqual(again, [])
        for item in SYMBOLS.values():
            self.assertIn(item["block"], doc.blocks)
        print("  [2/8] 图块创建幂等，重复调用不重复建块")

    def test_insert_uses_layer_and_scale(self) -> None:
        doc = ezdxf.new("R2010")
        doc.layers.add("TEST-设施", color=3)
        ensure_symbol_blocks(doc)
        msp = doc.modelspace()
        insert_symbol(msp, "fire_hydrant", 1000.0, 2000.0, "TEST-设施", 3, size_mm=2000.0)
        inserts = list(msp.query("INSERT"))
        self.assertEqual(len(inserts), 1)
        self.assertEqual(inserts[0].dxf.name, "SLP_HYDRANT")
        self.assertEqual(inserts[0].dxf.layer, "TEST-设施")
        self.assertAlmostEqual(inserts[0].dxf.xscale, 2.0)
        print("  [3/8] 插入图块带图层、块名与缩放")

    def test_categories_in_counts(self) -> None:
        model = {"facilities": [
            {"category": "fire_hydrant", "category_name": "消火栓"},
            {"category": "fire_hydrant", "category_name": "消火栓"},
            {"category": "processing_zone", "category_name": "加工区"},
        ]}
        rows = {item["category"]: item for item in categories_in(model)}
        self.assertEqual(rows["fire_hydrant"]["count"], 2)
        self.assertEqual(rows["processing_zone"]["count"], 1)
        print("  [4/8] 图例按类别聚合计数正确")

    def test_categories_in_counts_cranes(self) -> None:
        model = {"facilities": [], "cranes": [{"id": "TC-01"}, {"id": "TC-02"}]}
        rows = {item["category"]: item for item in categories_in(model)}
        self.assertEqual(rows["tower_crane"]["count"], 2)
        self.assertEqual(rows["tower_crane"]["block"], "SLP_CRANE")
        print("  [5/8] 塔吊计入图例，不因不在 facilities 中丢失")

    def test_crane_pictogram_has_structural_parts(self) -> None:
        """语义断言：不绑定单点坐标，允许后续继续优化造型。"""
        prims = primitives("tower_crane")
        kinds = _kinds(prims)
        self.assertGreaterEqual(kinds.count("poly"), 3)
        self.assertGreaterEqual(kinds.count("line"), 10)
        points = []
        for item in prims:
            if item[0] == "line":
                points += [(item[1], item[2]), (item[3], item[4])]
            elif item[0] in ("poly", "solid"):
                points += list(item[1])
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        self.assertGreaterEqual(max(xs), 490)      # 起重臂伸到 +500
        self.assertLessEqual(min(xs), -450)        # 平衡臂/配重伸到 -478
        self.assertGreaterEqual(max(ys) - min(ys), 450)
        # 塔身：左右弦杆成对，且至少 5 道跨塔身水平系杆
        chords = [i for i in prims if i[0] == "line"
                  and i[1] == i[3] and abs(i[4] - i[2]) >= 350]
        self.assertGreaterEqual(len({i[1] for i in chords}), 2, msg=chords)
        ties = [i for i in prims if i[0] == "line" and i[2] == i[4]
                and abs(i[3] - i[1]) >= 140 and abs(i[1] + i[3]) < 5]
        self.assertGreaterEqual(len({i[2] for i in ties}), 5, msg=ties)
        # 塔身交叉腹杆
        self.assertGreaterEqual(sum(1 for i in prims if i[0] == "line"
                                    and i[1] == -i[3] and i[2] != i[4]), 2)
        # 起重臂、平衡臂、塔尖拉杆、小车吊钩
        self.assertTrue(any(i[0] == "line" and max(i[1], i[3]) >= 490 for i in prims))
        self.assertTrue(any(i[0] == "line" and min(i[1], i[3]) <= -450 for i in prims))
        self.assertGreaterEqual(sum(1 for i in prims if i[0] == "line"
                                    and max(i[2], i[4]) >= 300 and min(i[2], i[4]) <= 100
                                    and abs(i[3] - i[1]) >= 250), 2)
        self.assertTrue(any(i[0] == "poly" and min(p[1] for p in i[1]) <= -240
                            for i in prims))
        # 基础填实
        self.assertTrue(any(i[0] == "solid" and min(p[1] for p in i[1]) <= -300
                            for i in prims))
        print("  [6/8] 塔吊图元含格构塔身、起重臂、平衡臂、塔尖拉杆、小车吊钩与基础")

    def test_elevator_pictogram_has_dual_rails_cage_and_stops(self) -> None:
        """语义断言：双导轨间距、腹杆、吊笼、停靠层、附着支撑。"""
        prims = primitives("construction_elevator")
        rails = [i for i in prims if i[0] == "line"
                 and i[1] == i[3] and abs(i[4] - i[2]) >= 590]
        self.assertEqual(len(rails), 2, msg=rails)
        gap = abs(rails[0][1] - rails[1][1])
        self.assertTrue(70 <= gap <= 110, msg=gap)
        rail_xs = {rails[0][1], rails[1][1]}
        braces = [i for i in prims if i[0] == "line"
                  and {i[1], i[3]} == rail_xs and i[2] != i[4]]
        self.assertGreaterEqual(len(braces), 6, msg=braces)
        cages = [i for i in prims if i[0] == "poly" and i[-1] is True
                 and 110 <= max(p[0] for p in i[1]) - min(p[0] for p in i[1]) <= 200
                 and max(p[1] for p in i[1]) - min(p[1] for p in i[1]) >= 200]
        self.assertEqual(len(cages), 1, msg=cages)
        cage_x1 = max(p[0] for p in cages[0][1])
        floors = [i for i in prims if i[0] == "line" and i[2] == i[4]
                  and abs(i[1] - cage_x1) < 5 and abs(i[3] - i[1]) >= 200]
        self.assertGreaterEqual(len({i[2] for i in floors}), 3, msg=floors)
        attachments = [i for i in prims if i[0] == "line" and i[2] == i[4]
                       and min(i[1], i[3]) >= 170 and abs(i[3] - i[1]) >= 100]
        self.assertGreaterEqual(len({i[2] for i in attachments}), 2, msg=attachments)
        self.assertTrue(any(i[0] == "circle" for i in prims))
        self.assertTrue(any(i[0] == "text" and i[1] == "SC" for i in prims))
        print("  [7/8] 施工电梯图元含双导轨、腹杆、吊笼、停靠层与附着")

    def test_draw_pictogram_renders_png_same_primitives(self) -> None:
        image = Image.new("RGB", (240, 240), "#ffffff")
        draw = ImageDraw.Draw(image)
        self.assertTrue(draw_pictogram(draw, "tower_crane", 120, 120,
                                       BASE * 0.18, "#b71c1c"))
        self.assertTrue(draw_pictogram(draw, "construction_elevator", 60, 60,
                                       BASE * 0.08, "#1f5f99"))
        self.assertFalse(draw_pictogram(draw, "not_a_category", 10, 10, 10, "#000000"))
        colors = {color for _count, color in image.getcolors(maxcolors=1000000)}
        self.assertGreater(len(colors), 1)
        print("  [8/8] PNG 图元与 DXF 图块同源，未知类别不误画")


if __name__ == "__main__":
    unittest.main(verbosity=2)
