#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
figure-bridge.py — reading-notes-master v2.9.1
把本机 academic-figures v5.9.0 的 38 种科研图型接进读书笔记版式流程。
v2.9：所有图型图表**默认 4K 级输出**（位图长边 ≥3840px 且短边 ≥2160px；
矢量 PDF/SVG/EPS 天然等效），渲染前自动换算 DPI、渲染后按 PNG IHDR 实测像素并硬门禁。

纯标准库实现；本脚本可用任意 python3 运行，但**调用引擎时自动探测带
matplotlib/numpy/scipy/pymupdf 的系统 python**（WorkBuddy 内置 python 缺这些依赖）。

用法：
  python3 scripts/figure-bridge.py --check
  python3 scripts/figure-bridge.py --list types|themes|journals
  python3 scripts/figure-bridge.py --type bar --data assets/data/ch01.json \
      --out assets/fig/ch01 --theme okabe-ito --journal nature --column double \
      --formats pdf,png --verify --alt --caption --title "第一章要点"
  python3 scripts/figure-bridge.py --pipeline assets/figures.yaml --verify

退出码：0 成功｜3 数据契约校验失败｜4 环境/依赖失败｜其余透传引擎退出码
（引擎：1 参数/致命校验｜2 verify 重叠或批量失败｜3 数据｜4 环境｜5 超时｜6 内存护栏）。
设计契约见 references/academic-chart-system.md §5 / §7。
"""

import argparse
import hashlib
import json
import math
import os
import re
import struct
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
ENGINE_CANDIDATES = [
    HOME / ".workbuddy/skills/academic-figures",   # ClawHub 发布包（含 pitfalls.md）
    HOME / ".openclaw/skills/academic-figures",    # GitHub tag v5.9.0 完整源码
]
PY_CANDIDATES = [
    "/opt/homebrew/bin/python3",
    "/usr/bin/python3",
    "/usr/local/bin/python3",
    sys.executable,
]
DEPS = ("matplotlib", "numpy", "scipy", "pymupdf")
FORMATS = ("png", "svg", "pdf", "tiff", "eps")
BITMAP_FORMATS = ("png", "tiff")
VECTOR_FORMATS = ("pdf", "svg", "eps")

# ---- v2.9 4K 门禁 ----
UHD_LONG = 3840          # 4K UHD 长边
UHD_SHORT = 2160         # 4K UHD 短边
UHD_PIXELS = UHD_LONG * UHD_SHORT   # 8,294,400
DEFAULT_DPI = 600        # 引擎线条图默认
MAX_DPI = 2000           # 上限，防内存护栏把 dpi 砍半后仍不死循环

# 主题默认画幅（英寸），用于反推达标 DPI；与引擎 gen_figure.py:THEMES 一致
THEME_FIGSIZE = {
    "glm": (10, 6), "glm-brand": (10, 6), "classic": (10, 6),
    "okabe-ito": (8, 5.5), "okabe": (8, 5.5), "colorblind": (8, 5.5),
    "nature": (8, 5.5), "npg": (8, 5.5), "science": (8, 5.5), "aaas": (8, 5.5),
    "cool": (9, 5.5), "conservative": (9, 5.5),
    "lancet": (9, 6), "nejm": (9, 6),
}

# 38 图型的必填字段（引擎 references/data-formats.md 权威；此处为渲染前闸门）
REQUIRED = {
    "bar": ("labels", "series"), "grouped_bar": ("labels", "series"),
    "hbar": ("labels", "series"), "horizontal_bar": ("labels", "series"),
    "stacked_bar": ("labels", "series"), "stacked": ("labels", "series"),
    "box": ("labels", "series"), "boxplot": ("labels", "series"),
    "violin": ("labels", "series"), "raincloud": ("labels", "series"),
    "ridgeline": ("labels", "datasets"),
    "paired": ("before", "after"), "slope": ("items",),
    "dumbbell": ("from", "to"), "line": ("labels", "series"),
    "scatter": ("x", "y"), "dual_axis": ("left", "right"),
    "heatmap": ("matrix",), "cluster_heatmap": ("matrix",), "pca": ("matrix",),
    "venn": ("sets",), "upset": ("sets",), "volcano": ("log2fc", "pvalue"),
    "forest": ("labels", "estimates", "ci_low", "ci_high"),
    "subgroup": ("subgroups",), "funnel": ("studies",), "galbraith": ("studies",),
    "km": ("groups",), "survival": ("groups",), "cif": ("time", "event"),
    "rmst": ("groups",), "roc": ("fpr", "tpr"),
    "calibration": (),  # bins[] 或 predicted/observed 二选一
    "dca": ("thresholds", "models"), "nomogram": ("variables", "outcome_scales"),
    "rcs": ("points",), "bland_altman": ("methods",),
    "waterfall": ("change",), "swimmer": ("end",),
    "composite": ("layout", "panels"),
    "diagram": ("blocks", "arrows"),
    "prisma": ("records_identified", "studies_included"),
}
# 必须等长的字段对（防止哑铃图 Δ 错位这类类级错误）
EQUAL_PAIRS = {
    "bar": (("labels", "errors"),), "grouped_bar": (("labels", "errors"),),
    "scatter": (("x", "y"),), "paired": (("before", "after"),),
    "forest": (("labels", "estimates", "ci_low", "ci_high"),),
    "roc": (("fpr", "tpr"),), "volcano": (("log2fc", "pvalue"),),
    "cif": (("time", "event"),), "dumbbell": (("from", "to"),),
    "calibration": (("predicted", "observed"),),
}

CJK_RE = re.compile(r"[\u3400-\u9fff\uf900-\ufaff\U00020000-\U0002ffff]")


# ---------------- v2.9 · 4K 分辨率门禁 ----------------
def png_size(path):
    """纯标准库读 PNG IHDR 宽高（避免为一次校验引入 Pillow）。"""
    try:
        with open(path, "rb") as f:
            h = f.read(24)
        if len(h) >= 24 and h[:8] == b"\x89PNG\r\n\x1a\n" and h[12:16] == b"IHDR":
            return struct.unpack(">II", h[16:24])
    except OSError:
        pass
    return None


def figure_inches(args, eng):
    """估算本次渲染画幅（英寸）：期刊锁宽优先，否则取主题默认 figsize。"""
    key = (args.theme or "glm").lower()
    tw, th = THEME_FIGSIZE.get(key, (8, 5.5))   # 未命中取最小画幅 → DPI 偏保守
    if args.journal:
        try:
            jf = eng / "scripts/journal" / (args.journal + ".json")
            j = json.loads(jf.read_text(encoding="utf-8"))
            mm = j["widths_mm"].get(args.column, j["widths_mm"]["double"])
            w = float(mm) / 25.4
            return w, w * (th / tw)
        except (OSError, ValueError, KeyError, TypeError):
            pass
    return float(tw), float(th)


def target_dpi(args, eng):
    """按画幅反推达标 DPI：同时满足长边 ≥min_long、短边 ≥min_short，且不低于 600。"""
    w_in, h_in = figure_inches(args, eng)
    if w_in <= 0 or h_in <= 0:
        return DEFAULT_DPI
    need = max(math.ceil(args.min_long_edge / w_in),
               math.ceil(args.min_short_edge / h_in),
               DEFAULT_DPI, int(args.dpi or 0))
    return min(int(need), int(args.max_dpi or MAX_DPI))


def check_4k(out, formats, args):
    """渲染后按真实像素硬校验；纯矢量输出视为等效 4K。"""
    fmts = ([f.strip() for f in formats.split(",") if f.strip()]
            if isinstance(formats, str) else list(formats))
    base = Path(out).with_suffix("") if Path(out).suffix else Path(out)
    if not any(f in BITMAP_FORMATS for f in fmts):
        return {"mode": "vector", "ok": True,
                "note": "PDF/SVG/EPS 矢量、分辨率无关，等效 ≥4K"}
    png = Path(str(base) + ".png")
    if not png.is_file() and str(out).lower().endswith(".png"):
        png = Path(out)
    if not png.is_file():
        return {"mode": "bitmap", "ok": False,
                "error": "未找到 PNG，无法实测像素（4K 模式会自动补 PNG 作校验代理）"}
    size = png_size(png)
    if not size:
        return {"mode": "bitmap", "ok": False, "error": "PNG IHDR 读取失败"}
    w, h = size
    return {"mode": "bitmap",
            "ok": max(w, h) >= args.min_long_edge and min(w, h) >= args.min_short_edge,
            "width": w, "height": h, "long_edge": max(w, h), "short_edge": min(w, h),
            "megapixels": round(w * h / 1e6, 2),
            "threshold": f"{args.min_long_edge}x{args.min_short_edge}",
            "png": str(png)}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def find_engine():
    for p in ENGINE_CANDIDATES:
        if (p / "scripts/gen_figure.py").is_file():
            return p
    return None


def find_python():
    seen = set()
    for p in PY_CANDIDATES:
        if not p or p in seen or not os.path.exists(p):
            continue
        seen.add(p)
        code = "import " + ",".join(DEPS)
        try:
            r = subprocess.run([p, "-c", code], capture_output=True, timeout=25)
            if r.returncode == 0:
                return p
        except (OSError, subprocess.TimeoutExpired):
            continue
    return None


def check_env(verbose=True):
    eng, py = find_engine(), find_python()
    info = {
        "engine": str(eng) if eng else None,
        "engine_version": None,
        "python": py,
        "deps": list(DEPS),
        "journals": [],
        "ok": bool(eng and py),
    }
    if eng:
        meta = eng / "_meta.json"
        if meta.is_file():
            try:
                info["engine_version"] = json.loads(meta.read_text(encoding="utf-8")).get("version")
            except (ValueError, OSError):
                pass
        info["journals"] = sorted(p.stem for p in (eng / "scripts/journal").glob("*.json")) \
            if (eng / "scripts/journal").is_dir() else []
    if verbose:
        print("=== figure-bridge 环境自检 ===")
        print(f"引擎     : {info['engine'] or '未找到'}")
        print(f"引擎版本 : {info['engine_version'] or '未知'}")
        print(f"运行python: {info['python'] or '未找到（缺 matplotlib/numpy/scipy/pymupdf）'}")
        print(f"期刊预设 : {', '.join(info['journals']) or '无'}")
        print(f"4K 门禁  : 位图长边≥{UHD_LONG}px 且短边≥{UHD_SHORT}px（{UHD_PIXELS/1e6:.2f}MP），"
              f"DPI 上限 {MAX_DPI}，矢量等效")
        print(f"结论     : {'OK 可出图' if info['ok'] else 'FAIL 请先安装 academic-figures 或用系统 python'}")
        if not info["ok"] and py is None:
            print("提示     : WorkBuddy 内置 python 缺依赖，用 /opt/homebrew/bin/python3 或 /usr/bin/python3")
    return info


def finite_numbers_ok(obj, path="$"):
    """递归检查所有数值有限（拦截 NaN/Inf/None 混入）。"""
    if isinstance(obj, bool) or obj is None:
        return True
    if isinstance(obj, (int, float)):
        return math.isfinite(float(obj))
    if isinstance(obj, dict):
        return all(finite_numbers_ok(v, path + "." + str(k)) for k, v in obj.items())
    if isinstance(obj, (list, tuple)):
        return all(finite_numbers_ok(v, path + f"[{i}]") for i, v in enumerate(obj))
    return True


def validate_data(path, chart_type):
    """渲染前校验闸门：存在 → JSON 合法 → 必填 → 等长 → 数值有限 → 自洽。"""
    p = Path(path)
    if not p.is_file():
        return [f"数据文件不存在: {p}"]
    if p.suffix.lower() not in (".json",):
        return [f"桥接闸门只接 JSON（CSV 会静默丢失 errors/significance/复杂 schema）: {p}"]
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, OSError) as e:
        return [f"JSON 解析失败: {e}"]
    if not isinstance(d, dict):
        return ["JSON 顶层必须是对象"]
    errs = []
    for k in REQUIRED.get(chart_type, ()):
        if k not in d:
            if chart_type == "calibration" and ({"bins", "predicted"} & set(d)):
                continue
            if chart_type in ("km", "survival") and ({"time", "survival"} & set(d)):
                continue
            errs.append(f"缺少必填字段 `{k}`（图型 {chart_type}）")
    for group in EQUAL_PAIRS.get(chart_type, ()):
        present = [(k, d[k]) for k in group if k in d and isinstance(d[k], list)]
        if len(present) > 1:
            lens = {k: len(v) for k, v in present}
            if len(set(lens.values())) > 1:
                errs.append(f"数组长度不一致 {lens}（{chart_type} 图型必须同源等长）")
    if not finite_numbers_ok(d):
        errs.append("存在 NaN/Inf 数值（火山图 p=0 须截断为 1e-300）")
    if chart_type == "prisma":
        a, b = d.get("records_identified"), d.get("studies_included")
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) and b > a:
            errs.append(f"PRISMA 数字不自洽: 纳入 {b} > 检出 {a}")
    if chart_type == "bland_altman" and isinstance(d.get("methods"), list):
        m = d["methods"]
        if len(m) != 2:
            errs.append(f"Bland-Altman 需恰 2 组方法，实得 {len(m)}")
        elif isinstance(m[0], list) and isinstance(m[1], list) and len(m[0]) != len(m[1]):
            errs.append("Bland-Altman 两组必须严格等长配对")
    return errs


def list_items(kind, eng, py):
    if not eng:
        print("未找到 academic-figures 引擎，先跑 --check", file=sys.stderr)
        return 4
    if kind == "journals":
        print(" ".join(sorted(p.stem for p in (eng / "scripts/journal").glob("*.json"))))
        return 0
    if not py:
        print("未找到带绘图依赖的系统 python，先跑 --check", file=sys.stderr)
        return 4
    g = eng / "scripts/gen_figure.py"
    flag = "--list-types" if kind == "types" else "--list-themes"
    return subprocess.run([py, str(g), flag], cwd=str(eng)).returncode


def build_cmd(args, eng, py, data):
    """流水线由 run_pipeline() 展开为逐条单图，本函数只负责单图命令。"""
    g = eng / "scripts/gen_figure.py"
    cmd = [py, str(g), "--type", args.type, "--data", str(Path(data).resolve()),
           "--out", str(Path(args.out).resolve())]
    if args.theme:
        cmd += ["--theme", args.theme]
    if args.journal:
        cmd += ["--journal", args.journal, "--column", args.column]
    if args.title:
        cmd += ["--title", args.title]
    fmts = [f.strip() for f in args.formats.split(",") if f.strip()]
    bad = [f for f in fmts if f not in FORMATS]
    if bad:
        raise ValueError(f"不支持的格式 {bad}，可用 {FORMATS}")
    res = getattr(args, "resolution", "4k")
    has_bitmap = any(f in BITMAP_FORMATS for f in fmts)
    # v2.9：位图输出必须可实测像素；只有 tiff 时补一张 png 作校验代理
    if res == "4k" and has_bitmap and "png" not in fmts:
        fmts.append("png")
        args.formats = ",".join(fmts)
    # v2.9：渲染前按画幅反推达标 DPI（期刊锁宽会显著缩小画幅，600dpi 未必够 4K）
    dpi = None
    if res == "4k" and has_bitmap:
        dpi = target_dpi(args, eng)
    elif args.dpi:
        dpi = int(args.dpi)
    if dpi:
        cmd += ["--dpi", str(dpi)]
    args.effective_dpi = dpi
    if len(fmts) > 1:
        cmd += ["--multi-format", ",".join(fmts)]
    elif fmts:
        cmd += ["--format", fmts[0]]
    if args.cjk or CJK_RE.search(Path(data).read_text(encoding="utf-8", errors="ignore")):
        cmd.append("--cjk")
    if args.verify:
        cmd.append("--verify")
    if args.alt:
        cmd.append("--alt")
    if args.caption:
        cmd.append("--caption")
    if args.audit:
        cmd.append("--audit")
    if args.repro:
        cmd.append("--repro")
    return cmd


def write_bridge_audit(out, data, cmd, rc, formats, res=None):
    """旁车 audit.json：输入 sha256 + 命令 + 退出码 + 4K 实测，保证可复现。"""
    base = Path(out).with_suffix("") if Path(out).suffix else Path(out)
    produced = []
    for f in formats:
        for suffix in (f"." + f, "." + f):
            cand = Path(str(base) + suffix)
            if cand.is_file():
                produced.append({"file": str(cand), "sha256": sha256(cand), "bytes": cand.stat().st_size})
    rec = {
        "bridge": "reading-notes-master/figure-bridge v2.9.1",
        "engine": "academic-figures v5.9.0",
        "input": str(Path(data).resolve()),
        "input_sha256": sha256(data),
        "command": cmd,
        "exit_code": rc,
        "resolution": res or {"mode": "not-checked"},
        "outputs": produced,
    }
    p = Path(str(base) + ".bridge-audit.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def execute_render(a, eng, py, data, label=""):
    """单图渲染 + v2.9 4K 硬门禁（一次提 DPI 重试）。返回 (rc, cmd, res)。"""
    try:
        cmd = build_cmd(a, eng, py, data)
    except (ValueError, OSError) as e:
        raise ValueError(f"命令构造失败: {e}") from e
    print((f"=== {label} 命令 ===") if label else "=== figure-bridge 命令 ===")
    print(" ".join(cmd))
    if a.dry_run:
        return 0, cmd, {"mode": "dry-run", "ok": True}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    rc = subprocess.run(cmd, cwd=str(eng)).returncode
    res = check_4k(a.out, a.formats, a) if a.resolution == "4k" else {"mode": "off", "ok": True}
    # 引擎内存护栏可能把 dpi 砍半 → 一次自动提 DPI 重渲染
    if rc == 0 and a.resolution == "4k" and res.get("mode") == "bitmap" and not res.get("ok"):
        cur = getattr(a, "effective_dpi", None) or DEFAULT_DPI
        bump = min(int(cur * 1.6), int(a.max_dpi or MAX_DPI))
        if bump > cur:
            print(f"[4K RETRY] 实测 {res.get('width')}x{res.get('height')} 未达 "
                  f"{res.get('threshold')}，提 DPI {cur}→{bump} 重渲染", file=sys.stderr)
            a.dpi = bump
            cmd = build_cmd(a, eng, py, data)
            rc = subprocess.run(cmd, cwd=str(eng)).returncode
            res = check_4k(a.out, a.formats, a)
    if a.resolution == "4k":
        if res.get("ok"):
            if res.get("mode") == "bitmap":
                print(f"[4K OK] {res['width']}×{res['height']} = {res['megapixels']}MP "
                      f"≥ {res['threshold']}")
            else:
                print(f"[4K OK] {res.get('mode')}: {res.get('note', '')}")
        else:
            print(f"[4K FAIL] {res}", file=sys.stderr)
            print("建议：--column double / 去掉 --journal 用自由尺寸 / --resolution auto 显式豁免",
                  file=sys.stderr)
            if rc == 0:
                rc = 2
    if not a.no_bridge_audit:
        try:
            write_bridge_audit(a.out, data, cmd, rc,
                               [f.strip() for f in a.formats.split(",") if f.strip()], res)
        except OSError as e:
            print(f"WARN 旁车写入失败: {e}", file=sys.stderr)
    if rc == 2:
        print("VERIFY / 4K FAIL：见 academic-chart-system.md §5 G1 + G5，修机制后重出",
              file=sys.stderr)
    return rc, cmd, res


def run_pipeline(args, eng, py):
    """自行展开 JSON 流水线：逐条过校验闸门 + --verify（引擎自带的流水线条目不支持 verify 键）。

    YAML 流水线委托引擎；此时若要求 --verify，明确告警并建议改用 JSON。
    """
    import copy
    p = Path(args.pipeline).resolve()
    g = eng / "scripts/gen_figure.py"
    if p.suffix.lower() != ".json":
        print("WARN: YAML 流水线委托引擎，桥接器无法逐条过 G1(verify) 与 G5(4K) 门禁；"
              "改用 JSON 流水线可让 38 图型全部强制 4K", file=sys.stderr)
        return subprocess.run([py, str(g), "--pipeline", str(p)], cwd=str(eng)).returncode
    try:
        spec = json.loads(p.read_text(encoding="utf-8"))
    except (ValueError, OSError) as e:
        print(f"流水线 JSON 解析失败: {e}", file=sys.stderr)
        return 3
    if isinstance(spec, list):
        defaults, figures = {}, spec
    elif isinstance(spec, dict):
        defaults, figures = spec.get("defaults") or {}, spec.get("figures")
    else:
        figures = None
    if not isinstance(defaults, dict) or not isinstance(figures, list) or not figures:
        print("流水线需为非空列表，或含非空 figures 列表 + 可选 defaults 对象", file=sys.stderr)
        return 3
    results = []
    print(f"=== figure-bridge 流水线：{len(figures)} 张图 ===")
    for i, raw in enumerate(figures, 1):
        if not isinstance(raw, dict):
            results.append({"index": i, "ok": False, "error": "条目必须是对象"})
            continue
        item = dict(defaults)
        item.update(raw)
        for k in ("data", "out"):
            v = item.get(k)
            if isinstance(v, str) and v and not os.path.isabs(v):
                item[k] = os.path.normpath(os.path.join(str(p.parent), v))
        a = copy.copy(args)
        a.pipeline = None
        a.type = str(item.get("type", ""))
        a.data = str(item.get("data", ""))
        a.out = str(item.get("out", ""))
        a.theme = item.get("theme") or args.theme
        a.journal = item.get("journal") or args.journal
        a.column = item.get("column") or args.column
        a.title = item.get("title") or args.title
        a.dpi = item.get("dpi") or args.dpi
        fmts = item.get("multi_format") or item.get("format") or args.formats
        a.formats = ",".join(str(x) for x in fmts) if isinstance(fmts, (list, tuple)) else str(fmts)
        for key in ("verify", "alt", "caption", "audit", "repro", "cjk"):
            setattr(a, key, bool(item.get(key, getattr(args, key))))
        print(f"[{i}/{len(figures)}] {a.type} <- {a.data}")
        errs = ["缺少 type/data/out"] if not (a.type and a.data and a.out) else validate_data(a.data, a.type)
        if errs:
            for e in errs:
                print(f"  FAIL {e}", file=sys.stderr)
            results.append({"index": i, "out": a.out, "ok": False, "error": errs})
            continue
        try:
            rc, cmd, res = execute_render(a, eng, py, a.data, label=f"[{i}/{len(figures)}]")
        except ValueError as e:
            results.append({"index": i, "out": a.out, "ok": False, "error": str(e)})
            continue
        results.append({"index": i, "out": a.out, "ok": rc == 0, "exit_code": rc,
                        "command": cmd, "resolution": res})
    report = p.parent / (p.stem + ".bridge-report.json")
    payload = {"pipeline": str(p), "total": len(results),
               "ok": sum(1 for r in results if r["ok"]),
               "failed": sum(1 for r in results if not r["ok"]), "items": results}
    report.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"批量报告: {report}（{payload['ok']}/{payload['total']} OK）")
    return 0 if payload["failed"] == 0 else 2


def main():
    ap = argparse.ArgumentParser(description="reading-notes-master v2.9 科研图表桥接器（默认 4K 输出）")
    ap.add_argument("--check", action="store_true", help="环境自检")
    ap.add_argument("--list", choices=("types", "themes", "journals"), help="列出图型/色板/期刊")
    ap.add_argument("--type", "-t", help="图型 slug，见 --list types")
    ap.add_argument("--data", "-d", help="输入 JSON 数据文件")
    ap.add_argument("--out", "-o", help="输出路径（不含扩展名时按 --formats 拼接）")
    ap.add_argument("--pipeline", help="引擎 YAML/JSON 流水线文件路径")
    ap.add_argument("--theme", help="色板，默认 glm；无障碍/投稿用 okabe-ito")
    ap.add_argument("--journal", help="期刊预设（锁宽，--width 被忽略）")
    ap.add_argument("--column", choices=("single", "double"), default="double")
    ap.add_argument("--title", default="")
    ap.add_argument("--dpi", type=int, default=None, help="显式 DPI（4K 模式下会自动取 max(显式, 反推值)）")
    ap.add_argument("--formats", default="pdf,png", help="逗号分隔：png,svg,pdf,tiff,eps")
    ap.add_argument("--resolution", choices=("4k", "auto"), default="4k",
                    help="4k=位图长边≥3840 且短边≥2160（默认；矢量等效）；auto=不强制")
    ap.add_argument("--min-long-edge", type=int, default=UHD_LONG, help="4K 长边阈值（默认 3840）")
    ap.add_argument("--min-short-edge", type=int, default=UHD_SHORT, help="4K 短边阈值（默认 2160）")
    ap.add_argument("--max-dpi", type=int, default=MAX_DPI, help="自动 DPI 上限（默认 2000）")
    ap.add_argument("--verify", action="store_true", help="PDF 真实墨迹重叠门禁（exit 2 = 必须修）")
    ap.add_argument("--alt", action="store_true", help="生成无障碍图注旁车")
    ap.add_argument("--caption", action="store_true", help="生成图注旁车")
    ap.add_argument("--audit", action="store_true", help="引擎侧计数+sha256 审计")
    ap.add_argument("--repro", action="store_true", help="生成复现包")
    ap.add_argument("--cjk", action="store_true", help="强制中文字体（数据含中文时已自动开启）")
    ap.add_argument("--dry-run", action="store_true", help="只打印命令，不执行")
    ap.add_argument("--no-bridge-audit", action="store_true", help="不写 bridge-audit.json")
    args = ap.parse_args()

    if args.check:
        info = check_env()
        return 0 if info["ok"] else 4
    if args.list:
        return list_items(args.list, find_engine(), find_python())

    eng, py = find_engine(), find_python()
    if not eng or not py:
        check_env()
        return 4
    if not args.pipeline:
        if not (args.type and args.data and args.out):
            print("单图模式需 --type / --data / --out；批量用 --pipeline", file=sys.stderr)
            return 1
        errs = validate_data(args.data, args.type)
        if errs:
            print("=== 渲染前校验闸门 FAIL（exit 3，未落盘）===", file=sys.stderr)
            for e in errs:
                print("  - " + e, file=sys.stderr)
            return 3
    if args.pipeline:
        return run_pipeline(args, eng, py)
    try:
        rc, cmd, res = execute_render(args, eng, py, args.data)
    except (ValueError, OSError) as e:
        print(str(e), file=sys.stderr)
        return 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
