#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""闭环演示：拿一枚"纸面完整"的假包，跑一遍评审器，看它拦不拦。

演示不依赖网络、不改任何被评审的包：临时目录造一个假包 → 跑评审器 → 打印两行结论 → 删除。
评审器缺失时返回 3，不输出伪造的 PASS。
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)


def find_reviewer():
    env = os.environ.get("REDTEAM_REVIEWER")
    if env and os.path.exists(env):
        return env
    base = os.path.dirname(PKG)
    cand = os.path.join(base, "lgd-skill-review", "scripts", "review.py")
    return cand if os.path.exists(cand) else None


FAKE_SKILL = """---
name: demo-fake
description: "A package that looks complete but verifies nothing. Used by the demo only."
version: 1.0.0
---

# demo-fake

## Quick start

```bash
python demo/run_demo.py
```

Prints one line and exits zero.
"""


def main():
    reviewer = find_reviewer()
    if reviewer is None:
        sys.stderr.write("demo: no reviewer found; set REDTEAM_REVIEWER\n")
        return 3

    tmp = tempfile.mkdtemp(prefix="redteam-demo-")
    try:
        pkg = os.path.join(tmp, "demo-fake")
        os.makedirs(os.path.join(pkg, "demo"))
        open(os.path.join(pkg, "SKILL.md"), "w", encoding="utf-8").write(FAKE_SKILL)
        open(os.path.join(pkg, "demo", "run_demo.py"), "w",
             encoding="utf-8").write("print('ok')\n")

        r = subprocess.run([sys.executable, reviewer, pkg, "--run"],
                           capture_output=True, text=True, encoding="utf-8", timeout=300)
        out = (r.stdout or "") + (r.stderr or "")
        total = [l for l in out.splitlines() if "总分" in l or "total" in l.lower()][:1]
        repro = [l for l in out.splitlines() if "reproducible" in l][:1]
        print("demo: fake package built at", pkg)
        print("demo: reviewer says ->", total[0].strip() if total else "(no score line)")
        print("demo: reproducible ->", repro[0].strip() if repro else "(no breakdown)")
        print("demo: this is what 'looks complete, verifies nothing' costs the reviewer")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
