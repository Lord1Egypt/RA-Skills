#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重新生成 tests/fixtures/*.json（合成数据，不含任何真实项目内容）。

用法：python3 scripts/make_fixtures.py
fixture 形态与 tests/test_municipal_qty.py 的 _payload/_legacy_chinese_payload
保持同源；改口径后重跑本脚本 + 全量单测。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS = ROOT / "scripts" / "tests"
FIXTURES = ROOT / "tests" / "fixtures"

sys.path.insert(0, str(TESTS))
from test_municipal_qty import _payload, _legacy_chinese_payload  # noqa: E402


def main() -> int:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    out = {
        "real_contract.json": _payload(),
        "legacy_chinese.json": _legacy_chinese_payload(),
        "empty_evidence.json": _payload(components=[], pipe_network=[],
                                        municipal_geometry=[], labels=[]),
        "m_unit_scale.json": _payload(
            coordinate_unit="m", unit_scale=1000,
            municipal_geometry=[
                {"type": "municipal_geometry", "category": "unclassified_municipal",
                 "system": "rainwater", "layer": "DIM_雨水", "sheet": "PS-01",
                 "geometry": [0, 0, 120, 0], "length_drawing_units": 120.0,
                 "status": "candidate"},
                {"type": "municipal_geometry", "category": "road_centerline",
                 "system": "road", "layer": "道路中线", "sheet": "DL-01",
                 "geometry": [0, 0, 0, 80], "length_drawing_units": 80.0,
                 "status": "candidate"},
            ]),
        # formal 来源却缺 contract_id：guard 3 -> 入口映射 22（契约无效）
        "forged_no_id.json": dict(
            _payload(),
            provenance="reader",
            contract_id=""),
    }
    for name, doc in out.items():
        path = FIXTURES / name
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        print("wrote %s" % path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
