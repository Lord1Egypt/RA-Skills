"""
backup.py — 目标技能目录 ZIP 备份与恢复

在修改目标技能前创建完整 ZIP 备份（时间戳命名），修改后支持回滚。
ZIP 格式避免备份目录被 Skill 扫描器识别为重复技能条目。

时间线集成：backup_skill() 自动记录 [START] 和 [END] marker。
"""
import os
import io
import re
import zipfile
import subprocess
import sys
from datetime import datetime

# 时间线输出 + 流程钩子
_TIMELINE_SCRIPT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "timeline.py"
))
_HOOKS_SCRIPT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "hooks.py"
))
def _tl(skill_dir: str, *args):
    """调用 timeline.py 记录 marker"""
    try:
        subprocess.run(
            [sys.executable, _TIMELINE_SCRIPT, "mark", skill_dir] + list(args),
            capture_output=True, timeout=10,
        )
    except Exception:
        pass


# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-function-test/data/"

SKILL_DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."
))
_data_dir_abs = os.path.normpath(os.path.join(
    SKILL_DIR, "..", ".standardization", "skill-function-test", "data"
))
_BACKUP_DIR = os.path.join(_data_dir_abs, "backup")
_ZIP_EXT = ".zip"


def _ensure_backup_dir():
    os.makedirs(_BACKUP_DIR, exist_ok=True)


def _walk_skill(skill_dir: str):
    """遍历技能目录，返回 (arcname, filepath) 生成器，排除缓存/版本控制文件"""
    skip_prefixes = {"__pycache__", ".git", "__MACOSX"}
    skip_suffixes = {".pyc", ".DS_Store", ".bak"}
    for root, dirs, files in os.walk(skill_dir):
        # 跳过排除目录
        dirs[:] = [d for d in dirs if d not in skip_prefixes]
        rel = os.path.relpath(root, skill_dir)
        for f in files:
            if any(f.endswith(s) for s in skip_suffixes):
                continue
            arcname = os.path.join(rel, f) if rel != "." else f
            yield arcname, os.path.join(root, f)


def backup_skill(skill_dir: str, label: str = "pre_test") -> str:
    """
    备份目标技能目录为 ZIP 文件
    返回备份路径（.zip）
    备份名: <skill-name>_<label>_<timestamp>.zip
    """
    _tl(skill_dir, "backup", f"备份: {os.path.basename(skill_dir)}", "--type", "py_script")
    _ensure_backup_dir()
    skill_name = os.path.basename(skill_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{skill_name}_{label}_{timestamp}{_ZIP_EXT}"
    backup_path = os.path.join(_BACKUP_DIR, backup_name)

    if not os.path.exists(skill_dir):
        _tl(skill_dir, "backup", f"备份失败: 目录不存在", "end", "--type", "py_script", "--detail", "目录不存在")
        raise FileNotFoundError(f"目标目录不存在: {skill_dir}")

    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for arcname, filepath in _walk_skill(skill_dir):
            zf.write(filepath, arcname)

    _tl(skill_dir, "backup", f"备份完成: {backup_name}", "end", "--type", "py_script", "--detail", backup_path)
    print(f"  [BACKUP] 已备份: {skill_dir} → {backup_path}")
    return backup_path


def list_backups(skill_dir: str = None) -> list[dict]:
    """列出所有 ZIP 备份（兼顾旧版目录备份兼容显示）"""
    _ensure_backup_dir()
    backups = []
    for name in sorted(os.listdir(_BACKUP_DIR), reverse=True):
        path = os.path.join(_BACKUP_DIR, name)

        # ZIP 格式
        if name.endswith(_ZIP_EXT) and os.path.isfile(path):
            try:
                with zipfile.ZipFile(path, "r") as zf:
                    size = sum(
                        zinfo.file_size for zinfo in zf.filelist
                    )
            except (zipfile.BadZipFile, OSError):
                size = os.path.getsize(path)
            mod_time = datetime.fromtimestamp(os.path.getmtime(path))
            backups.append({
                "name": name,
                "path": path,
                "size_bytes": size,
                "modified": mod_time.isoformat(),
            })
            continue

        # 旧版目录备份（过渡兼容，不再新建）
        if os.path.isdir(path):
            size = sum(os.path.getsize(os.path.join(dp, f))
                       for dp, _, fn in os.walk(path) for f in fn)
            mod_time = datetime.fromtimestamp(os.path.getmtime(path))
            backups.append({
                "name": name,
                "path": path,
                "size_bytes": size,
                "modified": mod_time.isoformat(),
            })

    return backups


def _infer_skill_name(backup_name: str) -> str:
    """从备份名推断技能名称：取第一个 _ 之前的部分"""
    return backup_name.split("_")[0]


def restore_backup(backup_path: str, target_dir: str = None) -> bool:
    """从 ZIP 备份恢复（兼容旧版目录备份）"""
    if not os.path.exists(backup_path):
        print(f"  [BACKUP] 备份不存在: {backup_path}")
        return False

    if target_dir is None:
        skill_name = _infer_skill_name(os.path.basename(backup_path))
        target_dir = os.path.normpath(
            os.path.join(_BACKUP_DIR, "..", skill_name)
        )

    # 删除当前目录
    if os.path.exists(target_dir):
        import shutil
        shutil.rmtree(target_dir)

    if backup_path.endswith(_ZIP_EXT):
        # ZIP 恢复
        os.makedirs(target_dir, exist_ok=True)
        with zipfile.ZipFile(backup_path, "r") as zf:
            zf.extractall(target_dir)
    else:
        # 旧版目录备份恢复
        import shutil
        shutil.copytree(
            backup_path, target_dir,
            ignore=shutil.ignore_patterns("__pycache__", ".git", "*.pyc",
                                           ".DS_Store", "*.zip")
        )

    print(f"  [BACKUP] 已恢复: {backup_path} → {target_dir}")
    return True


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        if sys.argv[1] == "backup":
            skill_dir = sys.argv[2]
            subprocess.run([sys.executable, _HOOKS_SCRIPT, "check", skill_dir, "backup"])
            backup_skill(skill_dir, sys.argv[3] if len(sys.argv) > 3 else "manual")
            subprocess.run([sys.executable, _HOOKS_SCRIPT, "done", skill_dir, "backup"])
        elif sys.argv[1] == "list":
            blist = list_backups()
            for b in blist:
                print(f"  {b['name']}  ({b['size_bytes']} bytes, {b['modified']})")
        elif sys.argv[1] == "restore" and len(sys.argv) >= 3:
            restore_backup(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    else:
        print("用法: python backup.py backup|list|restore <path> [label]")
