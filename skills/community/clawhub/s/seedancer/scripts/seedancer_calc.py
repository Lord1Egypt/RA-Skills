#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""seedancer_calc.py — 硬门的确定性计算器（零依赖，Python 3.8+）

SKILL.md 里的几道硬门（台词容量预检、分组时长上限、镜头密度 Smin/Gmax）都是**可计算的公式**，
但此前只能靠模型"心算"。心算是最容易出错、也最难复核的一环 —— 本脚本把公式落成代码，
让 Agent 在写分镜前先跑一遍，得到可复核的数字。

公式来源（以 SKILL.md 为准，改公式请两侧同改）：
  · 台词容量预检：最低时长 = 可发声汉字 ÷ 语速 + 标点停顿 + 反应留白
  · 分组硬门：按模型的单次最大时长
  · 镜头密度：Smin(T) = ceil(T × base15 / 15)；Gmax 按档位

用法：
  python scripts/seedancer_calc.py smin 12 ordinary
  python scripts/seedancer_calc.py dialogue "你终于来了。我等了整整三年……" --pace slow
  python scripts/seedancer_calc.py check-group --model seedance-2.0 --duration 12 \
      --type ordinary --shots 5 --line "你终于来了。" --line "嗯。"
  python scripts/seedancer_calc.py models
  （任一子命令加 --json 输出机器可读结果）

退出码：0 = 通过 / 纯计算；1 = 硬门未通过；2 = 参数错误
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys

# ---- 与 SKILL.md「分组硬门 · 时长上限（按模型）」一致 ----
MODEL_LIMITS = {
    "seedance-2.0": 15,
    "seedance-2.5": 30,
    "kling-3.0": 15,
    "veo-3": 8,
}
MODEL_ALIASES = {
    "seedance2": "seedance-2.0", "seedance-2": "seedance-2.0", "seedance2.0": "seedance-2.0",
    "seedance2.5": "seedance-2.5", "kling3": "kling-3.0", "kling-3": "kling-3.0",
    "kling3.0": "kling-3.0", "veo3": "veo-3",
}

# ---- 与 SKILL.md「镜头密度四道门 · 短漫剧三档」一致 ----
DENSITY = {
    "ordinary": {"base15": 6, "gmax": 3.0},
    "action_reversal": {"base15": 8, "gmax": 2.5},
    "fight": {"base15": 10, "gmax": 2.0},
}

# ---- 与 SKILL.md「台词容量预检系统 · 最低时长公式」一致（字/秒） ----
PACES = {
    "slow": (2.5, 3.2),     # 慢速压抑：恐惧、迟疑、压抑、真相揭示、告别
    "calm": (3.0, 3.8),     # 冷静克制：低声、从容威胁、冷硬问句
    "normal": (3.3, 4.2),   # 正常对白
    "fast": (4.3, 5.2),     # 快速急促：争吵、催促、慌乱
}
PAUSE_COMMA = (0.20, 0.35)
PAUSE_END = (0.35, 0.60)
PAUSE_LONG_EXTRA = (0.5, 2.0)    # 省略号 / 破折号 / 告别句 / 真相揭示
DEFAULT_ACTION_RESERVE = 3.0      # 每组默认预留必要动作时间

COMMA_CHARS = "，,、：:"
END_CHARS = "。！？!?；;"
LONG_RE = re.compile(r"……|…|——|—{2,}|\.{3,}")
VOICED_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]|[A-Za-z0-9]")


class UsageError(Exception):
    pass


def normalize_model(name: str) -> str:
    key = name.strip().lower().replace(" ", "-").replace("_", "-")
    key = MODEL_ALIASES.get(key.replace("-", ""), MODEL_ALIASES.get(key, key))
    if key not in MODEL_LIMITS:
        raise UsageError("未知模型：%s（可选：%s）" % (name, "、".join(MODEL_LIMITS)))
    return key


def smin(duration: int, kind: str) -> int:
    if kind not in DENSITY:
        raise UsageError("未知密度档位：%s（可选：%s）" % (kind, "、".join(DENSITY)))
    if duration <= 0:
        raise UsageError("组时长必须为正整数秒")
    # 整数运算避免浮点误差：ceil(T*base/15)
    return -(-duration * DENSITY[kind]["base15"] // 15)


def dialogue_cost(text: str, pace: str) -> dict:
    """返回一句（或一段）台词的最低时长区间（秒）。

    lower = 最快语速 + 最短停顿；upper = 最慢语速 + 最长停顿。
    规划时以 **upper** 为准（保守：宁可拆组，不可压语速）。
    """
    if pace not in PACES:
        raise UsageError("未知语速档：%s（可选：%s）" % (pace, "、".join(PACES)))
    voiced = len(VOICED_RE.findall(text))
    long_marks = len(LONG_RE.findall(text))
    stripped = LONG_RE.sub("", text)
    commas = sum(stripped.count(c) for c in COMMA_CHARS)
    ends = sum(stripped.count(c) for c in END_CHARS)
    lo_rate, hi_rate = PACES[pace]
    lower = (voiced / hi_rate + commas * PAUSE_COMMA[0] + ends * PAUSE_END[0]
             + long_marks * PAUSE_LONG_EXTRA[0])
    upper = (voiced / lo_rate + commas * PAUSE_COMMA[1] + ends * PAUSE_END[1]
             + long_marks * PAUSE_LONG_EXTRA[1])
    return {
        "text": text, "pace": pace, "voiced_chars": voiced,
        "commas": commas, "sentence_ends": ends, "long_pauses": long_marks,
        "min_seconds_lower": round(lower, 2), "min_seconds_upper": round(upper, 2),
    }


def check_group(model: str, duration: int, kind: str, shots, lines, pace: str,
                reserve: float, visual_read: float) -> dict:
    model = normalize_model(model)
    limit = MODEL_LIMITS[model]
    need_shots = smin(duration, kind)
    costs = [dialogue_cost(l, pace) for l in lines]
    dlg_upper = round(sum(c["min_seconds_upper"] for c in costs), 2)
    load = round(dlg_upper + visual_read + reserve, 2)
    gates = []
    gates.append({"gate": "分组时长上限", "ok": duration <= limit,
                  "detail": "组时长 %ds（%s 上限 %ds）" % (duration, model, limit)})
    gates.append({"gate": "台词容量预检", "ok": load <= duration,
                  "detail": "口型台词 %.2fs + 视觉读取 %.2fs + 动作预留 %.2fs = %.2fs（须 ≤ 组时长 %ds）"
                            % (dlg_upper, visual_read, reserve, load, duration)})
    if shots is not None:
        gates.append({"gate": "镜头数 ≥ Smin", "ok": shots >= need_shots,
                      "detail": "编号镜头 %d 个（须 ≥ Smin(%d, %s) = %d）" % (shots, duration, kind, need_shots)})
    ok = all(g["ok"] for g in gates)
    advice = []
    if not gates[0]["ok"]:
        advice.append("组时长超过模型上限：按场景/时间跳跃或动作目标断点拆组。")
    if not gates[1]["ok"]:
        advice.append("台词超载：在原文「。！？；」优先、其次「，」处拆段；禁止靠加快语速修补。")
    if shots is not None and shots < need_shots:
        advice.append("镜头数不足：补足有新反馈的编号镜头，而不是只换景别/运镜。")
    return {
        "model": model, "model_limit": limit, "duration": duration, "density": kind,
        "smin": need_shots, "gmax": DENSITY[kind]["gmax"], "pace": pace,
        "dialogue": costs, "dialogue_upper_total": dlg_upper, "load": load,
        "gates": gates, "ok": ok, "advice": advice,
    }


def _emit(obj, as_json: bool, human) -> None:
    if as_json:
        print(json.dumps(obj, ensure_ascii=False, indent=2))
    else:
        human(obj)


def _print_group(r):
    print("模型 %s（上限 %ds）｜组时长 %ds｜档位 %s｜Smin=%d｜Gmax=%.1fs"
          % (r["model"], r["model_limit"], r["duration"], r["density"], r["smin"], r["gmax"]))
    for c in r["dialogue"]:
        print("  台词「%s」：%d 字 → %.2f–%.2fs" % (c["text"], c["voiced_chars"],
                                              c["min_seconds_lower"], c["min_seconds_upper"]))
    for g in r["gates"]:
        print("[%s] %s — %s" % ("OK  " if g["ok"] else "FAIL", g["gate"], g["detail"]))
    for a in r["advice"]:
        print("  → " + a)
    print("RESULT: %s" % ("PASS" if r["ok"] else "FAIL"))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="seedancer_calc", description="Seedancer 硬门计算器")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("smin", help="计算镜头数硬下限 Smin")
    s.add_argument("duration", type=int)
    s.add_argument("type", nargs="?", default="ordinary", choices=sorted(DENSITY))
    s.add_argument("--json", action="store_true")

    d = sub.add_parser("dialogue", help="计算台词最低时长")
    d.add_argument("text")
    d.add_argument("--pace", default="normal", choices=sorted(PACES))
    d.add_argument("--json", action="store_true")

    g = sub.add_parser("check-group", help="对一组分镜跑时长 / 台词容量 / Smin 三道硬门")
    g.add_argument("--model", required=True)
    g.add_argument("--duration", type=int, required=True)
    g.add_argument("--type", default="ordinary", choices=sorted(DENSITY))
    g.add_argument("--shots", type=int)
    g.add_argument("--line", action="append", default=[], help="一句口型台词（可重复）")
    g.add_argument("--pace", default="normal", choices=sorted(PACES))
    g.add_argument("--reserve", type=float, default=DEFAULT_ACTION_RESERVE,
                   help="动作反应预留秒数（默认 3）")
    g.add_argument("--visual-read", type=float, default=0.0,
                   help="屏幕/短信等视觉读取所需秒数（不产生口型）")
    g.add_argument("--json", action="store_true")

    m = sub.add_parser("models", help="列出模型分组时长上限")
    m.add_argument("--json", action="store_true")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "smin":
            n = smin(args.duration, args.type)
            obj = {"duration": args.duration, "type": args.type, "smin": n,
                   "gmax": DENSITY[args.type]["gmax"]}
            _emit(obj, args.json, lambda o: print("Smin(%ds, %s) = %d；Gmax = %.1fs"
                                                  % (o["duration"], o["type"], o["smin"], o["gmax"])))
            return 0
        if args.cmd == "dialogue":
            c = dialogue_cost(args.text, args.pace)
            _emit(c, args.json, lambda o: print(
                "%d 个可发声字，%d 逗号停顿，%d 句末停顿，%d 长停顿 → 最低 %.2f–%.2fs（规划取 %.2fs）"
                % (o["voiced_chars"], o["commas"], o["sentence_ends"], o["long_pauses"],
                   o["min_seconds_lower"], o["min_seconds_upper"], o["min_seconds_upper"])))
            return 0
        if args.cmd == "check-group":
            r = check_group(args.model, args.duration, args.type, args.shots, args.line,
                            args.pace, args.reserve, args.visual_read)
            _emit(r, args.json, _print_group)
            return 0 if r["ok"] else 1
        if args.cmd == "models":
            _emit(MODEL_LIMITS, args.json,
                  lambda o: [print("%-14s %2ds" % kv) for kv in o.items()])
            return 0
    except UsageError as e:
        print("参数错误：%s" % e, file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
