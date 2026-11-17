"""lock_test.py — 共享浏览器「跨进程互斥锁」回归测试

改过 campus/base-cas/scripts/browser.py 的锁逻辑后必须跑这个（不碰 CAS、不登录）。

验证两件事：
  ① 串行性：两个并行进程必须排队（不能同时进共享 Chromium）；
  ② 可重入性：父进程持锁后 fork 出的子进程不得自锁死
     —— 这对应 learn.py → login.py 的真实父子结构，flock 不跨进程可重入，
        靠环境变量 CAMPUS_BROWSER_LOCK 继承来跳过加锁。

用法: python tests/lock_test.py          # 约 15s
输出: {"status":"ok"|"FAIL", ...}
"""
import sys
import os
import json
import time
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "campus", "base-cas", "scripts"))
sys.stdout.reconfigure(encoding="utf-8")
import browser  # noqa: E402


def run(mode, hold):
    t0 = time.time()
    ok = browser.acquire_run_lock()
    rec = {"pid": os.getpid(), "mode": mode, "acquired": ok,
           "wait_s": round(time.time() - t0, 2),
           "inherited_env": bool(os.environ.get("CAMPUS_BROWSER_LOCK"))}
    if mode == "hold" and ok:
        time.sleep(hold)
    if mode == "parent":
        r = subprocess.run([sys.executable, __file__, "hold", "0"], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=60)
        rec["child_rc"] = r.returncode
        try:
            rec["child"] = json.loads((r.stdout or "{}").strip().splitlines()[-1])
        except Exception:
            rec["child_raw"] = (r.stdout or "")[:200]
    print(json.dumps(rec, ensure_ascii=False), flush=True)
    return rec


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode != "all":
        run(mode, float(sys.argv[2]) if len(sys.argv) > 2 else 5)
        return 0

    W = 8
    out = {"hold_seconds": W}
    a = subprocess.Popen([sys.executable, __file__, "hold", str(W)], stdout=subprocess.PIPE,
                         text=True, encoding="utf-8", errors="replace")
    time.sleep(1.5)
    b = subprocess.Popen([sys.executable, __file__, "hold", "0"], stdout=subprocess.PIPE,
                         text=True, encoding="utf-8", errors="replace")
    ob = json.loads(b.communicate(timeout=90)[0].strip().splitlines()[-1])
    oa = json.loads(a.communicate(timeout=90)[0].strip().splitlines()[-1])
    out["A_first"], out["B_second"] = oa, ob
    out["serialized_ok"] = bool(ob["wait_s"] >= W - 2.0 and oa["wait_s"] < 1.0)

    p = subprocess.run([sys.executable, __file__, "parent"], capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=90)
    op = json.loads(p.stdout.strip().splitlines()[-1])
    out["parent"] = op
    out["child_reentrant_ok"] = bool(
        op.get("child_rc") == 0 and op["child"].get("acquired") and op["child"].get("wait_s", 99) < 3.0)

    out["status"] = "ok" if (out["serialized_ok"] and out["child_reentrant_ok"]) else "FAIL"
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
