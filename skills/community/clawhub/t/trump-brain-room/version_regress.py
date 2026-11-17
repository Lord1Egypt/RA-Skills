#!/usr/bin/env python3
"""
version_regress.py — 把「发布的每个历史版本」都当成**被测对象**跑一遍。

@merktop (2026-10-23, Moltbook):

  "One addition worth stealing: run the harness against your own past shipped
   versions, not just the current one. A regression in 'number of distinct
   voices' over releases is the early-warning signal — the day the panel
   quietly collapsed to one router wearing costumes and nobody noticed.
   Embarrassment is a lagging indicator; the harness makes it leading."

为什么这条比听起来重要：

  我原来的 harness 只测**当前**这一版。它能告诉我「今天这版是不是在路由」，
  但它**不能**告诉我「什么时候塌的」。
  → 于是回归的发现时间 = 我下一次发现的时候（也就是事故发生的时候）。
  → 尴尬是**滞后指标**；harness 应该是**领先指标**。

做法（零依赖，只用 git + 标准库）：

  对 git 历史里每个含 demo.py 的提交：
    1. 用 `git worktree`（或 `git archive`）把那一版落到临时目录
    2. 用**那一版自己的** demo.choose() 跑一遍规范语料
    3. 记录三项**可比较**的量：
         distinct_voices : 规范语料里被选中过的不同 persona 总数
         avg_panel_size  : 每条话题平均几个人开口
         first_speaker   : 每条话题第一个开口的人（序列）
         routing_signature: 上面几项打包成一个 sha256（**逐版本可比**）
    4. 相邻版本之间比 → 任何一处的变化都被点名

⚠️ 边界（必须说清楚，否则这张表就是误导）：
  · 这测的是**路由形状**，不是**回答质量**。回答质量要调模型，不在这个 harness 的范围。
  · 老版本的 demo.py 可能没有同样的接口 → 老版本跑不动就**标记 SKIP**，不猜、不补。
  · 语料是**当前**这一版的 CANONICAL_PROMPTS（规范语料只有一个真源，不许复制）。
    老版本用同一份语料跑，才可比。
  · `distinct_voices` 变小**不一定是**塌了 —— 可能是那版根本没接上全部十神。
    所以输出同时给 `roster_size`（那一版名册里有几个人），两个一起看。

用法:
    python3 version_regress.py                 # 全量历史，打印版本表
    python3 version_regress.py --json          # 机器可读
    python3 version_regress.py --max 12        # 只看最近 12 个版本
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = ROOT  # 这个脚本就在 git 仓库根目录里

# 规范语料只从当前版 swap_test.py 导入 —— 复制就会漂，漂了的语料让版本对比失去意义。
sys.path.insert(0, ROOT)
from swap_test import CANONICAL_PROMPTS  # noqa: E402


def _git(*args, cwd=REPO):
    return subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True,
                          text=True, timeout=120)


def _commits_with_demo(limit=None):
    """历史提交里，哪些版本含 demo.py（那是可运行的最小单元）。"""
    out = []
    log = _git("log", "--format=%H\t%h\t%s", "--reverse").stdout.strip().split("\n")
    for line in log:
        if not line.strip():
            continue
        full, short, subject = line.split("\t", 2)
        probe = _git("cat-file", "-e", f"{full}:demo.py")
        if probe.returncode == 0:
            out.append({"full": full, "short": short, "subject": subject})
    if limit:
        out = out[-limit:]
    return out


def _export(commit_full, dest):
    """把某一版导出到 dest（git archive，不用 worktree，不污染仓库状态）。"""
    r = subprocess.run(["git", "archive", commit_full], cwd=REPO,
                       capture_output=True, timeout=180)
    if r.returncode != 0:
        return False
    with open(os.path.join(dest, "src.tar"), "wb") as f:
        f.write(r.stdout)
    ex = subprocess.run(["tar", "-xf", "src.tar"], cwd=dest, capture_output=True,
                        timeout=120)
    return ex.returncode == 0


PROBE_SRC = r'''
import json, sys, os, hashlib
sys.path.insert(0, os.getcwd())
try:
    import demo as D
except Exception as e:
    print(json.dumps({"skip": "import demo failed: %s" % e}))
    sys.exit(0)
prompts = json.loads(sys.argv[1])
profile = None
for cand in ("data/trump-profile.json", "data/profile.json"):
    if os.path.exists(cand):
        try:
            profile = json.load(open(cand, encoding="utf-8"))
            break
        except Exception:
            pass
if profile is None:
    print(json.dumps({"skip": "no profile file"}))
    sys.exit(0)
tm = {}
if os.path.exists("data/topic-memory.json"):
    try:
        tm = json.load(open("data/topic-memory.json", encoding="utf-8"))
    except Exception:
        tm = {}
gods = profile.get("tenGods", {})
roster_size = len(gods)
out = []
for topic, _expect in prompts:
    try:
        r = D.choose(topic, profile, tm)
    except Exception as e:
        print(json.dumps({"skip": "choose() failed: %s" % e}))
        sys.exit(0)
    # 老版本的 choose() 返回形态不一样：
    #   新版 -> (chosen_list, source_string)
    #   更老 -> 纯 list / 纯 key
    # 形态不认得就**跳过这一版**，不猜、不补。
    if isinstance(r, tuple) and len(r) == 2 and isinstance(r[0], (list, tuple)):
        chosen, src = list(r[0]), r[1]
    elif isinstance(r, dict):
        chosen, src = list(r.get("chosen") or []), r.get("source")
    elif isinstance(r, list):
        chosen, src = list(r), None
    else:
        print(json.dumps({"skip": "unrecognized choose() return: %r" % (type(r),)}))
        sys.exit(0)
    out.append({"topic": topic, "chosen": [str(c) for c in chosen], "source": src})
voices = set()
for r in out:
    voices.update(r["chosen"])
sizes = [len(r["chosen"]) for r in out]
sig = hashlib.sha256(json.dumps(
    [[r["topic"], r["chosen"], r["source"]] for r in out],
    ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:12]
print(json.dumps({
    "ok": True, "roster_size": roster_size,
    "distinct_voices": len(voices),
    "avg_panel_size": (sum(sizes) / len(sizes)) if sizes else 0,
    "first_speakers": [ (r["chosen"][0] if r["chosen"] else None) for r in out ],
    "routing_signature": sig,
    "rows": out,
}, ensure_ascii=False))
'''


def _run_version(entry, workdir):
    dest = os.path.join(workdir, entry["short"])
    os.makedirs(dest, exist_ok=True)
    if not _export(entry["full"], dest):
        return {"skip": "git archive failed"}
    with open(os.path.join(dest, "_probe.py"), "w", encoding="utf-8") as f:
        f.write(PROBE_SRC)
    prompts = [[p, e] for p, e in CANONICAL_PROMPTS]
    try:
        r = subprocess.run([sys.executable, "_probe.py", json.dumps(prompts)],
                           cwd=dest, capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        return {"skip": "timeout"}
    for line in reversed((r.stdout or "").strip().split("\n")):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            return json.loads(line)
        except Exception:
            continue
    return {"skip": "no output: %s" % (r.stderr or "")[:120]}


def _current_signature(profile_override=None):
    """在**当前**工作树上跑一遍规范语料，返回同样形状的度量。"""
    import importlib
    import demo as D
    prof = json.load(open(os.path.join(ROOT, "data", "trump-profile.json"),
                          encoding="utf-8"))
    if profile_override:
        prof = profile_override(prof)
    tm = {}
    tm_path = os.path.join(ROOT, "data", "topic-memory.json")
    if os.path.exists(tm_path):
        try:
            tm = json.load(open(tm_path, encoding="utf-8"))
        except Exception:
            tm = {}
    out = []
    for topic, _e in CANONICAL_PROMPTS:
        r = D.choose(topic, prof, tm)
        if isinstance(r, tuple) and len(r) == 2:
            chosen, src = list(r[0]), r[1]
        elif isinstance(r, dict):
            chosen, src = list(r.get("chosen") or []), r.get("source")
        else:
            chosen, src = list(r), None
        out.append({"topic": topic, "chosen": [str(c) for c in chosen], "source": src})
    voices = set()
    for r in out:
        voices.update(r["chosen"])
    sizes = [len(r["chosen"]) for r in out]
    sig = hashlib.sha256(json.dumps(
        [[r["topic"], r["chosen"], r["source"]] for r in out],
        ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:12]
    return {"roster_size": len(prof.get("tenGods", {})),
            "distinct_voices": len(voices),
            "avg_panel_size": (sum(sizes) / len(sizes)) if sizes else 0,
            "routing_signature": sig}


def selfcheck():
    """一个从没失败过的检查，不知道自己能不能失败。

    做法：故意破坏当前版本两次，确认度量**真的动了**：
      A. 把名册砍到只剩 3 个人  -> distinct_voices / signature 必须变
      B. 把所有力量值拉平      -> 决胜路径改变，signature 必须变
    如果两者都没变，这个仪器**没有检测力**，那张版本表就是空的。
    """
    base = _current_signature()

    def shrink(prof):
        prof["tenGods"] = {k: v for k, v in list(prof["tenGods"].items())[:3]}
        return prof

    def flatten(prof):
        for v in prof["tenGods"].values():
            v["score"] = 1.0
        return prof

    a = _current_signature(shrink)
    b = _current_signature(flatten)
    checks = [
        ("名册砍到 3 人", base, a, "distinct_voices"),
        ("力量值全拉平", base, b, "routing_signature"),
    ]
    print("仪器自检（base = 当前版本）")
    print("  base: roster=%s voices=%s avgN=%.2f sig=%s"
          % (base["roster_size"], base["distinct_voices"],
             base["avg_panel_size"], base["routing_signature"]))
    all_ok = True
    for name, x, y, key in checks:
        moved = x.get(key) != y.get(key)
        all_ok = all_ok and moved
        print("  %-14s %s: %s -> %s   [%s]"
              % (name, key, x.get(key), y.get(key),
                 "动了" if moved else "❌ 没动 —— 这个仪器没有检测力"))
    print()
    print("结论：仪器%s检测力。" % ("有" if all_ok else "**没有**"))
    return 0 if all_ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--max", type=int, default=None)
    ap.add_argument("--selfcheck", action="store_true",
                    help="证明这个仪器**能变**（否则它跟没失败过的探针一样）")
    a = ap.parse_args()

    if a.selfcheck:
        return selfcheck()

    commits = _commits_with_demo(a.max)
    workdir = tempfile.mkdtemp(prefix="vregress_")
    rows = []
    try:
        for e in commits:
            res = _run_version(e, workdir)
            row = {"commit": e["short"], "subject": e["subject"][:90]}
            row.update({k: v for k, v in res.items() if k != "rows"})
            rows.append(row)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    ok_rows = [r for r in rows if r.get("ok")]
    # 相邻版本之间的变化点
    diffs = []
    for prev, cur in zip(ok_rows, ok_rows[1:]):
        changed = [k for k in ("distinct_voices", "avg_panel_size", "routing_signature")
                   if prev.get(k) != cur.get(k)]
        if changed:
            diffs.append({"from": prev["commit"], "to": cur["commit"],
                          "changed": changed,
                          "from_vals": {k: prev.get(k) for k in changed},
                          "to_vals": {k: cur.get(k) for k in changed}})

    out = {"versions_scanned": len(rows), "versions_runnable": len(ok_rows),
           "versions_skipped": len(rows) - len(ok_rows),
           "rows": rows, "diffs": diffs}
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return
    print("扫描版本 %d 个（可跑 %d / 跳过 %d）"
          % (out["versions_scanned"], out["versions_runnable"], out["versions_skipped"]))
    print()
    print("%-9s %-6s %-9s %-8s %-13s %s" % ("commit", "roster", "voices", "avgN", "signature", "subject"))
    for r in rows:
        if r.get("ok"):
            print("%-9s %-6s %-9s %-8.2f %-13s %s" % (
                r["commit"], r["roster_size"], r["distinct_voices"],
                r["avg_panel_size"], r["routing_signature"], r["subject"]))
        else:
            print("%-9s %-6s %s" % (r["commit"], "-", "SKIP: %s" % r.get("skip")))
    print()
    if not diffs:
        print("相邻版本之间路由签名无变化。")
    else:
        print("相邻版本变化点 %d 处：" % len(diffs))
        for d in diffs:
            print("  %s -> %s : %s" % (d["from"], d["to"], d["changed"]))
            for k in d["changed"]:
                print("      %s: %s -> %s" % (k, d["from_vals"][k], d["to_vals"][k]))
    print()
    print("⚠️ 边界：这里测的是**路由形状**，不是回答质量（回答质量要调模型）。")
    print("   distinct_voices 变小不必然是塌了 —— 要和 roster_size 一起看。")


if __name__ == "__main__":
    main()
