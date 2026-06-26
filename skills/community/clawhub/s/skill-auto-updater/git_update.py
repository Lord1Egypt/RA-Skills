#!/usr/bin/env python3
"""
Skill-Updater: 本地修改保护式 Skill 更新

核心逻辑：
1. 安装/首次运行 → 扫描 skill 的原始状态
2. 用户修改 skill → 自动保存 diff patch
3. clawhub 发布新版 → 尝试将 patch 应用到新版
4. 成功 → 写入新版，保留修改 ✅
  失败 → 报告冲突，列出 diff3，用户手动决策

用法：
  python3 git_update.py                        # 预览（哪些 skill 有新版，修改会不会冲突）
  python3 git_update.py --apply               # 实际执行
  python3 git_update.py --apply --skill <slug> # 仅更新指定 skill
  python3 git_update.py --show-patch          # 显示已保存的修改
  python3 git_update.py --discard             # 丢弃所有保存的修改
  python3 git_update.py --discard --skill <slug>  # 丢弃指定 skill 的修改
"""
import os
import sys
import subprocess
import json
import time
import shutil
import hashlib
from datetime import datetime
from pathlib import Path

SKILLS_DIR = os.environ.get("OPENCLAW_SKILLS_DIR", "/root/.openclaw/workspace/skills")
UPDATER_DIR = ".skill-updater"
PATCH_FILE = "mod.patch"
ORIGINALS_DIR = "originals"


# ============ 工具函数 ============

def run(cmd: list, cwd: str = SKILLS_DIR, timeout: int = 60, input: str = "") -> tuple[int, str, str]:
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                         timeout=timeout,
                         input=input if input else None)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except Exception as e:
        return -1, "", str(e)


def skill_updater_dir(skill_path: str) -> str:
    return os.path.join(skill_path, UPDATER_DIR)


def patch_path(skill_path: str) -> str:
    return os.path.join(skill_path, UPDATER_DIR, PATCH_FILE)


def originals_dir(skill_path: str) -> str:
    return os.path.join(skill_path, UPDATER_DIR, ORIGINALS_DIR)





def skill_origin_json(skill_path: str) -> str:
    return os.path.join(skill_path, ".clawhub", "origin.json")


# ============ 核心逻辑 ============

def get_clawhub_slug(skill_path: str) -> str | None:
    """从 .clawhub/origin.json 读取 slug"""
    origin = skill_origin_json(skill_path)
    if not os.path.exists(origin):
        return None
    try:
        with open(origin) as f:
            d = json.load(f)
        if d.get("registry") == "https://clawhub.ai":
            return d.get("slug")
    except Exception:
        pass
    return None


def list_clawhub_skills() -> list[dict]:
    """列出所有通过 clawhub 安装的 skill"""
    result = []
    for entry in os.listdir(SKILLS_DIR):
        skill_path = os.path.join(SKILLS_DIR, entry)
        if not os.path.isdir(skill_path):
            continue
        slug = get_clawhub_slug(skill_path)
        if not slug:
            continue
        origin = skill_origin_json(skill_path)
        with open(origin) as f:
            d = json.load(f)
        result.append({
            "slug": slug,
            "path": entry,
            "installed": d.get("installedVersion", "0"),
        })
    return result


def get_clawhub_latest(slug: str) -> str | None:
    """通过 clawhub inspect 获取某 skill 的最新版本"""
    try:
        r = subprocess.run(
            ["clawhub", "inspect", slug],
            cwd=SKILLS_DIR, capture_output=True, text=True, timeout=20
        )
        if r.returncode == 0:
            for line in r.stdout.split("\n"):
                if line.startswith("Latest:"):
                    return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return None


def has_local_modifications(skill_path: str) -> bool:
    """检查 skill 是否有未保存的本地修改"""
    p = patch_path(skill_path)
    if os.path.exists(p) and os.path.getsize(p) > 0:
        return True
    return False


def get_modified_files(skill_path: str) -> list[str]:
    """
    找出 skill 目录中，与 .skill-updater/originals/ 不同的文件。
    即：哪些文件被用户修改了。
    """
    orig_dir = originals_dir(skill_path)
    if not os.path.isdir(orig_dir):
        return []

    modified = []
    for root, dirs, files in os.walk(orig_dir):
        for fname in files:
            orig_file = os.path.join(root, fname)
            rel = os.path.relpath(orig_file, orig_dir)
            cur_file = os.path.join(skill_path, rel)
            if not os.path.exists(cur_file):
                continue  # 文件被删除了，不计入修改
            with open(orig_file, "rb") as f1, open(cur_file, "rb") as f2:
                if f1.read() != f2.read():
                    modified.append(rel)
    return modified


def save_modifications(skill_path: str) -> dict:
    """
    扫描 skill 目录，将所有文件保存原始快照到 .skill-updater/originals/，
    并与已保存的 originals 比较，生成 mod.patch。
    返回: {has_mods: bool, patch_size: int, modified_files: list}
    """
    updater = skill_updater_dir(skill_path)
    orig_dir = originals_dir(skill_path)
    p_path = patch_path(skill_path)

    os.makedirs(orig_dir, exist_ok=True)

    # 扫描 skill 目录下所有文本文件（排除隐藏目录和 updater 自身）
    current_files = {}
    for root, dirs, files in os.walk(skill_path):
        # 跳过隐藏目录和 skill-updater 自身
        dirs[:] = [d for d in dirs if not d.startswith(".") or d == UPDATER_DIR]
        for fname in files:
            if fname.startswith("."):
                continue
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, skill_path)
            if rel.startswith(UPDATER_DIR):
                continue
            try:
                with open(full, "r", encoding="utf-8", errors="ignore") as f:
                    current_files[rel] = f.read()
            except Exception:
                pass

    # 备份当前文件到 originals/
    for rel, content in current_files.items():
        orig_full = os.path.join(orig_dir, rel)
        os.makedirs(os.path.dirname(orig_full), exist_ok=True)
        with open(orig_full, "w", encoding="utf-8") as f:
            f.write(content)

    # 生成 patch（对比 originals 和当前文件，找出差异）
    patch_lines = []
    for rel in sorted(current_files.keys()):
        # diff -u .skill-updater/originals/<rel> <rel>
        # patch -p2 时：.skill-updater/originals/ 被剥离 → 写到 <rel>
        orig_rel = os.path.join(UPDATER_DIR, ORIGINALS_DIR, rel)
        code, diff_out, _ = run(
            ["diff", "-u", orig_rel, rel],
            cwd=skill_path
        )
        if diff_out.strip():
            patch_lines.append(diff_out)

    patch_content = "".join(patch_lines)
    with open(p_path, "w", encoding="utf-8") as f:
        f.write(patch_content)

    modified_files = get_modified_files(skill_path)
    return {
        "has_mods": bool(patch_content.strip()),
        "patch_size": len(patch_content),
        "modified_files": modified_files,
    }


def try_merge(skill_path: str) -> dict:
    """
    尝试将 mod.patch 应用到当前 skill 目录（新版本文件）。
    返回: {success: bool, applied: int, failed: list, diff3_output: str}
    """
    p = patch_path(skill_path)
    if not os.path.exists(p) or not os.path.getsize(p) > 0:
        return {"success": True, "applied": 0, "failed": [], "diff3_output": ""}

    # patch --dry-run -N（-N: 把未修改的文件视为已添加；允许应用到新文件）
    code, out, err = run([
        "patch", "--dry-run", "-p2", "-N", "--binary", "--no-backup-if-mismatch"
    ], cwd=skill_path, input=open(p).read())

    if code == 0:
        # 干跑成功，实际执行
        code2, out2, err2 = run([
            "patch", "-p2", "-N", "--binary", "--no-backup-if-mismatch"
        ], cwd=skill_path, input=open(p).read())
        if code2 == 0:
            return {"success": True, "applied": -1, "failed": [], "diff3_output": ""}
        else:
            # 干跑成功但实际失败，回退
            run(["patch", "-R", "-p2", "-N"], cwd=skill_path, input=open(p).read())
            return {
                "success": False,
                "applied": 0,
                "failed": ["patch apply failed after dry-run success"],
                "diff3_output": err2
            }

    # 干跑失败，生成 diff3 报告
    failed_files = _extract_failed_files(out + err)
    diff3 = _generate_diff3(skill_path, failed_files)

    return {
        "success": False,
        "applied": 0,
        "failed": failed_files,
        "diff3_output": diff3
    }


def _extract_failed_files(patch_output: str) -> list[str]:
    """
    从 patch --dry-run 的输出中提取失败的文件名。
    匹配格式:
      - "checking file <name>" 出现在 "Hunk #N FAILED" 之前
      - "patch: *** malformed patch" 格式
    """
    failed = []
    current_file = None
    for line in patch_output.split("\n"):
        if "checking file " in line:
            current_file = line.split("checking file ", 1)[1].strip()
        elif "FAILED" in line and current_file:
            if current_file not in failed:
                failed.append(current_file)
            current_file = None
    return failed


def _generate_diff3(skill_path: str, failed_files: list[str]) -> str:
    """
    为失败的文件生成 diff 对比。
    显示：原始版本 vs clawhub 新版（简化版，不做三路合并）
    """
    import subprocess as _subprocess
    orig_dir = originals_dir(skill_path)
    lines = []
    for rel in failed_files:
        orig_file = os.path.join(orig_dir, rel)
        cur_file = os.path.join(skill_path, rel)

        if not os.path.exists(cur_file):
            lines.append(f"\n=== {rel} ===")
            lines.append("(新版文件不存在，无法对比)")
            continue

        r = _subprocess.run(
            ["diff", "-u",
             "--label", f"BASE({rel} 原始版本)",
             "--label", f"REMOTE({rel} clawhub新版 — 你的修改与此冲突)",
             orig_file, cur_file],
            capture_output=True, text=True, timeout=15
        )

        lines.append(f"\n=== {rel} ===")
        if r.stdout:
            lines.append(r.stdout)
        else:
            lines.append("(两个版本完全相同，或 diff 生成失败)")
    return "".join(lines)


def do_update(slug: str) -> tuple[int, str, str]:
    """执行 clawhub update"""
    r = subprocess.run(
        ["clawhub", "update", slug],
        cwd=SKILLS_DIR, capture_output=True, text=True, timeout=120
    )
    return r.returncode, r.stdout, r.stderr


# ============ CLI 命令 ============

CMD_DRY_RUN = "dry_run"
CMD_APPLY = "apply"
CMD_SHOW_PATCH = "show_patch"
CMD_DISCARD = "discard"


def cmd_dry_run(target_slug: str | None = None):
    """预览模式：显示哪些 skill 有新版，修改会不会冲突"""
    print(f"=== Skill-Updater Dry-Run @ {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")

    skills = list_clawhub_skills()
    if not skills:
        print("未找到通过 clawhub 安装的 skill")
        return

    has_mods = False
    update_count = 0

    for skill in skills:
        slug = skill["slug"]
        path = os.path.join(SKILLS_DIR, skill["path"])

        # 跳过非目标 skill
        if target_slug and slug != target_slug:
            continue

        latest = get_clawhub_latest(slug)
        current = skill["installed"]
        has_update = False
        try:
            from packaging.version import parse as parse_ver
            has_update = latest and parse_ver(latest) > parse_ver(current)
        except Exception:
            has_update = latest != current

        has_mod = has_local_modifications(path)
        modified_files = get_modified_files(path) if has_mod else []
        status_icon = ""

        print(f"📦 {slug}")
        print(f"   版本: {current} → {latest or '?'}")
        if has_update:
            print(f"   🆕 有新版", end="")
            if has_mod:
                print(f"（有{len(modified_files)}个文件被修改）")
            else:
                print()
            update_count += 1
        else:
            print(f"   ✅ 已是最新", end="")
            if has_mod:
                print(f"（有{len(modified_files)}个文件被修改）")
            else:
                print()
        has_mods = has_mods or has_mod
        print()

    print(f"共 {len(skills)} 个 clawhub skill，{update_count} 个有新版")
    if has_mods:
        print("\n⚠️  有 skill 包含本地修改，更新时会尝试保留修改")
    print("\n使用 --apply 执行实际更新")


def cmd_show_patch(target_slug: str | None = None):
    """显示已保存的修改内容"""
    skills = list_clawhub_skills()
    found = False

    for skill in skills:
        slug = skill["slug"]
        if target_slug and slug != target_slug:
            continue
        path = os.path.join(SKILLS_DIR, skill["path"])
        p = patch_path(path)
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            continue
        found = True
        with open(p) as f:
            content = f.read()
        modified = get_modified_files(path)
        print(f"📄 {slug} — 修改文件: {', '.join(modified) if modified else '(全部文件)'}")
        print(f"   patch 大小: {len(content)} 字节")
        print("-" * 50)
        print(content[:2000])
        if len(content) > 2000:
            print(f"...（省略 {len(content)-2000} 字节）")
        print()

    if not found:
        print("没有已保存的修改")


def cmd_discard(target_slug: str | None = None):
    """丢弃保存的修改（接受新版，放弃本地修改）"""
    skills = list_clawhub_skills()
    count = 0

    for skill in skills:
        slug = skill["slug"]
        if target_slug and slug != target_slug:
            continue
        path = os.path.join(SKILLS_DIR, skill["path"])
        updater = skill_updater_dir(path)
        if not os.path.isdir(updater):
            continue
        shutil.rmtree(updater)
        print(f"🗑  已丢弃 {slug} 的保存修改")
        count += 1

    if count == 0:
        print("没有可丢弃的修改")


def cmd_apply(target_slug: str | None = None, dry_run: bool = True):
    """执行更新"""
    mode = "[DRY-RUN] " if dry_run else ""
    print(f"=== {mode}Skill-Updater @ {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")

    if dry_run:
        print("ℹ️  Dry-run 模式：只显示将执行的操作，不实际修改\n")

    skills = list_clawhub_skills()
    updated = []
    skipped = []
    failed = []

    for skill in skills:
        slug = skill["slug"]
        if target_slug and slug != target_slug:
            continue

        path = os.path.join(SKILLS_DIR, skill["path"])
        latest = get_clawhub_latest(slug)
        current = skill["installed"]
        has_update = False
        try:
            from packaging.version import parse as parse_ver
            has_update = latest and parse_ver(latest) > parse_ver(current)
        except Exception:
            has_update = latest != current

        if not has_update:
            continue

        print(f"📦 {slug}: {current} → {latest}")

        # Step 1: 保存本地修改（如果还没有快照）
        has_mod = has_local_modifications(path)
        mod_info = None
        if not has_mod:
            mod_info = save_modifications(path)
            has_mod = mod_info["has_mods"]
            if has_mod:
                print(f"   📋 已保存 {mod_info['patch_size']} 字节修改，"
                      f"涉及 {mod_info['modified_files']}")

        # Step 2: 执行 clawhub update
        if not dry_run:
            print(f"   ⬇️  执行 clawhub update...")
            code, out, err = do_update(slug)
            if code != 0:
                print(f"   ❌ clawhub update 失败: {err}")
                failed.append(slug)
                continue
            print(f"   ✅ clawhub update 完成")
        else:
            print(f"   ⏭️  [dry-run] 跳过 clawhub update")

        # Step 3: 尝试合并保存的修改
        if has_mod:
            merge_result = try_merge(path)
            if merge_result["success"]:
                applied = merge_result.get("applied", 0)
                # 合并成功后，如果 patch 已全部应用（即 mod.patch 现在为空），删除它
                p = patch_path(path)
                if os.path.exists(p) and os.path.getsize(p) == 0:
                    os.remove(p)
                if applied == -1:
                    print(f"   ✅ 修改已保留并应用（所有文件）")
                elif isinstance(applied, list):
                    print(f"   ✅ 修改已保留并应用（{len(applied)} 个文件）")
                else:
                    print(f"   ✅ 修改已保留并应用")
                updated.append(slug)
            else:
                print(f"   ⚠️  修改无法自动保留（{len(merge_result['failed'])} 个文件冲突）")
                print(f"   📄 diff3 报告已生成，请手动处理")
                # 写入详细报告
                _write_conflict_report(path, slug, merge_result)
                failed.append(slug)
        else:
            print(f"   ✅ 无本地修改，直接使用新版")
            updated.append(slug)

        print()

    # 汇总
    print("=" * 50)
    if dry_run:
        print("【dry-run 结果，仅预览】")
    if updated:
        print(f"✅ 将更新: {', '.join(updated)}")
    if failed:
        print(f"⚠️  有冲突需手动处理: {', '.join(failed)}")
    if not updated and not failed:
        print("所有 skill 已是最新的，无需更新")
    print("=" * 50)


def _write_conflict_report(skill_path: str, slug: str, merge_result: dict):
    """写入冲突详细报告"""
    updater = skill_updater_dir(skill_path)
    os.makedirs(updater, exist_ok=True)
    report_file = os.path.join(updater, "CONFLICTS.md")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    content = f"""# Skill 更新冲突报告
更新 skill: **{slug}**
时间: {timestamp}

## 冲突文件

"""
    for f in merge_result.get("failed", []):
        content += f"- `{f}`\n"

    content += f"""
## 冲突详情（diff3 格式）

{LOCAL} = 你的修改
BASE = 原始版本（安装时）
REMOTE = clawhub 新版

```
{merge_result.get('diff3_output', '(无可用详情)')}
```

## 处理方式

1. **接受新版（丢弃你的修改）**：
   ```bash
   python3 git_update.py --discard --skill {slug}
   ```

2. **手动合并**：
   - 打开冲突文件，搜索 `<<<<<<<` 和 `>>>>>>>` 标记
   - 手动决定保留哪些修改
   - 保存后，重新运行：
     ```bash
     python3 git_update.py --apply --skill {slug}
     ```

---
此报告由 skill-updater 自动生成
"""
    with open(report_file, "w") as f:
        f.write(content)



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Skill-Updater")
    parser.add_argument("--apply", action="store_true",
                       help="执行实际更新（默认 dry-run）")
    parser.add_argument("--dry-run", action="store_true", default=False,
                       help="dry-run 模式")
    parser.add_argument("--show-patch", action="store_true",
                       help="显示已保存的本地修改")
    parser.add_argument("--discard", action="store_true",
                       help="丢弃保存的本地修改（接受新版）")
    parser.add_argument("--skill", metavar="SLUG",
                       help="指定要操作的 skill slug")
    args = parser.parse_args()

    if args.show_patch:
        cmd_show_patch(args.skill)
    elif args.discard:
        cmd_discard(args.skill)
    elif args.apply or args.dry_run:
        cmd_apply(args.skill, dry_run=not args.apply)
    else:
        cmd_dry_run(args.skill)
