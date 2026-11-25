#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自检：跑自己带的探针，断言"全部被拦下"。

设计：这套件本身是仪器，仪器也要能自证。找不到评审器就直接判 UNVERIFIABLE(rc=3)，
不伪造 PASS —— 宁可让调用方看见"没验成"，也不给一个空转的绿。
"""
import io, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SUITE = os.path.join(os.path.dirname(HERE), "run_suite.py")


def find_reviewer():
    """找一个能跑的评审器：环境变量优先，其次同级的兄弟包。"""
    env = os.environ.get("REDTEAM_REVIEWER")
    if env and os.path.exists(env):
        return env
    pkg = os.path.dirname(HERE)                 # redteam-suite/
    base = os.path.dirname(pkg)                 # 同级矩阵目录
    cand = os.path.join(base, "lgd-skill-review", "scripts", "review.py")
    if os.path.exists(cand):
        return cand
    cand2 = os.path.join(os.path.dirname(base), "lgd-skill-review", "scripts", "review.py")
    if os.path.exists(cand2):
        return cand2
    return None


def main():
    reviewer = find_reviewer()
    if reviewer is None:
        sys.stderr.write("KEYS INCOMPLETE: no reviewer found; set REDTEAM_REVIEWER\n")
        return 3
    r = subprocess.run([sys.executable, SUITE, "--reviewer", reviewer],
                       capture_output=True, text=True, encoding="utf-8", timeout=300)
    out = (r.stdout or "") + (r.stderr or "")
    m = re.search(r"probes:\s*(\d+)", out)
    total = int(m.group(1)) if m else 0
    if "ALL PROBES BLOCKED" in out and total:
        print("---- %d/%d PASS ----" % (total, total))
        return 0
    got = re.search(r"(\d+) probe\(s\) got through", out)
    print("---- %d/%d PASS ----" % (total - int(got.group(1)) if got else 0, total))
    print(out.strip()[-300:])
    return 1


if __name__ == "__main__":
    sys.exit(main())
