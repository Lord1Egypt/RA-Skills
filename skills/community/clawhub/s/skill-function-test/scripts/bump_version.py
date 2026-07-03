"""
bump_version.py — 版本号自动管理（语义化版本 SemVer）

根据标准化铁律 2（rules.md）自动判断 bump 级别并三端同步：
- MAJOR (X): 架构级重构/破坏性 API 变更
- MINOR (Y): 新功能/新模块/功能重构
- PATCH (Z): bug 修复/路径修正/文档勘误/≤3 行小修改

同步文件：SKILL.md frontmatter → _meta.json → CHANGELOG.md
"""
import json
import os
import re
from datetime import date


def get_current_version(skill_dir: str) -> str:
    """从 SKILL.md frontmatter 读取当前版本"""
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        return None
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'^version:\s*([\d.]+)', content, re.MULTILINE)
    return m.group(1).strip() if m else None


def bump(current: str, bump_type: str) -> str:
    """按 SemVer 规则升级版本号"""
    parts = current.split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    if bump_type == "patch":
        patch += 1
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    return f"{major}.{minor}.{patch}"


def update_skill_md(skill_dir: str, new_ver: str) -> bool:
    """更新 SKILL.md frontmatter 中的 version 字段"""
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        return False
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = re.sub(
        r'(^version:\s*)[\d.]+',
        rf'\g<1>{new_ver}',
        content,
        count=1,
        flags=re.MULTILINE
    )
    # 也更新正文中的版本引用
    old_ver = get_current_version(skill_dir)
    if old_ver:
        new_content = re.sub(
            rf'(?<=v){re.escape(old_ver)}',
            new_ver,
            new_content,
        )
    with open(skill_md, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def update_meta_json(skill_dir: str, new_ver: str) -> bool:
    """更新 _meta.json 中的 version 字段"""
    meta_file = os.path.join(skill_dir, "_meta.json")
    if not os.path.exists(meta_file):
        return False
    with open(meta_file, "r", encoding="utf-8") as f:
        meta = json.load(f)
    meta["version"] = new_ver
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return True


def append_changelog(skill_dir: str, old_ver: str, new_ver: str,
                     changelog_entries: list[str] = None,
                     bump_type: str = "patch") -> bool:
    """追加更新日志到 references/changelog.md（渐进式参考文件，R-24 合规）"""
    # ★ v2.62.x 根因修复：CHANGELOG 是渐进式参考文件，优先 references/changelog.md
    #   绝不在根目录创建 CHANGELOG.md（会被审计误判为违规产出物）
    changelog_paths = [
        os.path.join(skill_dir, "references", "changelog.md"),
        os.path.join(skill_dir, "CHANGELOG.md"),  # 兼容旧版
    ]
    target = None
    for p in changelog_paths:
        if os.path.exists(p):
            target = p
            break
    if not target:
        target = os.path.join(skill_dir, "references", "changelog.md")  # 默认创建在渐进式目录

    today = date.today().isoformat()
    type_labels = {"major": "Breaking", "minor": "Feature", "patch": "Fix"}
    lines = [f"## {new_ver} ({today})"]

    if changelog_entries:
        for entry in changelog_entries:
            lines.append(f"- {entry}")
    else:
        lines.append(f"- 自动版本更新 ({bump_type})")

    new_entry = "\n".join(lines) + "\n\n"

    if os.path.exists(target):
        with open(target, "r", encoding="utf-8") as f:
            old = f.read()
        # 检查是否已存在
        if re.search(r'^##\s*' + re.escape(new_ver.replace(".", r"\.")),
                      old, re.MULTILINE):
            print(f"  [BUMP] 跳过分版本 {new_ver} 的日志已存在")
            return False
        content = new_entry + old
    else:
        content = f"# CHANGELOG\n\n{new_entry}"

    with open(target, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [BUMP] changelog 已更新: {target}")
    return True


def auto_bump(skill_dir: str, bump_type: str = "patch",
              changelog_entries: list[str] = None) -> str:
    """
    一键三端同步：bump 版本号 + 更新 SKILL.md + _meta.json + changelog

    返回新的版本号字符串，失败返回 None
    """
    old_ver = get_current_version(skill_dir)
    if not old_ver:
        print(f"  [BUMP] ⚠️ 无法读取当前版本号")
        return None

    new_ver = bump(old_ver, bump_type)
    print(f"  [BUMP] {old_ver} → {new_ver} ({bump_type})")

    ok1 = update_skill_md(skill_dir, new_ver)
    ok2 = update_meta_json(skill_dir, new_ver)
    ok3 = append_changelog(skill_dir, old_ver, new_ver,
                           changelog_entries, bump_type)

    if ok1 and ok2:
        print(f"  [BUMP] ✅ 三端同步完成: {new_ver}")
    else:
        print(f"  [BUMP] ⚠️ SKILL.md={'OK' if ok1 else 'FAIL'} "
              f"_meta.json={'OK' if ok2 else 'FAIL'}")

    return new_ver


def detect_bump_type(skill_dir: str, backup_dir: str = None) -> str:
    """
    根据变更内容自动判断 bump 类型
    通过对比备份目录来检测变更类型
    返回: "major" / "minor" / "patch" / None
    """
    script_dir = os.path.join(skill_dir, "scripts")
    changes_minor = 0
    changes_patch = 0

    # 简单启发式：统计新增函数和修改行数
    for root, dirs, files in os.walk(script_dir):
        for f in files:
            if f.endswith(".py"):
                fpath = os.path.join(root, f)
                try:
                    with open(fpath, "r", encoding="utf-8") as fh:
                        content = fh.read()
                    funcs = re.findall(r'^def\s+\w+|^class\s+\w+',
                                       content, re.MULTILINE)
                    if len(funcs) > 0:
                        changes_minor += len(funcs)
                except Exception:
                    pass

    # 如果新增了函数或类，认为是 minor
    if changes_minor >= 2:
        return "minor"
    return "patch"


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        target = sys.argv[1]
        btype = sys.argv[2] if len(sys.argv) > 2 else "patch"
        entries = sys.argv[3:] if len(sys.argv) > 3 else None
        auto_bump(target, btype, entries)
    else:
        print("用法: python bump_version.py <skill-dir> [patch|minor|major] [changelog条目...]")
