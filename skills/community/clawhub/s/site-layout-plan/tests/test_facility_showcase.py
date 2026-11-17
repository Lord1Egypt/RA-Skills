#!/usr/bin/env python3
"""0.7.0 设施标准块与合并/分张大样回归测试。

覆盖：
- 7 类设施的块名稳定且唯一；
- 图元复杂度与关键几何语义（塔吊/电梯/地磅/洗车台/三区）；
- 全部 BLOCK 可由 ezdxf 创建；
- showcase CLI 合并大样 + 7 张单图非空；
- 未知 --only 键拒绝执行。
"""
from __future__ import annotations

import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "render_facility_showcase.py"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.bootstrap import ensure_runtime  # noqa: E402

ensure_runtime(__file__)

import ezdxf  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

from site_layout.symbols import (  # noqa: E402
    BASE, SYMBOLS, block_name, draw_pictogram, ensure_symbol_blocks, primitives,
)

SHOWCASE = {
    "crane": "tower_crane",
    "elev": "construction_elevator",
    "weighbridge": "weighbridge",
    "wash": "wheel_wash",
    "office": "site_office",
    "dorm": "staff_dormitory",
    "living": "worker_living_zone",
}
STABLE_BLOCKS = {
    "tower_crane": "SLP_CRANE",
    "construction_elevator": "SLP_ELEV",
    "weighbridge": "SLP_WEIGHBRIDGE",
    "wheel_wash": "SLP_WASH",
    "site_office": "SLP_OFFICE",
    "staff_dormitory": "SLP_STAFFDORM",
    "worker_living_zone": "SLP_LIVING",
}
MIN_PRIMITIVES = {
    "tower_crane": 70,
    "construction_elevator": 60,
    "weighbridge": 30,
    "wheel_wash": 50,
    "site_office": 50,
    "staff_dormitory": 80,
    "worker_living_zone": 90,
}


def _bounds(prims):
    points = []
    for item in prims:
        kind = item[0]
        if kind == "line":
            points.extend([(item[1], item[2]), (item[3], item[4])])
        elif kind in ("poly", "solid"):
            points.extend(item[1])
        elif kind in ("circle", "arc"):
            x, y, r = item[1], item[2], item[3]
            points.extend([(x - r, y - r), (x + r, y + r)])
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return min(xs), min(ys), max(xs), max(ys)


def _rects(prims):
    result = []
    for item in prims:
        if item[0] != "poly" or not item[2] or len(item[1]) != 4:
            continue
        xs = [point[0] for point in item[1]]
        ys = [point[1] for point in item[1]]
        result.append((min(xs), min(ys), max(xs), max(ys)))
    return result


def _has_rect(prims, expected, tolerance=0.01):
    return any(all(abs(actual - expected[index]) <= tolerance for index, actual in enumerate(rect))
               for rect in _rects(prims))


def _lines_in_rect(prims, x0, y0, x1, y1):
    lines = []
    for item in prims:
        if item[0] != "line":
            continue
        if (x0 <= min(item[1], item[3]) and max(item[1], item[3]) <= x1
                and y0 <= min(item[2], item[4]) and max(item[2], item[4]) <= y1):
            lines.append(item)
    return lines


def _circle_count(prims, y_min=None, y_max=None):
    count = 0
    for item in prims:
        if item[0] != "circle":
            continue
        if y_min is not None and item[2] < y_min:
            continue
        if y_max is not None and item[2] > y_max:
            continue
        count += 1
    return count


class StableBlockTest(unittest.TestCase):
    def test_showcase_keys_map_to_unique_blocks(self) -> None:
        self.assertEqual(len(SHOWCASE), 7)
        blocks = []
        for key, category in SHOWCASE.items():
            self.assertEqual(SYMBOLS[category]["showcase"], key)
            self.assertEqual(block_name(category), STABLE_BLOCKS[category])
            for field in ("layer", "stages", "showcase", "note"):
                self.assertTrue(SYMBOLS[category].get(field), (category, field))
            blocks.append(block_name(category))
        self.assertEqual(len(blocks), len(set(blocks)), "7 类展示块名必须唯一")
        print("  [1/7] 7 个展示键对应稳定且唯一的 SLP_* 块名")

    def test_primitives_have_enough_geometry_and_cover_block_base(self) -> None:
        for category, minimum in MIN_PRIMITIVES.items():
            prims = primitives(category)
            self.assertGreaterEqual(len(prims), minimum, category)
            x0, y0, x1, y1 = _bounds(prims)
            self.assertGreaterEqual(x1 - x0, BASE * 0.50, category)
            self.assertGreaterEqual(y1 - y0, BASE * 0.40, category)
            self.assertGreaterEqual(x0, -BASE / 2 - 1, category)
            self.assertLessEqual(x1, BASE / 2 + 1, category)
            self.assertGreaterEqual(y0, -BASE / 2 - 1, category)
            self.assertLessEqual(y1, BASE / 2 + 1, category)
        print("  [2/7] 7 类图元数量达下限，几何覆盖 1000×1000 基准")

    def test_elevator_and_weighbridge_key_semantics(self) -> None:
        elev = primitives("construction_elevator")
        rails = [item for item in elev if item[0] == "line"
                 and item[1] == item[3] and abs(item[4] - item[2]) >= 590]
        self.assertEqual(len(rails), 2, "施工电梯应只有双导轨，不应多出第三根通高导轨")
        floors = [rect for rect in _rects(elev)
                  if 45 <= rect[2] - rect[0] <= 70 and 35 <= rect[3] - rect[1] <= 70]
        self.assertGreaterEqual(len(floors), 3, "施工电梯至少应有 3 道层门")

        weigh = primitives("weighbridge")
        deck = (-360.0, -95.0, 360.0, 95.0)
        self.assertTrue(_has_rect(weigh, deck), "地磅应有分节秤台")
        sensor_rects = [rect for rect in _rects(weigh)
                        if 35 <= rect[2] - rect[0] <= 45 and 24 <= rect[3] - rect[1] <= 32]
        limit_blocks = [rect for rect in _rects(weigh)
                        if 12 <= rect[2] - rect[0] <= 20 and 40 <= rect[3] - rect[1] <= 48]
        self.assertEqual(len(sensor_rects), 4, "地磅应有四角称重传感器")
        self.assertEqual(len(limit_blocks), 4, "地磅应有四角限位挡块")
        print("  [3/7] 电梯双导轨/层门、地磅秤台/传感器语义成立")

    def test_wash_three_stage_pool_labels_and_office_two_rows(self) -> None:
        wash = primitives("wheel_wash")
        self.assertTrue(_has_rect(wash, (-460.0, -365.0, -160.0, -265.0)))
        self.assertTrue(_has_rect(wash, (-150.0, -365.0, 150.0, -265.0)))
        self.assertTrue(_has_rect(wash, (160.0, -365.0, 460.0, -265.0)))
        numeral_counts = [len(_lines_in_rect(wash, x0, -365.0, x1, -265.0))
                          for x0, x1 in ((-460.0, -160.0), (-150.0, 150.0), (160.0, 460.0))]
        self.assertEqual(numeral_counts, [1, 5, 4],
                         "三级沉淀池应保留线段绘制的 1/2/3 编号")

        office = primitives("site_office")
        self.assertTrue(_has_rect(office, (-430.0, 210.0, 300.0, 320.0)))
        self.assertTrue(_has_rect(office, (-430.0, 40.0, 300.0, 150.0)),
                        "办公区应有上下两层箱房排")
        self.assertTrue(_has_rect(office, (315.0, 40.0, 415.0, 210.0)),
                        "办公区应有一部楼梯")
        print("  [4/7] 洗车台 1/2/3 沉淀池、办公区两层箱房语义成立")

    def test_dorm_and_living_key_semantics(self) -> None:
        dorm = primitives("staff_dormitory")
        self.assertEqual(_circle_count(dorm, 326, 362), 6, "员工宿舍应画出 6 台空调外机")
        self.assertTrue(_has_rect(dorm, (-465.0, 20.0, -385.0, 190.0)))
        self.assertTrue(_has_rect(dorm, (315.0, 20.0, 395.0, 190.0)),
                        "员工宿舍两端应有疏散楼梯")
        beds = [rect for rect in _rects(dorm)
                if 50 <= rect[2] - rect[0] <= 55 and 38 <= rect[3] - rect[1] <= 42]
        self.assertGreaterEqual(len(beds), 10, "员工宿舍应画出成排床位")

        living = primitives("worker_living_zone")
        self.assertTrue(_has_rect(living, (-455.0, 240.0, -110.0, 330.0)))
        self.assertTrue(_has_rect(living, (-455.0, 140.0, -110.0, 230.0)),
                        "工人生活区应有宿舍排")
        self.assertTrue(_has_rect(living, (-455.0, -330.0, -110.0, 50.0)))
        self.assertTrue(_has_rect(living, (-60.0, 240.0, 455.0, 330.0)))
        self.assertTrue(_has_rect(living, (-60.0, -330.0, 455.0, 50.0)),
                        "工人生活区应含食堂、淋浴/厕所和活动场")
        dashed = [item for item in living if item[0] == "line"
                  and math.hypot(item[3] - item[1], item[4] - item[2]) <= 27
                  and (abs(item[1] - item[3]) < 0.01 or abs(item[2] - item[4]) < 0.01)]
        self.assertGreaterEqual(len(dashed), 20, "工人生活区应有可见的虚线分区")
        print("  [5/7] 员工宿舍空调/床位/双楼梯、工人生活区配套与虚线分区成立")

    def test_rotated_png_symbols_keep_circle_bounds_valid(self) -> None:
        image = Image.new("RGB", (520, 520), "#ffffff")
        draw = ImageDraw.Draw(image)
        for category in SHOWCASE.values():
            for rotation in (0, 90, 180, 270):
                self.assertTrue(draw_pictogram(draw, category, 260, 260, 360,
                                               "#1f2933", width=3, rotation=rotation),
                                (category, rotation))
        print("  [6/7] 90°/180°/270° 旋转下圆形图元包围盒有效，不触发绘制异常")

    def test_all_blocks_can_be_created_in_dxf(self) -> None:
        doc = ezdxf.new("R2010")
        created = ensure_symbol_blocks(doc)
        self.assertGreaterEqual(len(created), 30)
        for category in SHOWCASE.values():
            name = block_name(category)
            self.assertIn(name, doc.blocks)
            self.assertGreater(len(doc.blocks[name]), 10, f"{name} 的 DXF 图元为空")
        print("  [7/7] 7 类及全部 SLP_* 图块可由 ezdxf 创建且非空")


class ShowcaseCliTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = tempfile.TemporaryDirectory(prefix="facility_showcase_test_")
        cls.base = Path(cls.tmp.name)
        cls.merged = cls.base / "all.png"
        cls.items = cls.base / "items"
        cls.proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--out", str(cls.merged), "--out-dir", str(cls.items),
             "--only", ",".join(SHOWCASE)],
            cwd=str(ROOT), capture_output=True, text=True,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tmp.cleanup()

    def test_01_merged_and_seven_single_pngs(self) -> None:
        self.assertEqual(self.proc.returncode, 0,
                         msg=f"stdout={self.proc.stdout}\nstderr={self.proc.stderr}")
        self.assertGreater(self.merged.stat().st_size, 50 * 1024, "合并大样应为非空 PNG")
        with Image.open(self.merged) as image:
            self.assertEqual(image.size, (1720, 1260))
            self.assertGreater(len(image.getcolors(maxcolors=1000000) or []), 10)
        self.assertEqual(len(list(self.items.glob("facility-showcase-*.png"))), 7)
        for key in SHOWCASE:
            path = self.items / f"facility-showcase-{key}.png"
            self.assertTrue(path.is_file(), path)
            self.assertGreater(path.stat().st_size, 30 * 1024, path)
            with Image.open(path) as image:
                self.assertEqual(image.size, (1400, 1500))
                image.verify()
        print("  [附加] 合并大样与 7 张单图非空，尺寸、颜色和文件名符合约定")

    def test_02_unknown_only_key_is_rejected(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--only", "not_a_facility",
             "--out-dir", str(self.base / "invalid")],
            cwd=str(ROOT), capture_output=True, text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("未知设施键", proc.stderr)
        self.assertFalse((self.base / "invalid").exists())
        print("  [额外] 未知 --only 键在出图前拒绝执行")


if __name__ == "__main__":
    unittest.main(verbosity=2)
