#!/usr/bin/env python3
"""按效果优先级挑出当前可用的最佳「支持参考图编辑」生图模型。

输出: <provider>/<model>，无可用时输出 NONE。
优先级: Gemini 3.1 Flash Image > GPT Image 2 > OpenRouter Gemini > fal nano-banana > Grok Imagine > MiniMax
"""
import json
import subprocess
import sys

PREF = ["google", "openai", "openrouter", "fal", "xai", "minimax", "minimax-portal"]


def load_providers():
    p = subprocess.run(
        ["openclaw", "infer", "image", "providers", "--json"],
        capture_output=True, text=True,
    )
    if p.returncode != 0 or not p.stdout.strip():
        raise RuntimeError((p.stderr or "empty output").strip()[:200])
    j = json.loads(p.stdout)
    if isinstance(j, list):
        return j
    return j.get("providers") or j.get("data") or []


def main():
    try:
        arr = load_providers()
    except Exception as e:  # noqa: BLE001
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    ready = {}
    for p in arr:
        edit = (p.get("capabilities") or {}).get("edit") or {}
        if p.get("configured") and edit.get("enabled"):
            ready[p.get("id")] = p.get("defaultModel")
    for pid in PREF:
        if ready.get(pid):
            print("%s/%s" % (pid, ready[pid]))
            return 0
    print("NONE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
