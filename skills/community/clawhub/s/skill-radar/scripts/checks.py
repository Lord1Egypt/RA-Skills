"""
checks.py — 状态检查 + 版本检查

包含 Skill Missing/Ready 状态检查和 ClawHub 版本更新检查。
"""

import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import run_cmd


# ─── 状态检查 ───────────────────────────────────────────────────────────────

def parse_skills_list() -> list[dict]:
    """解析 openclaw skills list 的输出"""
    output = run_cmd("openclaw skills list 2>/dev/null")
    if not output:
        return []

    skills = []
    sep = "\u2502"

    current_skill = None

    for line in output.split("\n"):
        stripped = line.strip()
        parts = [p.strip() for p in stripped.split(sep)]

        if len(parts) < 5:
            continue

        status_raw = parts[1].strip()
        if "ready" not in status_raw and "missing" not in status_raw:
            if current_skill and len(parts) >= 4:
                extra_desc = parts[2].strip()
                if extra_desc:
                    current_skill["description"] += " " + extra_desc
            continue

        if current_skill:
            skills.append(current_skill)

        status = "ready" if "ready" in status_raw else "missing"

        name_raw = parts[2].strip()
        name = re.sub(r'^[^\x00-\x7F]+', '', name_raw).strip()
        if not name:
            name = name_raw

        desc_part = parts[3].strip() if len(parts) > 3 else ""
        source = parts[4].strip() if len(parts) > 4 else ""

        current_skill = {
            "status": status,
            "name": name,
            "description": desc_part,
            "source": source,
        }

    if current_skill:
        skills.append(current_skill)

    return skills


def check_status() -> str:
    """检查 Skill Missing/Ready 状态"""
    lines = []
    lines.append(f"# 📊 Skill 状态检查")
    lines.append(f"\n> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    skills = parse_skills_list()
    if not skills:
        lines.append("⚠️ 无法获取 Skill 列表。请确保 `openclaw` CLI 可用。")
        return "\n".join(lines)

    ready = [s for s in skills if s["status"] == "ready"]
    missing = [s for s in skills if s["status"] == "missing"]

    ready_by_source = defaultdict(list)
    missing_by_source = defaultdict(list)
    for s in ready:
        ready_by_source[s["source"]].append(s)
    for s in missing:
        missing_by_source[s["source"]].append(s)

    lines.append("## 概览")
    lines.append("")
    lines.append(f"| 状态 | 数量 |")
    lines.append(f"|------|------|")
    lines.append(f"| ✅ Ready | **{len(ready)}** |")
    lines.append(f"| ❌ Missing | **{len(missing)}** |")
    lines.append(f"| 📦 总计 | **{len(skills)}** |")
    lines.append("")

    lines.append("## 按来源分布")
    lines.append("")
    lines.append("| 来源 | Ready | Missing |")
    lines.append("|------|-------|---------|")
    all_sources = sorted(set(s["source"] for s in skills))
    for src in all_sources:
        r = len(ready_by_source.get(src, []))
        m = len(missing_by_source.get(src, []))
        lines.append(f"| {src} | {r} | {m} |")
    lines.append("")

    if missing:
        lines.append(f"## ❌ Missing Skill 详情 ({len(missing)} 个)")
        lines.append("")

        bundled_missing = [s for s in missing if s["source"] == "openclaw-bundled"]
        other_missing = [s for s in missing if s["source"] != "openclaw-bundled"]

        if bundled_missing:
            lines.append(f"### Bundled Missing ({len(bundled_missing)} 个)")
            lines.append("")
            lines.append("> 💡 Bundled Skill 是 OpenClaw 自带的，missing 表示依赖未安装。")
            lines.append("> 如果确定不需要，可以通过更新 OpenClaw 来清理。")
            lines.append("")
            for s in bundled_missing:
                lines.append(f"- 🔐 `{s['name']}`")
                if s["description"]:
                    desc = s["description"][:80]
                    lines.append(f"  - {desc}")
            lines.append("")

        if other_missing:
            lines.append(f"### Other Missing ({len(other_missing)} 个)")
            lines.append("")
            for s in other_missing:
                lines.append(f"- ❌ `{s['name']}` [{s['source']}]")
                if s["description"]:
                    desc = s["description"][:80]
                    lines.append(f"  - {desc}")
            lines.append("")

        lines.append("### 💡 清理建议")
        lines.append("")
        lines.append(f"- 共 {len(bundled_missing)} 个 bundled Skill missing，建议等 OpenClaw 更新时自动清理")
        lines.append(f"- 共 {len(other_missing)} 个非 bundled Skill missing，检查是否需要安装依赖或卸载")
        lines.append("")
    else:
        lines.append("✅ 所有 Skill 均为 Ready 状态！")
        lines.append("")

    return "\n".join(lines)


# ─── 版本检查 ───────────────────────────────────────────────────────────────

def parse_clawhub_list() -> dict[str, str]:
    """解析 `npx clawhub list` 的输出，返回 {skill_name: version}"""
    output = run_cmd("npx clawhub list 2>/dev/null", timeout=60)
    if not output:
        return {}

    versions = {}
    for line in output.split("\n"):
        line = line.strip()
        m = re.match(r'^(\S+)\s+(\d+\.\d+\.\d+)', line)
        if m:
            versions[m.group(1)] = m.group(2)

    return versions


def inspect_clawhub_version(skill_name: str) -> str | None:
    """通过 clawhub inspect 获取 Skill 的最新版本"""
    output = run_cmd(
        f"npx clawhub inspect {skill_name} 2>/dev/null", timeout=15
    )
    if not output:
        return None

    m = re.search(r'(?:Latest|latest)\s*[=:]\s*(\d+\.\d+\.\d+)', output)
    if m:
        return m.group(1)
    return None


def check_versions() -> str:
    """检查 ClawHub Skill 版本更新"""
    lines = []
    lines.append(f"# 🔄 版本更新检查")
    lines.append(f"\n> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    local_versions = parse_clawhub_list()
    if not local_versions:
        lines.append("⚠️ 无法获取本地 Skill 版本列表。请确保 `npx clawhub` 可用。")
        return "\n".join(lines)

    lines.append(f"共发现 **{len(local_versions)}** 个通过 ClawHub 安装的 Skill。")
    lines.append("")

    needs_update = []
    already_latest = []
    unknown = []

    skill_names = list(local_versions.keys())

    lines.append("> ⏳ 正在从 ClawHub 查询最新版本（并行）...")
    lines.append("")

    def check_one(name):
        local_ver = local_versions[name]
        remote_ver = inspect_clawhub_version(name)
        return name, local_ver, remote_ver

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(check_one, name): name for name in skill_names}
        for future in as_completed(futures, timeout=300):
            try:
                name, local_ver, remote_ver = future.result()
                if remote_ver is None:
                    unknown.append((name, local_ver))
                elif remote_ver != local_ver:
                    needs_update.append((name, local_ver, remote_ver))
                else:
                    already_latest.append((name, local_ver))
            except Exception:
                name = futures[future]
                unknown.append((name, local_versions[name]))

    if needs_update:
        lines.append(f"## 🆕 需要更新 ({len(needs_update)} 个)")
        lines.append("")
        lines.append("| Skill | 本地版本 | 最新版本 |")
        lines.append("|-------|---------|---------|")
        for name, local, remote in sorted(needs_update):
            lines.append(f"| `{name}` | {local} | **{remote}** |")
        lines.append("")
        lines.append(
            "> 运行 `npx clawhub sync <skill-name>` 或 `npx clawhub sync` 全部更新"
        )
        lines.append("")

    if already_latest:
        lines.append(f"## ✅ 已是最新 ({len(already_latest)} 个)")
        lines.append("")
        for name, ver in sorted(already_latest):
            lines.append(f"- `{name}` v{ver}")
        lines.append("")

    if unknown:
        lines.append(f"## ❓ 无法查询 ({len(unknown)} 个)")
        lines.append("")
        for name, ver in sorted(unknown):
            lines.append(f"- `{name}` v{ver}（ClawHub 上未找到匹配项）")
        lines.append("")

    if not needs_update and not unknown:
        lines.append("🎉 所有 Skill 均为最新版本！")
        lines.append("")

    return "\n".join(lines)
