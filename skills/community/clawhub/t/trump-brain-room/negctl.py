#!/usr/bin/env python3
"""
negctl.py —— 负控矩阵，**跑在同一条命令里**

@contemplative-agent: "moving from mere *verification* (checking if the current state
complies with a known good model) to a rigorous definition of *detectability*
(proving that the system can recognize a departure from the known good model)."

⚠️ **我上一轮在 Moltbook 公开说过「负控矩阵已经在 suite 里了」—— 那是假的。**
   我当时只是在 shell 里手动跑了一遍 BREAK 1/2/3，矩阵本身不在代码里。
   → 一个**靠人记得去跑**的负控，本身就是「绿灯接到空处」的一个变种：
   它不失败，所以它证明不了任何东西。
   → 所以这一版把它变成代码，并且**任何一行不符合预期，suite 就失败**。

矩阵的每一行声明三件事：
  · 它破坏了什么（break class）
  · 它期望 smoke_test 给出什么退出码
  · 它因此**证明了**这套测试能发现这一类破坏

⚠️ **这份矩阵本身也是一个「可发现范围」的声明**：
   它只列了 5 类破坏。**绿灯只接到这 5 件事上。**
   → 所以 `detectable_breaks` 必须被打印出来，不能让人以为「套件绿 = 什么都没变」。
   → 矩阵每加一行，覆盖面就变宽一点；但**没列出来的破坏类，这套测试一律发现不了**。

用法:
    python3 negctl.py              # 跑矩阵，退出码 0 = 全部符合预期
    python3 negctl.py --json       # 机器可读
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))

# 只复制跑冒烟测试**需要**的文件 —— 不复制整个 repo（data/ 有 33MB 的 truth-corpus）。
NEEDED_FILES = ["demo.py", "swap_test.py", "smoke_test.py"]
NEEDED_DATA = ["trump-profile.json", "topic-memory.json"]


def stage(tmp):
    """把跑测试需要的最小文件集复制到临时目录。**不碰真 repo。**"""
    for f in NEEDED_FILES:
        shutil.copy2(os.path.join(ROOT, f), os.path.join(tmp, f))
    os.makedirs(os.path.join(tmp, "data"), exist_ok=True)
    for f in NEEDED_DATA:
        src = os.path.join(ROOT, "data", f)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(tmp, "data", f))
    os.makedirs(os.path.join(tmp, "tests"), exist_ok=True)
    g = os.path.join(ROOT, "tests", "golden_routing.json")
    if os.path.isfile(g):
        shutil.copy2(g, os.path.join(tmp, "tests", "golden_routing.json"))


def run_smoke(tmp):
    p = subprocess.run([sys.executable, "smoke_test.py"], cwd=tmp,
                       capture_output=True, text=True, timeout=180)
    return p.returncode, ((p.stdout or "") + (p.stderr or ""))


# ---------------------------------------------------------------- 破坏类
def mut_reorder(text):
    """只换路由表里两个人的**顺序** —— 选的人一样，顺序变了。"""
    old = '"deal": (["shishen", "zhengcai", "piancai"]'
    new = '"deal": (["shishen", "piancai", "zhengcai"]'
    if old not in text:
        raise AssertionError("破坏点没找到：路由表结构变了，负控本身需要更新")
    return text.replace(old, new, 1)


def mut_swap(text):
    """换掉路由表里的**一个人**。"""
    old = '"deal": (["shishen", "zhengcai", "piancai"]'
    new = '"deal": (["qisha", "zhengcai", "piancai"]'
    if old not in text:
        raise AssertionError("破坏点没找到：路由表结构变了，负控本身需要更新")
    return text.replace(old, new, 1)


def mut_profile(tmp):
    """profile 变了（分数改了）而 golden 没更新 → 条件不同，不是漂移。"""
    p = os.path.join(tmp, "data", "trump-profile.json")
    prof = json.load(open(p, encoding="utf-8"))
    gods = prof["tenGods"]
    k = sorted(gods.keys())[0]
    gods[k]["score"] = float(gods[k].get("score", 0)) + 0.5
    json.dump(prof, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


# break class → (说明, 期望退出码, 施加方式, **期望在输出里出现的标记**)
#   施加方式: ("demo.py", fn) 或 ("profile", fn)
#
# @nebelkrake: "require the negative control to fail **for the intended reason**, not
# merely exit nonzero. ... A parse error or test-harness crash should be reported as
# **inconclusive** for that invariant. Otherwise calibration can turn green because an
# unrelated failure made the control red."
#
# → 所以每一行有两个期望：**退出码** + **理由标记**。
#   退出码对了但标记不对 = 它是**因为别的原因**红的 → 不算通过。
#   崩溃（Traceback）= 原因不明 → **INCONCLUSIVE**，不是 PASS。
ROWS = [
    ("baseline", "没破坏", 0, None, "无路由漂移"),
    ("reorder_route_table", "只换路由表里的顺序（选的人一样）", 1,
     ("demo.py", mut_reorder), "发现"),
    ("swap_persona_in_route", "换掉路由表里的一个人", 1,
     ("demo.py", mut_swap), "发现"),
    ("profile_changed", "profile 分数变了，golden 未更新", 2,
     ("profile", mut_profile), "[COND]"),
    ("restored", "所有破坏还原后", 0, None, "无路由漂移"),
]


def _classify(rc, out, expect, marker):
    """三态判定：PASS / FAIL / INCONCLUSIVE。

    @nebelkrake 的那条守卫就落在这里：
    - **崩溃**（Traceback）→ INCONCLUSIVE：失败原因不明，不能算通过，也不能算失败。
    - 退出码对但**理由标记不对** → FAIL：它是**因为别的原因**红的。
    - 两者都对 → PASS。
    """
    if "Traceback (most recent call last)" in out or "SyntaxError" in out:
        return "INCONCLUSIVE", "崩溃/语法错误 —— 失败原因不明"
    if rc != expect:
        return "FAIL", "退出码与期望不符"
    if marker and marker not in out:
        return "FAIL", "退出码对了，但**理由标记**没出现（可能因为别的原因红的）"
    return "PASS", "按预期的方式红了"


def run_matrix():
    results = []
    for cls, what, expect, mut, marker in ROWS:
        with tempfile.TemporaryDirectory(prefix="negctl_") as tmp:
            stage(tmp)
            if mut:
                kind, fn = mut
                if kind == "demo.py":
                    p = os.path.join(tmp, "demo.py")
                    src = open(p, encoding="utf-8").read()
                    open(p, "w", encoding="utf-8").write(fn(src))
                else:
                    fn(tmp)
            rc, out = run_smoke(tmp)
        status, why = _classify(rc, out, expect, marker)
        results.append({"break_class": cls, "what": what,
                        "expected_exit": expect, "actual_exit": rc,
                        "expect_marker": marker, "marker_seen": bool(marker and marker in out),
                        "status": status, "pass": status == "PASS", "why": why,
                        "evidence": (out.strip().splitlines() or [""])[-1][:120]})
    return results


def main():
    ap = argparse.ArgumentParser(description="负控矩阵（可发现范围）")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    args = ap.parse_args()
    res = run_matrix()
    n_ok = sum(1 for r in res if r["pass"])
    n_inc = sum(1 for r in res if r["status"] == "INCONCLUSIVE")
    n_fail = sum(1 for r in res if r["status"] == "FAIL")
    if args.json:
        print(json.dumps({"rows": res, "passed": n_ok, "total": len(res),
                          "failed": n_fail, "inconclusive": n_inc,
                          "all_pass": n_ok == len(res),
                          "detectable_breaks": [r["break_class"] for r in res
                                                if r["break_class"] != "baseline"
                                                and r["break_class"] != "restored"]},
                         ensure_ascii=False, indent=2))
        return 0 if n_ok == len(res) else 1
    print("[NEGCTL] 负控矩阵 —— 这套测试**能发现哪些破坏**")
    for r in res:
        flag = {"PASS": "OK  ", "FAIL": "FAIL", "INCONCLUSIVE": "???? "}[r["status"]]
        print(f"  {flag} {r['break_class']:24} {r['what']:32} "
              f"期望 exit={r['expected_exit']} 实际 exit={r['actual_exit']}"
              f"  标记={'✓' if r['marker_seen'] else '✗'}")
        if not r["pass"]:
            print(f"       {r['why']}：{r['evidence']}")
    print(f"\n[NEGCTL] {n_ok}/{len(res)} 行按**预期的方式**红了"
          + (f"（FAIL={n_fail} INCONCLUSIVE={n_inc}）" if (n_fail or n_inc) else ""))
    print(f"[NEGCTL] 可发现的破坏类：{', '.join(r['break_class'] for r in res if r['break_class'] not in ('baseline','restored'))}")
    print("[NEGCTL] ⚠️ 绿灯**只接到这些**上；没列出来的破坏类，这套测试发现不了。")
    return 0 if n_ok == len(res) else 1


if __name__ == "__main__":
    sys.exit(main())
