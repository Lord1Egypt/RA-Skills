# -*- coding: utf-8 -*-
"""
能力评测套件总入口（持续能力进化闭环·感知层）
- 读 suite_registry.json，遍历 enabled 模块
- 每个模块：subprocess 跑其 script（cwd=脚本所在目录），读 report
- 对比 baseline / warn_below，判定 pass / warn / fail
- 汇总 suite_report.json（最新）+ suite_history.jsonl（能力进化轨迹）+ 打印摘要
"""
import os, json, subprocess, datetime, sys

SUITE_DIR = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.join(SUITE_DIR, "suite_registry.json")
RESULTS_DIR = os.path.join(SUITE_DIR, "results")
PY = sys.executable  # 使用当前解释器，无需硬编码路径

STATUS_RANK = {"pass": 0, "warn": 1, "fail": 2, "error": 3, "missing": 1}

def judge(val, base, warn):
    if val is None:
        return "missing"
    if val >= base:
        return "pass"
    if val >= warn:
        return "warn"
    return "fail"

def run_module(mod):
    script = os.path.normpath(os.path.join(SUITE_DIR, mod["script"]))
    script_dir = os.path.dirname(script)
    if not os.path.exists(script):
        return {"module_id": mod["id"], "status": "error", "error": f"脚本不存在: {script}"}
    print(f"\n>>> 运行模块 [{mod['id']}] {mod['name']}")
    try:
        r = subprocess.run([PY, script], cwd=script_dir,
                           capture_output=True, text=True, timeout=300)
    except Exception as e:
        return {"module_id": mod["id"], "status": "error", "error": str(e)}
    if r.returncode != 0:
        return {"module_id": mod["id"], "status": "error",
                "error": (r.stderr or r.stdout)[-600:]}
    report_path = os.path.normpath(os.path.join(SUITE_DIR, mod.get("report", "../rag_eval_report.json")))
    if not os.path.exists(report_path):
        return {"module_id": mod["id"], "status": "error", "error": f"报告未生成: {report_path}"}
    report = json.load(open(report_path, encoding="utf-8"))

    metrics = []
    worst = "pass"
    for m in mod.get("metrics", []):
        val = report.get(m["key"])
        st = judge(val, m.get("baseline", 1.0), m.get("warn_below", 0))
        metrics.append({"label": m["label"], "key": m["key"], "unit": m.get("unit"),
                        "value": val, "baseline": m.get("baseline"),
                        "warn_below": m.get("warn_below"), "status": st})
        if STATUS_RANK[st] > STATUS_RANK[worst]:
            worst = st
    return {"module_id": mod["id"], "name": mod["name"], "owner": mod.get("owner"),
            "status": worst, "metrics": metrics,
            "engine": report.get("engine"), "corpus_size": report.get("corpus_size"),
            "total": report.get("total")}

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    reg = json.load(open(REGISTRY, encoding="utf-8"))
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    modules_out, alerts = [], []
    suite_worst = "pass"
    for mod in reg.get("modules", []):
        if not mod.get("enabled", True):
            continue
        res = run_module(mod)
        if res.get("status") in ("error", "missing", "fail"):
            alerts.append(f"[{res.get('module_id')}] 状态={res.get('status')} "
                          + res.get("error", "指标缺失"))
        elif res.get("status") == "warn":
            alerts.append(f"[{res.get('module_id')}] 有指标低于基线但未触底")
        if res.get("metrics"):
            for mt in res["metrics"]:
                if mt["status"] in ("fail", "warn", "missing"):
                    alerts.append(f"  - {mt['label']}={mt['value']} ({mt['status']})")
        if STATUS_RANK.get(res.get("status"), 0) > STATUS_RANK[suite_worst]:
            suite_worst = res.get("status")
        modules_out.append(res)

    suite_report = {
        "suite_name": reg["suite_name"],
        "version": reg.get("version"),
        "run_at": now,
        "overall_status": suite_worst,
        "modules": modules_out,
        "alerts": alerts,
    }
    rp = os.path.join(SUITE_DIR, "suite_report.json")
    json.dump(suite_report, open(rp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    # 进化轨迹（每日滚动追加）
    hist = os.path.join(SUITE_DIR, "suite_history.jsonl")
    with open(hist, "a", encoding="utf-8") as f:
        f.write(json.dumps({"run_at": now, "overall_status": suite_worst,
                            "modules": [{k: m[k] for k in ("module_id", "status")} for m in modules_out]},
                           ensure_ascii=False) + "\n")

    print("\n================ 能力评测套件汇总 ================")
    print(f"运行时间 : {now}")
    print(f"整体状态 : {suite_worst.upper()}")
    for m in modules_out:
        print(f"  [{m.get('status','?').upper()}] {m.get('name')}")
        for mt in m.get("metrics", []):
            v = mt["value"]
            vs = f"{v:.1%}" if mt["unit"] == "rate" and isinstance(v, (int, float)) else str(v)
            print(f"      - {mt['label']}: {vs} ({mt['status']})")
    if alerts:
        print(f"\n⚠️ 告警 {len(alerts)} 条：")
        for a in alerts:
            print("  " + a)
    else:
        print("\n✅ 无告警，全部达标")
    print(f"\n报告: {rp}")
    print(f"轨迹: {hist}")

if __name__ == "__main__":
    main()
