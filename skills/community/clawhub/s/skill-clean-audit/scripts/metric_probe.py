#!/usr/bin/env python3
"""
metric_probe.py — lightweight metric signal probe for skill-clean-audit.

Pure Python standard library (ast), offline, reads no env, no credentials, read-only.
It ONLY emits "worth a closer look" hints for five signals — it never grades
red/amber/green. The agent still judges severity via the A/B two-axis model.

Signals (mirror of 《轻量指标信号》in SKILL.md):
  1. function > 40 lines
  2. parameters >= 4
  3. nesting depth >= 4 (if/for/while/with/try)
  4. boolean-flag parameter (def f(..., dry_run=False))
  5. same logic repeated >= 3x within a function

Usage:
  python metric_probe.py --src path/to/file.py
  python metric_probe.py --src path/to/file.py --json
"""
import argparse
import ast
import json
import os
import sys

FUNC_LINE_LIMIT = 40
PARAM_LIMIT = 4
NESTING_LIMIT = 4
REPEAT_LIMIT = 3

CONTROL = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith, ast.Try)


def _norm_text(node: ast.AST) -> str:
    """A rough normalized fingerprint of a statement, ignoring literals/numbers."""
    try:
        src = ast.dump(node)
    except Exception:
        src = type(node).__name__
    # strip concrete string/number values so repeated logic collapses to one key
    import re
    src = re.sub(r"Constant\(value=[^)]*\)", "Constant", src)
    return src


def _count_params(func: ast.arguments) -> int:
    n = len(func.args) + len(func.kwonlyargs)
    if func.vararg:
        n += 1
    if func.kwarg:
        n += 1
    return n


def _bool_flag_params(func: ast.arguments) -> list[str]:
    names = []
    # positional-or-keyword + kwonly defaults align by trailing position
    pos = func.args
    pos_defaults = func.defaults
    for i, a in enumerate(pos):
        default = pos_defaults[i - len(pos) + len(pos_defaults)] if (i - len(pos) + len(pos_defaults)) >= 0 else None
        if isinstance(default, ast.Constant) and isinstance(default.value, bool):
            names.append(a.arg)
    for a in func.kwonlyargs:
        if isinstance(a.default, ast.Constant) and isinstance(a.default.value, bool):
            names.append(a.arg)
    return names


def _max_nesting(body) -> int:
    best = 0

    def walk(stmts, depth):
        nonlocal best
        for st in stmts:
            if isinstance(st, CONTROL):
                best = max(best, depth + 1)
                for child in st.body:
                    if isinstance(child, CONTROL):
                        walk([child], depth + 2)
                # also descend into orelse / finalbody / handlers
                for blk in (getattr(st, "orelse", []), getattr(st, "finalbody", [])):
                    walk(blk, depth + 2)
                for h in getattr(st, "handlers", []):
                    walk(h.body, depth + 2)

    walk(body, 1)
    return best


def _repeated_logic(func: ast.FunctionDef) -> list[tuple[str, list[int]]]:
    keys = {}
    for st in ast.walk(func):
        if isinstance(st, (ast.Assign, ast.Expr, ast.AugAssign, ast.AnnAssign)):
            key = _norm_text(st)
            keys.setdefault(key, []).append(getattr(st, "lineno", func.lineno))
    out = []
    for key, lines in keys.items():
        if len(lines) >= REPEAT_LIMIT:
            out.append((key, sorted(set(lines))[:5]))
    return out


def analyze(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)
    hits = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        name = node.name
        ln = node.lineno
        end = getattr(node, "end_lineno", ln)
        length = end - ln + 1
        if length > FUNC_LINE_LIMIT:
            hits.append({"signal": "long-function", "line": ln, "detail": f"{name} {length} lines > {FUNC_LINE_LIMIT}"})
        nparams = _count_params(node.args)
        if nparams >= PARAM_LIMIT:
            hits.append({"signal": "many-params", "line": ln, "detail": f"{name} has {nparams} params >= {PARAM_LIMIT}"})
        depth = _max_nesting(node.body)
        if depth >= NESTING_LIMIT:
            hits.append({"signal": "deep-nesting", "line": ln, "detail": f"{name} nesting depth {depth} >= {NESTING_LIMIT}"})
        bools = _bool_flag_params(node.args)
        if bools:
            hits.append({"signal": "bool-flag", "line": ln, "detail": f"{name} boolean-flag param(s): {', '.join(bools)}"})
        for key, lines in _repeated_logic(node):
            hits.append({"signal": "repeated-logic", "line": lines[0],
                         "detail": f"{name} same logic ~{len(lines)}x at lines {lines} (DRY check)"})
    return {"file": path, "hits": hits}


def _self_check(path: str) -> str:
    return (
        "无法读取目标文件，请自查 / Cannot read target — self-check:\n"
        "  1) 核对路径拼写与相对/绝对形式（`./` 相对工作区根目录） / check path spelling & relative/absolute form\n"
        "  2) 确认文件存在——列出目录验证 / confirm the file exists (list the dir)\n"
        "  3) 贴正确路径，或把文件放进工作区根目录再试 / paste the correct path or drop it in the workspace root\n"
        f"  path = {path}"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Probe lightweight clean-code metric signals")
    ap.add_argument("--src", required=True, help="target .py file")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    args = ap.parse_args()

    if not os.path.isfile(args.src):
        print(_self_check(args.src))
        raise SystemExit(2)

    try:
        result = analyze(args.src)
    except SyntaxError as e:
        print(f"语法错误，跳过 / Syntax error, skipped: {e}")
        raise SystemExit(2)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"# Metric probe · {result['file']}")
    print()
    print("> 仅作「值得多看一眼」的探针，不判红黄绿；严重度由 A/B 两轴判定。")
    print("> Hints only — not red/amber/green. Severity is judged via the A/B axes.")
    print()
    if not result["hits"]:
        print("未发现指标信号 / No metric signals found.")
        return
    print("| # | 信号 / signal | 位置 / line | 说明 / detail |")
    print("|---|---|---|---|")
    for i, h in enumerate(result["hits"], 1):
        print(f"| {i} | {h['signal']} | {h['line']} | {h['detail']} |")


if __name__ == "__main__":
    main()
