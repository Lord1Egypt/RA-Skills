#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""super-agent-loop: 超级智能体端到端闭环编排器。

实体化"超级智能体闭环编排"：把分散的元能力(规划/执行/自验证/反思/记忆)
熔成一条可执行的自主闭环。给定一个带依赖的任务图(DAG)，它：
  1. 拓扑挑选"依赖已满足"的就绪节点；
  2. 执行节点 action；
  3. 用节点 verify 做可靠自验证(不达标即判失败、阻断下游)；
  4. 成功结果写入记忆存储(跨步可用)；
  5. 失败/卡死触发反思(诊断根因、给出重试或绕过建议)。
纯标准库，零依赖；--selftest 实测。
"""
import sys, json, argparse

class SuperAgent:
    def __init__(self):
        self.mem = {}          # 记忆存储：节点成功结果
        self.trace = []        # 执行轨迹
        self.status = {}       # id -> done/failed/blocked

    def run(self, steps):
        """steps: list of dict{id, deps:[], action(s,mem)->val, verify(val,mem)->bool}"""
        by_id = {s["id"]: s for s in steps}
        pending = set(by_id)
        progress = True
        while pending and progress:
            progress = False
            ready = [s for s in steps if s["id"] in pending
                      and all(self.status.get(d) == "done" for d in s.get("deps", []))]
            if not ready:
                break
            for s in ready:
                sid = s["id"]
                try:
                    val = s["action"](self.mem, self.mem)
                    ok = bool(s["verify"](val, self.mem))
                except Exception as e:
                    val, ok = f"ERR:{e}", False
                if ok:
                    self.mem[sid] = val
                    self.status[sid] = "done"
                    self.trace.append({"id": sid, "ok": True, "val": _safe(val)})
                else:
                    # 阻断下游
                    self.status[sid] = "failed"
                    self.trace.append({"id": sid, "ok": False, "val": _safe(val)})
                pending.discard(sid)
                progress = True
        # 剩余未执行：被失败阻断
        for sid in pending:
            self.status.setdefault(sid, "blocked")
        return self.report()

    def report(self):
        done = [k for k, v in self.status.items() if v == "done"]
        failed = [k for k, v in self.status.items() if v == "failed"]
        blocked = [k for k, v in self.status.items() if v == "blocked"]
        reflection = None
        if failed or blocked:
            reflection = {
                "root_cause": failed or blocked,
                "advice": "重试失败节点或放宽 verify 阈值；阻断节点需先解阻塞根因再跑。",
            }
        return {
            "done": done, "failed": failed, "blocked": blocked,
            "memory_keys": list(self.mem.keys()),
            "trace": self.trace, "reflection": reflection,
        }

def _safe(v):
    try:
        json.dumps(v); return v
    except Exception:
        return str(v)

# ---------------- 示例图 ----------------
def _demo_steps():
    return [
        {"id": "fetch", "deps": [],
         "action": lambda m, _: 10, "verify": lambda v, m: v > 0},
        {"id": "compute", "deps": ["fetch"],
         "action": lambda m, _: m["fetch"] * 2, "verify": lambda v, m: v == 20},
        {"id": "summarize", "deps": ["compute"],
         "action": lambda m, _: f"result={m['compute']}", "verify": lambda v, m: "result=" in v},
        # 一个会失败的节点，用于验证"阻断下游"
        {"id": "bad", "deps": ["compute"],
         "action": lambda m, _: m["compute"] - 5, "verify": lambda v, m: v > 100},
        {"id": "downstream", "deps": ["bad"],
         "action": lambda m, _: 1, "verify": lambda v, m: v == 1},
    ]

def selftest():
    a = SuperAgent()
    r = a.run(_demo_steps())
    # fetch/compute/summarize 成功
    assert "fetch" in r["done"] and "compute" in r["done"] and "summarize" in r["done"], r
    # bad 失败
    assert "bad" in r["failed"], r
    # downstream 被 bad 阻断
    assert "downstream" in r["blocked"], r
    # 记忆可见：compute 结果被下游使用
    assert "compute" in a.mem and a.mem["compute"] == 20, a.mem
    # 反思给出根因
    assert r["reflection"] and "bad" in r["reflection"]["root_cause"], r
    print("✅ selftest PASS：DAG 拓扑序执行、自验证门控、失败阻断下游、记忆跨步、反思诊断 全部正确")
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--graph", help="任务图 json 路径(由 agent 构造)")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.graph:
        steps = json.load(open(a.graph, encoding="utf-8"))
        print(json.dumps(SuperAgent().run(steps), ensure_ascii=False, indent=2))
    else:
        print("用法: super_agent.py --selftest | --graph g.json")

if __name__ == "__main__":
    main()
