#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
schema.py — 把工具说明转换为 OpenAI 函数调用风格 schema。

用法:
  python schema.py --spec tool_spec.json --out schema.json
  tool_spec.json: {"name","description","parameters":[{"name","type","required","description"}]}
"""
import os, sys, json, argparse


def build(spec):
    props = {}
    required = []
    for p in spec.get("parameters", []):
        props[p["name"]] = {
            "type": p.get("type", "string"),
            "description": p.get("description", ""),
        }
        if p.get("required"):
            required.append(p["name"])
    return {
        "type": "function",
        "function": {
            "name": spec["name"],
            "description": spec.get("description", ""),
            "parameters": {
                "type": "object",
                "properties": props,
                "required": required,
            },
        },
    }


def main():
    ap = argparse.ArgumentParser(description="生成函数调用 schema")
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out")
    args = ap.parse_args()
    spec = json.loads(open(args.spec, encoding="utf-8").read())
    schema = build(spec)
    out = json.dumps(schema, ensure_ascii=False, indent=2)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(out)
        print(f"✅ schema 已生成 -> {args.out}（{schema['function']['name']}）")
    else:
        print(out)


if __name__ == "__main__":
    main()
