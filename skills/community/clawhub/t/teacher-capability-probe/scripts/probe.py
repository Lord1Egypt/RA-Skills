#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""teacher-capability-probe: 对教师(WorkBuddy 内部模型/专家技能)做能力探针与评测，
量化其能力边界与失败模式，产出结构化能力画像——这是「跨模型蒸馏」工程化收口的关键子能力
(发现→探针→提取→合成→对抗验证)之一，让蒸馏不再"凭手感"，而是用探针任务量化教师能力边界。

能力：
  - 探针生成：gen_probes(signature) 从能力签名(标题/工作流步/限制)派生覆盖性探针任务
  - 评测：evaluate(probes, results) 覆盖 pass/fail/partial，定位失败模式，算置信与边界
  - 能力画像：report() 输出 {coverage, failure_modes, confidence, boundary, probes[]}
  - 置信自检：selftest 覆盖 探针生成 / 覆盖统计 / 失败模式发现 / 置信计算 / 边界判定

用法：
  python probe.py --selftest
  python probe.py --signature '{"capabilities":["翻译","摘要"],"limits":["不擅长长文"]}'
  python probe.py --eval-json '[{"probe":"翻译短句","result":"pass"},...]'
"""
import argparse
import json
import sys
import datetime


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


# 由能力名派生探针模板（覆盖核心用法 + 边界/失败易发场景）
PROBE_TEMPLATES = {
    "翻译": ["翻译一句日常短句", "翻译一段含术语的专业段落", "翻译一首古诗(文化负载)"],
    "摘要": ["摘取 3 条要点", "对 5000 字长文做结构化摘要", "摘要后保留关键数字"],
    "推理": ["单步逻辑推导", "多步链式推理", "含反例的归谬推理"],
    "编码": ["写一个函数", "调试一段报错代码", "重构已有模块"],
    "检索": ["精确关键词检索", "模糊语义检索", "跨文档去重聚合"],
    "规划": ["拆解 3 步任务", "含依赖的 10 步里程碑规划", "资源受限下的重规划"],
}
GENERIC = ["核心用法探针", "边界/异常输入探针", "多步组合探针"]


def gen_probes(signature):
    """从签名派生覆盖性探针。signature: {capabilities:[], limits:[]}。"""
    caps = signature.get("capabilities", []) or []
    limits = signature.get("limits", []) or []
    probes = []
    for cap in caps:
        base = None
        for key, tmpl in PROBE_TEMPLATES.items():
            if key in cap:
                base = tmpl
                break
        if base:
            for t in base:
                probes.append({"capability": cap, "probe": t, "kind": "core"})
        else:
            for g in GENERIC:
                probes.append({"capability": cap, "probe": f"{cap}：{g}", "kind": "generic"})
    # 针对已知限制生成对抗/边界探针
    for lim in limits:
        probes.append({"capability": "(限制)", "probe": f"边界探查：{lim}", "kind": "limit"})
    if not probes:
        probes.append({"capability": "(无签名)", "probe": "通用能力探针", "kind": "generic"})
    return probes


def _norm(r):
    return (r or "fail").lower()


def evaluate(probes, results):
    """results: list of {probe, result, note?} 或 [(probe,result)]。返回评测结构。"""
    records = []
    fail_modes = {}
    n_pass = n_partial = n_fail = 0
    for i, p in enumerate(probes):
        res = results[i] if i < len(results) else {"result": "fail"}
        if isinstance(res, dict):
            r = _norm(res.get("result"))
            note = res.get("note", "")
        else:
            r = _norm(res)
            note = ""
        rec = {"capability": p["capability"], "probe": p["probe"],
               "kind": p["kind"], "result": r, "note": note}
        if r == "pass":
            n_pass += 1
        elif r == "partial":
            n_partial += 1
            fail_modes.setdefault(p["capability"], []).append(note or "部分通过")
        else:
            n_fail += 1
            fail_modes.setdefault(p["capability"], []).append(note or "未通过")
        records.append(rec)
    total = len(probes) or 1
    coverage = (n_pass + 0.5 * n_partial) / total
    # 置信：覆盖率 + 失败模式分散度惩罚
    n_caps = len({r["capability"] for r in records}) or 1
    spread = sum(len(v) for v in fail_modes.values())
    confidence = max(0.0, round(coverage - 0.05 * spread / n_caps, 3))
    # 能力边界：每能力 pass 率低于 0.5 视为薄弱边界
    by_cap = {}
    for r in records:
        c = r["capability"]
        by_cap.setdefault(c, {"n": 0, "ok": 0})
        by_cap[c]["n"] += 1
        if r["result"] in ("pass", "partial"):
            by_cap[c]["ok"] += 1
    boundary = {c: round(v["ok"] / v["n"], 2)
                for c, v in by_cap.items() if v["n"] and v["ok"] / v["n"] < 0.5}
    return {
        "ts": now(),
        "total": len(probes),
        "n_pass": n_pass,
        "n_partial": n_partial,
        "n_fail": n_fail,
        "coverage": round(coverage, 3),
        "confidence": confidence,
        "failure_modes": fail_modes,
        "weak_boundary": boundary,
        "records": records,
    }


# ---------------------------------------------------------------------------
def selftest():
    sig = {"capabilities": ["翻译", "摘要"], "limits": ["不擅长长文"]}
    probes = gen_probes(sig)
    assert len(probes) >= 6, f"探针数不足: {len(probes)}"
    print(f"[1] 探针生成（翻译3+摘要3+限制1={len(probes)}） ✓")

    # 评测：翻译全过，摘要1过1partial1fail，限制探针 fail
    results = [
        {"result": "pass"}, {"result": "pass"}, {"result": "pass"},
        {"result": "pass"}, {"result": "partial", "note": "遗漏数字"},
        {"result": "fail", "note": "长文丢失结构"},
        {"result": "fail", "note": "长文超限"},
    ]
    rep = evaluate(probes, results)
    assert rep["total"] == len(probes)
    assert rep["n_pass"] == 4 and rep["n_partial"] == 1 and rep["n_fail"] == 2
    print(f"[2] 覆盖统计 pass={rep['n_pass']} partial={rep['n_partial']} fail={rep['n_fail']} ✓")

    # 失败模式发现
    assert "摘要" in rep["failure_modes"], rep["failure_modes"]
    assert any("数字" in m for m in rep["failure_modes"]["摘要"])
    print(f"[3] 失败模式发现: {list(rep['failure_modes'].keys())} ✓")

    # 置信计算（0<=conf<=1）
    assert 0.0 <= rep["confidence"] <= 1.0, rep["confidence"]
    print(f"[4] 置信度 = {rep['confidence']} ✓")

    # 边界判定：限制探针 fail -> (限制) 进 weak_boundary
    assert "(限制)" in rep["weak_boundary"], rep["weak_boundary"]
    print(f"[5] 能力边界薄弱项: {rep['weak_boundary']} ✓")

    print("\n✅ teacher-capability-probe selftest 全部通过")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--signature")
    ap.add_argument("--eval-json")
    args = ap.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    if args.signature:
        sig = json.loads(args.signature)
        probes = gen_probes(sig)
        print(json.dumps(probes, ensure_ascii=False, indent=2))
        return 0
    if args.eval_json:
        data = json.loads(args.eval_json)
        probes = data.get("probes") or gen_probes(data.get("signature", {}))
        rep = evaluate(probes, data.get("results", []))
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return 0
    print("用法: --selftest | --signature '{...}' | --eval-json '{...}'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
