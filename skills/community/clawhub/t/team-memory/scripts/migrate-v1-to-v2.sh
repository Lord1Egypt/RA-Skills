#!/usr/bin/env bash

# Team Memory v2.4.0 - v1 数据迁移脚本
# 默认 dry-run；加 --apply 才复制文件。

set -euo pipefail

python3 - "$@" <<'PY'
from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Member:
    member_id: str
    name: str
    alias: str = ""


def clean_value(raw: str) -> str:
    raw = raw.split("#", 1)[0].strip()
    if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
        return raw[1:-1]
    return raw


def default_skill_dir() -> Path:
    cwd = Path.cwd()
    if (cwd / "SKILL.md").exists() and (cwd / "data").exists():
        return cwd
    return Path.home() / ".config" / "opencode" / "skills" / "team-memory"


def parse_config(config_path: Path) -> tuple[list[Member], list[str]]:
    text = config_path.read_text(encoding="utf-8")
    members: list[Member] = []
    errors: list[str] = []
    current: dict[str, str] | None = None
    in_members = False
    in_shortcuts = False
    shortcut_owner: dict[str, str] = {}
    identity_owner: dict[str, str] = {}

    def finish_current() -> None:
        nonlocal current
        if not current:
            return
        member_id = current.get("id", "")
        name = current.get("name", "")
        alias = current.get("alias", "")
        if not member_id or not name:
            errors.append(f"成员配置缺少 id 或 name: {current}")
        else:
            members.append(Member(member_id, name, alias))
            for key in [name, alias]:
                if not key:
                    continue
                old = identity_owner.get(key)
                if old and old != member_id:
                    errors.append(f"成员名称/别名冲突: {key} 同时指向 {old} 和 {member_id}")
                identity_owner[key] = member_id
        current = None

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        is_top_level = bool(line) and not line[0].isspace()
        if is_top_level and re.match(r"^[A-Za-z0-9_-]+:", stripped) and not stripped.startswith("- "):
            section = stripped.split(":", 1)[0]
            if section != "members":
                finish_current()
            in_members = section == "members"
            in_shortcuts = section == "shortcuts"
            continue
        if in_members:
            if stripped.startswith("- "):
                finish_current()
                current = {}
                rest = stripped[2:].strip()
                if ":" in rest:
                    key, value = rest.split(":", 1)
                    current[key.strip()] = clean_value(value)
                continue
            if current is not None and ":" in stripped:
                key, value = stripped.split(":", 1)
                current[key.strip()] = clean_value(value)
        elif in_shortcuts and ":" in stripped:
            key, value = stripped.split(":", 1)
            shortcut = clean_value(key)
            member_id = clean_value(value)
            old = shortcut_owner.get(shortcut)
            if old and old != member_id:
                errors.append(f"快捷输入冲突: {shortcut} 同时指向 {old} 和 {member_id}")
            shortcut_owner[shortcut] = member_id

    finish_current()

    member_ids = {m.member_id for m in members}
    for shortcut, member_id in shortcut_owner.items():
        if member_id not in member_ids:
            errors.append(f"快捷输入 {shortcut} 指向不存在的成员 {member_id}")
        old = identity_owner.get(shortcut)
        if old and old != member_id:
            errors.append(f"快捷输入与成员别名冲突: {shortcut} 同时指向 {old} 和 {member_id}")

    return members, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate Team Memory v1 files to v2 layout.")
    parser.add_argument("--apply", action="store_true", help="copy files after validation")
    parser.add_argument("--skill-dir", default=None, help="team-memory skill directory")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve() if args.skill_dir else default_skill_dir().resolve()
    data_dir = skill_dir / "data"
    members_dir = data_dir / "members"
    config_path = skill_dir / "skill-config.yaml"

    if not config_path.exists():
        print(f"ERROR: 缺少配置文件: {config_path}")
        return 1
    if not members_dir.exists():
        print(f"ERROR: 缺少成员目录: {members_dir}")
        return 1

    members, errors = parse_config(config_path)
    if not members:
        errors.append("skill-config.yaml 中没有可用成员")
    if errors:
        print("ERROR: 配置校验失败")
        for error in errors:
            print(f"- {error}")
        return 1

    mapping = {
        "档案": "profile.md",
        "时间轴": "timeline.md",
        "蒸馏": "distill.md",
    }
    planned: list[tuple[Path, Path, Member]] = []

    for member in members:
        for suffix, target_name in mapping.items():
            src = members_dir / f"{member.name}-{suffix}.md"
            if not src.exists():
                continue
            dst = members_dir / member.member_id / target_name
            planned.append((src, dst, member))

    if not planned:
        print("没有发现可迁移的 v1 文件。")
        return 0

    existing = [dst for _, dst, _ in planned if dst.exists()]
    if existing:
        print("ERROR: 目标文件已存在，脚本不会覆盖。")
        for path in existing:
            print(f"- {path}")
        return 1

    print("迁移预览" + ("（执行模式）" if args.apply else "（dry-run，不会写入）"))
    print(f"Skill 目录: {skill_dir}")
    for src, dst, member in planned:
        print(f"- {member.member_id} {member.name}: {src.relative_to(skill_dir)} -> {dst.relative_to(skill_dir)}")

    if not args.apply:
        print("确认无误后运行: bash scripts/migrate-v1-to-v2.sh --apply")
        return 0

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = data_dir / ".backup" / timestamp
    backup_dir.mkdir(parents=True, exist_ok=False)

    for src, dst, _ in planned:
        backup_target = backup_dir / src.relative_to(data_dir)
        backup_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, backup_target)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    print(f"迁移完成。备份目录: {backup_dir}")
    print("旧 v1 文件已保留。")
    return 0


raise SystemExit(main())
PY
