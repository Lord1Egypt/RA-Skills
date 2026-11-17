#!/usr/bin/env python3
"""
verify_remediation.py — 整改闭环验证器

解决的问题：整改最容易失败的地方不是「没找到」，而是「以为修好了」。

常见的假修复：
  · 把密钥从当前文件删了，但旧 commit 里还在（仓库一clone 全都在）
  · 改了代码但忘了吊销凭证——泄露出去的那把钥匙依然能用
  · 报告里写「已修复」，但没人再跑一遍扫描
  · 为了让扫描过关，直接放宽规则 / 加大范围忽略，把问题藏起来

本工具只认机器证据：对比整改前后的两份 JSON 报告，逐项给出
已消除 / 仍存在 / 新引入 三种状态，并强制产出吊销清单。

用法：
    # 1. 整改前留存基线
    python3 release_gate.py <repo> --format json > before.json

    # 2. 完成整改后再跑一次
    python3 release_gate.py <repo> --format json > after.json

    # 3. 验证整改效果
    python3 verify_remediation.py before.json after.json
    python3 verify_remediation.py before.json after.json --format json

退出码：0 = 整改达标；1 = 仍有未消除的 P0 或新引入问题；2 = 用法错误
"""

import argparse
import json
import sys
from pathlib import Path


def load(path):
    p = Path(path)
    if not p.exists():
        print(f"错误：报告文件不存在: {path}", file=sys.stderr)
        sys.exit(2)
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误：{path} 不是合法 JSON（是否忘了加 --format json？）: {e}",
              file=sys.stderr)
        sys.exit(2)


def fingerprint(f):
    """定位可能因整改而位移，所以指纹不含行号——用「类别+描述+内容」。"""
    return (f.get("category", ""), f.get("desc", ""), f.get("snippet", "").strip())


def surface_of(f):
    return f.get("surface", "")


# 与 release_gate.py 保持一致：哪些 surface 构成公开面
BLOCKING_SURFACES = ("tracked", "history", "worktree", "file")


def main():
    ap = argparse.ArgumentParser(description="整改闭环验证：对比前后报告，只认机器证据")
    ap.add_argument("before", help="整改前的 JSON 报告")
    ap.add_argument("after", help="整改后的 JSON 报告")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    b, a = load(args.before), load(args.after)
    bf = {fingerprint(f): f for f in b.get("findings", [])}
    af = {fingerprint(f): f for f in a.get("findings", [])}

    resolved = [bf[k] for k in bf.keys() - af.keys()]
    remaining = [af[k] for k in bf.keys() & af.keys()]
    introduced = [af[k] for k in af.keys() - bf.keys()]

    # 公开面上仍存在的 P0 = 未达标
    blocking = [f for f in remaining
                if f.get("severity") == "P0" and surface_of(f) in BLOCKING_SURFACES]
    new_blocking = [f for f in introduced
                    if f.get("severity") == "P0" and surface_of(f) in BLOCKING_SURFACES]

    # 凭证类必须吊销：只要它曾出现在公开面，删代码就不够
    revoke = [f for f in b.get("findings", [])
              if f.get("category") == "CREDENTIAL"
              and surface_of(f) in BLOCKING_SURFACES
              and not f.get("possible_false_positive")]

    # 历史残留：当前文件已清理，但历史里还在
    history_left = [f for f in remaining if surface_of(f) == "history"]

    ok = not blocking and not new_blocking

    if args.format == "json":
        print(json.dumps({
            "verdict": "PASS" if ok else "FAIL",
            "resolved": len(resolved),
            "remaining": len(remaining),
            "introduced": len(introduced),
            "blocking_remaining": blocking,
            "blocking_introduced": new_blocking,
            "history_residue": history_left,
            "must_revoke": revoke,
        }, ensure_ascii=False, indent=2))
        return 0 if ok else 1

    RESET, BOLD, RED, YEL, GRN = "\033[0m", "\033[1m", "\033[31m", "\033[33m", "\033[32m"
    if not sys.stdout.isatty():
        RESET = BOLD = RED = YEL = GRN = ""

    print(f"{BOLD}整改闭环验证{RESET}")
    print("=" * 68)
    print(f"整改前命中: {len(b.get('findings', []))}")
    print(f"整改后命中 : {len(a.get('findings', []))}")
    print(f"  已消除   : {len(resolved)}")
    print(f"  仍存在   : {len(remaining)}")
    print(f"  新引入   : {len(introduced)}")
    print("=" * 68)

    if blocking:
        print(f"\n{RED}{BOLD}未消除的公开面 P0（{len(blocking)} 项）{RESET}")
        for f in blocking[:20]:
            print(f"  · [{surface_of(f)}] {f.get('location')}  {f.get('desc')}")
            print(f"    > {f.get('snippet')}")

    if new_blocking:
        print(f"\n{RED}{BOLD}整改过程中新引入的 P0（{len(new_blocking)} 项）{RESET}")
        print("  整改本身把新问题带进来了，这比原问题更值得警惕。")
        for f in new_blocking[:20]:
            print(f"  · [{surface_of(f)}] {f.get('location')}  {f.get('desc')}")
            print(f"    > {f.get('snippet')}")

    if history_left:
        print(f"\n{YEL}{BOLD}git 历史残留（{len(history_left)} 项）{RESET}")
        print("  当前文件已清理，但旧 commit仍含敏感内容——任何人 clone 都能拿到。")
        print("  需重写历史（git-filter-repo / BFG）并 force push，且提前通知协作者。")
        for f in history_left[:10]:
            print(f"  · {f.get('location')}  {f.get('desc')}")

    if revoke:
        print(f"\n{RED}{BOLD}必须吊销的凭证清单（{len(revoke)} 项）{RESET}")
        print("  这些凭证曾出现在公开面。删代码 ≠ 修复——凭证已经泄露了，")
        print("  唯一有效动作是到对应服务控制台吊销并轮换：")
        seen = set()
        for f in revoke:
            k = (f.get("desc"), f.get("snippet", "")[:60])
            if k in seen:
                continue
            seen.add(k)
            print(f"  [ ] {f.get('desc')}  （出现于 {f.get('location')}）")
        print("\n  勾选完成前，不要在报告里写「已修复」。")

    print("\n" + "=" * 68)
    if ok:
        print(f"{GRN}{BOLD}裁决：整改达标{RESET} — 公开面无未消除 P0，且未引入新问题")
        if history_left:
            print(f"  {YEL}但仍有历史残留待处理，见上。{RESET}")
        if revoke:
            print(f"  {YEL}吊销清单请逐项确认完成。{RESET}")
    else:
        print(f"{RED}{BOLD}裁决：整改未达标{RESET}")
        print("  不要通过放宽规则或扩大忽略范围来「通过」——那是把问题藏起来，")
        print("  下一个 clone 仓库的人依然会拿到它。")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
