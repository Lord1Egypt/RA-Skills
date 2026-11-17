#!/usr/bin/env python3
"""Independent, standard-library checks for the bundled comparison examples."""
import json
import math
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
FACTORS = {"g": ("mass", 1), "kg": ("mass", 1000), "ml": ("volume", 1), "l": ("volume", 1000), "pcs": ("count", 1)}

def compare(payload):
    target = payload["target_unit"].lower()
    dimension, target_factor = FACTORS[target]
    base = payload["items"][0]
    comparable, rejected = [], []
    for item in payload["items"]:
        unit = item["unit"].lower()
        if unit not in FACTORS or FACTORS[unit][0] != dimension:
            rejected.append((item["name"], "单位维度不同，缺少明确换算因子"))
            continue
        if item["currency"] != base["currency"]:
            rejected.append((item["name"], "币种不同，缺少汇率规则"))
            continue
        if item["shipping_included"] != base["shipping_included"]:
            rejected.append((item["name"], "运费口径不同"))
            continue
        standardized = item["quantity"] * FACTORS[unit][1] / target_factor
        comparable.append({**item, "standardized": standardized,
                           "unit_price": item["price"] / standardized * payload["display_quantity"]})
    return comparable, rejected

def main():
    success = json.loads((ROOT / "fixtures/success-input.json").read_text())
    rows, rejected = compare(success)
    assert not rejected and len(rows) == 2
    assert [round(x["unit_price"], 2) for x in rows] == [8.00, 7.00]
    assert [math.ceil(success["demand_quantity"] / x["standardized"]) for x in rows] == [3, 2]

    failed = json.loads((ROOT / "fixtures/failure-input.json").read_text())
    rows, rejected = compare(failed)
    assert len(rows) == 0 and len(rejected) == 2
    assert "单位维度不同" in rejected[0][1] and "币种不同" in rejected[1][1]
    failure_output = (ROOT / "fixtures/failure-output.md").read_text()
    assert "2026-10-04" in failure_output and "含运费" in failure_output, "failure delivery must preserve price date and shipping basis"
    for path in ("SKILL.md", "manifest.yaml", "agents/openai.yaml", "fixtures/success-output.md", "fixtures/failure-output.md"):
        assert (ROOT / path).is_file(), path
    ui = (ROOT / "agents/openai.yaml").read_text()
    manifest = (ROOT / "manifest.yaml").read_text()
    assert 'default_prompt: "' in ui and "$shop-pack-unit-price-compare-cn" in ui
    assert 'default_prompt: 使用 $shop-pack-unit-price-compare-cn' in manifest
    assert 'icon_small: "./icon-512.png"' in ui and 'icon_large: "./icon-512.png"' in ui
    for image, expected in ((ROOT / "icon-512.png", (512, 512)), (ROOT / "assets/promo-1600x900.png", (1600, 900))):
        data = image.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n", image
        assert struct.unpack(">II", data[16:24]) == expected, image
    print("PASS: success case calculates CNY 8.00 and 7.00 per 100 g with 3 and 2 packs")
    print("PASS: failure case refuses mass-volume and cross-currency ranking")

if __name__ == "__main__":
    main()
