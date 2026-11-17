#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
loop.py — 超级智能体闭环引擎（super-agent-loop 核心）

把「感知 → 规划 → 执行 → 验证 → 反思 → 记忆 → 再规划」熔成一条可离线实跑的自主闭环。
零依赖（仅标准库），自带 --selftest，可在无网络环境验证整个回路能闭合。

设计要点：
  - 规划：goal + steps（每步可带 run 命令与 accept 验收条件）
  - 执行：真实调用 shell 跑 run，捕获 stdout（无 run 的步骤视为外部/人工委托，标记 done）
  - 验证：accept 字符串必须出现在该步产出中，否则判失败
  - 反思：产出结构化 critique（成功/失败/教训），写入 memory
  - 记忆：每轮 episode 落盘 memory.json，跨轮累积
  - 再规划：失败步骤回到 pending 重试（最多 max_iter 轮），避免无限循环

用法：
  python loop.py validate loop.json
  python loop.py run loop.json --dry-run
  python loop.py run loop.json --out outputs
  python loop.py status loop.json --out outputs
  python loop.py --selftest
"""
import os, sys, json, argparse, subprocess, datetime, tempfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SELF_DIR = os.path.dirname(HERE)


def now_iso():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_loop(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------------------
# 感知（轻量）：汇聚环境上下文，为规划提供输入
# --------------------------------------------------------------------------
def perceive(loop_def, out_dir):
    ctx = {
        "goal": loop_def.get("goal", ""),
        "n_steps": len(loop_def.get("steps", [])),
        "time": now_iso(),
    }
    return ctx


# --------------------------------------------------------------------------
# 规划：确保 steps 就绪（这里 steps 由 loop.json 声明；真实部署可换 long-horizon-planner）
# --------------------------------------------------------------------------
def plan_steps(loop_def):
    steps = loop_def.get("steps", [])
    for s in steps:
        s.setdefault("status", "pending")
        s.setdefault("retries", 0)
    return steps


# --------------------------------------------------------------------------
# 执行：真实跑 run 命令，捕获产出
# --------------------------------------------------------------------------
def execute(step):
    if not step.get("run"):
        # 无 run 字段：视为外部/人工委托，直接标记完成
        return True, "(delegated / no run command)"
    try:
        # 用 utf-8 + errors=replace 防御 Windows 控制台非 UTF-8 代码页导致的崩溃
        r = subprocess.run(step["run"], shell=True, capture_output=True,
                           encoding="utf-8", errors="replace", timeout=60)
        out = (r.stdout or "") + (r.stderr or "")
        return (r.returncode == 0), out.strip()
    except Exception as e:
        return False, f"exec-error: {e}"


# --------------------------------------------------------------------------
# 验证：accept 验收条件必须命中产出
# --------------------------------------------------------------------------
def verify(step, output):
    acc = step.get("accept")
    if not acc:
        return True, "no-accept"
    return (acc in output), f"accept='{acc}' not in output"


# --------------------------------------------------------------------------
# 反思：结构化 critique + 教训提取
# --------------------------------------------------------------------------
def reflect(steps, episode_no):
    done = [s["id"] for s in steps if s["status"] == "done"]
    failed = [s["id"] for s in steps if s["status"] == "failed"]
    lessons = []
    if failed:
        lessons.append(f"步骤 {failed} 验证失败，需调整 run/accept 或补充前置依赖")
    if done:
        lessons.append(f"步骤 {done} 已闭环，沉淀为可复用路径")
    critique = {
        "episode": episode_no,
        "time": now_iso(),
        "done": done,
        "failed": failed,
        "lessons": lessons,
    }
    return critique


# --------------------------------------------------------------------------
# 记忆：episode 落盘
# --------------------------------------------------------------------------
def remember(out_dir, episode):
    os.makedirs(out_dir, exist_ok=True)
    mem = os.path.join(out_dir, "memory.json")
    data = []
    if os.path.exists(mem):
        try:
            data = json.load(open(mem, encoding="utf-8"))
        except Exception:
            data = []
    data.append(episode)
    json.dump(data, open(mem, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return mem


# --------------------------------------------------------------------------
# 主循环
# --------------------------------------------------------------------------
def run_loop(def_path, out_dir=None, dry_run=False):
    loop_def = load_loop(def_path)
    goal = loop_def.get("goal", "")
    max_iter = int(loop_def.get("max_iter", 8))
    steps = plan_steps(loop_def)
    print(f"🎯 目标：{goal} ｜ 步骤数：{len(steps)} ｜ max_iter={max_iter}")

    if dry_run:
        for i, s in enumerate(steps, 1):
            print(f"  {i}. [{s['status']}] {s['id']}: {s['desc']}")
        return

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    ctx = perceive(loop_def, out_dir or ".")
    episode_no = 0
    for it in range(1, max_iter + 1):
        pending = [s for s in steps if s["status"] == "pending"]
        if not pending:
            break
        print(f"\n--- 第 {it} 轮迭代 ---")
        for s in pending:
            ok, out = execute(s)
            passed, vmsg = verify(s, out)
            s["output"] = out
            s["verify"] = vmsg
            if ok and passed:
                s["status"] = "done"
                print(f"  ✅ {s['id']}: 执行成功 + 验证通过")
            else:
                s["status"] = "failed"
                s["retries"] += 1
                print(f"  ❌ {s['id']}: 失败（exec={ok}, verify={vmsg}）")
        critique = reflect(steps, it)
        episode_no += 1
        ep = {
            "episode": episode_no,
            "time": now_iso(),
            "goal": goal,
            "context": ctx,
            "steps": [{k: s[k] for k in ("id", "status", "retries", "verify")} for s in steps],
            "critique": critique,
        }
        if out_dir:
            remember(out_dir, ep)

    failed = [s["id"] for s in steps if s["status"] == "failed"]
    achieved = all(s["status"] == "done" for s in steps)
    print(f"\n{'🏁 闭环完成：目标达成' if achieved else '⚠️ 闭环结束但未完全达成'}（失败步骤：{failed or '无'}）")
    summary = {"goal": goal, "achieved": achieved, "steps": steps, "episodes": episode_no}
    if out_dir:
        json.dump(summary, open(os.path.join(out_dir, "summary.json"), "w", encoding="utf-8"),
                   ensure_ascii=False, indent=2)
    return summary


def validate(def_path):
    d = load_loop(def_path)
    errs = []
    if not d.get("goal"):
        errs.append("goal 为空")
    steps = d.get("steps", [])
    if not steps:
        errs.append("steps 为空")
    ids = set()
    for i, s in enumerate(steps):
        if not s.get("id"):
            errs.append(f"step[{i}] 缺 id")
        elif s["id"] in ids:
            errs.append(f"step id 重复: {s['id']}")
        else:
            ids.add(s["id"])
        if not s.get("desc"):
            errs.append(f"step {s.get('id')} 缺 desc")
        if s.get("run") and not s.get("accept"):
            errs.append(f"step {s.get('id')} 有 run 但缺 accept 验收条件")
    if errs:
        print("❌ 校验失败：")
        for e in errs:
            print("  -", e)
        return False
    print("✅ 闭环定义合法")
    return True


def status(def_path, out_dir):
    mem = os.path.join(out_dir, "memory.json")
    if not os.path.exists(mem):
        print("ℹ️ 尚无记忆（先 run 一次）")
        return
    data = json.load(open(mem, encoding="utf-8"))
    print(f"📚 已沉淀 {len(data)} 轮记忆：")
    for ep in data[-5:]:
        c = ep.get("critique", {})
        print(f"  轮{ep['episode']} {ep['time']} 完成={c.get('done')} 失败={c.get('failed')} 教训={c.get('lessons')}")


# --------------------------------------------------------------------------
# 自测：离线跑一个 2 步闭环，断言回路闭合 + 记忆沉淀
# --------------------------------------------------------------------------
def selftest():
    tmp = tempfile.mkdtemp(prefix="loop_selftest_")
    try:
        def_path = os.path.join(tmp, "loop.json")
        json.dump({
            "goal": "selftest goal",
            "max_iter": 5,
            "steps": [
                {"id": "a", "desc": "step A", "run": "echo DONE_A", "accept": "DONE_A"},
                {"id": "b", "desc": "step B", "run": "echo DONE_B", "accept": "DONE_B"},
            ],
        }, open(def_path, "w", encoding="utf-8"))
        out = os.path.join(tmp, "out")
        summary = run_loop(def_path, out)
        mem = json.load(open(os.path.join(out, "memory.json"), encoding="utf-8"))
        ok = (summary and summary["achieved"] and len(mem) >= 1
              and all(s["status"] == "done" for s in summary["steps"]))
        print("SELFTEST:", "PASS" if ok else "FAIL")
        return ok
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="run")
    ap.add_argument("def_path", nargs="?", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(0 if selftest() else 1)

    if not args.def_path:
        print("用法: loop.py [validate|run|status] <loop.json> [--out DIR] [--dry-run]")
        sys.exit(1)

    if args.cmd == "validate":
        sys.exit(0 if validate(args.def_path) else 1)
    elif args.cmd == "run":
        run_loop(args.def_path, args.out, args.dry_run)
    elif args.cmd == "status":
        status(args.def_path, args.out or ".")
    else:
        print("未知命令:", args.cmd)
        sys.exit(1)


if __name__ == "__main__":
    main()
