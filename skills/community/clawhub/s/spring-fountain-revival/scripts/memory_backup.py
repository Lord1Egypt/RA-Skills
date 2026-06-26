#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QClaw 记忆生存系统 - 核心备份引擎
功能：
  1. 扫描所有记忆文件
  2. 本地隐藏备份（带时间戳快照）
  3. 云端同步目录同步
  4. 完整性校验
  5. 时间点还原
"""

import os
import sys
import json
import shutil
import hashlib
import zipfile
from datetime import datetime
from pathlib import Path

# ─── 路径配置 ───────────────────────────────────────────────
HOME            = Path.home()
WORKSPACE       = HOME / ".qclaw" / "workspace"
LOCAL_BACKUP    = HOME / ".qclaw" / ".memory_backup"   # 本地隐藏备份
CLOUD_SYNC_DIR  = Path(r"C:\Users\Administrator\Desktop\QC百度同步\QClaw记忆备份")  # 云端同步目录（百度网盘同步）
SNAPSHOTS_DIR   = LOCAL_BACKUP / "snapshots"           # 时间点快照
LATEST_DIR      = LOCAL_BACKUP / "latest"              # 最新备份（快速恢复用）
RESTORE_TOOL    = HOME / "Desktop" / "QClaw一键还原.bat"
MANIFEST_FILE   = WORKSPACE / "memory_manifest.json"

# ─── 记忆文件列表（硬编码 + 清单双重保障）──────────────────
MEMORY_FILES = [
    WORKSPACE / "MEMORY.md",
    WORKSPACE / "USER.md",
    WORKSPACE / "IDENTITY.md",
    WORKSPACE / "AGENTS.md",
    WORKSPACE / "SOUL.md",
    WORKSPACE / "HEARTBEAT.md",
    WORKSPACE / "TOOLS.md",
    WORKSPACE / "memory_manifest.json",
]
MEMORY_DIRS = [
    WORKSPACE / "diary",
    WORKSPACE / "memory",
]

def ensure_dirs():
    for d in [LOCAL_BACKUP, SNAPSHOTS_DIR, LATEST_DIR, CLOUD_SYNC_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def file_hash(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def collect_all_files():
    """收集所有记忆文件（文件 + 目录内文件）"""
    files = []
    for f in MEMORY_FILES:
        if f.exists():
            files.append(f)
    for d in MEMORY_DIRS:
        if d.exists():
            for f in d.rglob("*"):
                if f.is_file():
                    files.append(f)
    return files

def backup_to_latest():
    """备份到 latest 目录（覆盖式，始终是最新状态）"""
    ensure_dirs()
    copied = 0
    for src in collect_all_files():
        rel = src.relative_to(HOME / ".qclaw" / "workspace")
        dst = LATEST_DIR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1
    return copied

def create_snapshot(label="auto"):
    """创建带时间戳的快照 zip"""
    ensure_dirs()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    snap_name = f"snapshot_{ts}_{label}.zip"
    snap_path = SNAPSHOTS_DIR / snap_name

    files = collect_all_files()
    with zipfile.ZipFile(snap_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for src in files:
            rel = src.relative_to(HOME / ".qclaw" / "workspace")
            zf.write(src, str(rel))
        # 写入快照元数据
        meta = {
            "timestamp": datetime.now().isoformat(),
            "label": label,
            "file_count": len(files),
            "files": [str(f.relative_to(HOME / ".qclaw" / "workspace")) for f in files]
        }
        zf.writestr("_snapshot_meta.json", json.dumps(meta, ensure_ascii=False, indent=2))

    size_kb = snap_path.stat().st_size // 1024
    print(f"[OK] 快照已创建: {snap_name} ({size_kb} KB, {len(files)} 个文件)")
    return snap_path

def sync_to_cloud():
    """同步到云端目录"""
    ensure_dirs()
    CLOUD_SYNC_DIR.mkdir(parents=True, exist_ok=True)

    # 同步 latest 到云端
    synced = 0
    for src in (LATEST_DIR).rglob("*"):
        if src.is_file():
            rel = src.relative_to(LATEST_DIR)
            dst = CLOUD_SYNC_DIR / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists() or file_hash(src) != file_hash(dst):
                shutil.copy2(src, dst)
                synced += 1

    # 同步最新快照到云端
    snaps = sorted(SNAPSHOTS_DIR.glob("snapshot_*.zip"), reverse=True)
    if snaps:
        latest_snap = snaps[0]
        cloud_snap = CLOUD_SYNC_DIR / "snapshots" / latest_snap.name
        cloud_snap.parent.mkdir(parents=True, exist_ok=True)
        if not cloud_snap.exists():
            shutil.copy2(latest_snap, cloud_snap)
            synced += 1

    # 同步还原工具到云端
    if RESTORE_TOOL.exists():
        cloud_tool = CLOUD_SYNC_DIR / RESTORE_TOOL.name
        shutil.copy2(RESTORE_TOOL, cloud_tool)

    print(f"[OK] 云端同步完成: {synced} 个文件已更新 -> {CLOUD_SYNC_DIR}")
    return synced

def list_snapshots():
    """列出所有可用快照"""
    snaps = sorted(SNAPSHOTS_DIR.glob("snapshot_*.zip"), reverse=True)
    if not snaps:
        print("[INFO] 暂无快照")
        return []
    result = []
    for i, s in enumerate(snaps):
        size_kb = s.stat().st_size // 1024
        # 解析时间戳
        parts = s.stem.split("_")
        if len(parts) >= 3:
            ts_str = f"{parts[1][:4]}-{parts[1][4:6]}-{parts[1][6:]} {parts[2][:2]}:{parts[2][2:4]}:{parts[2][4:]}"
        else:
            ts_str = s.stem
        label = "_".join(parts[3:]) if len(parts) > 3 else "auto"
        result.append({"index": i, "name": s.name, "time": ts_str, "label": label, "size_kb": size_kb, "path": str(s)})
    return result

def restore_from_snapshot(snap_path: Path, dry_run=False):
    """从快照还原"""
    if not snap_path.exists():
        print(f"[ERROR] 快照不存在: {snap_path}")
        return False

    target = WORKSPACE
    with zipfile.ZipFile(snap_path, "r") as zf:
        names = [n for n in zf.namelist() if not n.startswith("_snapshot")]
        if dry_run:
            print(f"[DRY-RUN] 将还原 {len(names)} 个文件到 {target}")
            for n in names[:10]:
                print(f"  {n}")
            if len(names) > 10:
                print(f"  ... 共 {len(names)} 个")
            return True
        for name in names:
            dst = target / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(name) as src_f, open(dst, "wb") as dst_f:
                dst_f.write(src_f.read())

    print(f"[OK] 还原完成: {len(names)} 个文件已恢复到 {target}")
    return True

def restore_from_latest():
    """从 latest 快速还原"""
    if not LATEST_DIR.exists():
        print("[ERROR] 本地备份不存在，请尝试从云端恢复")
        return False
    files = list(LATEST_DIR.rglob("*"))
    files = [f for f in files if f.is_file()]
    for src in files:
        rel = src.relative_to(LATEST_DIR)
        dst = WORKSPACE / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    print(f"[OK] 快速还原完成: {len(files)} 个文件")
    return True

def integrity_check():
    """完整性校验：比对工作区 vs 本地备份"""
    issues = []
    for src in collect_all_files():
        rel = src.relative_to(WORKSPACE)
        bak = LATEST_DIR / rel
        if not bak.exists():
            issues.append(f"备份缺失: {rel}")
        elif file_hash(src) != file_hash(bak):
            issues.append(f"内容不一致: {rel}")
    # 检查备份中有但工作区没有的
    if LATEST_DIR.exists():
        for bak in LATEST_DIR.rglob("*"):
            if bak.is_file():
                rel = bak.relative_to(LATEST_DIR)
                src = WORKSPACE / rel
                if not src.exists():
                    issues.append(f"工作区缺失（可还原）: {rel}")
    return issues

def full_backup(label="manual"):
    """完整备份流程：latest + 快照 + 云端同步"""
    print("=" * 50)
    print(f"QClaw 记忆备份 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
    print("=" * 50)
    n = backup_to_latest()
    print(f"[OK] 本地备份: {n} 个文件 -> {LATEST_DIR}")
    snap = create_snapshot(label)
    sync_to_cloud()
    print("=" * 50)
    print("备份完成！三重保障已就绪。")
    return snap

# ─── CLI ────────────────────────────────────────────────────
def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "backup":
        label = sys.argv[2] if len(sys.argv) > 2 else "manual"
        full_backup(label)

    elif cmd == "snapshot":
        label = sys.argv[2] if len(sys.argv) > 2 else "manual"
        create_snapshot(label)

    elif cmd == "sync":
        sync_to_cloud()

    elif cmd == "list":
        snaps = list_snapshots()
        if snaps:
            print(f"\n可用快照 ({len(snaps)} 个):\n")
            for s in snaps:
                print(f"  [{s['index']}] {s['time']}  标签:{s['label']}  大小:{s['size_kb']}KB")
                print(f"       {s['name']}")

    elif cmd == "restore":
        if len(sys.argv) < 3:
            # 交互式选择
            snaps = list_snapshots()
            if not snaps:
                print("无可用快照，尝试从 latest 还原...")
                restore_from_latest()
                return
            print(f"\n可用快照 ({len(snaps)} 个):\n")
            for s in snaps:
                print(f"  [{s['index']}] {s['time']}  标签:{s['label']}  大小:{s['size_kb']}KB")
            print(f"\n输入序号还原（直接回车=还原最新）: ", end="")
            choice = input().strip()
            idx = int(choice) if choice.isdigit() else 0
            snap = snaps[idx]
            print(f"\n将还原到: {snap['time']} ({snap['label']})")
            print("确认？(y/n): ", end="")
            if input().strip().lower() == "y":
                restore_from_snapshot(Path(snap["path"]))
        elif sys.argv[2] == "latest":
            restore_from_latest()
        else:
            restore_from_snapshot(Path(sys.argv[2]))

    elif cmd == "check":
        print("正在检查完整性...")
        issues = integrity_check()
        if issues:
            print(f"\n发现 {len(issues)} 个问题:")
            for i in issues:
                print(f"  ! {i}")
            print("\n建议运行: python memory_backup.py backup")
        else:
            print("[OK] 所有记忆文件完整一致")

    elif cmd == "auto":
        # 自动备份（由定时任务调用）
        full_backup("auto")

    else:
        print("QClaw 记忆生存系统 - 备份引擎")
        print("\n用法: python memory_backup.py <命令>")
        print("\n命令:")
        print("  backup [标签]   完整备份（本地+快照+云端）")
        print("  snapshot [标签] 仅创建快照")
        print("  sync            同步到云端目录")
        print("  list            列出所有快照")
        print("  restore [序号]  还原到指定时间点（交互式）")
        print("  restore latest  快速还原最新备份")
        print("  check           完整性校验")
        print(f"\n本地备份: {LOCAL_BACKUP}")
        print(f"云端目录: {CLOUD_SYNC_DIR}")

if __name__ == "__main__":
    main()
