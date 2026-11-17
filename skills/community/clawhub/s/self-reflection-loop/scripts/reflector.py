#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reflector.py — 自我反思闭环引擎（超越性元能力 #2）

设计依据（2023-2026 主流研究）：
  - Reflexion (Shinn 2023, NeurIPS)：Actor → Evaluator → Self-Reflection；失败教训以「自然语言」存入记忆，
    并在下一轮拼回 Actor 提示词（**关键：教训必须回灌**）。verbal reinforcement，无需梯度更新。
  - Self-Refine (Madaan 2023)：生成 → 自批评 → 精炼，迭代提升。
  - PRM (Process Reward Model)：对**每一步**打分，早期错误检测、引导搜索（而非只在终点判对错）。
  - 工具锚定验证 (tool-grounded)：代码用 py_compile/单测、事实用检索、计算用执行，比纯自省更可靠。
  - 停止准则：基于质量阈值/分数，而非固定迭代次数。

本脚本提供**确定性、可复跑**的反思测量仪表：
  - 内置可扩展 rubric（带权重与多种检查类型：关键词 / 最小字数 / 代码编译 / 正则）
  - assess：对产物做结构化自评 + 工具锚定校验，输出分数、缺口、整改清单
  - loop：生成→评估→（可选 refine-cmd 自动整改）→再评估，直到达到阈值或上限（Reflexion 闭环）
  - log：复盘历史，沉淀「反复出现的失败模式」

用法：
  python reflector.py init   --out rubric.json [--preset code|text|generic]
  python reflector.py assess <artifact> --rubric rubric.json --out report.md [--json]
  python reflector.py loop   <artifact> --rubric rubric.json --max 3 [--threshold 0.8] [--refine-cmd "..."]
  python reflector.py log    reflect_log.json
"""
import os, sys, json, argparse, subprocess, re, datetime

PRESETS = {
    "generic": [
        {"key": "completeness", "desc": "覆盖任务核心诉求", "weight": 0.4, "type": "min_words", "arg": 80},
        {"key": "structure",    "desc": "具备清晰结构/分段", "weight": 0.3, "type": "keyword", "arg": ["#", "##", "1.", "第一步", "步骤"]},
        {"key": "actionable",   "desc": "给出可执行结论", "weight": 0.3, "type": "keyword", "arg": ["建议", "步骤", "执行", "结论", "方案"]},
    ],
    "code": [
        {"key": "compiles",   "desc": "语法可编译 (py_compile)", "weight": 0.5, "type": "code_compile"},
        {"key": "docstring",  "desc": "含模块/函数文档", "weight": 0.2, "type": "keyword", "arg": ["\"\"\"", "'''"]},
        {"key": "structure",  "desc": "具备函数/类封装", "weight": 0.15, "type": "regex", "arg": r"(def |class )"},
        {"key": "readme",     "desc": "含用法说明", "weight": 0.15, "type": "keyword", "arg": ["用法", "usage", "example", "示例"]},
    ],
    "text": [
        {"key": "length",     "desc": "足够展开 (>=200字)", "weight": 0.3, "type": "min_words", "arg": 200},
        {"key": "evidence",   "desc": "含论据/数据/引用", "weight": 0.35, "type": "keyword", "arg": ["因为", "数据", "研究", "例如", "依据"]},
        {"key": "structure",  "desc": "有层次结构", "weight": 0.2, "type": "keyword", "arg": ["#", "##", "第一", "首先", "1."]},
        {"key": "closure",    "desc": "有结论/行动项", "weight": 0.15, "type": "keyword", "arg": ["结论", "建议", "总结", "行动"]},
    ],
}


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def check_criterion(c, text):
    """返回 (passed:bool, detail:str)。"""
    t = c.get("type")
    arg = c.get("arg")
    if t == "min_words":
        n = len(re.findall(r"\S+", text))
        ok = n >= int(arg)
        return ok, f"字数 {n} / 要求 >= {arg}"
    if t == "keyword":
        keys = arg if isinstance(arg, list) else [arg]
        hit = [k for k in keys if k in text]
        return bool(hit), f"命中 {hit or '无'} / 候选 {keys}"
    if t == "regex":
        ok = re.search(arg, text) is not None
        return ok, f"正则 {arg} 命中={ok}"
    if t == "code_compile":
        if not text.strip().endswith(".py"):
            # 直接传入源码字符串时写临时文件编译
            tmp = "_reflect_tmp.py"
            open(tmp, "w", encoding="utf-8").write(text)
            fp = tmp
        else:
            fp = text
        r = subprocess.run([sys.executable, "-m", "py_compile", fp],
                           capture_output=True, text=True)
        if os.path.exists("_reflect_tmp.py"):
            os.remove("_reflect_tmp.py")
        return r.returncode == 0, (r.stderr.strip()[:300] or "编译通过")
    return False, f"未知检查类型 {t}"


def assess(artifact, rubric):
    text = artifact
    if os.path.exists(artifact):
        try:
            text = open(artifact, encoding="utf-8").read()
        except Exception:
            pass
    results = []
    total_w = 0.0
    earned = 0.0
    for c in rubric["criteria"]:
        ok, detail = check_criterion(c, text)
        w = c.get("weight", 0)
        total_w += w
        if ok:
            earned += w
        results.append({
            "key": c["key"], "desc": c.get("desc", ""), "weight": w,
            "passed": ok, "detail": detail,
            "rectify": "" if ok else f"针对「{c.get('desc','')}」补充：{detail}",
        })
    score = round(earned / total_w, 3) if total_w else 0.0
    gaps = [r for r in results if not r["passed"]]
    return {"score": score, "results": results, "gaps": gaps}


def render_report(art, rubric, res):
    L = [f"# 反思评估 · {os.path.basename(art)}",
         "", f"- 时间: {now()} ｜ 综合分: **{res['score']:.2f}** / 1.00", ""]
    L.append("| 维度 | 权重 | 通过 | 细节 |")
    L.append("|------|------|------|------|")
    for r in res["results"]:
        L.append(f"| {r['key']} ({r['desc']}) | {r['weight']} | {'✅' if r['passed'] else '❌'} | {r['detail']} |")
    L.append("")
    L.append("## 缺口与整改清单")
    if not res["gaps"]:
        L.append("（无，达标）")
    else:
        for i, g in enumerate(res["gaps"], 1):
            L.append(f"{i}. **{g['key']}** — {g['rectify']}")
    L.append("")
    L.append("> 闭环：将上面对应整改项回灌下一轮生成（Reflexion：教训必须回灌 Actor），"
             "直至综合分 ≥ 阈值或达到迭代上限。")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="自我反思闭环引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init"); p.add_argument("--out", required=True); p.add_argument("--preset", default="generic")
    def f_init(a):
        if a.preset not in PRESETS:
            print(f"❌ 预设 {a.preset} 不存在，可选 {list(PRESETS)}"); return
        rubric = {"version": 1, "preset": a.preset,
                  "criteria": PRESETS[a.preset]}
        json.dump(rubric, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"✅ rubric -> {a.out}（{len(rubric['criteria'])} 项，预设 {a.preset}）")
    p.set_defaults(func=f_init)

    p = sub.add_parser("assess"); p.add_argument("artifact"); p.add_argument("--rubric", required=True); p.add_argument("--out"); p.add_argument("--json", action="store_true")
    def f_assess(a):
        rubric = json.load(open(a.rubric, encoding="utf-8"))
        res = assess(a.artifact, rubric)
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            print(render_report(a.artifact, rubric, res))
        if a.out:
            open(a.out, "w", encoding="utf-8").write(render_report(a.artifact, rubric, res))
            print(f"📄 报告已写入 {a.out}")
    p.set_defaults(func=f_assess)

    p = sub.add_parser("loop"); p.add_argument("artifact"); p.add_argument("--rubric", required=True); p.add_argument("--max", type=int, default=3); p.add_argument("--threshold", type=float, default=0.8); p.add_argument("--refine-cmd", default="")
    def f_loop(a):
        rubric = json.load(open(a.rubric, encoding="utf-8"))
        log = {"artifact": a.artifact, "threshold": a.threshold, "runs": []}
        cur = a.artifact
        for it in range(1, a.max + 1):
            res = assess(cur, rubric)
            log["runs"].append({"iter": it, "artifact": cur, "score": res["score"],
                                "gaps": [g["key"] for g in res["gaps"]]})
            print(f"🔁 第 {it} 轮：综合分 {res['score']:.2f} ｜ 缺口 {[g['key'] for g in res['gaps']]}")
            if res["score"] >= a.threshold:
                print(f"✅ 达到阈值 {a.threshold}，闭环收敛。")
                break
            if a.refine_cmd:
                # 自动整改：把本轮缺口作为上下文交给 refine 命令，产出下一版产物
                gap_txt = "; ".join(g["rectify"] for g in res["gaps"])
                cmd = a.refine_cmd.replace("{artifact}", cur).replace("{gaps}", gap_txt)
                r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                nxt = (r.stdout or "").strip().splitlines()
                nxt = nxt[-1] if nxt else ""
                if nxt and os.path.exists(nxt):
                    cur = nxt
                    print(f"   ↳ refine 产出: {cur}")
                else:
                    print(f"   ⚠️ refine 未产出新产物路径（stdout 末行应为新文件路径）")
            else:
                print("   ⚠️ 无 --refine-cmd，请人工整改后再次 loop（或传入 refine 命令形成自动闭环）。")
        log["converged"] = log["runs"][-1]["score"] >= a.threshold if log["runs"] else False
        json.dump(log, open("reflect_log.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"📜 复盘历史 -> reflect_log.json")
    p.set_defaults(func=f_loop)

    p = sub.add_parser("log"); p.add_argument("path")
    def f_log(a):
        log = json.load(open(a.path, encoding="utf-8"))
        print(f"闭环历史（阈值 {log.get('threshold')}，收敛={log.get('converged')}）：")
        for r in log.get("runs", []):
            print(f"  第{r['iter']}轮 分={r['score']:.2f} 缺口={r['gaps']}")
    p.set_defaults(func=f_log)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
