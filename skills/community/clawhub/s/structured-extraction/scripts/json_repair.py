#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JSON 提取 / 修复 / 校验。

从模型混合输出中提取 JSON 块，尝试修复常见语法错误，可选按 schema 校验。

用法:
  python json_repair.py <输入文件或'-'(stdin)> [--out clean.json] [--schema schema.json]
"""
import argparse
import json
import os
import sys


def extract_block(text):
    """提取最可能的 JSON 块（对象或数组）。优先标记包裹，其次首个 { 或 [。"""
    # 1) 标记包裹
    for a, b in [("---BEGIN JSON---", "---END JSON---"), ("```json", "```"), ("```", "```")]:
        if a in text and b in text:
            s = text.index(a) + len(a)
            e = text.index(b, s)
            cand = text[s:e]
            if cand.strip():
                return cand.strip()
    # 2) 首个平衡括号
    for opener, closer in [("{", "}"), ("[", "]")]:
        i = text.find(opener)
        if i >= 0:
            depth = 0
            in_str = False
            esc = False
            for j in range(i, len(text)):
                c = text[j]
                if esc:
                    esc = False
                    continue
                if c == "\\":
                    esc = True
                    continue
                if c == '"':
                    in_str = not in_str
                    continue
                if in_str:
                    continue
                if c == opener:
                    depth += 1
                elif c == closer:
                    depth -= 1
                    if depth == 0:
                        return text[i : j + 1]
    return None


def repair(s):
    """尝试修复常见 JSON 错误。"""
    s = s.strip()
    # 去掉尾随逗号
    import re
    s = re.sub(r",(\s*[}\]])", r"\1", s)
    # 单引号 -> 双引号（粗略，仅当整段无双引号包裹冲突时）
    # 补齐未闭合括号
    depth = {"{": 0, "[": 0}
    stack = []
    in_str = False
    esc = False
    for c in s:
        if esc:
            esc = False
            continue
        if c == "\\":
            esc = True
            continue
        if c == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if c == "{":
            depth["{"] += 1
            stack.append("}")
        elif c == "[":
            depth["["] += 1
            stack.append("]")
        elif c in ("}", "]"):
            if stack and stack[-1] == c:
                stack.pop()
    s += "".join(reversed(stack))  # 补闭合
    return s


def validate(obj, schema):
    # 轻量校验：required 字段存在 + 类型匹配
    errors = []
    props = schema.get("properties", {})
    req = schema.get("required", [])
    if not isinstance(obj, dict):
        return ["根对象应为 object"]
    for k in req:
        if k not in obj:
            errors.append(f"缺少必填字段: {k}")
    type_map = {"string": str, "number": (int, float), "integer": int,
                "boolean": bool, "array": list, "object": dict}
    for k, spec in props.items():
        if k in obj and k in spec:
            t = spec.get("type")
            if t in type_map and not isinstance(obj[k], type_map[t]):
                errors.append(f"字段 {k} 类型应为 {t}，实际 {type(obj[k]).__name__}")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="输入文件，或 - 读 stdin")
    ap.add_argument("--out", help="输出清洗后的 JSON")
    ap.add_argument("--schema", help="JSON Schema 文件做校验")
    args = ap.parse_args()

    if args.input == "-":
        text = sys.stdin.read()
    else:
        text = open(args.input, "r", encoding="utf-8").read()

    block = extract_block(text)
    if not block:
        print("❌ 未找到 JSON 块", file=sys.stderr)
        sys.exit(1)
    try:
        obj = json.loads(block)
    except json.JSONDecodeError:
        fixed = repair(block)
        try:
            obj = json.loads(fixed)
            print("🔧 已修复 JSON 语法")
        except json.JSONDecodeError as e:
            print(f"❌ JSON 无法解析: {e}", file=sys.stderr)
            sys.exit(1)

    errors = []
    if args.schema and os.path.exists(args.schema):
        schema = json.load(open(args.schema, encoding="utf-8"))
        errors = validate(obj, schema)
        if errors:
            print("⚠️ Schema 校验未通过:")
            for e in errors:
                print("  -", e)
        else:
            print("✅ Schema 校验通过")

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        print(f"💾 已写入 {args.out}")

    print("__JSON__" + json.dumps(obj, ensure_ascii=False)[:2000])


if __name__ == "__main__":
    main()
