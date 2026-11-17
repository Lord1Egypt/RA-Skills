#!/usr/bin/env python3
"""test_render_security.py — 渲染器安全回归测试。

覆盖 visual_system 各颜色 token（accent/ink/paper/muted）的注入面：闭合 <style>
标签、SVG 属性 breakout、CSS 外链 payload、非法颜色名、非字符串值。
合法十六进制颜色应正常通过，且产物必须带 CSP、不含 <script>、不含外链。
另覆盖全部 palette preset（含 v1.3.0 新增 editorial/technical/warm）的渲染烟测。
"""
import json
import sys

import render_infographic_html as R


def _plan(vs_overrides):
    return {
        "version": "1.0",
        "meta": {"title": "安全测试"},
        "layout": "dashboard",
        "visual_system": vs_overrides,
        "blocks": [
            {"id": "a", "title": "指标A", "value": "10", "unit": "个",
             "metric": "销量", "time": "本周"},
            {"id": "b", "title": "指标B", "value": "20", "unit": "个",
             "metric": "营收", "time": "本周"},
        ],
    }


BAD_VALUES = [
    ("</style><script>alert(1)</script>", "闭合 style 标签注入"),
    ('" onload="alert(1)', "SVG 属性 breakout"),
    ('red;background:url(https://evil.example/x)', "CSS 外链 payload"),
    ('url(javascript:alert(1))', "CSS javascript: URL"),
    ('red', "非十六进制颜色名"),
    ('#GGGGGG', "非法 hex 字符"),
    ('#12345', "非法长度（5 位）"),
    (123456, "非字符串（数字）"),
]

GOOD_ACCENTS = [
    ("#C96F4A", "#RRGGBB"),
    ("#c96f4a", "#rrggbb 小写"),
    ("#F0A", "#RGB 简写"),
]


def main():
    failures = 0

    # 每个 token 字段都要挡住全部注入 payload（v1.3.0：ink/paper/muted 与 accent 同边界）
    for field in ("accent", "ink", "paper", "muted"):
        for bad, label in BAD_VALUES:
            try:
                R.render_html(_plan({field: bad}))
            except ValueError:
                print(f"✅ 拒绝注入 [{field}/{label}]: {bad!r}")
            except Exception as e:  # noqa: BLE001
                print(f"✅ 拒绝注入 [{field}/{label}]（异常 {type(e).__name__}）: {bad!r}")
            else:
                failures += 1
                print(f"❌ 未拦截注入 [{field}/{label}]: {bad!r}")

    for accent, label in GOOD_ACCENTS:
        try:
            html = R.render_html(_plan({"accent": accent}))
        except Exception as e:  # noqa: BLE001
            failures += 1
            print(f"❌ 合法颜色被误拒 [{label}]: {accent!r} -> {e}")
            continue
        csp_ok = 'Content-Security-Policy' in html
        no_script = '<script' not in html.lower()
        no_ext = 'http://' not in html and 'https://' not in html
        print(f"✅ 合法颜色通过 [{label}]: {accent!r} "
              f"(CSP={csp_ok}, 无script={no_script}, 无外链={no_ext})")
        if not (csp_ok and no_script and no_ext):
            failures += 1

    # None / 缺失 accent 应安全回退默认配色，不抛错、不注入
    for accent in (None, ""):
        try:
            html = R.render_html(_plan({"accent": accent}))
        except Exception as e:  # noqa: BLE001
            failures += 1
            print(f"❌ 空 accent 处理异常: {accent!r} -> {e}")
            continue
        safe = 'None' not in html and '<script' not in html.lower()
        print(f"✅ 空 accent 安全回退: {accent!r} (无注入={safe})")
        if not safe:
            failures += 1

    # 全部 preset 烟测（含 v1.3.0 新增三个）
    for palette in sorted(R.PALETTES):
        try:
            html = R.render_html(_plan({"palette": palette}))
        except Exception as e:  # noqa: BLE001
            failures += 1
            print(f"❌ preset {palette} 渲染失败: {e}")
            continue
        ok = ('<script' not in html.lower()
              and 'http://' not in html and 'https://' not in html)
        print(f"✅ preset {palette} 渲染正常 (无script/无外链={ok})")
        if not ok:
            failures += 1

    # token 覆盖 + preset 组合：paper/ink/muted 覆盖应落到产物 CSS
    try:
        html = R.render_html(_plan({"palette": "editorial", "paper": "#FFF8EE"}))
        if "#FFF8EE" in html or "#fff8ee" in html.lower():
            print("✅ token 覆盖生效 [paper@editorial]: #FFF8EE")
        else:
            failures += 1
            print("❌ token 覆盖未生效 [paper@editorial]")
    except Exception as e:  # noqa: BLE001
        failures += 1
        print(f"❌ token 覆盖异常 [paper@editorial]: {e}")

    print(f"\n{'通过' if failures == 0 else '失败'}: {failures} 项未通过")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
