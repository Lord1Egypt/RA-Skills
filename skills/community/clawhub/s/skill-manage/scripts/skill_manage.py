#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Manage - OpenClaw Skills 查看/检查更新/升级/卸载
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

# ── 路径配置 ────────────────────────────────────────────────────────────────
WORKSPACE_SKILLS = Path(r"C:\Users\andy8\.qclaw\workspace\skills")
QCLAW_SKILLS = Path(r"C:\Users\andy8\.qclaw\skills")
SKILLHUB_LOCK = WORKSPACE_SKILLS / "skillhub.lock.json"

# ── 元数据提取 ──────────────────────────────────────────────────────────────
def get_skill_meta(skill_dir: Path) -> dict:
    skill_md = skill_dir / "SKILL.md"
    name = skill_dir.name
    version = None
    source = None
    remote_version = None

    try:
        exists = skill_md.exists()
    except PermissionError:
        exists = False

    if exists:
        try:
            text = skill_md.read_text(encoding="utf-8")
        except Exception:
            text = ""
        if text.startswith("---"):
            m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
            if m:
                yml = m.group(1)
                nv = re.search(r'^\s*version:\s*["\']?([\w.]+)', yml, re.MULTILINE)
                if nv:
                    version = nv.group(1)
                nn = re.search(r'^\s*name:\s*["\']?(.+)', yml, re.MULTILINE)
                if nn:
                    name = nn.group(1).strip()

    try:
        children = [p.name for p in skill_dir.iterdir()]
    except PermissionError:
        children = []

    if ".git" in children:
        source = "GitHub"
    elif "_meta.json" in children:
        source = "SkillHub"
        slug = name.lower().replace(" ", "-")
        try:
            req = urllib.request.Request(
                f"https://clawhub.com/api/v1/skill/{slug}",
                headers={"User-Agent": "OpenClaw"},
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
                remote_version = data.get("version")
        except Exception:
            pass
    elif "config.json" in children:
        source = "Config"
    else:
        source = "Local"

    has_update = (
        bool(version and remote_version and version != remote_version)
        if source == "SkillHub"
        else None
    )

    return {
        "name": name,
        "version": version or "N/A",
        "source": source,
        "path": str(skill_dir),
        "remote_version": remote_version,
        "has_update": has_update,
    }


def get_skillhub_lock() -> dict:
    if not SKILLHUB_LOCK.exists():
        return {}
    try:
        return json.loads(SKILLHUB_LOCK.read_text(encoding="utf-8"))
    except Exception:
        return {}


def scan_skills() -> list[dict]:
    """扫描所有 Skill，按 name 去重（workspace 优先）"""
    all_skills = []
    seen = {}
    for base in [WORKSPACE_SKILLS, QCLAW_SKILLS]:
        if not base.exists():
            continue
        try:
            dirs = sorted(base.iterdir())
        except PermissionError:
            print(f"  ⚠ 权限不足，跳过目录: {base}", file=sys.stderr)
            continue
        for d in dirs:
            if not d.is_dir():
                continue
            meta = get_skill_meta(d)
            key = meta["name"].lower()
            if key not in seen:
                seen[key] = meta
                all_skills.append(meta)
    return all_skills


# ── 命令实现 ────────────────────────────────────────────────────────────────
def cmd_list(args: argparse.Namespace) -> None:
    all_skills = scan_skills()
    sep = "=" * 62
    print(f"\n{sep}")
    print(f"  {'Name':<34} {'Ver':<14} {'Source':<10} Path")
    print(sep)
    for s in all_skills:
        ver = s["version"]
        if s.get("has_update"):
            ver = f"{s['version']} -> {s['remote_version']} (!)"
        print(f"  {s['name']:<34} {ver:<14} {s['source']:<10} {s['path']}")
    print(sep)
    print(f"  Total: {len(all_skills)} skills (workspace + ~/.qclaw/skills)")

    lock = get_skillhub_lock()
    if lock:
        print(f"\n  SkillHub lock: {SKILLHUB_LOCK}")
        for slug, info in lock.items():
            print(f"    {slug}: locked={info.get('version', '?')}")


def cmd_check(args: argparse.Namespace) -> bool:
    all_skills = scan_skills()
    print(f"\n{'='*50}")
    print("  Check for updates (Dry Run)")
    print("=" * 50)
    has_update = False
    for s in all_skills:
        if s["source"] == "GitHub":
            print(f"\n  [GitHub] {s['name']}")
            print(f"    Current : {s['version']}")
            print(f"    Command : cd {s['path']} && git pull")
            has_update = True
        elif s["source"] == "SkillHub" and s.get("has_update"):
            print(f"\n  [SkillHub] {s['name']}")
            print(f"    Current : {s['version']}")
            print(f"    Latest  : {s['remote_version']}")
            print(f"    Command : skillhub install {s['name'].lower().replace(' ', '-')}")
            has_update = True
        elif s["source"] == "Local":
            print(f"\n  [Local] {s['name']} - no auto-update path")
    if not has_update:
        print("\n  All skills are up to date.")
    return has_update


def cmd_update(args: argparse.Namespace) -> None:
    slug = args.name.lower().replace(" ", "-")
    skill_path = WORKSPACE_SKILLS / slug
    if not skill_path.exists():
        print(f"Skill '{slug}' not found in {WORKSPACE_SKILLS}")
        return
    meta = get_skill_meta(skill_path)
    if meta["source"] == "GitHub":
        print(f"[GitHub] {meta['name']} -> git pull")
        try:
            r = subprocess.run(
                ["git", "pull"],
                cwd=str(skill_path),
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            print(r.stdout or "(no output)")
            if r.stderr:
                print("STDERR:", r.stderr)
        except Exception as e:
            print(f"Error: {e}")
    elif meta["source"] == "SkillHub":
        slug_arg = meta["name"].lower().replace(" ", "-")
        print(f"[SkillHub] {meta['name']} -> skillhub install {slug_arg}")
        try:
            r = subprocess.run(
                ["skillhub", "install", slug_arg],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            print(r.stdout or "(no output)")
            if r.stderr:
                print("STDERR:", r.stderr)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Skill '{slug}' source={meta['source']}, auto-update not supported")


# ── 卸载辅助函数 ─────────────────────────────────────────────────────────────

def _scan_residuals(skill_name: str, skill_path: Path) -> dict:
    """扫描系统各角落，查找 skill 的残留痕迹"""
    residuals = {
        "lock_entries": [],   # skillhub.lock.json 中的记录
        "config_files": [],   # 配置文件
        "cache_dirs": [],     # 缓存目录
        "log_files": [],      # 日志文件
        "tmp_files": [],      # 临时文件
        "openclaw_config_refs": [],  # openclaw.json 中的引用
        "has_credentials": False,   # 是否包含敏感凭证
    }

    # 1. 检查 skillhub.lock.json（精确匹配 slug）
    lock = get_skillhub_lock()
    slug = skill_name.lower().replace(" ", "-")
    matched_slugs = []
    for lock_slug in lock.keys():
        if lock_slug == slug or lock_slug.replace("-", " ") == skill_name.lower():
            matched_slugs.append(lock_slug)
    if matched_slugs:
        residuals["lock_entries"].append((str(SKILLHUB_LOCK), matched_slugs))

    # 2. 检查 skill 主目录内是否有 config.json（含凭证风险）
    config_file = skill_path / "config.json"
    if config_file.exists():
        residuals["has_credentials"] = True
        residuals["config_files"].append(str(config_file))
    # 扫描主目录下的所有 .json / .env / .yaml 文件
    for pattern in ["*.json", "*.env", "*.yaml", "*.yml", "*.ini", "*.cfg"]:
        for f in skill_path.rglob(pattern):
            if f.is_file():
                residuals["config_files"].append(str(f))

    # 3. 检查 OpenClaw 主配置文件中的引用
    openclaw_json_paths = [
        Path(r"C:\Users\andy8\.qclaw\workspace\openclaw.json"),
        Path(r"C:\Users\andy8\AppData\Roaming\openclaw\openclaw.json"),
        Path(r"C:\Users\andy8\.openclaw\openclaw.json"),
    ]
    keyword = skill_name.lower()
    for oc_path in openclaw_json_paths:
        if not oc_path.exists():
            continue
        try:
            text = oc_path.read_text(encoding="utf-8")
            if keyword in text.lower():
                residuals["openclaw_config_refs"].append(str(oc_path))
        except Exception:
            pass

    # 4. 检查 workspace 根目录残留（TMP/、scripts/、output/、archive/ 中的 skill 名文件）
    workspace_root = Path(r"C:\Users\andy8\.qclaw\workspace")
    for sub_dir in ["TMP", "scripts", "output", "archive"]:
        sub = workspace_root / sub_dir
        if not sub.exists():
            continue
        for f in sub.rglob("*"):
            if f.is_file() and (keyword in f.stem.lower() or keyword in f.name.lower()):
                residuals["tmp_files"].append(str(f))

    # 5. 检查 ~/.qclaw/ 下的缓存目录
    qclaw_base = Path(r"C:\Users\andy8\.qclaw")
    for sub in qclaw_base.iterdir():
        if sub.is_dir() and sub != skill_path and sub.name not in ["skills", "workspace"]:
            for f in sub.rglob("*"):
                if f.is_file() and (keyword in f.stem.lower() or keyword in f.name.lower()):
                    residuals["cache_dirs"].append(str(f))

    return residuals


def _print_residuals(residuals: dict) -> None:
    """打印残留扫描结果"""
    sep = "─" * 50
    print(f"\n  {sep}")
    print("  🔍 残留痕迹扫描结果")
    print(f"  {sep}")

    if residuals["lock_entries"]:
        print(f"\n  📋 SkillHub 锁文件记录:")
        for p, _ in residuals["lock_entries"]:
            print(f"     → {p}")

    if residuals["config_files"]:
        cred = "⚠️ 含凭证" if residuals["has_credentials"] else ""
        print(f"\n  📄 配置文件 {cred}:")
        for p in residuals["config_files"]:
            print(f"     → {p}")

    if residuals["openclaw_config_refs"]:
        print(f"\n  ⚙️  OpenClaw 配置引用:")
        for p in residuals["openclaw_config_refs"]:
            print(f"     → {p}")

    if residuals["cache_dirs"]:
        print(f"\n  📦 缓存/临时文件:")
        for p in residuals["cache_dirs"]:
            print(f"     → {p}")

    if residuals["tmp_files"]:
        print(f"\n  🗂️  workspace 中的残留文件:")
        for p in residuals["tmp_files"]:
            print(f"     → {p}")

    if not any(residuals.values()):
        print("\n  ✅ 未发现残留痕迹，干净卸载！")


def _clean_residuals(residuals: dict, dry_run: bool = False) -> dict:
    """清理残留文件，返回清理结果"""
    cleaned = {"lock_entries": [], "config_files": [], "tmp_files": [], "errors": []}

    # 清理 skillhub.lock.json（精确删除匹配的 slug 条目）
    if residuals["lock_entries"]:
        try:
            lock = get_skillhub_lock()
            for lock_path, matched_slugs in residuals["lock_entries"]:
                for ms in matched_slugs:
                    if ms in lock:
                        del lock[ms]
            if not dry_run:
                SKILLHUB_LOCK.write_text(
                    json.dumps(lock, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )
            cleaned["lock_entries"].append(f"已移除 {len(matched_slugs)} 条锁记录")
        except Exception as e:
            cleaned["errors"].append(f"锁文件清理失败: {e}")

    # 清理缓存/临时文件
    for p_str in residuals["cache_dirs"] + residuals["tmp_files"]:
        p = Path(p_str)
        if p.exists():
            try:
                if not dry_run:
                    if p.is_dir():
                        shutil.rmtree(p)
                    else:
                        p.unlink()
                cleaned["tmp_files"].append(p_str)
            except Exception as e:
                cleaned["errors"].append(f"删除失败 {p_str}: {e}")

    # 清理配置文件（含凭证）
    for p_str in residuals["config_files"]:
        p = Path(p_str)
        if p.exists():
            try:
                if not dry_run:
                    p.unlink()
                cleaned["config_files"].append(p_str)
            except Exception as e:
                cleaned["errors"].append(f"删除配置失败 {p_str}: {e}")

    return cleaned


def cmd_uninstall(args: argparse.Namespace) -> None:
    name = args.name
    found, found_path = None, None
    for base in [WORKSPACE_SKILLS, QCLAW_SKILLS]:
        if not base.exists():
            continue
        for d in base.iterdir():
            if d.is_dir() and d.name.lower() == name.lower():
                meta = get_skill_meta(d)
                found = meta
                found_path = d
                break
        if found:
            break
    if not found:
        print(f"Skill '{name}' not found")
        return

    # ── Step 1: 显示 skill 信息 ──────────────────────────────────────────────
    sep = "=" * 56
    print(f"\n{sep}")
    print("  🗑️  Uninstall Skill — 彻底卸载")
    print(sep)
    print(f"  名称   : {found['name']}")
    print(f"  版本   : {found['version']}")
    print(f"  来源   : {found['source']}")
    print(f"  路径   : {found['path']}")
    print(sep)

    # ── Step 2: 扫描残留 ─────────────────────────────────────────────────────
    residuals = _scan_residuals(found["name"], found_path)

    # 去重：config.json 可能同时被锁文件扫描和配置文件扫描收录
    if residuals["config_files"]:
        residuals["config_files"] = list(dict.fromkeys(residuals["config_files"]))

    _print_residuals(residuals)

    # ── Step 3: Dry Run 模式 ────────────────────────────────────────────────
    if args.dry_run:
        print("\n  🔎 Dry Run 模式：仅展示，不执行任何删除")
        cleaned = _clean_residuals(residuals, dry_run=True)
        print(f"\n  如执行，将清理:")
        if cleaned["lock_entries"]:
            print(f"    • 锁文件记录: {len(cleaned['lock_entries'])} 项")
        if cleaned["config_files"]:
            print(f"    • 配置文件: {len(cleaned['config_files'])} 项")
        if cleaned["tmp_files"]:
            print(f"    • 缓存/临时文件: {len(cleaned['tmp_files'])} 项")
        if not any(cleaned.values()):
            print("    • 无")
        return

    # ── Step 4: 凭证风险提示 ─────────────────────────────────────────────────
    if residuals["has_credentials"]:
        print(f"\n  ⚠️  检测到配置文件可能含敏感凭证（AppSecret/Token 等）")
        print("     建议：先备份，再卸载")
        print("     操作：输入 's' 跳过 skill 主目录删除，仅清理残留")
        print("            输入 'y' 确认全部删除（含凭证文件）")
        print("            输入 'n' 取消退出")
        confirm = input("  继续? (y/s/n): ").strip().lower()
    elif not args.force:
        confirm = input("  确认卸载? (y/N): ").strip().lower()
    else:
        confirm = "y"

    if confirm not in ("y", "s"):
        print("  取消退出。")
        return

    # ── Step 5: 执行清理 ────────────────────────────────────────────────────
    print("\n  🧹 开始清理...")

    # 5a. 清理残留（先于主目录删除，因为主目录删除后路径就不存在了）
    if confirm == "s":
        # 仅清理残留，不删主目录
        cleaned = _clean_residuals(residuals)
        print(f"  ✅ 残留清理完成")
        for k, v in cleaned.items():
            if v and k != "errors":
                print(f"     • {k}: {len(v)} 项")
        if cleaned["errors"]:
            for err in cleaned["errors"]:
                print(f"     ❌ {err}")
        print("  ℹ️  skill 主目录已保留（凭证文件未删除）")
        return

    # 5b. 清理残留
    cleaned = _clean_residuals(residuals)
    print(f"  ✅ 残留清理完成")
    for k, v in cleaned.items():
        if v and k != "errors":
            print(f"     • {k}: {len(v)} 项")
    if cleaned["errors"]:
        for err in cleaned["errors"]:
            print(f"     ❌ {err}")

    # 5c. 删除 skill 主目录
    try:
        shutil.rmtree(found_path)
        print(f"  ✅ 主目录已删除: {found_path}")
    except Exception as e:
        print(f"  ❌ 主目录删除失败: {e}")
        return

    # ── Step 6: 完成后提示 ──────────────────────────────────────────────────
    if residuals["openclaw_config_refs"]:
        print(f"\n  ℹ️  OpenClaw 配置文件中仍有引用，建议手动检查并移除:")
        for p in residuals["openclaw_config_refs"]:
            print(f"     → {p}")

    print("\n  🎉 卸载完成！")


# ── 入口 ────────────────────────────────────────────────────────────────────
def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser(description="OpenClaw Skill Manager")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="List all installed skills")
    p_check = sub.add_parser("check", help="Check for updates (dry run)")

    p_up = sub.add_parser("update", help="Update a skill")
    p_up.add_argument("name", help="Skill name or slug")

    p_un = sub.add_parser("uninstall", help="Uninstall a skill (彻底卸载)")
    p_un.add_argument("name", help="Skill name")
    p_un.add_argument("--force", "-y", action="store_true", help="跳过确认直接卸载")
    p_un.add_argument("--dry-run", action="store_true", help="仅扫描残留，不执行删除")

    args = parser.parse_args()

    if args.cmd == "list":
        cmd_list(args)
    elif args.cmd == "check":
        cmd_check(args)
    elif args.cmd == "update":
        cmd_update(args)
    elif args.cmd == "uninstall":
        cmd_uninstall(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
