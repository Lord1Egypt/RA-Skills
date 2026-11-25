#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RoutePilot route cost calculator (Python standard library only).

Compares 2-6 driving routes on one total-cost basis:
fuel + toll + time cost + fatigue cost + travel-time risk premium.

Usage:
    python route_cost.py --demo
    python route_cost.py --json input.json
    python route_cost.py            # reads JSON from stdin

Input JSON:
{
  "params": {
    "consumption_l_per_100km": 7.5,
    "fuel_price_cny_per_l": 7.60,
    "time_value_cny_per_hour": 60,
    "weight_sum": 1.9,
    "fatigue_free_min": 120,
    "fatigue_k": 0.3,
    "fatigue_multiplier": 1.0,
    "variance_z": 0.5,
    "holiday_free": false,
    "deadline_min": null
  },
  "routes": [
    {"name": "expressway", "distance_km": 118, "time_min": 78,
     "toll_cny": 46, "lights": 12, "time_min_slow": 92},
    {"name": "national-road", "distance_km": 103, "time_min": 112,
     "toll_cny": 0, "lights": 31, "time_min_slow": 133}
  ]
}

Exit codes: 0 ok, 2 input error.
"""

from __future__ import annotations

import json
import sys

DEFAULTS = {
    "consumption_l_per_100km": 7.5,
    "fuel_price_cny_per_l": None,
    "time_value_cny_per_hour": 36.0,
    "weight_sum": 1.0,
    "fatigue_free_min": 120.0,
    "fatigue_k": 0.3,
    "fatigue_multiplier": 1.0,
    "variance_z": 0.5,
    "holiday_free": False,
    "deadline_min": None,
}

NO_TOLL_RATIO = 4.5   # min/km, fuel-only break-even
TOLL_RATIO = 7.5      # min/km, with toll
FATIGUE_FREE_RATIO = 2.4
CRUISE_RATIO = 1.5


def merged_params(raw: dict) -> dict:
    p = dict(DEFAULTS)
    p.update({k: v for k, v in (raw or {}).items() if v is not None})
    if p["fuel_price_cny_per_l"] is None:
        raise ValueError("params.fuel_price_cny_per_l is required "
                         "(use the pump price on the travel day)")
    return p


def value_per_min(p: dict) -> float:
    """Effective value of one in-car minute, CNY."""
    return p["time_value_cny_per_hour"] / 60.0 * p["weight_sum"]


def score(route: dict, p: dict) -> dict:
    d = float(route["distance_km"])
    t = float(route["time_min"])
    toll = 0.0 if p["holiday_free"] else float(route.get("toll_cny") or 0.0)
    v = value_per_min(p)

    fuel = d / 100.0 * p["consumption_l_per_100km"] * p["fuel_price_cny_per_l"]
    time_cost = t * v
    over = max(0.0, t - p["fatigue_free_min"])
    fatigue = over * v * p["fatigue_k"] * p["fatigue_multiplier"]

    slow = route.get("time_min_slow")
    if slow is None:
        variance = 0.0
        sigma = 0.0
    else:
        sigma = max(0.0, (float(slow) - t) / 2.0)
        variance = sigma * p["variance_z"] * v

    total = fuel + toll + time_cost + fatigue + variance
    rhythm = t / d if d else float("inf")
    return {
        "name": route.get("name") or "route",
        "distance_km": d,
        "time_min": t,
        "toll": toll,
        "lights": int(route.get("lights") or 0),
        "light_density": (int(route.get("lights") or 0) / d) if d else 0.0,
        "fuel": fuel,
        "time_cost": time_cost,
        "fatigue": fatigue,
        "variance": variance,
        "total": total,
        "rhythm": rhythm,
        "sigma": sigma,
        "v_per_min": v,
    }


def money(x: float) -> str:
    return "%.2f" % x


def fmt_rhythm(x: float) -> str:
    return "%.2f" % x


def pair_verdict(fast: dict, short: dict, p: dict) -> list:
    """Threshold rules applied to the fastest vs the shortest route."""
    lines = []
    ds = fast["distance_km"] - short["distance_km"]
    dt = short["time_min"] - fast["time_min"]
    v = fast["v_per_min"]

    if abs(ds) < 0.1:
        lines.append("- 两条路线里程差 <0.1km，ΔT/ΔS 不适用；按总成本与红绿灯数决胜。")
    else:
        ratio = dt / ds
        limit = NO_TOLL_RATIO if abs(fast["toll"] - short["toll"]) < 0.5 else TOLL_RATIO
        lines.append("- ΔT/ΔS = %s/%s = %s min/km，阈值 %s min/km；"
                     "油耗维度指向：%s。"
                     % ("%+.0f" % dt, money(ds), fmt_rhythm(ratio),
                        money(limit), "快路线" if ratio > limit else "短路"))
    if abs(fast["rhythm"] - short["rhythm"]) < 0.15:
        lines.append("- 节奏差 %s min/km < 0.15，油耗维度失效，改比红绿灯数。"
                     % fmt_rhythm(abs(fast["rhythm"] - short["rhythm"])))
    if short["rhythm"] > FATIGUE_FREE_RATIO and fast["rhythm"] < CRUISE_RATIO:
        lines.append("- R1 触发：短路线节奏 %s > 2.4 且快路线 %s < 1.5，存在跨区红利。"
                     % (fmt_rhythm(short["rhythm"]), fmt_rhythm(fast["rhythm"])))

    extra_cash = (fast["toll"] - short["toll"]) + (fast["fuel"] - short["fuel"])
    if abs(dt) > 0.1:
        per_min = extra_cash / dt
        lines.append("- 净每分钟成本 =（过路费差 ¥%s + 油费差 ¥%s）÷ ΔT = ¥%s/min；"
                     "有效时间价值 ¥%s/min，比值 %.2f。"
                     % (money(fast["toll"] - short["toll"]),
                        money(fast["fuel"] - short["fuel"]),
                        money(per_min), money(v), (per_min / v) if v else float("nan")))
        if v:
            k = per_min / v
            if k <= 0.5:
                verdict = "必买时间（比值 <0.5）"
            elif k <= 1.0:
                verdict = "倾向买时间（比值 0.5–1.0）"
            elif k <= 1.5:
                verdict = "看是否赶时间（比值 1.0–1.5）"
            else:
                verdict = "走短路线（比值 >1.5）"
            lines.append("- 按比值分档：%s。" % verdict)

    light_diff = abs(fast["lights"] - short["lights"])
    if light_diff and dt > 0 and light_diff * 0.5 > dt:
        lines.append("- R5 触发：灯差 %d × 0.5min = %.1fmin > 时间优势 %smin，改选灯少者。"
                     % (light_diff, light_diff * 0.5, money(dt)))
    return lines


def report(payload: dict) -> str:
    p = merged_params(payload.get("params") or {})
    raw_routes = payload.get("routes") or []
    if len(raw_routes) < 2:
        raise ValueError("at least two routes are required for a comparison")
    rows = [score(r, p) for r in raw_routes]
    rows.sort(key=lambda r: r["total"])

    out = []
    out.append("| 路线 | 里程 km | 时长 min | 节奏 min/km | 灯/km | 油费 | 过路费 | 时间成本 | 疲劳 | 风险溢价 | 合计 |")
    out.append("|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
    for r in rows:
        out.append("| %s | %.0f | %.0f | %s | %.2f | %s | %s | %s | %s | %s | **%s** |"
                   % (r["name"], r["distance_km"], r["time_min"], fmt_rhythm(r["rhythm"]),
                      r["light_density"], money(r["fuel"]), money(r["toll"]),
                      money(r["time_cost"]), money(r["fatigue"]),
                      money(r["variance"]), money(r["total"])))

    best, second = rows[0], rows[1]
    diff = second["total"] - best["total"]
    pct = diff / best["total"] * 100.0 if best["total"] else 0.0
    out.append("")
    out.append("**推荐：%s**，合计 ¥%s；次优 %s 为 ¥%s，差额 ¥%s（%.1f%%）。"
               % (best["name"], money(best["total"]), second["name"],
                  money(second["total"]), money(diff), pct))
    if pct < 3.0:
        out.append("差额 <3%%，判为等价；改用红绿灯数与到达可靠性决胜，不硬造胜者。")
    out.append("")
    out.append("参数：油耗 %s L/100km，油价 ¥%s/L，单人时间价值 ¥%s/小时，乘员权重和 %s，"
               "有效时间价值 ¥%s/min，免费通行 %s。"
               % (p["consumption_l_per_100km"], money(p["fuel_price_cny_per_l"]),
                  money(p["time_value_cny_per_hour"]), p["weight_sum"],
                  money(value_per_min(p)), "是" if p["holiday_free"] else "否"))

    fast = min(rows, key=lambda r: r["time_min"])
    short = min(rows, key=lambda r: r["distance_km"])
    if fast["name"] != short["name"]:
        out.append("")
        out.append("规则族交叉验证（快路线 %s vs 短路线 %s）：" % (fast["name"], short["name"]))
        out.extend(pair_verdict(fast, short, p))

    deadline = p.get("deadline_min")
    if deadline:
        for r in rows:
            slack = float(deadline) - r["time_min"]
            out.append("- 到达余量：%s 剩 %smin（含风险 σ=%.0fmin）。"
                       % (r["name"], money(slack), r["sigma"]))
    out.append("")
    out.append("口径：所有金额为当日实价代入后的结果；油价、费率、免费政策以出行当日实际为准。")
    return "\n".join(out)


DEMO = {
    "params": {
        "consumption_l_per_100km": 7.5,
        "fuel_price_cny_per_l": 7.60,
        "time_value_cny_per_hour": 60,
        "weight_sum": 1.9,
        "holiday_free": False,
    },
    "routes": [
        {"name": "A 高速优先", "distance_km": 118, "time_min": 78, "toll_cny": 46,
         "lights": 12, "time_min_slow": 92},
        {"name": "B 国道优先", "distance_km": 103, "time_min": 112, "toll_cny": 0,
         "lights": 31, "time_min_slow": 133},
    ],
}


def main(argv: list) -> int:
    try:
        if "--demo" in argv:
            payload = DEMO
        elif "--json" in argv:
            path = argv[argv.index("--json") + 1]
            with open(path, "r", encoding="utf-8") as fh:
                payload = json.load(fh)
        else:
            payload = json.load(sys.stdin)
        print(report(payload))
        return 0
    except Exception as exc:  # noqa: BLE001 - CLI must fail with a readable message
        print("input error: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
