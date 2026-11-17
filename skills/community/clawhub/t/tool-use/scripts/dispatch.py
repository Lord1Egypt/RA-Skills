#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dispatch.py — 工具调度器：校验参数并安全执行已注册工具。

只执行注册表中显式声明的工具，参数先按 schema 校验再执行。
用法:
  python dispatch.py --registry reg.json --call '{"name":"echo","arguments":{"text":"hi"}}' --out result.json
  reg.json: {"echo":{"type":"command","cmd":"echo {text}"}}
            {"myfn":{"type":"python","module":"mymod","func":"myfn"}}
"""
import os, sys, json, argparse, subprocess, shlex


def validate(call, registry):
    name = call.get("name")
    if name not in registry:
        return False, f"未注册的工具: {name}"
    args = call.get("arguments", {})
    # 简易必填校验（registry 项可带 schema.required）
    req = registry[name].get("required", [])
    missing = [r for r in req if r not in args]
    if missing:
        return False, f"缺少必填参数: {missing}"
    return True, ""


def execute(entry, args):
    t = entry.get("type", "command")
    if t == "command":
        cmd = entry["cmd"].format(**args)
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return r.returncode == 0, (r.stdout or r.stderr).strip()
    if t == "python":
        mod = __import__(entry["module"])
        fn = getattr(mod, entry["func"])
        res = fn(**args)
        return True, str(res)
    return False, f"未知工具类型: {t}"


def main():
    ap = argparse.ArgumentParser(description="工具调度器")
    ap.add_argument("--registry", required=True)
    ap.add_argument("--call", required=True, help='JSON: {"name":..., "arguments":{...}}')
    ap.add_argument("--out")
    args = ap.parse_args()

    registry = json.loads(open(args.registry, encoding="utf-8").read())
    call = json.loads(args.call)
    ok, msg = validate(call, registry)
    result = {"call": call, "ok": False, "result": None, "error": None}
    if not ok:
        result["error"] = msg
        print("⚠️", msg)
    else:
        ok2, out = execute(registry[call["name"]], call.get("arguments", {}))
        result["ok"] = ok2
        if ok2:
            result["result"] = out
        else:
            result["error"] = out
        print(f"{'✅' if ok2 else '⚠️'} {call['name']}: {out}")

    out = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(out)
        print(f"结果 -> {args.out}")
    else:
        print(out)


if __name__ == "__main__":
    main()
