#!/usr/bin/env python3
"""site-layout-plan 0.6.7 · R12 看图版导出回归测试。

覆盖 CAD快速看图（macOS）黑屏的三个根因：
1. 只认 R12（AC1009）；
2. 不自动 zoom-extents，必须写 VPORT *Active 中心/高度；
3. 工程坐标（5e8/4e9 级）必须平移到原点并把偏移写进 $USERR1/2。
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORT_CLI = ROOT / "scripts" / "dxf_view_export.py"
ALLOWED = {"LINE", "POLYLINE", "CIRCLE", "ARC", "POINT", "SOLID", "TEXT", "INSERT"}

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from site_layout.bootstrap import ensure_runtime  # noqa: E402

ensure_runtime(__file__)

import ezdxf  # noqa: E402


def build_source(path: Path) -> None:
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()
    ox, oy = 519010512.5, 4065695798.9  # 实测工程坐标量级
    msp.add_line((ox, oy), (ox + 200000, oy + 80000))
    msp.add_lwpolyline([(ox, oy), (ox + 50000, oy), (ox + 50000, oy + 30000)],
                       close=True)
    msp.add_circle((ox + 30000, oy + 20000), 2500)
    msp.add_arc((ox + 60000, oy + 20000), 1500, 0, 90)
    msp.add_text("塔吊 TC-01", dxfattribs={"height": 2500, "style": "Standard"}
                 ).set_placement((ox + 10000, oy + 40000))
    msp.add_mtext("施工电梯\\P双笼", dxfattribs={"char_height": 2000}
                  ).set_location((ox + 12000, oy + 50000))
    blk = doc.blocks.new("SLP_TEST")
    blk.add_line((-500, -500), (500, 500))
    blk.add_circle((0, 0), 300)
    msp.add_blockref("SLP_TEST", (ox + 70000, oy + 30000))
    dim = msp.add_linear_dim(base=(ox, oy - 10000), p1=(ox, oy), p2=(ox + 200000, oy),
                             dimstyle="Standard")
    dim.render()
    doc.saveas(str(path))


class DxfViewExportTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="slp_r12_test_")
        self.base = Path(self.tmp.name)
        self.src = self.base / "source.dxf"
        build_source(self.src)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_01_r12_view_export(self) -> None:
        out = self.base / "source-r12.dxf"
        proc = subprocess.run(
            [sys.executable, str(EXPORT_CLI), str(self.src), "-o", str(out)],
            cwd=str(ROOT), capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        self.assertTrue(out.is_file())

        doc = ezdxf.readfile(str(out))
        self.assertEqual(doc.dxfversion, "AC1009")
        types = {e.dxftype() for e in doc.modelspace()}
        self.assertLessEqual(types, ALLOWED, f"R12 看图版含不兼容实体: {types}")
        self.assertNotIn("DIMENSION", types)
        self.assertNotIn("MTEXT", types)
        self.assertNotIn("LWPOLYLINE", types)

        auditor = doc.audit()
        self.assertEqual(len(auditor.errors), 0, msg=[str(e) for e in auditor.errors])

        ext_min = tuple(float(v) for v in doc.header["$EXTMIN"])
        ext_max = tuple(float(v) for v in doc.header["$EXTMAX"])
        self.assertTrue(all(abs(v) < 1e12 for v in ext_min + ext_max))
        # 平移后应从原点附近开始
        self.assertLess(abs(ext_min[0]), 1e5)
        self.assertLess(abs(ext_min[1]), 1e5)
        # 偏移量记录在 USERR 变量，量测时可回算
        self.assertGreater(doc.header["$USERR1"], 5e8)
        self.assertGreater(doc.header["$USERR2"], 4e9)

        # 视图必须对准图形：CAD快速看图不自动 zoom-extents
        vp = doc.viewports.get("*Active")[0]
        cx, cy = float(vp.dxf.center[0]), float(vp.dxf.center[1])
        self.assertAlmostEqual(cx, (ext_min[0] + ext_max[0]) / 2, delta=1.0)
        self.assertAlmostEqual(cy, (ext_min[1] + ext_max[1]) / 2, delta=1.0)
        self.assertGreaterEqual(float(vp.dxf.height), ext_max[1] - ext_min[1])
        print("  [1/1] R12 导出：类型={} 视图中心=({:.0f},{:.0f}) 高度={:.0f}".format(
            sorted(types), cx, cy, float(vp.dxf.height)))

    def test_02_dimension_block_kept(self) -> None:
        out = self.base / "dim-r12.dxf"
        proc = subprocess.run(
            [sys.executable, str(EXPORT_CLI), str(self.src), "-o", str(out)],
            cwd=str(ROOT), capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        doc = ezdxf.readfile(str(out))
        refs = [e for e in doc.modelspace() if e.dxftype() == "INSERT"]
        self.assertGreaterEqual(len(refs), 2, "尺寸几何块与符号块都应保留")
        doc.audit()
        print("  [2/2] 标注转几何块：INSERT={}".format(len(refs)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
