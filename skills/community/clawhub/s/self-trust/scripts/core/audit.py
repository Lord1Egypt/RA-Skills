# -*- coding: utf-8 -*-
"""审计区仅追加写入（设计文档 §10.1 / 公式 F8）。

- 落点：<data-dir>/audit/<log_name>.jsonl，每行一条 JSON（仅追加，不提供删除/改写接口）。
- 撤回/覆写以「追加反向记录」表达，绝不抹除原记录。
- 关键失败显式抛错不吞（规范 #8）。
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

from . import crypto as crypto_io

AUDIT_SUBDIR = "audit"

# 合法审计日志名（§10.1 五类 + 契约重建事件复用 override_log）
VALID_LOGS = frozenset({
    "approval_log", "appeal_log", "override_log", "reward_log", "monthly_history",
})


def audit_dir(data_dir: Path) -> Path:
    return Path(data_dir) / AUDIT_SUBDIR


def log_path(data_dir: Path, log_name: str) -> Path:
    if log_name not in VALID_LOGS:
        raise ValueError(f"未知审计日志: {log_name}（合法值: {sorted(VALID_LOGS)}）")
    return audit_dir(data_dir) / f"{log_name}.jsonl"


def now_iso(today: date | None = None) -> str:
    """审计时间戳（M1/N4）：逻辑重放时间 today（可被测试/重放覆盖）。

    - 真实运行（today 为 None，或 today 即真实今日）：保留真实墙钟时刻；
    - 重放（today 为显式指定且 ≠ 真实今日）：时间部分固定为午夜 00:00:00，
      使同一 today 的审计链在多次重放间秒级可复现（避免 datetime.now() 漂移，N4）。
    """
    base = today or date.today()
    # N4：仅当 today 为显式重放日期（≠ 真实今日）时锁定时间，保证可复现；
    #     真实运行仍用墙钟，保留真实发生时刻。
    t = (datetime.min.time()
         if (today is not None and today != date.today())
         else datetime.now().time())
    return datetime.combine(base, t).isoformat(timespec="seconds")


def _locked_append(path: Path, line: str) -> None:
    """跨平台追加一行并加文件锁，避免多进程并发写审计 jsonl 时行交错损坏（M7）。

    - Unix：fcntl.flock 整文件排他锁；
    - Windows：msvcrt.locking 锁文件首字节作为互斥（Windows 不保证 O_APPEND 原子性）。
    锁不可用时退化为无锁追加（单进程场景安全）。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a+b") as f:
        locked = False
        try:
            if sys.platform == "win32":
                import msvcrt
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            locked = True
        except (ImportError, OSError):
            locked = False
        try:
            f.seek(0, 2)  # 末尾追加
            f.write((line + "\n").encode("utf-8"))
        finally:
            if locked:
                try:
                    if sys.platform == "win32":
                        import msvcrt
                        f.seek(0)
                        msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                    else:
                        import fcntl
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                except (ImportError, OSError):
                    pass


def _atomic_write_bytes(path: Path, blob: bytes) -> None:
    """加密日志整文件原子写（tmp + replace），写后回读校验防静默写坏。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".jsonl.tmp")
    with open(tmp, "wb") as f:
        f.write(blob)
    os.replace(tmp, path)
    # CQ-1：写后回读校验，确保落盘字节与写入一致（防半截写/静默写坏）
    if path.read_bytes() != blob:
        raise IOError(f"审计日志写回校验失败: {path}")


def _append_encrypted(path: Path, line: str) -> None:
    """加密日志追加：读解密 → 追加行 → 重加密整文件写回（个人单机场景可接受）。"""
    existing = ""
    if path.is_file():
        raw = path.read_bytes()
        if crypto_io.is_encrypted(raw):
            existing = crypto_io.unseal(raw).decode("utf-8")
        else:
            existing = raw.decode("utf-8")   # 明文转加密（如刚开启加密的存量日志）
    text = (existing + "\n" + line) if existing.strip() else line
    _atomic_write_bytes(path, crypto_io.seal(text.encode("utf-8")))


def append(data_dir: Path, log_name: str, record: dict[str, Any]) -> Path:
    """仅追加一条审计记录。record 必须是可 JSON 序列化 dict。

    透明加密：审计加密标志开启（契约 crypto.enabled）→ 整文件加密追加；
    若日志已加密则解密追加后重加密；否则明文追加（沿用原文件锁逻辑）。
    """
    if not isinstance(record, dict):
        raise TypeError(f"审计记录必须为 dict，得到 {type(record).__name__}")
    path = log_path(data_dir, log_name)
    line = json.dumps(record, ensure_ascii=False)
    if crypto_io._audit_encrypted or (
            path.is_file() and crypto_io.is_encrypted(path.read_bytes())):
        if not crypto_io.have_session():
            raise crypto_io.CryptoError(
                "审计日志已启用加密，追加需密钥材料：--pass / --key-file 或对应环境变量")
        _append_encrypted(path, line)
    else:
        _locked_append(path, line)
    return path


def read_all(data_dir: Path, log_name: str) -> list[dict[str, Any]]:
    """只读全量读取（记账日志 查询用）；文件不存在返回空列表。

    透明解密：日志为加密格式（crypto.is_encrypted）→ 解密后逐行解析；
    否则明文逐行解析（向后兼容）。
    """
    path = log_path(data_dir, log_name)
    if not path.is_file():
        return []
    raw = path.read_bytes()
    if crypto_io.is_encrypted(raw):
        text = crypto_io.unseal(raw).decode("utf-8")
    else:
        text = raw.decode("utf-8")
    records: list[dict[str, Any]] = []
    for i, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            # L9：损坏行（如崩溃时的半截写入）跳过而非抛错，避免前序已读记录全部丢失；
            # 仅追加日志的健壮性优先于严格性，关键失败仍由调用方业务逻辑暴露。
            continue
    return records


def append_approval_snapshot(data_dir: Path, snapshot: dict[str, Any]) -> Path:
    """F8 审批快照落盘（结构由 formulas.f8_audit_snapshot 组装校验）。"""
    for key in ("time", "amount", "category", "scene", "inputs",
                "formulas_used", "decision"):
        if key not in snapshot:
            raise ValueError(f"F8 快照缺少必备键: {key}")
    return append(data_dir, "approval_log", snapshot)
