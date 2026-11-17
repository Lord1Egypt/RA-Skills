#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selfcheck.py — 专家包「最懂你的保险顾问」上架前一键自检

一次跑完六件事，任一失败即退出码 1（可直接当发布门禁用）：

  1. 同步一致性   shared/ 与各 skill 内嵌副本是否一致（防止改了权威源忘下发）
  2. 合规自检     compliance_scan.py 内置用例是否全过
  3. 代理人红队   从保险代理人视角提 45 个请求，必须全部被拦（防被当销售工具用）
  4. 全包扫描     所有 .md 输出类内容是否命中九类黑名单 / 术语未翻译
  5. 脚本冒烟     五个业务脚本能否正常跑出结果
  6. 小白体验     口语输入能不能懂、输错时提示友不友好、有没有静默出错

用法：
    python3 scripts/selfcheck.py
    python3 scripts/selfcheck.py --quiet      # 只打结论
"""

import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

SMOKE = [
    ("买什么 · 预算试算", ["skills/ins-what-to-buy/scripts/budget_calc.py",
                     "--income", "30", "--expense", "15000", "--existing", "10000"]),
    ("怎么买 · 条款四看", ["skills/ins-how-to-buy/scripts/clause_check.py",
                     "--insurance-type", "重疾险"]),
    ("健康告知 · 核对清单", ["skills/ins-health-disclosure/scripts/disclosure_checklist.py",
                      "--insurance-type", "百万医疗", "--role", "本人",
                      "--findings", "甲状腺结节 3mm"]),
    ("保单体检 · 检视表", ["skills/ins-policy-checkup/scripts/policy_review.py",
                     "--demo", "--income", "30"]),
    ("理赔怎么办 · 材料清单", ["skills/ins-claims-guide/scripts/claim_checklist.py",
                       "--insurance-type", "百万医疗", "--event", "住院"]),
]

SKIP_DIRS = {".git", "__pycache__"}


def run(args, **kw):
    return subprocess.run([PY] + args, cwd=ROOT, capture_output=True, text=True, **kw)


def step_sync(quiet):
    r = run(["scripts/sync_shared.py", "--check"])
    ok = r.returncode == 0
    if not quiet or not ok:
        print(r.stdout.strip() or r.stderr.strip())
    return ok, "共享文件同步"


def step_selftest(quiet):
    r = run(["scripts/compliance_scan.py", "--selftest"])
    ok = r.returncode == 0
    line = [l for l in r.stdout.splitlines() if "自检通过" in l or "自检失败" in l]
    if not quiet or not ok:
        print(line[-1] if line else r.stdout.strip()[-300:])
    return ok, "扫描器内置用例"


def step_agent(quiet):
    r = run(["scripts/agentprobe.py"])
    ok = r.returncode == 0
    if not quiet or not ok:
        for line in r.stdout.splitlines():
            if line.startswith(("❌", "⚠️", "✅", "结论")):
                print("  " + line.strip())
    return ok, "代理人视角红队"


def step_scan_all(quiet):
    files = []
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in names:
            if n.endswith(".md"):
                files.append(os.path.join(base, n))
    bad = []
    for f in sorted(files):
        r = run(["scripts/compliance_scan.py", "--file", f])
        if r.returncode != 0:
            bad.append((os.path.relpath(f, ROOT), r.stdout))
    if bad:
        print("  ❌ 未通过的文件：")
        for path, out in bad:
            print("   ·", path)
            if not quiet:
                for l in out.splitlines():
                    if "❌" in l or "未解释" in l:
                        print("     ", l.strip())
    elif not quiet:
        print(f"  ✅ {len(files)} 个 .md 文件全部通过")
    return not bad, f"全包扫描（{len(files)} 个 md）"


def step_smoke(quiet):
    ok_all = True
    for name, cmd in SMOKE:
        r = run(cmd)
        good = r.returncode == 0 and len(r.stdout.strip()) > 50
        if not good:
            ok_all = False
            print(f"  ❌ {name} 运行失败：{(r.stderr or r.stdout).strip()[:300]}")
        elif not quiet:
            print(f"  ✅ {name}")
    return ok_all, "业务脚本冒烟"


def step_user(quiet):
    r = run(["scripts/usertest.py"])
    ok = r.returncode == 0
    if not quiet or not ok:
        for line in r.stdout.splitlines():
            if line.startswith(("✅", "❌", "结论")):
                print("  " + line.strip())
    return ok, "小白用户体验"


def main():
    ap = argparse.ArgumentParser(description="保险专家包上架前自检")
    ap.add_argument("--quiet", action="store_true", help="只打印结论")
    args = ap.parse_args()

    steps = [step_sync, step_selftest, step_agent, step_scan_all, step_smoke, step_user]
    results = []
    print("=" * 60)
    print("保险专家包 · 上架前自检")
    print("=" * 60)
    for fn in steps:
        print(f"\n▶ {fn.__doc__ or fn.__name__}")
        ok, label = fn(args.quiet)
        results.append((ok, label))

    print("\n" + "=" * 60)
    for ok, label in results:
        print(f"{'✅' if ok else '❌'} {label}")
    failed = [l for ok, l in results if not ok]
    print("=" * 60)
    if failed:
        print(f"结论：不通过（{len(failed)} 项失败：{'、'.join(failed)}）")
        return 1
    print("结论：全部通过，可以打包上架。")
    return 0


if __name__ == "__main__":
    # 给每个 step 补一句中文说明（docstring 为空时用）
    step_sync.__doc__ = "1/6 共享文件同步一致性"
    step_selftest.__doc__ = "2/6 合规扫描器内置用例"
    step_agent.__doc__ = "3/6 代理人视角红队（防被当销售工具）"
    step_scan_all.__doc__ = "4/6 全包输出合规扫描"
    step_smoke.__doc__ = "5/6 业务脚本冒烟"
    step_user.__doc__ = "6/6 小白用户体验（口语输入 / 报错友好 / 不静默出错）"
    sys.exit(main())
