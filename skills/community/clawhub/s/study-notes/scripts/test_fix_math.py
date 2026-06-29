#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Self-contained tests for fix_math.py — the naked-Unicode-in-math repair tool.

Run:  python scripts/test_fix_math.py
"""
import fix_math as fx
import build_and_check as b


def run():
    # 1. degree OUTSIDE \text -> {}^\circ  (e.g. $17\,°\text{C}$ -> $17\,{}^\circ\text{C}$)
    src = r"<div class=\"fbox\">$17\,°\text{C}$</div>"
    fixed, n = fx.fix_html(src)
    assert n == 1 and r"{}^\circ" in fixed and "°" not in fixed, fixed

    # 2. middot INSIDE \text must break the text group, not sit literally inside it
    src = r"<p>$C=20.8\,\text{J/(mol·K)}$</p>"
    fixed, n = fx.fix_html(src)
    assert r"\text{J/(mol}\cdot\text{K)}" in fixed, fixed
    assert "·" not in fixed

    # 3. prose Unicode OUTSIDE math is left untouched (only math spans are rewritten)
    src = "<p>温度约 20°C，单位 J·mol⁻¹。</p>"  # no $...$ here
    fixed, n = fx.fix_html(src)
    assert n == 0 and fixed == src, fixed

    # 4. result is checker-clean and idempotent
    src = r"<p>$\theta=45°$ and $P=\text{W·m}^{-2}$ and $\Delta=-5$</p>".replace("-5", "−5")
    fixed, _ = fx.fix_html(src)
    assert not b.check_unicode_in_math(fixed), b.check_unicode_in_math(fixed)
    again, n2 = fx.fix_html(fixed)
    assert n2 == 0 and again == fixed, "fix must be idempotent"

    print("OK  fix_math regression tests passed (4/4)")


if __name__ == "__main__":
    run()
