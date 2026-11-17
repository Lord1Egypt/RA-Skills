#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 工作空间跨盘迁移 —— 公共库

提供四个脚本共用的路径推导、文本改写、体积统计、数据库改名等能力。
本模块只读优先：所有写操作都由调用方显式触发。

关键事实（来自实测，Windows + WorkBuddy 2.x）：
  1. 工作空间本体 = 目录本身（含 .workbuddy/ 记忆与项目级 skills）
  2. 会话历史 = <APP>/projects/<slug>/，slug 由工作空间绝对路径派生
  3. 应用数据库 = <APP>/workbuddy.db 里的 workspaces / sessions / automations /
     workspace_trust_decisions 四张表
  4. 侧边栏显示名 = <APP>/workspace-display-names.json
"""

from __future__ import annotations

import ctypes
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------- 应用目录

def app_dir() -> Path:
    """WorkBuddy 用户数据目录，可用 WORKBUDDY_HOME 覆盖（便于测试）。"""
    env = os.environ.get("WORKBUDDY_HOME")
    if env:
        return Path(env).expanduser().resolve()
    return (Path.home() / ".workbuddy").resolve()


APP_ROOT = app_dir()
PROJECTS_DIR = APP_ROOT / "projects"
DISPLAY_NAMES = APP_ROOT / "workspace-display-names.json"
DB_PATH = APP_ROOT / "workbuddy.db"
STATE_ROOT = APP_ROOT / "workspace-migrations"


def now_ms() -> int:
    return int(time.time() * 1000)


def stamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def human_bytes(n: int) -> str:
    v = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if v < 1024 or unit == "TB":
            return f"{v:.1f} {unit}" if unit != "B" else f"{int(v)} B"
        v /= 1024.0
    return f"{n} B"


# ---------------------------------------------------------------- slug 与路径

def slug_for_path(path: str) -> str:
    """
    由工作空间绝对路径派生 projects 目录名。

    规则（实测）：盘符小写 + "-" + 各级路径用 "-" 连接；
    盘符冒号去掉，反斜杠/斜杠全部变 "-"，空格与中文、下划线、大小写原样保留。
      例：D:\\WorkBuddyWork\\2026-10-21-09-32-06
          -> d-WorkBuddyWork-2026-10-21-09-32-06
      例：D:\\workbuddy disk d\\2026-09-05-23-24-59
          -> d-workbuddy disk d-2026-09-05-23-24-59
    """
    p = os.path.abspath(path)
    drive, rest = os.path.splitdrive(p)
    drive_letter = drive.rstrip(":").lower()
    parts = [x for x in re.split(r"[\\/]+", rest) if x]
    if drive_letter:
        return "-".join([drive_letter] + parts)
    return "-".join(parts)  # POSIX 无盘符时退化为纯路径连接


def display_key(path: str) -> str:
    """workspace-display-names.json 的键：全小写 + 正斜杠。"""
    return os.path.abspath(path).replace("\\", "/").lower()


def normalize_path(path: str) -> str:
    """比较用归一化：去引号空白、统一正斜杠、全小写、去尾部斜杠。"""
    p = (path or "").strip().strip('"').strip("'")
    p = p.replace("\\", "/")
    while len(p) > 3 and p.endswith("/"):
        p = p[:-1]
    return p.lower()


def same_path(a: str, b: str) -> bool:
    return normalize_path(a) == normalize_path(b)


def to_style(path: str, like: str) -> str:
    """把 path 转成与 like 相同的分隔符风格。"""
    if "/" in like and "\\" not in like:
        return path.replace("\\", "/")
    return path.replace("/", "\\")


# ---------------------------------------------------------------- 文本改写

def build_path_regex(old: str) -> re.Pattern:
    """
    构造「工作空间路径」的匹配式：
      - 分隔符 \\ 与 / 任意混用均匹配
      - 大小写不敏感（Windows 路径不区分大小写）
      - 右侧边界收紧，避免把 D:\\a\\proj 误改到 D:\\a\\proj-old
    """
    core_parts = [p for p in re.split(r"[\\/]+", os.path.abspath(old)) if p]
    core = r"[\\/]+".join(re.escape(part) for part in core_parts)
    return re.compile(core + r"(?![0-9A-Za-z_.\-])", re.IGNORECASE)


def make_replacer(new: str):
    """
    按被匹配文本的分隔符风格生成替换值，重点处理 jsonl 里的转义形态：
      D:/Work/x      -> 正斜杠
      D:\\Work\\x    -> 单反斜杠（普通文本）
      D:\\\\Work\\\\x -> 双反斜杠（JSON 字符串里的转义），必须还原成转义形态，否则 JSON 会被写坏
    """
    def _repl(m: re.Match) -> str:
        matched = m.group(0)
        if "/" in matched and "\\" not in matched:
            return new.replace("\\", "/")
        if "\\\\" in matched:
            return new.replace("\\", "\\\\")
        return new.replace("/", "\\")
    return _repl


def rewrite_text(text: str, old: str, new: str) -> tuple[str, int]:
    """返回 (改写后文本, 命中次数)。"""
    pattern = build_path_regex(old)
    return pattern.subn(make_replacer(new), text)


def count_occurrences(text: str, old: str) -> int:
    return len(build_path_regex(old).findall(text))


# ---------------------------------------------------------------- 文件系统

def is_reparse_point(path: Path) -> bool:
    """Windows 目录联接/符号链接（os.path.islink 认不出 junction）。"""
    try:
        st = path.stat(follow_symlinks=False)
    except OSError:
        return False
    attrs = getattr(st, "st_file_attributes", 0)
    return bool(attrs & 0x400)  # FILE_ATTRIBUTE_REPARSE_POINT


def iter_files(root: Path, skip_reparse: bool = True):
    """遍历普通文件，跳过 junction / symlink。"""
    root = Path(root)
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        if skip_reparse:
            dirnames[:] = [d for d in dirnames if not is_reparse_point(Path(dirpath) / d)]
        for name in filenames:
            fp = Path(dirpath) / name
            if skip_reparse and is_reparse_point(fp):
                continue
            yield fp


def dir_stats(root: Path) -> dict:
    files = 0
    total = 0
    longest = 0
    longest_rel = ""
    for fp in iter_files(root):
        try:
            size = fp.stat().st_size
        except OSError:
            size = 0
        files += 1
        total += size
        rel = str(fp.relative_to(root))
        if len(rel) > longest:
            longest, longest_rel = len(rel), rel
    return {"files": files, "bytes": total, "longest_rel": longest, "longest_rel_path": longest_rel}


def md5_of(path: Path, chunk: int = 1 << 20) -> str:
    import hashlib
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            block = f.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def find_nested_workspaces(root: Path) -> list[str]:
    """找出工作空间内部「嵌着的」其他工作空间（含 .workbuddy 的子目录）。"""
    root = Path(root)
    found = []
    for dirpath, dirnames, _ in os.walk(root):
        cur = Path(dirpath)
        if cur == root:
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            continue
        if ".workbuddy" in [d.lower() for d in dirnames] or (cur / ".workbuddy").is_dir():
            found.append(str(cur))
            dirnames[:] = []  # 不再深入
    return found


def find_repo_markers(root: Path, limit: int = 40) -> list[str]:
    markers = {".git", "node_modules", ".venv", "venv", "__pycache__", ".nuxt", "dist", ".next"}
    hits = []
    for dirpath, dirnames, _ in os.walk(root):
        for d in list(dirnames):
            if d in markers:
                hits.append(str(Path(dirpath) / d))
                if len(hits) >= limit:
                    return hits
    return hits


# ---------------------------------------------------------------- 卷信息

def get_volume_info(path: str) -> dict:
    """返回卷根、文件系统、剩余/总空间。非 Windows 退化到 shutil。"""
    info = {"root": "", "fs": "", "free": None, "total": None, "exists": False}
    if os.name != "nt":
        root = "/"
        try:
            usage = shutil.disk_usage(root)
            info.update(root=root, exists=True, free=usage.free, total=usage.total, fs="posix")
        except OSError:
            pass
        return info

    drive = os.path.splitdrive(os.path.abspath(path))[0]
    root = (drive or "C:") + "\\"
    info["root"] = root
    info["exists"] = os.path.exists(root)
    if not info["exists"]:
        return info
    try:
        k32 = ctypes.windll.kernel32
        free = ctypes.c_ulonglong(0)
        total = ctypes.c_ulonglong(0)
        total_free = ctypes.c_ulonglong(0)
        ok = k32.GetDiskFreeSpaceExW(
            ctypes.c_wchar_p(root), ctypes.byref(free), ctypes.byref(total), ctypes.byref(total_free)
        )
        if ok:
            info["free"] = total_free.value
            info["total"] = total.value
        fsname = ctypes.create_unicode_buffer(64)
        if k32.GetVolumeInformationW(
            ctypes.c_wchar_p(root), None, 0, None, None, None, fsname, 64
        ):
            info["fs"] = fsname.value
    except Exception:
        pass
    return info


def is_inside(child: str, parent: str) -> bool:
    c = normalize_path(child)
    p = normalize_path(parent)
    return c == p or c.startswith(p.rstrip("/") + "/")


# ---------------------------------------------------------------- 进程检测

def running_app_processes() -> list[str]:
    """粗查 WorkBuddy/CodeBuddy 进程，用于提醒「改数据库前先退出应用」。"""
    if os.name != "nt":
        return []
    try:
        out = subprocess.run(
            ["tasklist", "/FO", "CSV", "/NH"],
            capture_output=True, timeout=25, check=False,
        ).stdout
    except Exception:
        return []
    text = out.decode("mbcs", errors="replace")
    names = set()
    for line in text.splitlines():
        if not line.strip():
            continue
        first = line.split('","')[0].strip('"').strip()
        if first:
            names.add(first)
    return sorted(n for n in names if "workbuddy" in n.lower() or "codebuddy" in n.lower())


# ---------------------------------------------------------------- 显示名文件

def load_json(path: Path, default=None):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except Exception:
        return default


def save_json(path: Path, data, indent: int = 2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
    os.replace(tmp, path)


def display_name_entry(old: str) -> dict | None:
    data = load_json(DISPLAY_NAMES, {}) or {}
    return (data.get("workspaces") or {}).get(display_key(old))


# ---------------------------------------------------------------- 数据库

def db_connect(path: Path, readonly: bool = False) -> sqlite3.Connection:
    if readonly:
        uri = f"file:{str(path).replace('\\', '/')}?mode=ro"
        return sqlite3.connect(uri, uri=True, timeout=10)
    return sqlite3.connect(str(path), timeout=10)


def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone()
    return row is not None


def db_snapshot(path: Path, old: str) -> dict:
    """只读统计：这一次迁移会影响数据库里多少行。"""
    out = {"ok": False, "workspaces": 0, "sessions": 0, "automations": 0, "trust": 0, "error": None}
    if not Path(path).exists():
        out["error"] = "数据库不存在"
        return out
    try:
        conn = db_connect(path, readonly=True)
    except sqlite3.Error as e:
        out["error"] = str(e)
        return out
    try:
        if _table_exists(conn, "workspaces"):
            for (p,) in conn.execute("SELECT path FROM workspaces"):
                if same_path(p, old):
                    out["workspaces"] += 1
        if _table_exists(conn, "sessions"):
            for (c,) in conn.execute("SELECT cwd FROM sessions WHERE cwd IS NOT NULL AND cwd<>''"):
                if same_path(c, old):
                    out["sessions"] += 1
        if _table_exists(conn, "automations"):
            for (cwds,) in conn.execute("SELECT cwds FROM automations WHERE cwds IS NOT NULL"):
                try:
                    arr = json.loads(cwds)
                except Exception:
                    continue
                if any(isinstance(x, str) and same_path(x, old) for x in arr):
                    out["automations"] += 1
        if _table_exists(conn, "workspace_trust_decisions"):
            for (k,) in conn.execute("SELECT workspace_key FROM workspace_trust_decisions"):
                if same_path(k, old):
                    out["trust"] += 1
        out["ok"] = True
    except sqlite3.Error as e:
        out["error"] = str(e)
    finally:
        conn.close()
    return out


def db_patch(path: Path, old: str, new: str) -> dict:
    """
    把数据库里指向旧路径的记录改成新路径。
    应用在运行时会持有数据库锁；此处用 busy_timeout 排队，锁死则返回错误并提示退出应用。
    """
    report = {
        "applied": False, "locked": False, "error": None,
        "workspaces": 0, "sessions": 0, "automations": 0, "trust": 0,
    }
    if not Path(path).exists():
        report["error"] = f"数据库不存在：{path}"
        return report
    conn = db_connect(path, readonly=False)
    try:
        conn.execute("PRAGMA busy_timeout=10000")
        conn.execute("BEGIN IMMEDIATE")

        if _table_exists(conn, "workspaces"):
            rows = conn.execute("SELECT rowid, path FROM workspaces").fetchall()
            has_new = any(same_path(p, new) for _, p in rows)
            for rowid, p in rows:
                if same_path(p, old):
                    if has_new:
                        conn.execute("DELETE FROM workspaces WHERE rowid=?", (rowid,))
                    else:
                        conn.execute(
                            "UPDATE workspaces SET path=? WHERE rowid=?",
                            (to_style(new, p), rowid),
                        )
                        has_new = True
                    report["workspaces"] += 1

        if _table_exists(conn, "sessions"):
            rows = conn.execute(
                "SELECT id, cwd FROM sessions WHERE cwd IS NOT NULL AND cwd<>''"
            ).fetchall()
            for sid, cwd in rows:
                if same_path(cwd, old):
                    conn.execute(
                        "UPDATE sessions SET cwd=? WHERE id=?", (to_style(new, cwd), sid)
                    )
                    report["sessions"] += 1

        if _table_exists(conn, "automations"):
            rows = conn.execute("SELECT id, cwds FROM automations WHERE cwds IS NOT NULL").fetchall()
            for aid, cwds in rows:
                try:
                    arr = json.loads(cwds)
                except Exception:
                    continue
                if not isinstance(arr, list):
                    continue
                changed = False
                out = []
                for item in arr:
                    if isinstance(item, str) and same_path(item, old):
                        out.append(to_style(new, item))
                        changed = True
                    else:
                        out.append(item)
                if changed:
                    conn.execute(
                        "UPDATE automations SET cwds=? WHERE id=?",
                        (json.dumps(out, ensure_ascii=False), aid),
                    )
                    report["automations"] += 1

        if _table_exists(conn, "workspace_trust_decisions"):
            rows = conn.execute(
                "SELECT rowid, workspace_key, decision, revision FROM workspace_trust_decisions"
            ).fetchall()
            has_new = any(same_path(k, new) for _, k, _, _ in rows)
            for rowid, key, decision, revision in rows:
                if same_path(key, old):
                    if has_new:
                        continue
                    conn.execute(
                        "UPDATE workspace_trust_decisions SET workspace_key=?, updated_at=? WHERE rowid=?",
                        (to_style(new, key), now_ms(), rowid),
                    )
                    has_new = True
                    report["trust"] += 1

        conn.commit()
        report["applied"] = True
    except sqlite3.OperationalError as e:
        try:
            conn.rollback()
        except sqlite3.Error:
            pass
        msg = str(e).lower()
        report["locked"] = "locked" in msg or "busy" in msg
        report["error"] = str(e)
    except sqlite3.Error as e:
        try:
            conn.rollback()
        except sqlite3.Error:
            pass
        report["error"] = str(e)
    finally:
        conn.close()
    return report


# ---------------------------------------------------------------- 迁移状态

def new_state_dir(source: str, target: str) -> Path:
    d = STATE_ROOT / f"{stamp()}-{Path(target).name}"
    d.mkdir(parents=True, exist_ok=True)
    state = {
        "version": 1,
        "id": d.name,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source": os.path.abspath(source),
        "target": os.path.abspath(target),
        "old_slug": slug_for_path(source),
        "new_slug": slug_for_path(target),
        "app_dir": str(APP_ROOT),
        "backup_dir": str(d / "backup"),
        "status": "planned",
        "steps": [],
        "db_patched": False,
        "source_isolated": None,
    }
    save_json(d / "state.json", state)
    return d


def load_state(path: str | Path) -> dict:
    p = Path(path)
    if p.is_dir():
        p = p / "state.json"
    state = load_json(p)
    if not state:
        raise SystemExit(f"读不到迁移状态文件：{p}")
    state["_state_dir"] = str(p.parent)
    state["_state_file"] = str(p)
    return state


def save_state(state: dict) -> None:
    path = Path(state["_state_file"])
    data = {k: v for k, v in state.items() if not k.startswith("_")}
    save_json(path, data)


def latest_state() -> dict | None:
    if not STATE_ROOT.exists():
        return None
    dirs = sorted([d for d in STATE_ROOT.iterdir() if (d / "state.json").exists()],
                  key=lambda d: d.name, reverse=True)
    if not dirs:
        return None
    return load_state(dirs[0] / "state.json")


def log_step(state: dict, name: str, ok: bool, detail: str = "") -> None:
    state.setdefault("steps", []).append(
        {"name": name, "ok": bool(ok), "detail": detail, "at": time.strftime("%H:%M:%S")}
    )
    save_state(state)


# ---------------------------------------------------------------- 输出

def hr(title: str = "", char: str = "-", width: int = 64) -> None:
    if title:
        print(f"\n{title}")
    print(char * width)


def ok(msg: str) -> None:
    print(f"  [OK]   {msg}")


def warn(msg: str) -> None:
    print(f"  [WARN] {msg}")


def bad(msg: str) -> None:
    print(f"  [STOP] {msg}")
