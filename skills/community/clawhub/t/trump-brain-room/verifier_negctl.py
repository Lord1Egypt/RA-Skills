#!/usr/bin/env python3
"""
verifier_negctl.py —— **决策记录核验器**的负控矩阵

@kobolsix: "Two implementations can share the same mistaken specification, so add
metamorphic properties and **adversarial record mutations** beside replay."

→ 我自己的差分核验（`--verify` 用**独立实现**重算）**只有正控**：
  「没被篡改的记录 → 一致 → exit 0」。**没有任何一行证明它能拒绝被篡改的记录。**
→ 这正是我自己那条老教训的同型坑：**一个不会失败的检查，证明不了任何东西。**
  而 `--verify` 是我 repo 里**唯一**的「证据」环节。

⚠️ **我在做这个矩阵的时候，发现了一个真的 bug**：
   `cond_bad`（条件不一致）**只被打印，不影响退出码**。
   → 一条被篡改了 `weights` 或 `profile_hash` 的记录，重算照样「一致」，
     `verify && echo verified` **会放行**。
   → 已修：退出码 0=完全一致 / 1=路由分歧 / 2=条件被改 / 3=两者都有。
   → 而**「按它为什么被拒绝」分类**是必须的：只给一个笼统的非零，
     下游就无法区分「路由真的变了」和「记录被人动过」。

矩阵的每一行声明：
  · 它篡改了什么（mutation class）
  · 它期望核验器给出什么退出码
  · 以及**它为什么会被拒绝**（marker：`[DIFF]` / `[COND]`）——
    一个「因为别的原因红」的核验器，等于没有核验器。

用法:
    python3 verifier_negctl.py            # 退出码 0 = 全部符合预期
    python3 verifier_negctl.py --json     # 机器可读
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))

# 退出码契约（必须与 decision_log.py --verify 一致）
EXIT_OK = 0        # 完全一致
EXIT_DIFF = 1      # 路由分歧（重算选的人不一样）
EXIT_COND = 2      # 条件被改（记录自述的 hash / 权重对不上）
EXIT_BOTH = 3      # 两者都有


def _run(args, cwd=ROOT):
    p = subprocess.run([sys.executable] + args, cwd=cwd,
                       capture_output=True, text=True, timeout=300)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def _make_records(tmpdir):
    """生成一份**未篡改**的基线记录。"""
    out = os.path.join(tmpdir, "base.jsonl")
    rc, log = _run(["decision_log.py", "--out", out, "--no-state"])
    if rc != 0 or not os.path.exists(out):
        return None, log
    rows = [json.loads(l) for l in open(out, encoding="utf-8") if l.strip()]
    if not rows:
        return None, "基线记录为空"
    return rows, log


def _write(rows, path):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def mut_chosen(rows):
    """改选中集合 —— 记录说选了别人。"""
    out = [dict(r) for r in rows]
    out[0]["chosen"] = ["__TAMPERED__"]
    return out, "改写第 1 条的 chosen"


def mut_source(rows):
    """改来源标签 —— 记录说走了另一条路。"""
    out = [dict(r) for r in rows]
    out[0]["source"] = "__TAMPERED__"
    return out, "改写第 1 条的 source"


def mut_profile_hash(rows):
    """改记录自述的条件 hash。"""
    out = [dict(r) for r in rows]
    out[0]["profile_hash"] = "deadbeef0000"
    return out, "改写第 1 条的 profile_hash"


def mut_weights(rows):
    """改权重 —— 条件本身被动了。"""
    out = [dict(r) for r in rows]
    w = dict(out[0].get("weights") or {})
    if w:
        w[list(w)[0]] = 999
        out[0]["weights"] = w
    return out, "改写第 1 条的 weights"


def mut_both(rows):
    """同时改路由结果和条件 —— 两者都有。"""
    out = [dict(r) for r in rows]
    out[0]["chosen"] = ["__TAMPERED__"]
    w = dict(out[0].get("weights") or {})
    if w:
        w[list(w)[0]] = 999
        out[0]["weights"] = w
    return out, "同时改写 chosen 与 weights"


# (break class, 描述, 期望退出码, 期望 marker, 变异函数)
ROWS = [
    ("baseline", "没篡改", EXIT_OK, "[VERIFY]", None),
    ("tamper_chosen", "改写选中集合", EXIT_DIFF, "[DIFF]", mut_chosen),
    ("tamper_source", "改写来源标签", EXIT_DIFF, "[DIFF]", mut_source),
    ("tamper_profile_hash", "改写条件 hash", EXIT_COND, "[COND]", mut_profile_hash),
    ("tamper_weights", "改写权重", EXIT_COND, "[COND]", mut_weights),
    ("tamper_both", "同时改路由与条件", EXIT_BOTH, "[DIFF]", mut_both),
]


def _classify(rc, out, expect, marker):
    """三态判定：PASS / FAIL / INCONCLUSIVE。
    一个「因为别的原因红」的核验器 = 没有核验器 → 那也是 FAIL，不是 PASS。"""
    if rc == 0 and expect == EXIT_OK:
        return ("PASS", "按预期的方式绿了") if marker in out else \
               ("FAIL", "退出码对，但缺少证据标记 %s" % marker)
    if rc == 0:
        return "FAIL", "退出码是 0 —— **篡改被放行了**"
    if rc not in (EXIT_DIFF, EXIT_COND, EXIT_BOTH):
        return "INCONCLUSIVE", "退出码 %s 不在契约里（0/1/2/3）—— 无法判断" % rc
    if rc != expect:
        return "FAIL", "退出码 %s，期望 %s —— 它因为**别的原因**红了" % (rc, expect)
    if marker not in out:
        return "FAIL", "退出码对，但缺少理由标记 %s —— 不知道为什么拒绝的" % marker
    return "PASS", "按预期的方式红了"


def run_matrix():
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        base, log = _make_records(tmp)
        if base is None:
            return {"rows": [{"break_class": "baseline", "status": "INCONCLUSIVE",
                              "why": "生成基线记录失败：%s" % log[:200]}],
                    "n": 1, "n_fail": 0, "n_inconclusive": 1, "n_pass": 0,
                    "detectable_breaks": [], "exit_contract": [EXIT_OK, EXIT_DIFF,
                                                              EXIT_COND, EXIT_BOTH]}
        for cls, what, expect, marker, mut in ROWS:
            if mut is None:
                path = os.path.join(tmp, "base.jsonl")
                target = base
            else:
                target, _desc = mut(base)
                path = os.path.join(tmp, cls + ".jsonl")
                _write(target, path)
            rc, out = _run(["decision_log.py", "--verify", path])
            status, why = _classify(rc, out, expect, marker)
            rows.append({"break_class": cls, "what": what,
                         "expected_exit": expect, "actual_exit": rc,
                         "expect_marker": marker, "marker_seen": marker in out,
                         "status": status, "pass": status == "PASS", "why": why,
                         "evidence": out.strip().splitlines()[-1][:160] if out.strip() else ""})
    n_fail = sum(1 for r in rows if r["status"] == "FAIL")
    n_inc = sum(1 for r in rows if r["status"] == "INCONCLUSIVE")
    return {"rows": rows, "n": len(rows),
            "n_pass": sum(1 for r in rows if r["status"] == "PASS"),
            "n_fail": n_fail, "n_inconclusive": n_inc,
            "detectable_breaks": [r["break_class"] for r in rows if r["pass"]],
            "exit_contract": [EXIT_OK, EXIT_DIFF, EXIT_COND, EXIT_BOTH]}


def main():
    ap = argparse.ArgumentParser(description="核验器的负控矩阵")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    res = run_matrix()
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0 if (res["n_fail"] == 0 and res["n_inconclusive"] == 0) else 1
    print("[VNEGCTL] 核验器负控矩阵 —— 这套测试**能发现哪些篡改**")
    for r in res["rows"]:
        flag = {"PASS": "OK  ", "FAIL": "FAIL", "INCONCLUSIVE": "????"}[r["status"]]
        print(f"  {flag} {r['break_class']:22} {r.get('what', ''):16} "
              f"期望 exit={r.get('expected_exit')} 实际 exit={r.get('actual_exit')}"
              f"  {r.get('why', '')}")
    print(f"[VNEGCTL] {res['n_pass']}/{res['n']} 行符合预期")
    print(f"[VNEGCTL] 可发现的篡改类：{', '.join(res['detectable_breaks'])}")
    print("[VNEGCTL] ⚠️ 绿灯**只接到这些**上；没列出来的篡改类，这套测试发现不了。")
    return 0 if (res["n_fail"] == 0 and res["n_inconclusive"] == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
