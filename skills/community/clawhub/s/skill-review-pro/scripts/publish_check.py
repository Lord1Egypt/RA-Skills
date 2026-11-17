#!/usr/bin/env python3
"""publish_check.py — ClawHub 发布核验(确定性比对)。

对给定的 skill 目录,比对本地 SKILL.md 与 ClawHub 线上最新版本:
  1. 版本一致性:本地 frontmatter version 是否等于线上 latestVersion.version;
  2. 内容一致性:线上 skill.description 是否与本地 SKILL.md 逐字节一致
     (CI publish 上传的正文就是本地 SKILL.md 全文,任何差异都说明没发布成功);
  3. 发布来源(可选):latestVersion.changelog 内嵌的 commit sha 与 --expect-sha 比对,
     用于确认「这次合并」确实触发了发布。

为什么需要这个脚本(2026-10-31 实战教训):
  - publish CI 校验「本地版本 > ClawHub 最新」,改了 SKILL.md 没 bump 版本 → CI 红,内容从未发布;
  - CI 的发布循环逐个执行,一个 skill 失败会中断并吞掉后续 skill 的发布——
    「重试的 skill 成功」不代表「所有预期发布的 skill 都成功」,必须逐个核验;
  - 「发布成功」的最终判据是 inspect 内容一致,而不是命令退出码或 tags 字段
    (ClawHub 存在孤儿版本、tag 标签滞后等异常);
  - 安全扫描有分钟级延迟,刚发布后 inspect 内容可能短暂滞后——此时脚本判 WARN(delay),
    等几分钟重试即可,不要误判为发布失败。

用法:
    python3 publish_check.py check <skill目录> [<skill目录>...] [--expect-sha <git sha>]
    # skill 目录 = 含 SKILL.md 的目录;slug 取目录名(与 publish CI 口径一致)

依赖: clawhub CLI(直接调用 `clawhub`,不存在时回退 `npx --yes clawhub@<锁定版本>`,版本号见下方 NPX_CLAWHUB_PIN)。
输出: 每个 skill 一行结论 + 汇总;--json 时输出机器可读结果。
退出码: 0 = 全部 PASS, 1 = 存在 FAIL/WARN(delay), 2 = 用法错误。
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

SCAN_DELAY_MINUTES = 15  # 安全扫描/索引延迟窗口,窗口内的内容不一致判 WARN(delay)


def read_frontmatter_version(skill_dir: Path) -> str | None:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    vm = re.search(r'^version:\s*"?([^"\n]+)"?', m.group(1), re.M)
    return vm.group(1).strip() if vm else None


# npx 回退时锁定 clawhub 版本,避免 "npx --yes clawhub" 每次拉取最新版导致的供应链漂移
NPX_CLAWHUB_PIN = "0.23.3"


def resolve_clawhub_bin(override: str | None) -> str:
    if override:
        return override
    from shutil import which
    if which("clawhub"):
        return "clawhub"
    return f"npx --yes clawhub@{NPX_CLAWHUB_PIN}"


def inspect_remote(slug: str, clawhub_bin: str, timeout: int) -> tuple[dict | None, str]:
    """返回 (inspect 结果 dict 或 None, 错误消息)。None 且错误消息含 not-found 表示未发布。"""
    cmd = clawhub_bin.split() + ["inspect", slug, "--json"]
    try:
        # 安全说明:cmd 来自 clawhub_bin.split() + 固定参数列表,argv 直传、不经 shell、无拼接用户输入
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, f"inspect 超时(>{timeout}s)"
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        if "not found" in err.lower() or "unavailable" in err.lower():
            return None, "not-found"
        if "reset in" in err.lower():
            return None, f"rate-limited: {err.splitlines()[0][:120]}"
        return None, f"inspect 失败: {err.splitlines()[0][:120] if err else 'exit ' + str(proc.returncode)}"
    try:
        return json.loads(proc.stdout), ""
    except json.JSONDecodeError as e:
        return None, f"inspect 输出不是合法 JSON: {e}"


def first_divergence(a: str, b: str) -> str:
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            return f"首个差异在字符 {i}: 本地 {a[i:i+40]!r} vs 线上 {b[i:i+40]!r}"
    return f"前缀一致,长度不同: 本地 {len(a)} vs 线上 {len(b)}"


def check_one(skill_dir: Path, expect_sha: str | None, clawhub_bin: str, timeout: int) -> dict:
    slug = skill_dir.name
    r: dict = {"slug": slug, "status": "FAIL", "checks": []}

    def add(name: str, ok: bool | None, detail: str):
        r["checks"].append({"check": name, "ok": ok, "detail": detail})

    local_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    local_ver = read_frontmatter_version(skill_dir)
    if not local_ver:
        add("frontmatter-version", False, "本地 SKILL.md 缺 version")
        return r
    add("frontmatter-version", True, f"本地 v{local_ver}")

    data, err = inspect_remote(slug, clawhub_bin, timeout)
    if data is None:
        if err == "not-found":
            add("remote-version", False, "ClawHub 上不存在该 skill → 从未发布成功")
        else:
            add("remote-version", None, err + "(环境问题,稍后重试)")
        return r

    latest = (data.get("latestVersion") or {})
    remote_ver = latest.get("version") or (data.get("skill", {}) or {}).get("tags", {}).get("latest")
    if remote_ver != local_ver:
        if remote_ver is None:
            add("remote-version", False, "线上无版本信息")
            return r
        newer = True
        try:
            def vt(v):
                return [int(x) for x in re.findall(r"\d+", v)][:3]
            newer = vt(local_ver) > vt(remote_ver)
        except Exception:
            pass
        if newer:
            add("remote-version", False,
                f"本地 v{local_ver} > 线上 v{remote_ver} → 本次改动尚未发布;若 publish CI 结论是 success,"
                f"先查 publish 步骤日志的「Update submitted...pending security scans」行再判等待(该形态下提交已排队、"
                f"等安全扫描落库即可,勿 bump/勿 rerun,详见 SKILL.md 发布核验模式第 4 态)")
        else:
            add("remote-version", False,
                f"本地 v{local_ver} 落后线上 v{remote_ver}(本地有未发布/回退的改动?)")
        return r
    add("remote-version", True, f"本地=线上 v{remote_ver}")

    # 内容一致性:线上 description 应与本地 SKILL.md 全文逐字节一致
    remote_desc = (data.get("skill", {}) or {}).get("description")
    if remote_desc is None:
        add("content-match", None, "线上无 description 字段,无法比对")
        return r
    if remote_desc == local_text:
        add("content-match", True, f"逐字节一致({len(local_text)} chars)")
    else:
        created_ms = latest.get("createdAt")
        recent = False
        if created_ms:
            age_min = (datetime.datetime.now().timestamp() * 1000 - created_ms) / 60000
            recent = age_min < SCAN_DELAY_MINUTES
        if recent:
            add("content-match", None,
                f"内容不一致,但该版本发布于 {age_min:.1f} 分钟前(<{SCAN_DELAY_MINUTES} 分钟窗口)→ "
                f"疑似安全扫描/索引延迟,等几分钟重试;{first_divergence(local_text, remote_desc)}")
            r["status"] = "WARN(delay)"
        else:
            add("content-match", False,
                f"内容不一致(非刚发布,延迟窗口已过)→ 发布了旧内容或半成品;"
                f"{first_divergence(local_text, remote_desc)}")
        if r["status"] != "WARN(delay)":
            return r

    # 发布来源 sha(可选)
    changelog = latest.get("changelog") or ""
    m = re.search(r"commit ([0-9a-f]{7,40})", changelog)
    if expect_sha:
        if not m:
            add("publish-sha", None, "changelog 无 commit sha,无法核对")
        elif m.group(1).startswith(expect_sha[:7]) or expect_sha.startswith(m.group(1)[:7]):
            add("publish-sha", True, f"changelog sha {m.group(1)[:10]} 匹配期望 {expect_sha[:10]}")
        else:
            add("publish-sha", False,
                f"changelog sha {m.group(1)[:10]} ≠ 期望 {expect_sha[:10]} → 线上是旧提交发布的")
    else:
        if m:
            r["info_sha"] = m.group(1)

    if r["status"] != "WARN(delay)":
        r["status"] = "PASS" if all(c["ok"] is True for c in r["checks"]) else "FAIL"
    return r


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("mode", nargs="?", default="check", choices=["check"], help="子命令,当前仅 check")
    ap.add_argument("skills", nargs="*", help="skill 目录(含 SKILL.md),可多个")
    ap.add_argument("--expect-sha", dest="expect_sha", default=None, help="期望的发布 commit sha")
    ap.add_argument("--bin", dest="bin", default=None, help="clawhub 命令(默认自动探测 clawhub / npx)")
    ap.add_argument("--timeout", type=int, default=90, help="单次 inspect 超时秒数")
    ap.add_argument("--json", dest="as_json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    if not args.skills:
        print(__doc__)
        return 2
    dirs = []
    for s in args.skills:
        d = Path(s).resolve()
        if not (d / "SKILL.md").exists():
            print(f"错误: {d} 不含 SKILL.md", file=sys.stderr)
            return 2
        dirs.append(d)

    clawhub_bin = resolve_clawhub_bin(args.bin)
    results = [check_one(d, args.expect_sha, clawhub_bin, args.timeout) for d in dirs]

    if args.as_json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    else:
        for r in results:
            icon = {"PASS": "✅", "FAIL": "❌", "WARN(delay)": "⏳"}.get(r["status"], "❓")
            print(f"{icon} {r['slug']}: {r['status']}")
            for c in r["checks"]:
                mark = {True: "  ✓", False: "  ✗", None: "  ?"}[c["ok"]]
                print(f"{mark} {c['check']}: {c['detail']}")
            if r.get("info_sha"):
                print(f"  ℹ 发布来源 commit: {r['info_sha'][:10]}")
        fails = [r["slug"] for r in results if r["status"] != "PASS"]
        if fails:
            print(f"\n汇总: {len(results) - len(fails)}/{len(results)} PASS;待处理: {', '.join(fails)}")
        else:
            print(f"\n汇总: {len(results)}/{len(results)} 全部 PASS——线上内容与本地一致,发布确认完成")
    return 1 if any(r["status"] != "PASS" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
