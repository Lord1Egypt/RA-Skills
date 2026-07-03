#!/usr/bin/env python3
"""
progress.py - 同步进度文件管理

写入 vault 插件目录下的 progress.json，供 Agent 在后台同步时轮询查看进度，
避免前台阻塞等待导致进程被超时杀掉。

progress.json 结构：
{
  "status": "running" | "completed" | "error" | "interrupted",
  "pid": 12345,
  "mode": "incremental",
  "started_at": "2026-06-24T19:00:00+08:00",
  "updated_at": "2026-06-24T19:01:23+08:00",
  "finished_at": "" | "2026-06-24T19:03:00+08:00",
  "total": 64,                  # 本次需处理的文档/文件总数（扫描后确定）
  "done": 30,                   # 已处理数（含成功+跳过+失败）
  "current": "公众号/xxx.md",   # 当前正在处理的文件
  "stats": {...},               # 实时统计（与报告一致）
  "recent_errors": [            # 最近若干条失败记录
    {"rel_path": "...", "error": "...", "retries": 3}
  ],
  "message": ""                 # 人类可读的当前状态描述
}
仅依赖标准库。
"""

import json
import os
from datetime import datetime, timezone, timedelta

PROGRESS_FILE = "progress.json"
PLUGIN_DIR = "sync-obsidian-to-lexiang"

_TZ = timezone(timedelta(hours=8))


def _now_iso():
    return datetime.now(_TZ).isoformat(timespec="seconds")


def get_progress_path(vault_path):
    return os.path.join(vault_path, ".obsidian", "plugins", PLUGIN_DIR, PROGRESS_FILE)


class ProgressWriter:
    """同步进度写入器。do_sync 持有它，关键节点调用 update()。"""

    def __init__(self, vault_path, mode, total=0, enabled=True):
        self.path = get_progress_path(vault_path)
        self.enabled = enabled
        self.state = {
            "status": "running",
            "pid": os.getpid(),
            "mode": mode,
            "started_at": _now_iso(),
            "updated_at": _now_iso(),
            "finished_at": "",
            "total": total,
            "done": 0,
            "current": "",
            "stats": {},
            "recent_errors": [],
            "message": "正在初始化…",
        }
        self._flush()

    def _flush(self):
        if not self.enabled:
            return
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            tmp = self.path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
            os.replace(tmp, self.path)  # 原子写，避免读到半截
        except OSError:
            pass

    def set_total(self, total):
        self.state["total"] = total
        self.state["updated_at"] = _now_iso()
        self._flush()

    def tick(self, current="", stats=None, message=None, done_delta=1):
        """处理完一项后调用：done 自增，刷新当前项与统计。"""
        self.state["done"] += done_delta
        if current:
            self.state["current"] = current
        if stats is not None:
            self.state["stats"] = dict(stats)
        if message is not None:
            self.state["message"] = message
        self.state["updated_at"] = _now_iso()
        self._flush()

    def note(self, current="", message=None, stats=None):
        """仅刷新当前项/消息，不推进 done（用于开始处理某项时）。"""
        if current:
            self.state["current"] = current
        if message is not None:
            self.state["message"] = message
        if stats is not None:
            self.state["stats"] = dict(stats)
        self.state["updated_at"] = _now_iso()
        self._flush()

    def record_error(self, rel_path, error, retries=0):
        self.state["recent_errors"].append({
            "rel_path": rel_path, "error": str(error)[:200], "retries": retries,
        })
        # 只保留最近 20 条
        self.state["recent_errors"] = self.state["recent_errors"][-20:]
        self.state["updated_at"] = _now_iso()
        self._flush()

    def finish(self, status="completed", stats=None, message=None):
        self.state["status"] = status
        self.state["finished_at"] = _now_iso()
        self.state["updated_at"] = _now_iso()
        if stats is not None:
            self.state["stats"] = dict(stats)
        if message is not None:
            self.state["message"] = message
        self._flush()


def read_progress(vault_path):
    """读取当前进度文件，返回 dict；不存在返回 None。"""
    path = get_progress_path(vault_path)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
