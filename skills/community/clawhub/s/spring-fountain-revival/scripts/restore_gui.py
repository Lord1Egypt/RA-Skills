#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QClaw 一键还原工具 - 图形界面
双击即可运行，无需命令行
"""

import os
import sys
import json
import shutil
import zipfile
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from pathlib import Path
import threading
import subprocess

# ─── 路径配置（与 memory_backup.py 保持一致）──────────────
HOME           = Path.home()
WORKSPACE      = HOME / ".qclaw" / "workspace"
LOCAL_BACKUP   = HOME / ".qclaw" / ".memory_backup"
CLOUD_SYNC_DIR = Path(r"C:\Users\Administrator\Desktop\QC百度同步\QClaw记忆备份")
SNAPSHOTS_DIR  = LOCAL_BACKUP / "snapshots"
LATEST_DIR     = LOCAL_BACKUP / "latest"
SCRIPTS_DIR    = WORKSPACE / "scripts"

# ─── 颜色主题 ─────────────────────────────────────────────
BG       = "#1a1a2e"
BG2      = "#16213e"
BG3      = "#0f3460"
ACCENT   = "#e94560"
GREEN    = "#00b894"
YELLOW   = "#fdcb6e"
TEXT     = "#eaeaea"
TEXT_DIM = "#888888"

def file_hash(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def list_snapshots():
    snaps = []
    if SNAPSHOTS_DIR.exists():
        snaps = sorted(SNAPSHOTS_DIR.glob("snapshot_*.zip"), reverse=True)
    # 也检查云端快照
    cloud_snaps_dir = CLOUD_SYNC_DIR / "snapshots"
    if cloud_snaps_dir.exists():
        for s in sorted(cloud_snaps_dir.glob("snapshot_*.zip"), reverse=True):
            if s.name not in [x.name for x in snaps]:
                snaps.append(s)
    result = []
    for s in snaps:
        parts = s.stem.split("_")
        try:
            ts_str = f"{parts[1][:4]}-{parts[1][4:6]}-{parts[1][6:]} {parts[2][:2]}:{parts[2][2:4]}:{parts[2][4:]}"
        except:
            ts_str = s.stem
        label = "_".join(parts[3:]) if len(parts) > 3 else "auto"
        source = "☁ 云端" if str(s).startswith(str(CLOUD_SYNC_DIR)) else "💾 本地"
        size_kb = s.stat().st_size // 1024
        result.append({
            "display": f"{source}  {ts_str}  [{label}]  {size_kb}KB",
            "time": ts_str,
            "label": label,
            "source": source,
            "path": str(s),
            "size_kb": size_kb
        })
    return result

def do_restore(snap_path_str, log_func):
    snap_path = Path(snap_path_str)
    if not snap_path.exists():
        log_func(f"[错误] 快照文件不存在: {snap_path}")
        return False
    try:
        with zipfile.ZipFile(snap_path, "r") as zf:
            names = [n for n in zf.namelist() if not n.startswith("_snapshot")]
            log_func(f"正在还原 {len(names)} 个文件...")
            for name in names:
                dst = WORKSPACE / name
                dst.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(name) as sf, open(dst, "wb") as df:
                    df.write(sf.read())
                log_func(f"  ✓ {name}")
        log_func(f"\n[完成] 成功还原 {len(names)} 个文件！")
        return True
    except Exception as e:
        log_func(f"[错误] 还原失败: {e}")
        return False

def do_backup(log_func):
    try:
        backup_py = SCRIPTS_DIR / "memory_backup.py"
        if not backup_py.exists():
            log_func("[错误] 备份引擎不存在，请重新安装")
            return False
        result = subprocess.run(
            [sys.executable, str(backup_py), "backup", "manual"],
            capture_output=True, text=True, encoding="utf-8"
        )
        for line in result.stdout.splitlines():
            log_func(line)
        if result.returncode == 0:
            log_func("\n[完成] 备份成功！")
            return True
        else:
            log_func(f"[错误] {result.stderr}")
            return False
    except Exception as e:
        log_func(f"[错误] {e}")
        return False

def do_check(log_func):
    issues = []
    log_func("正在检查记忆文件完整性...\n")
    memory_files = [
        WORKSPACE / "MEMORY.md",
        WORKSPACE / "USER.md",
        WORKSPACE / "IDENTITY.md",
        WORKSPACE / "AGENTS.md",
        WORKSPACE / "SOUL.md",
    ]
    for f in memory_files:
        exists = f.exists()
        bak = LATEST_DIR / f.relative_to(WORKSPACE)
        bak_exists = bak.exists()
        if exists and bak_exists:
            match = file_hash(f) == file_hash(bak)
            status = "✓ 一致" if match else "! 不一致"
            if not match:
                issues.append(str(f.name))
        elif exists and not bak_exists:
            status = "! 备份缺失"
            issues.append(str(f.name))
        elif not exists and bak_exists:
            status = "! 工作区缺失（可还原）"
            issues.append(str(f.name))
        else:
            status = "- 不存在"
        log_func(f"  {f.name:20s}  {status}")
    # 检查日记
    diary_dir = WORKSPACE / "diary"
    if diary_dir.exists():
        diary_files = list(diary_dir.glob("*.md"))
        log_func(f"\n  日记文件: {len(diary_files)} 个")
    snaps = list_snapshots()
    log_func(f"  可用快照: {len(snaps)} 个")
    if issues:
        log_func(f"\n[警告] 发现 {len(issues)} 个问题: {', '.join(issues)}")
        log_func("建议点击「立即备份」修复")
    else:
        log_func("\n[OK] 所有记忆文件完整！")
    return issues

# ─── GUI ──────────────────────────────────────────────────
class RestoreApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QClaw 记忆还原工具")
        self.geometry("780x600")
        self.resizable(True, True)
        self.configure(bg=BG)
        self.snapshots = []
        self._build_ui()
        self._refresh_snapshots()
        self._run_check()

    def _build_ui(self):
        # ── 标题栏 ──
        header = tk.Frame(self, bg=BG3, pady=12)
        header.pack(fill="x")
        tk.Label(header, text="🧠  QClaw 记忆还原工具",
                 font=("Microsoft YaHei", 16, "bold"),
                 bg=BG3, fg=TEXT).pack(side="left", padx=20)
        tk.Label(header, text="记忆永不丢失",
                 font=("Microsoft YaHei", 10),
                 bg=BG3, fg=TEXT_DIM).pack(side="left")

        # ── 主体分栏 ──
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=16, pady=12)

        # 左栏：快照列表
        left = tk.Frame(body, bg=BG2, bd=0)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(left, text="📦 可用快照（选择时间点）",
                 font=("Microsoft YaHei", 10, "bold"),
                 bg=BG2, fg=YELLOW).pack(anchor="w", padx=10, pady=(10, 4))

        list_frame = tk.Frame(left, bg=BG2)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.snap_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            bg=BG, fg=TEXT,
            selectbackground=BG3,
            selectforeground=ACCENT,
            font=("Consolas", 9),
            borderwidth=0,
            highlightthickness=1,
            highlightcolor=BG3,
            activestyle="none"
        )
        self.snap_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.snap_listbox.yview)

        # 右栏：操作区
        right = tk.Frame(body, bg=BG, width=220)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(right, text="⚡ 操作",
                 font=("Microsoft YaHei", 10, "bold"),
                 bg=BG, fg=YELLOW).pack(anchor="w", pady=(0, 8))

        btn_cfg = dict(font=("Microsoft YaHei", 10, "bold"),
                       width=18, pady=8, bd=0, cursor="hand2")

        tk.Button(right, text="🔄  还原选中快照",
                  bg=ACCENT, fg="white",
                  command=self._restore_selected,
                  **btn_cfg).pack(pady=4)

        tk.Button(right, text="⚡  还原最新备份",
                  bg=GREEN, fg="white",
                  command=self._restore_latest,
                  **btn_cfg).pack(pady=4)

        tk.Button(right, text="💾  立即备份",
                  bg=BG3, fg=TEXT,
                  command=self._do_backup,
                  **btn_cfg).pack(pady=4)

        tk.Button(right, text="🔍  检查完整性",
                  bg=BG3, fg=TEXT,
                  command=self._run_check,
                  **btn_cfg).pack(pady=4)

        tk.Button(right, text="🔃  刷新列表",
                  bg=BG3, fg=TEXT,
                  command=self._refresh_snapshots,
                  **btn_cfg).pack(pady=4)

        # 状态指示
        self.status_var = tk.StringVar(value="就绪")
        tk.Label(right, textvariable=self.status_var,
                 font=("Microsoft YaHei", 9),
                 bg=BG, fg=GREEN, wraplength=200,
                 justify="left").pack(pady=(16, 4), anchor="w")

        # ── 日志区 ──
        log_frame = tk.Frame(self, bg=BG2)
        log_frame.pack(fill="x", padx=16, pady=(0, 12))

        tk.Label(log_frame, text="📋 操作日志",
                 font=("Microsoft YaHei", 9, "bold"),
                 bg=BG2, fg=TEXT_DIM).pack(anchor="w", padx=10, pady=(6, 2))

        self.log_text = scrolledtext.ScrolledText(
            log_frame, height=8,
            bg=BG, fg=GREEN,
            font=("Consolas", 9),
            borderwidth=0,
            state="disabled"
        )
        self.log_text.pack(fill="x", padx=10, pady=(0, 8))

    def _log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        self.update_idletasks()

    def _refresh_snapshots(self):
        self.snapshots = list_snapshots()
        self.snap_listbox.delete(0, "end")
        if self.snapshots:
            for s in self.snapshots:
                self.snap_listbox.insert("end", s["display"])
            self.snap_listbox.selection_set(0)
        else:
            self.snap_listbox.insert("end", "  （暂无快照，请先备份）")
        self.status_var.set(f"共 {len(self.snapshots)} 个快照")

    def _run_check(self):
        def _check():
            self._log("\n── 完整性检查 ──")
            do_check(self._log)
        threading.Thread(target=_check, daemon=True).start()

    def _restore_selected(self):
        sel = self.snap_listbox.curselection()
        if not sel or not self.snapshots:
            messagebox.showwarning("提示", "请先选择一个快照")
            return
        snap = self.snapshots[sel[0]]
        if not messagebox.askyesno("确认还原",
            f"将还原到：\n{snap['time']}\n标签：{snap['label']}\n\n当前工作区文件将被覆盖，确认继续？"):
            return
        def _do():
            self._log(f"\n── 还原快照: {snap['time']} ──")
            self.status_var.set("还原中...")
            ok = do_restore(snap["path"], self._log)
            self.status_var.set("还原完成！" if ok else "还原失败")
            if ok:
                messagebox.showinfo("完成", "记忆还原成功！\n请重启 QClaw 使记忆生效。")
        threading.Thread(target=_do, daemon=True).start()

    def _restore_latest(self):
        if not LATEST_DIR.exists():
            messagebox.showerror("错误", "本地备份不存在\n请尝试从快照列表中选择云端快照还原")
            return
        if not messagebox.askyesno("确认还原", "将还原最新备份到工作区\n当前文件将被覆盖，确认继续？"):
            return
        def _do():
            self._log("\n── 还原最新备份 ──")
            self.status_var.set("还原中...")
            files = list(LATEST_DIR.rglob("*"))
            files = [f for f in files if f.is_file()]
            for src in files:
                rel = src.relative_to(LATEST_DIR)
                dst = WORKSPACE / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                self._log(f"  ✓ {rel}")
            self._log(f"\n[完成] 还原 {len(files)} 个文件")
            self.status_var.set("还原完成！")
            messagebox.showinfo("完成", "记忆还原成功！\n请重启 QClaw 使记忆生效。")
        threading.Thread(target=_do, daemon=True).start()

    def _do_backup(self):
        def _do():
            self._log("\n── 开始备份 ──")
            self.status_var.set("备份中...")
            ok = do_backup(self._log)
            self.status_var.set("备份完成！" if ok else "备份失败")
            if ok:
                self._refresh_snapshots()
        threading.Thread(target=_do, daemon=True).start()

if __name__ == "__main__":
    app = RestoreApp()
    app.mainloop()
