#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
orchestrator.py — 多步工具链编排引擎（超越性元能力 #3）

设计依据（2024-2026 主流研究/框架）：
  - Beyond ReAct：以「规划器为中心」生成 DAG 执行计划（节点=工具，边=依赖），克服反应式「局部优化陷阱」，
    支持全局优化、并行识别、依赖追踪。
  - Strands GraphBuilder / Shannon：图执行模型（节点=agent/tool，边=数据流），确定性、可观测、可重放。
  - ReAct / Plan-and-Execute：Thought→Action→Observation 交织；或 规划-执行-重规划 闭环。
  - 企业实践：显式工作流、可观测性(链路追踪)、失败恢复、中断重跑。

本脚本提供**确定性、可复跑**的工具链编排（CLI 驱动，不依赖 LLM）：
  - 声明式链定义（JSON，可选 YAML）：节点 + 依赖 + 命令 + 输出捕获
  - validate：语法/依赖存在性/成环检测/命令可达性检查
  - run：拓扑序执行，节点间通过 {{node_id}} 透传上游 stdout，支持 --dry-run / --from / --only / 中断重跑
  - dot：导出 Graphviz DOT 用于可视化

链定义 (chain.json) 示例：
{
  "name": "etl-demo",
  "nodes": {
    "extract": {"run": "python extract.py data.csv", "depends_on": [], "capture": "stdout"},
    "transform": {"run": "python transform.py", "depends_on": ["extract"], "capture": "stdout"},
    "load": {"run": "echo done: {{transform}}", "depends_on": ["transform"], "capture": "stdout"}
  }
}

用法：
  python orchestrator.py validate chain.json
  python orchestrator.py run chain.json [--dry-run] [--from node] [--only node] [--out outputs]
  python orchestrator.py dot chain.json --out chain.dot
"""
import os, sys, json, argparse, subprocess, shutil
from collections import deque

PY = sys.executable


def load_chain(path):
    if path.endswith((".yaml", ".yml")):
        try:
            import yaml
            return yaml.safe_load(open(path, encoding="utf-8").read())
        except ImportError:
            # 极简 YAML 子集回退（仅支持本脚本所用结构）
            return _mini_yaml(open(path, encoding="utf-8").read())
    return json.load(open(path, encoding="utf-8"))


def _mini_yaml(text):
    """仅支持：缩进映射、'- ' 列表、标量（str/int/float/bool/null）。非通用，仅作回退。"""
    lines = [l.rstrip() for l in text.splitlines() if l.strip() and not l.strip().startswith("#")]
    root = {}
    stack = [(-1, root)]
    cur_list = None
    for ln in lines:
        indent = len(ln) - len(ln.lstrip(" "))
        key, _, val = ln.strip().partition(":")
        key = key.strip()
        val = val.strip()
        while stack and indent <= stack[-1][0] and stack[-1][0] != -1:
            stack.pop()
        parent = stack[-1][1]
        if key.startswith("- "):
            item = key[2:].strip()
            parent.setdefault("_list", []).append(_scalar(item))
        elif val == "":
            node = {}
            parent[key] = node
            stack.append((indent, node))
        else:
            parent[key] = _scalar(val)
    return root


def _scalar(s):
    if s.lower() in ("true", "false"):
        return s.lower() == "true"
    if s.lower() == "null" or s == "":
        return None
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s.strip("\"'")


def topo(nodes):
    indeg = {k: 0 for k in nodes}
    adj = {k: [] for k in nodes}
    for k, n in nodes.items():
        for d in n.get("depends_on", []):
            if d in nodes:
                adj[d].append(k)
                indeg[k] += 1
    q = deque([k for k, d in indeg.items() if d == 0])
    order, seen = [], set()
    while q:
        x = q.popleft()
        order.append(x); seen.add(x)
        for y in adj[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                q.append(y)
    cycle = [k for k in nodes if k not in seen]
    return order, cycle


def validate(chain):
    errs = []
    nodes = chain.get("nodes", {})
    if not nodes:
        errs.append("无 nodes 定义")
    for k, n in nodes.items():
        for d in n.get("depends_on", []):
            if d not in nodes:
                errs.append(f"节点 {k} 依赖不存在的 {d}")
        run = n.get("run", "")
        if not run:
            errs.append(f"节点 {k} 无 run 命令")
        else:
            tok = run.split()
            if tok and tok[0] == "python":
                # 仅当第二个 token 是 .py 脚本时才校验文件存在（python -c/-m 等无需文件）
                if len(tok) > 1 and tok[1].endswith(".py") and not os.path.exists(tok[1]):
                    errs.append(f"节点 {k} 引用的脚本不存在: {tok[1]}")
            else:
                # shell 命令：首个 token 可能是 shell 内建 (exit/cd/echo/set)，
                # 运行期由 shell 解析，这里仅做软提示，不阻断（避免误杀合法内建命令）
                first = shutil.which(tok[0]) if tok else None
                if not first and tok and "/" not in tok[0] and not os.path.exists(tok[0]):
                    print(f"  ⚠️ 提示: 节点 {k} 首词 '{tok[0]}' 非独立可执行（可能为 shell 内建），运行期由 shell 解析")
    order, cycle = topo(nodes)
    if cycle:
        errs.append(f"依赖成环: {cycle}")
    return errs, order


def run(chain, dry=False, only=None, start_from=None, outdir="outputs"):
    errs, order = validate(chain)
    if errs and not dry:
        print("❌ 校验未通过，终止执行：")
        for e in errs:
            print("   -", e)
        return False
    if dry:
        print("🔍 执行计划（拓扑序）：")
        for k in order:
            print(f"   {k}: {chain['nodes'][k].get('run','')}")
        return True
    os.makedirs(outdir, exist_ok=True)
    outputs = {}
    log = {"name": chain.get("name"), "steps": []}
    skip = bool(start_from)
    for k in order:
        if only and k != only:
            continue
        if skip:
            if k != start_from:
                continue
            skip = False
        n = chain["nodes"][k]
        cmd = n.get("run", "")
        for dep, val in outputs.items():
            cmd = cmd.replace(f"{{{{{dep}}}}}", (val or "").strip())
        print(f"▶ 运行 {k}: {cmd}")
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        stdout = r.stdout
        if n.get("capture") == "stdout":
            outputs[k] = stdout
            open(os.path.join(outdir, f"{k}.out"), "w", encoding="utf-8").write(stdout)
        status = "ok" if r.returncode == 0 else f"fail({r.returncode})"
        if r.returncode != 0 and r.stderr:
            print("   stderr:", r.stderr.strip()[:300])
        log["steps"].append({"node": k, "rc": r.returncode, "status": status})
        if r.returncode != 0:
            print(f"⛔ 节点 {k} 失败，停止（可用 --from {k} 修复后重跑）")
            json.dump(log, open(os.path.join(outdir, "run_log.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            return False
    json.dump(log, open(os.path.join(outdir, "run_log.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"✅ 链执行完成，日志 -> {outdir}/run_log.json")
    return True


def dot(chain):
    L = ["digraph chain {", "  rankdir=LR;"]
    for k, n in chain.get("nodes", {}).items():
        label = (n.get("run", "") or "")[:30].replace('"', "'")
        L.append('  "%s" [label="%s\\n%s"];' % (k, k, label))
        for d in n.get("depends_on", []):
            L.append('  "%s" -> "%s";' % (d, k))
    L.append("}")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="多步工具链编排引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("validate"); p.add_argument("chain")
    def f_v(a):
        c = load_chain(a.chain)
        errs, order = validate(c)
        if errs:
            print("❌ 校验失败：")
            for e in errs: print("   -", e)
            sys.exit(1)
        print(f"✅ 校验通过，拓扑序: {order}")
    p.set_defaults(func=f_v)
    p = sub.add_parser("run"); p.add_argument("chain"); p.add_argument("--dry-run", action="store_true"); p.add_argument("--only"); p.add_argument("--from", dest="from_"); p.add_argument("--out", default="outputs")
    def f_r(a):
        c = load_chain(a.chain)
        ok = run(c, dry=a.dry_run, only=a.only, start_from=a.from_, outdir=a.out)
        sys.exit(0 if ok else 1)
    p.set_defaults(func=f_r)
    p = sub.add_parser("dot"); p.add_argument("chain"); p.add_argument("--out")
    def f_d(a):
        c = load_chain(a.chain)
        d = dot(c)
        if a.out:
            open(a.out, "w", encoding="utf-8").write(d)
            print(f"✅ DOT -> {a.out}")
        else:
            print(d)
    p.set_defaults(func=f_d)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
