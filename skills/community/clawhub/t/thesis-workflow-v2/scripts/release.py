#!/usr/bin/env python3
"""
scripts/release.py — MBA Thesis Workflow 统一发布脚本

使用方式：
  python3 scripts/release.py              # 发 beta 包（默认）
  python3 scripts/release.py --release    # 发正式 release 包
  python3 scripts/release.py --check      # 仅检查版本状态

发布规则（v2.1.0 起执行）：
  1. SKILL.md metadata.clawdbot.version 是唯一真实来源（SSOT）
  2. 每次发布必须通过本脚本，禁止手动 clawhub publish / git tag
  3. beta 包：git tag = v{version}-beta.N，ClawHub = {version}-beta.N（N 自动递增）
  4. release 包：git tag = v{version}，ClawHub = {version}
  5. 所有 tag 永久保留，不覆盖，不删除
  6. ClawHub latest 只跟随正式 release 包

版本号格式：
  metadata.clawdbot.version: "2.1.0"（无后缀）
  git tag: v2.1.0-beta.1 / v2.1.0 / v2.1.1-beta.1 ...
  ClawHub: 2.1.0-beta.1 / 2.1.0 / 2.1.1-beta.1 ...
"""

import argparse
import os
import re
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional, List


REPO_ROOT = Path(__file__).parent.parent.resolve()
SKILL_PATH = REPO_ROOT / "SKILL.md"
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG-v2.md"
SKILL_METADATA_PATH = REPO_ROOT / ".openclaw" / "metadata.json"


def run(cmd: List[str], check=True, capture=True) -> subprocess.CompletedProcess:
    """执行 shell 命令，失败时默认退出。"""
    print(f"  $ {' '.join(cmd)}")
    kwargs = {}
    if capture:
        kwargs["capture_output"] = True
        kwargs["text"] = True
    result = subprocess.run(cmd, cwd=REPO_ROOT, **kwargs)
    if check and result.returncode != 0:
        print(f"❌ 命令失败: {' '.join(cmd)}")
        if capture:
            print(result.stderr)
        sys.exit(1)
    return result


def read_skill_version() -> str:
    """从 SKILL.md frontmatter 读取 metadata.clawdbot.version。"""
    content = SKILL_PATH.read_text()
    m = re.search(r'version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)["\']?', content)
    if not m:
        sys.exit("❌ 未找到 metadata.clawdbot.version，请检查 SKILL.md")
    return m.group(1)


def get_clawhub_latest_version(slug: str) -> Optional[str]:
    """获取 ClawHub 当前 latest 版本。"""
    result = run(
        ["clawhub", "skill", "verify", slug],
        check=False,
        capture=True,
    )
    # clawhub verify 可能 exit code 1（security check 失败），但 stdout 仍有 JSON
    try:
        data = json.loads(result.stdout)
        return data.get("version")
    except Exception:
        return None


def get_max_beta_tag(base_version: str) -> int:
    """获取当前 base_version 下最大的 beta.N 编号。"""
    result = run(
        ["git", "tag", "-l", f"v{base_version}-beta.*"],
        capture=True,
    )
    tags = result.stdout.strip().split("\n")
    max_n = 0
    for tag in tags:
        m = re.search(rf"v{re.escape(base_version)}-beta\.(\d+)", tag)
        if m:
            max_n = max(max_n, int(m.group(1)))
    return max_n


def get_current_git_tags() -> List[str]:
    """获取当前仓库所有 v2.x tags。"""
    result = run(["git", "tag", "-l", "v2.*"], capture=True)
    return [t.strip() for t in result.stdout.strip().split("\n") if t.strip()]


def check_version():
    """仅检查版本状态，不做发布。"""
    version = read_skill_version()
    clawhub = get_clawhub_latest_version("thesis-workflow-v2")
    git_tags = get_current_git_tags()

    print()
    print("=" * 50)
    print("版本状态检查")
    print("=" * 50)
    print(f"  SKILL.md version:    {version}")
    print(f"  ClawHub latest:      {clawhub or '(未发布)'}")
    print(f"  Git tags (v2.x):     {', '.join(sorted(git_tags, key=lambda t: tuple(int(x) for x in re.findall(r'[0-9]+', t)))) or '(无)'}")
    print()

    if clawhub is None:
        print("  ⚠️  未在 ClawHub 发布过，请先发布首个版本")
    elif version == clawhub:
        print("  ✅ 三端一致（正式 release）")
    elif clawhub.startswith(version + "-beta."):
        print(f"  ✅ beta 包状态正常：SKILL.md={version}（正式号），ClawHub={clawhub}（beta 快照）")
    else:
        print(f"  ⚠️  版本不一致，SKILL.md={version} ≠ ClawHub={clawhub}")
    print()
    sys.exit(0)


def update_changelog_header(version: str, tag_suffix: str):
    """更新 CHANGELOG-v2.md header 的 latest 版本号。"""
    if not CHANGELOG_PATH.exists():
        return
    content = CHANGELOG_PATH.read_text()
    full_version = f"{version}{tag_suffix}"
    # 替换 header 中的 latest 版本号
    content = re.sub(
        r"> 当前 latest: \*\*[0-9]+\.[0-9]+\.[0-9]+(?:-[a-z0-9.]+)?\*\*",
        f"> 当前 latest: **{full_version}**",
        content,
    )
    CHANGELOG_PATH.write_text(content)
    print(f"  ✅ CHANGELOG-v2.md header 更新为 {full_version}")


def release(release_mode: bool):
    """
    发布核心逻辑。

    release_mode=True  → 正式 release（无后缀）
    release_mode=False → beta 包（自动递增 beta.N 后缀）
    """
    slug = "thesis-workflow-v2"
    version = read_skill_version()
    clawhub_latest = get_clawhub_latest_version(slug)

    print()
    print("=" * 50)
    print(f"发布: thesis-workflow-v2@{version}")
    print(f"模式: {'正式 release' if release_mode else 'beta 包'}")
    print("=" * 50)

    # Step 1: 计算完整版本号
    if release_mode:
        tag_suffix = ""
        full_git_tag = f"v{version}"
        full_clawhub_version = version
    else:
        max_beta = get_max_beta_tag(version)
        next_beta_n = max_beta + 1
        tag_suffix = f"-beta.{next_beta_n}"
        full_git_tag = f"v{version}{tag_suffix}"
        full_clawhub_version = f"{version}{tag_suffix}"

    print(f"\n版本信息:")
    print(f"  SKILL.md:       {version}（源数据）")
    print(f"  Git tag:        {full_git_tag}")
    print(f"  ClawHub:        {full_clawhub_version}")

    # Step 2: 检查是否已有相同版本
    existing_tags = get_current_git_tags()
    if full_git_tag in existing_tags:
        print(f"\n❌ Git tag {full_git_tag} 已存在，请先确认代码变更")
        sys.exit(1)

    if clawhub_latest == full_clawhub_version:
        print(f"\n❌ ClawHub 已存在相同版本 {full_clawhub_version}")
        sys.exit(1)

    # Step 3: 更新 CHANGELOG header
    update_changelog_header(version, tag_suffix)

    # Step 4: git add + commit（如果有未提交变更）
    status = run(["git", "status", "--porcelain"], check=False, capture=True)
    if status.stdout.strip():
        print("\n📦 提交所有变更...")
        run(["git", "add", "-A"])
        run(["git", "commit", "-m", f"chore: pre-release commit for {full_git_tag}"])

    # Step 5: 打 git tag
    print(f"\n🏷️  打 git tag: {full_git_tag}")
    run(["git", "tag", "-a", full_git_tag, "-m", f"Release {full_git_tag}"])

    # Step 6: clawhub publish
    print(f"\n📤 发布到 ClawHub...")
    changelog_lines = [
        f"Release {full_git_tag}",
        f"- SKILL.md version: {version}",
        f"- git tag: {full_git_tag}",
        f"- ClawHub: {full_clawhub_version}",
    ]
    changelog_text = " | ".join(changelog_lines)

    result = run(
        [
            "clawhub", "skill", "publish", str(REPO_ROOT),
            "--slug", slug,
            "--owner", "hehe973781230",
            "--version", full_clawhub_version,
            "--tags", "latest" if release_mode else "beta",
            "--changelog", changelog_text,
        ],
        check=False,
        capture=True,
    )
    if result.returncode != 0:
        print(f"❌ ClawHub publish 失败:")
        print(result.stdout)
        print(result.stderr)
        # 回滚 git tag
        print(f"\n🔙 回滚 git tag...")
        run(["git", "tag", "-d", full_git_tag], check=False)
        sys.exit(1)

    # Step 7: git push + push tags
    print(f"\n🚀 推送到 GitHub...")
    run(["git", "push", "origin", "v2"])
    run(["git", "push", "--tags"])

    # Step 8: 验证
    print(f"\n✅ 发布完成，版本状态:")
    print(f"  SKILL.md:  {version}")
    print(f"  Git tag:   {full_git_tag}")
    print(f"  ClawHub:   {full_clawhub_version}")

    if not release_mode:
        print(f"\n  ℹ️  beta 包已发布，如需发正式 release，请运行:")
        print(f"     python3 scripts/release.py --release")

    print()


def main():
    parser = argparse.ArgumentParser(description="MBA Thesis Workflow 发布脚本")
    parser.add_argument("--check", action="store_true", help="仅检查版本状态，不发布")
    parser.add_argument("--release", action="store_true", help="发正式 release 包（默认发 beta 包）")
    args = parser.parse_args()

    if args.check:
        check_version()
    else:
        release(args.release)


if __name__ == "__main__":
    main()
