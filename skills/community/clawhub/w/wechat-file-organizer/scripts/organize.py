#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信文件自动归类 (wechat-file-organizer) — 无头版
扫描微信接收文件，按类型/月份归类、去重、生成报告。

本脚本与 GUI 应用 wechat-file-organizer-gui（main.py，v1.17.0）的扫描逻辑
保持一致，作为无头/定时任务/自动化场景的对应物。

多语言：简体中文 / English，由同目录的 i18n.py 提供。
语言优先级 --lang > 环境变量 WFO_LANG / WECHAT_ORG_LANG > 系统语言自动判定。

设计原则：
- 零依赖：仅用 Python 标准库，无需 pip install。
- 安全优先：默认 dry-run（只读），绝不改动任何源文件；--apply 才是复制。
- 清理可恢复：--trash 只会把源文件移入回收站/废纸篓（可恢复），绝不永久删除。
- 可移植：路径全部运行时推导，无写死绝对路径；支持 Windows / macOS / Linux。
"""
import argparse
import fnmatch
import hashlib
import html as html_mod
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import defaultdict
from datetime import datetime
from pathlib import Path, PurePosixPath

# 语言包与本脚本同目录；先定语言，后面的分类名/报告文案才能按语言生成
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i18n

i18n.set_lang(i18n.lang_from_argv(sys.argv[1:]))

# 平台标识：win / mac / linux
PLATFORM = "mac" if sys.platform == "darwin" else (
    "win" if os.name == "nt" else "linux")

MB = 1024 * 1024

# 分类规则：内部 key -> 扩展名（显示名由 i18n.cat_name 提供）
CATEGORIES = {
    "documents": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt",
                  "md", "csv", "rtf", "wps", "ofd", "pages", "key", "numbers",
                  "epub", "mobi"],
    "images":   ["png", "jpg", "jpeg", "gif", "bmp", "webp", "heic", "tiff",
                 "tif", "svg"],
    "archives": ["zip", "rar", "7z", "tar", "gz", "tgz", "bz2", "xz", "zst"],
    "videos":   ["mp4", "mov", "avi", "mkv", "wmv", "flv", "webm", "m4v"],
    "audio":    ["mp3", "wav", "m4a", "aac", "flac", "ogg", "wma"],
    "others":   [],
}
OTHER_CAT = "others"
EXT_TO_CAT = {}
for _cat, _exts in CATEGORIES.items():
    for _e in _exts:
        EXT_TO_CAT[_e] = _cat

MONTH_RE = re.compile(r"^(\d{4})-(\d{2})$")

# 兼容模式（递归扫描）时跳过的微信系统/缓存目录
SYSTEM_DIRS = {
    "all_users", "db_storage", "apm_record", "business", "resource",
    "cache", "backup", "temp", "tmp", "logs", "log", "config", "mmkv",
    "thumb", "thumbs", ".thumbnails", "favorite", "emoticon", "sns",
    "xweb", "xeditor", "migrate", "InputTemp", "MsgAttach",
}

# 跳过的微信内部文件扩展名（非用户主动保存的文件）
SKIP_EXTS = {
    ".dat", ".db", ".db-wal", ".db-shm", ".mmkv", ".crc", ".kvdb",
    ".kvdb-wal", ".kvdb-shm", ".ini", ".lock", ".tmp", ".temp", ".bak",
    ".shm", ".wal", ".sqlite", ".sqlitedb",
}

# macOS 微信沙盒中 MessageTemp 下用户文件的类型子目录
MAC_FILE_SUBDIRS = {"File", "Image", "Video", "Audio"}
def trash_label():
    """删除操作在本平台上的叫法（回收站 / 废纸篓 / Recycle Bin / Trash）。"""
    return i18n.trash_label(PLATFORM)


# ---------- 中文宽度对齐 ----------
def wlen(s):
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in str(s))


def wpad(s, width, fill=" "):
    s = str(s)
    return s + fill * max(0, width - wlen(s))


def human(n):
    if n >= 1024 ** 3:
        return "%.1f GB" % (n / 1024 ** 3)
    if n >= MB:
        return "%.1f MB" % (n / MB)
    if n >= 1024:
        return "%.1f KB" % (n / 1024)
    return "%d B" % n


def log(*a):
    print(*a)


def cat_of(path):
    ext = os.path.splitext(path)[1].lstrip(".").lower()
    return EXT_TO_CAT.get(ext, OTHER_CAT)


def month_of(path):
    # 优先用 File/YYYY-MM 或 msg/file/YYYY-MM 父目录名
    parent = os.path.basename(os.path.dirname(path))
    m = MONTH_RE.match(parent)
    if m:
        return "%s-%s" % (m.group(1), m.group(2))
    try:
        ts = os.path.getmtime(path)
        return datetime.fromtimestamp(ts).strftime("%Y-%m")
    except OSError:
        return i18n.t("unknown")


def sha256_of(p, chunk=1 << 20):
    h = hashlib.sha256()
    try:
        with open(p, "rb") as f:
            for b in iter(lambda: f.read(chunk), b""):
                h.update(b)
    except OSError:
        return "ERR"
    return h.hexdigest()


# ---------- 路径发现 ----------
def _is_account_dir(d):
    """是否为单个微信账号目录（Windows 认 msg/FileStorage，mac 认 Message）。"""
    if PLATFORM == "mac":
        return os.path.isdir(os.path.join(d, "Message"))
    return (os.path.isdir(os.path.join(d, "msg"))
            or os.path.isdir(os.path.join(d, "FileStorage")))


def _mac_wechat_roots():
    """返回 macOS 微信沙盒账号目录列表（按版本号倒序）。非 mac 返回 []。"""
    if PLATFORM != "mac":
        return []
    base = os.path.expanduser(
        "~/Library/Containers/com.tencent.xinWeChat/Data/Library/"
        "Application Support/com.tencent.xinWeChat")
    if not os.path.isdir(base):
        return []
    roots = []
    try:
        for ver in sorted(os.listdir(base), reverse=True):
            vdir = os.path.join(base, ver)
            if not os.path.isdir(vdir):
                continue
            for acct in os.listdir(vdir):
                d = os.path.join(vdir, acct)
                if os.path.isdir(d) and os.path.isdir(os.path.join(d, "Message")):
                    if d not in roots:
                        roots.append(d)
    except OSError:
        pass
    return roots


def _scan_for_wechat_all(root, max_depth=4, limit=8):
    """在 root 下有限深度搜索所有微信文件根目录。"""
    found = []
    if not os.path.isdir(root):
        return found
    root = os.path.normpath(root)
    try:
        for dirpath, dirnames, _ in os.walk(root):
            depth = dirpath[len(root):].count(os.sep)
            if depth > max_depth:
                dirnames[:] = []
                continue
            if "FileStorage" in dirnames or "msg" in dirnames:
                p = os.path.dirname(dirpath) or dirpath
                if p not in found:
                    found.append(p)
                if len(found) >= limit:
                    break
    except OSError:
        pass
    return found


def find_all_wechat_dirs():
    """探测电脑上所有微信文件根目录（新版/旧版/自定义可并存）。"""
    out = []

    def add(p):
        if not p or not os.path.isdir(p):
            return
        p = os.path.normpath(p)
        low = p.lower()
        if all(low != x.lower() for x in out):
            out.append(p)

    env = os.environ.get("WECHAT_FILES_DIR")
    if env:
        add(env)
    if PLATFORM == "mac":
        for d in _mac_wechat_roots():
            add(d)
        return out
    home = os.path.expanduser("~")
    for name in ("WeChat Files", "Weixin Files", "xwechat_files"):
        add(os.path.join(home, "Documents", name))
        add(os.path.join(home, name))
    for p in _scan_for_wechat_all(os.path.join(home, "Documents"), max_depth=4):
        add(p)
    return out


def find_wechat_files_dir():
    """探测单个最优先的微信根目录（供 --source 未指定时使用）。"""
    env = os.environ.get("WECHAT_FILES_DIR")
    if env and os.path.isdir(env):
        return env
    dirs = find_all_wechat_dirs()
    return dirs[0] if dirs else None


def discover_account_dirs(root):
    """返回 root 下的微信账号目录列表（新旧结构均可，mac BFS 下探）。"""
    if not root or not os.path.isdir(root):
        return []
    root = os.path.normpath(root)
    if _is_account_dir(root):
        return [root]
    accounts = []
    if PLATFORM == "mac":
        from collections import deque
        q = deque([(root, 0)])
        seen = set()
        while q:
            d, depth = q.popleft()
            if d in seen:
                continue
            seen.add(d)
            if _is_account_dir(d):
                if d not in accounts:
                    accounts.append(d)
                continue
            if depth >= 6:
                continue
            try:
                for name in sorted(os.listdir(d)):
                    dd = os.path.join(d, name)
                    if os.path.isdir(dd):
                        q.append((dd, depth + 1))
            except OSError:
                pass
        return accounts
    try:
        for name in sorted(os.listdir(root)):
            d = os.path.join(root, name)
            if os.path.isdir(d) and _is_account_dir(d) and d not in accounts:
                accounts.append(d)
    except OSError:
        pass
    return accounts


def account_label_of(path, root):
    """判断文件属于哪个微信账号，返回账号目录名。"""
    r = os.path.normpath(root)
    p = os.path.normpath(path)
    if _is_account_dir(r):
        return os.path.basename(r)
    if p.lower().startswith(r.lower() + os.sep):
        parts = os.path.relpath(p, r).split(os.sep)
        if len(parts) > 1:
            return parts[0]
    return os.path.basename(r)


def discover_accounts(root):
    """返回所有『用户接收文件目录』（旧版 FileStorage / 新版 msg/file）。"""
    if os.path.basename(root).lower() == "filestorage":
        return [root]
    targets = []
    if not os.path.isdir(root):
        return targets
    if os.path.isdir(os.path.join(root, "File")):
        targets.append(root)
        return targets
    mf_self = os.path.join(root, "msg", "file")
    if os.path.isdir(mf_self):
        targets.append(mf_self)
    fs_self = os.path.join(root, "FileStorage")
    if os.path.isdir(fs_self):
        targets.append(fs_self)
    for name in os.listdir(root):
        d = os.path.join(root, name)
        if not os.path.isdir(d):
            continue
        fs = os.path.join(d, "FileStorage")
        if os.path.isdir(fs):
            targets.append(fs)
        mf = os.path.join(d, "msg", "file")
        if os.path.isdir(mf):
            targets.append(mf)
    return targets


def recursive_collect(root):
    """兼容模式：递归扫描整个目录，跳过微信系统目录与内部文件。"""
    files = []
    seen = set()
    for dirpath, dirnames, fnames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d.lower() not in SYSTEM_DIRS and not d.startswith(".")]
        for fn in fnames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in SKIP_EXTS:
                continue
            p = os.path.join(dirpath, fn)
            if p in seen:
                continue
            seen.add(p)
            files.append(p)
    return files


def collect_mac_files(acct_dir, include_media=False):
    """收集 macOS 账号目录下 MessageTemp 中的用户文件（四类类型目录）。"""
    files = []
    msg_temp = os.path.join(acct_dir, "Message", "MessageTemp")
    if not os.path.isdir(msg_temp):
        return files
    keep = set(MAC_FILE_SUBDIRS) if include_media else {"File"}
    walked = set()

    def collect_under(p):
        try:
            for dp, _, fnames in os.walk(p):
                for fn in fnames:
                    ext = os.path.splitext(fn)[1].lower()
                    if ext in SKIP_EXTS:
                        continue
                    files.append(os.path.join(dp, fn))
        except OSError:
            pass

    def descend(d):
        if d in walked:
            return
        walked.add(d)
        try:
            entries = sorted(os.listdir(d))
        except OSError:
            return
        for e in entries:
            p = os.path.join(d, e)
            if not os.path.isdir(p):
                continue
            if e in keep:
                collect_under(p)
            else:
                descend(p)

    descend(msg_temp)
    return files


def collect_files(roots, include_media=False, scan_all=False, recursive=False):
    """扫描多个微信根目录，返回 (path, account) 列表（已去重）。"""
    out = []
    seen = set()
    if isinstance(roots, str):
        roots = [roots]
    for root in roots:
        if not root or not os.path.isdir(root):
            continue
        if PLATFORM == "mac":
            for acct in (discover_account_dirs(root) or [root]):
                for p in collect_mac_files(acct, include_media or scan_all):
                    key = os.path.normcase(p)
                    if key in seen:
                        continue
                    seen.add(key)
                    out.append((p, os.path.basename(acct)))
            continue
        if recursive:
            files = recursive_collect(root)
            if not include_media:
                files = [f for f in files
                         if os.path.splitext(f)[1].lower() != ".dat"]
            for p in files:
                key = os.path.normcase(p)
                if key in seen:
                    continue
                seen.add(key)
                out.append((p, account_label_of(p, root)))
            continue
        targets = discover_accounts(root)
        if not targets:
            targets = [root]
        for target in targets:
            dirs_to_walk = []
            if os.path.basename(target).lower() == "filestorage":
                file_dir = os.path.join(target, "File")
                if os.path.isdir(file_dir):
                    dirs_to_walk.append(file_dir)
                if scan_all:
                    for sub in ("Image", "Video", "Voice", "Attachment",
                                "CustomEmotion", "Fav"):
                        sd = os.path.join(target, sub)
                        if os.path.isdir(sd):
                            dirs_to_walk.append(sd)
            else:
                dirs_to_walk.append(target)
            for t in dirs_to_walk:
                for dirpath, _, fnames in os.walk(t):
                    for fn in fnames:
                        ext = os.path.splitext(fn)[1].lower()
                        if ext in SKIP_EXTS:
                            continue
                        if not include_media and ext == ".dat":
                            continue
                        p = os.path.join(dirpath, fn)
                        key = os.path.normcase(p)
                        if key in seen:
                            continue
                        seen.add(key)
                        out.append((p, account_label_of(p, root)))
    return out


# ---------- 回收站（可恢复删除） ----------
def send_to_recycle_bin(paths):
    """把文件移入系统回收站（可恢复）。返回 (ok, failures)。

    Windows: SHFileOperationW；macOS: osascript Finder delete；Linux: 跳过。
    任何平台删除失败都只计入 failures，绝不静默回退为永久删除。
    """
    paths = [p for p in paths if p and os.path.exists(p)]
    if not paths:
        return 0, []

    if PLATFORM == "linux":
        return 0, [(p, i18n.t("trash.linux_skip") % trash_label())
                   for p in paths]

    if PLATFORM == "mac":
        def esc(s):
            return s.replace("\\", "\\\\").replace('"', '\\"')

        def run_osa(script):
            try:
                r = subprocess.run(["osascript", "-e", script],
                                   capture_output=True, text=True)
                return r.returncode == 0, (r.stderr or r.stdout).strip()
            except Exception as e:
                return False, str(e)

        items = ", ".join('POSIX file "%s"' % esc(p) for p in paths)
        ok_all, _err = run_osa('tell application "Finder" to delete {%s}' % items)
        if ok_all:
            return len(paths), []
        ok = 0
        failures = []
        for p in paths:
            ok_one, err_one = run_osa(
                'tell application "Finder" to delete POSIX file "%s"' % esc(p))
            if ok_one:
                ok += 1
            else:
                failures.append((p, i18n.t("trash.mac_fail")
                                 % (trash_label(), err_one[:200])))
        return ok, failures

    import ctypes
    from ctypes import wintypes
    try:
        shell32 = ctypes.windll.shell32
    except Exception:
        return 0, [(p, i18n.t("trash.win_unavailable") % trash_label())
                   for p in paths]

    class SHFILEOPSTRUCT(ctypes.Structure):
        _fields_ = [
            ("hwnd", wintypes.HWND),
            ("wFunc", wintypes.UINT),
            ("pFrom", wintypes.LPCWSTR),
            ("pTo", wintypes.LPCWSTR),
            ("fFlags", wintypes.UINT),
            ("fAnyOperationsAborted", wintypes.BOOL),
            ("hNameMappings", ctypes.c_void_p),
            ("lpszProgressTitle", wintypes.LPCWSTR),
        ]

    FO_DELETE = 3
    FOF_ALLOWUNDO = 0x40
    FOF_NOCONFIRMATION = 0x10
    FOF_NOERRORUI = 0x0400
    FOF_SILENT = 0x0004

    from_str = "\0".join(paths) + "\0\0"
    op = SHFILEOPSTRUCT()
    op.hwnd = None
    op.wFunc = FO_DELETE
    op.pFrom = from_str
    op.pTo = None
    op.fFlags = FOF_ALLOWUNDO | FOF_NOCONFIRMATION | FOF_NOERRORUI | FOF_SILENT
    rc = shell32.SHFileOperationW(ctypes.byref(op))
    if rc == 0 and not op.fAnyOperationsAborted:
        return len(paths), []
    failures = [(p, i18n.t("trash.still_exists") % rc)
                for p in paths if os.path.exists(p)]
    return len(paths) - len(failures), failures


# ---------- 自定义归类规则 ----------
class RuleError(Exception):
    """规则文件读取/格式/正则错误，携带可直接展示给用户的消息。"""
    pass


_ILLEGAL_PATH_CHARS = re.compile(r'[<>:"|?*\x00-\x1f]')
_PLACEHOLDER = re.compile(r"\{(month|year|account|cat|ext|name)\}")


def load_rules(path):
    """读取并编译规则文件，返回规则列表；出错抛 RuleError。"""
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except OSError as e:
        raise RuleError(i18n.t("err.rules_read") % (path, e))
    except (ValueError, UnicodeDecodeError) as e:
        raise RuleError(i18n.t("err.rules_json") % (path, e))

    if not isinstance(data, dict) or not isinstance(data.get("rules"), list):
        raise RuleError(i18n.t("err.rules_format") % "rules")

    compiled = []
    for i, raw in enumerate(data["rules"], 1):
        if not isinstance(raw, dict):
            raise RuleError(i18n.t("err.rules_format") % ("rules[%d]" % i))
        match = raw.get("match")
        if not isinstance(match, dict):
            raise RuleError(i18n.t("err.rules_format") % ("rules[%d].match" % i))
        dest = raw.get("dest")
        if not isinstance(dest, str) or not dest.strip():
            raise RuleError(i18n.t("err.rules_format") % ("rules[%d].dest" % i))

        globs = match.get("glob") or []
        path_globs = match.get("path_glob") or []
        exts = match.get("ext") or []
        if isinstance(globs, str):
            globs = [globs]
        if isinstance(path_globs, str):
            path_globs = [path_globs]
        if isinstance(exts, str):
            exts = [exts]
        if not all(isinstance(x, str) for x in globs + path_globs + exts):
            raise RuleError(i18n.t("err.rules_format") % ("rules[%d].match" % i))

        regex = None
        if match.get("regex"):
            try:
                regex = re.compile(match["regex"])
            except (re.error, TypeError) as e:
                raise RuleError(i18n.t("err.rules_regex") % (i, e))

        compiled.append({
            "name": str(raw.get("name") or ("Rule %d" % i)),
            "globs": globs,
            "path_globs": path_globs,
            "exts": [e.lstrip(".").lower() for e in exts],
            "regex": regex,
            "dest": dest.strip(),
        })
    return compiled


def _rule_matches(rule, record):
    """规则内各匹配维度取 AND，同一维度内多值取 OR；空规则不匹配任何文件。"""
    fname = os.path.basename(record["path"])
    full = record["path"].replace("\\", "/").lower()
    ext = os.path.splitext(fname)[1].lstrip(".").lower()
    used = False

    if rule["globs"]:
        used = True
        if not any(fnmatch.fnmatch(fname, g) for g in rule["globs"]):
            return False
    if rule["path_globs"]:
        used = True
        if not any(fnmatch.fnmatch(full, g.replace("\\", "/").lower())
                   for g in rule["path_globs"]):
            return False
    if rule["exts"]:
        used = True
        if ext not in rule["exts"]:
            return False
    if rule["regex"]:
        used = True
        if not rule["regex"].search(fname):
            return False
    return used


def _safe_component(s):
    """把占位符展开后的单级目录名清洗成跨平台安全名字。"""
    s = _ILLEGAL_PATH_CHARS.sub("_", str(s)).strip().strip(".")
    if s.lower() in ("con", "prn", "aux", "nul") or re.match(
            r"^(com|lpt)[1-9]$", s.lower()):
        s = "_" + s
    return s or i18n.t("unknown")


def expand_rule_dest(dest_tpl, record):
    """替换 dest 里的 {month}/{year}/{account}/{cat}/{ext}/{name}，并清洗路径。"""
    month = record.get("month") or ""
    values = {
        "month": month,
        "year": month[:4] if re.match(r"^\d{4}", month) else "",
        "account": record.get("account") or "",
        "cat": i18n.cat_name(record.get("cat")),
        "ext": os.path.splitext(record["path"])[1].lstrip(".").lower(),
        "name": os.path.splitext(os.path.basename(record["path"]))[0],
    }
    expanded = _PLACEHOLDER.sub(lambda m: values.get(m.group(1), ""), dest_tpl)
    parts = []
    for raw in re.split(r"[/\\]+", expanded):
        if raw in ("", ".", ".."):
            continue
        parts.append(_safe_component(raw))
    return os.path.join(*parts) if parts else i18n.cat_name(record.get("cat"))


def match_rule(rules, record):
    """按规则顺序返回第一条命中的规则（规则名为 dest 哦），未命中返回 None。"""
    for rule in rules:
        if _rule_matches(rule, record):
            return rule
    return None


def dest_path(dest_root, scheme, cat, month, fname, used, rule_dir=None):
    # 自定义规则的 dest 优先于 scheme；未命中规则时走原 type/month/type-month
    if rule_dir:
        rel = os.path.join(rule_dir, fname)
    else:
        # 输出目录里的文件夹名用当前语言的类别名
        cat_name = i18n.cat_name(cat)
        if scheme == "month":
            rel = os.path.join(month, fname)
        elif scheme == "type-month":
            rel = os.path.join(cat_name, month, fname)
        else:  # type
            rel = os.path.join(cat_name, fname)
    base, ext = os.path.splitext(fname)
    cand = rel
    i = 1
    while os.path.join(dest_root, cand) in used or os.path.exists(os.path.join(dest_root, cand)):
        cand = os.path.join(os.path.dirname(rel), "%s_%d%s" % (base, i, ext))
        i += 1
    used.add(os.path.join(dest_root, cand))
    return os.path.join(dest_root, cand)


# ---------- 单文件 HTML 报告 ----------
# 设计方向：Fathom Information Design（数据新闻派）——暖纸底 + 海军蓝 + 单一朱红，
# 章节编号 + 细线分隔 + 衬线大数字，拒绝圆角卡片堆叠。深浅双主题自适应。
# 字体全部走系统栈（Newsreader/Source Serif 缺失时回退 Georgia/宋体），零外部依赖。
_HTML_STYLE = """
:root{
  --paper:#F7F5F0; --paper-2:#EFECE4; --card:#FDFCF9;
  --ink:#23262B; --muted:#6E6A62; --faint:#9A958B;
  --navy:#1F3A5F; --navy-soft:#DDE5EE; --accent:#B3371D; --accent-soft:#F3E3DC;
  --line:#D8D3C8; --line-soft:#E7E2D8;
  --mark:#F6E7A8; --bar:#1F3A5F; --fg:#23262B;
  --display:"Newsreader","Source Serif 4","Iowan Old Style",Georgia,"Songti SC",serif;
  --body:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
  --mono:ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace;
}
@media (prefers-color-scheme: dark){
  :root{
    --paper:#14181D; --paper-2:#1B2027; --card:#1A1F26;
    --ink:#E8E5DE; --muted:#9C9A93; --faint:#6E6C66;
    --navy:#8FB4DC; --navy-soft:#22303F; --accent:#E8735A; --accent-soft:#3A2620;
    --line:#333A43; --line-soft:#282F37;
    --mark:#6B5A20; --bar:#8FB4DC; --fg:#E8E5DE;
  }
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font-family:var(--body);
  font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:1040px;margin:0 auto;padding:56px 40px 80px}

/* ---- masthead ---- */
.masthead{border-bottom:2px solid var(--ink);padding-bottom:18px;margin-bottom:0}
.kicker{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--accent);margin-bottom:12px}
h1{font-family:var(--display);font-weight:600;font-size:46px;line-height:1.1;
  letter-spacing:-.02em;margin:0 0 12px}
.dek{font-family:var(--display);font-size:19px;color:var(--muted);font-style:italic;
  margin:0 0 20px;max-width:640px}
.meta{display:flex;flex-wrap:wrap;gap:8px 24px;font-family:var(--mono);
  font-size:11px;color:var(--faint);letter-spacing:.02em}
.meta b{font-weight:600;color:var(--muted)}

/* ---- http hint ---- */
.http-hint{display:none;background:var(--accent-soft);border-top:1px solid var(--accent);
  color:var(--accent);padding:12px 16px;margin:24px 0 0;font-size:13px}

/* ---- search ---- */
.searchbar{display:flex;align-items:center;gap:12px;margin:32px 0 44px;
  border-bottom:1px solid var(--line);padding-bottom:10px}
.searchbar input{flex:1;min-width:0;border:0;background:transparent;color:var(--ink);
  font-family:var(--body);font-size:15px;padding:6px 0;outline:none}
.searchbar input::placeholder{color:var(--faint)}
.searchbar .search-stat{font-family:var(--mono);font-size:12px;color:var(--accent);white-space:nowrap}
.searchbar button{border:0;background:transparent;color:var(--faint);
  font-size:20px;line-height:1;cursor:pointer;padding:2px 6px}
.searchbar button:hover{color:var(--ink)}

/* ---- stat band ---- */
.statband{display:grid;grid-template-columns:repeat(6,1fr);gap:0;
  border-top:1px solid var(--ink);border-bottom:1px solid var(--ink);margin-bottom:52px}
.stat{padding:20px 16px 18px;border-right:1px solid var(--line-soft)}
.stat:first-child{padding-left:0}
.stat:last-child{border-right:0;padding-right:0}
.stat .k{font-size:11px;color:var(--muted);letter-spacing:.04em;margin-bottom:8px;
  text-transform:uppercase}
.stat .v{font-family:var(--display);font-size:34px;line-height:1;font-weight:600;
  letter-spacing:-.02em;color:var(--navy)}
.stat .v.accent{color:var(--accent)}
.stat .v small{font-family:var(--body);font-size:13px;font-weight:400;color:var(--muted);
  letter-spacing:0;margin-left:2px}

/* ---- section ---- */
section{margin:0 0 46px}
.sec-head{display:flex;align-items:baseline;gap:16px;border-bottom:1px solid var(--line);
  padding-bottom:10px;margin-bottom:20px}
.sec-num{font-family:var(--mono);font-size:13px;color:var(--accent);font-weight:600}
h2{font-family:var(--display);font-size:23px;font-weight:600;letter-spacing:-.01em;margin:0}
.sec-note{margin-left:auto;font-family:var(--mono);font-size:11px;color:var(--faint)}

/* ---- type rows ---- */
.type-row{display:grid;grid-template-columns:88px 1fr 130px;gap:16px;align-items:center;
  padding:11px 0;border-bottom:1px solid var(--line-soft)}
.type-row:last-child{border-bottom:0}
.type-row .lab{font-size:14px}
.type-row .track{height:8px;background:var(--paper-2);position:relative}
.type-row .fill{position:absolute;left:0;top:0;bottom:0;background:var(--navy)}
.type-row .num{text-align:right;font-family:var(--mono);font-size:12px;color:var(--muted)}

/* ---- tables ---- */
table{width:100%;border-collapse:collapse;font-size:14px}
thead th{font-family:var(--mono);font-size:11px;font-weight:600;text-transform:uppercase;
  letter-spacing:.06em;color:var(--muted);text-align:left;padding:0 12px 10px 0;
  border-bottom:1px solid var(--ink)}
thead th.r{text-align:right}
tbody td{padding:11px 12px 11px 0;border-bottom:1px solid var(--line-soft);vertical-align:middle}
tbody tr:last-child td{border-bottom:0}
td.r{text-align:right;font-family:var(--mono);font-size:13px;color:var(--muted)}
.ext-badge{font-family:var(--mono);font-size:12px;color:var(--navy);font-weight:600}
.extbar{height:5px;background:var(--navy);display:inline-block;vertical-align:middle;
  margin-right:8px}
.extpct{font-family:var(--mono);font-size:12px;color:var(--muted)}

/* ---- month chart ---- */
.chart-wrap{margin-top:4px}
.chart-wrap svg{display:block;width:100%;height:auto}

/* ---- dup details ---- */
details{border-top:1px solid var(--line);padding:14px 0}
details:last-of-type{border-bottom:1px solid var(--line)}
details summary{cursor:pointer;list-style:none;display:flex;align-items:center;gap:12px;
  font-family:var(--mono);font-size:13px;color:var(--navy)}
details summary::-webkit-details-marker{display:none}
details summary::before{content:"+";display:inline-block;width:16px;font-weight:700;color:var(--accent)}
details[open] summary::before{content:"\\2212"}
details .hash{color:var(--faint)}
details table{margin-top:14px}

/* ---- path cells ---- */
.path{font-family:var(--mono);font-size:12px;word-break:break-all;color:var(--muted)}
a.open{color:var(--navy);text-decoration:none;border-bottom:1px solid var(--navy-soft)}
a.open:hover{border-bottom-color:var(--navy)}
button.copy{border:1px solid var(--line);background:transparent;color:var(--muted);
  font-family:var(--mono);font-size:10px;padding:2px 7px;margin-left:6px;cursor:pointer;
  border-radius:2px}
button.copy:hover{border-color:var(--navy);color:var(--navy)}
button.copy.ok{border-color:var(--accent);color:var(--accent)}
mark{background:var(--mark);color:inherit;padding:0 1px}

/* ---- footer ---- */
.colophon{border-top:1px solid var(--ink);margin-top:56px;padding-top:16px;
  font-family:var(--mono);font-size:11px;color:var(--faint);line-height:1.8}
.acct-tag{font-family:var(--mono);font-size:11px;color:var(--faint)}
.empty{color:var(--muted);font-style:italic}
.small{font-family:var(--mono);font-size:11px;color:var(--faint);margin-top:12px}

@media (max-width:760px){
  .wrap{padding:32px 20px 56px}
  h1{font-size:34px}
  .statband{grid-template-columns:repeat(3,1fr)}
  .stat{border-bottom:1px solid var(--line-soft)}
  .type-row{grid-template-columns:64px 1fr 96px}
  .sec-note{display:none}
}
"""

_HTML_SCRIPT = """
<script>
(function(){
  var COPIED = %s, HITS = %s, NOMATCH = %s;

  // http(s) 页面里浏览器禁止导航到 file://，显示提示并让「复制」按钮兜底
  try {
    if (location.protocol !== 'file:') {
      var h = document.getElementById('httpHint');
      if (h) h.style.display = 'block';
    }
  } catch(e) {}

  // 复制按钮：事件委托，搜索隐藏/显示行后仍有效
  document.addEventListener('click', function(ev){
    var btn = ev.target;
    while (btn && btn.tagName !== 'BUTTON') btn = btn.parentNode;
    if (!btn || !btn.classList.contains('copy')) return;
    var p = btn.getAttribute('data-path');
    var done = function(){
      var old = btn.textContent;
      btn.textContent = COPIED;
      btn.classList.add('ok');
      setTimeout(function(){ btn.textContent = old; btn.classList.remove('ok'); }, 1400);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(p).then(done, function(){ legacyCopy(p, done); });
    } else {
      legacyCopy(p, done);
    }
  });
  function legacyCopy(text, cb){
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); cb(); } catch(e) {}
    document.body.removeChild(ta);
  }

  // ---- 搜索：实时过滤 + 高亮 + 命中计数 ----
  var input = document.getElementById('wfoSearch');
  var stat  = document.getElementById('wfoStat');
  var clear = document.getElementById('wfoClear');
  var rows = [];
  document.querySelectorAll('table tbody tr').forEach(function(tr){
    // 只存原始单元格片段，避免整行 innerHTML 在 mark 高亮后反复嵌套
    var cells = [];
    tr.querySelectorAll('td').forEach(function(td){ cells.push(td.innerHTML); });
    rows.push({ tr: tr, cells: cells, text: tr.textContent.toLowerCase() });
  });

  function highlight(td, q){
    var walker = document.createTreeWalker(td, NodeFilter.SHOW_TEXT, null, false);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function(node){
      var s = node.nodeValue, low = s.toLowerCase(), pos = 0, frag = null, at;
      while ((at = low.indexOf(q, pos)) !== -1) {
        if (!frag) frag = document.createDocumentFragment();
        if (at > pos) frag.appendChild(document.createTextNode(s.slice(pos, at)));
        var mk = document.createElement('mark');
        mk.textContent = s.slice(at, at + q.length);
        frag.appendChild(mk);
        pos = at + q.length;
      }
      if (frag) {
        if (pos < s.length) frag.appendChild(document.createTextNode(s.slice(pos)));
        node.parentNode.replaceChild(frag, node);
      }
    });
  }

  function runSearch(){
    var q = (input.value || '').trim().toLowerCase();
    var hits = 0;
    rows.forEach(function(r){
      var match = !q || r.text.indexOf(q) !== -1;
      r.tr.style.display = match ? '' : 'none';
      // 还原原始单元格后按需高亮，避免 mark 叠加
      var tds = r.tr.querySelectorAll('td');
      for (var i = 0; i < tds.length; i++) tds[i].innerHTML = r.cells[i];
      if (q && match) {
        hits++;
        for (var j = 0; j < tds.length; j++) highlight(tds[j], q);
      }
    });
    // 命中的重复文件组自动展开
    document.querySelectorAll('details').forEach(function(d){
      if (q && d.querySelector('tr[style="display: none;"]') === null
          && d.querySelector('tbody tr')) {
        var anyVisible = false;
        d.querySelectorAll('tbody tr').forEach(function(tr){
          if (tr.style.display !== 'none') anyVisible = true;
        });
        if (anyVisible) d.open = true;
      }
    });
    clear.style.visibility = q ? 'visible' : 'hidden';
    stat.textContent = q ? (hits ? HITS.replace('%%d', hits) : NOMATCH) : '';
  }

  input.addEventListener('input', runSearch);
  clear.addEventListener('click', function(){
    input.value = ''; runSearch(); input.focus();
  });
  document.addEventListener('keydown', function(ev){
    if (ev.key === '/' && document.activeElement !== input) {
      ev.preventDefault(); input.focus();
    }
    if (ev.key === 'Escape' && document.activeElement === input) {
      input.value = ''; runSearch(); input.blur();
    }
  });
})();
</script>
"""


def _esc(s):
    return html_mod.escape(str(s), quote=True)


def _file_uri(path):
    """把本地路径转成 file:// URI（stdlib pathlib.as_uri，自动处理中文/空格/#）。

    按路径自身形态判断 POSIX / Windows 绝对路径，避免跨平台查看报告时被
    Path.absolute() 误加当前盘符（例如 Windows 上遇到 /home/user/x）。
    """
    try:
        if path.startswith("/"):
            return PurePosixPath(path).as_uri()
        return Path(path).absolute().as_uri()
    except (ValueError, OSError):
        return None


def _openable_path(path):
    """可点击打开的路径单元格：file:// 链接 + 复制按钮（http 下用按钮兜底）。"""
    uri = _file_uri(path)
    if not uri:
        return '<span class="path">%s</span>' % _esc(path)
    return ('<a class="open" href="%s" title="%s">%s</a> '
            '<button class="copy" type="button" data-path="%s">%s</button>'
            % (_esc(uri), _esc(i18n.t("html.click_open")), _esc(path),
               _esc(path), _esc(i18n.t("html.copy"))))


def _svg_month_chart(months):
    """纯内联 SVG 柱状图，不依赖任何 JS 库（Fathom 版式：细网格 + 海军蓝柱 + 双行标注）。"""
    if not months:
        return '<p class="empty">-</p>'
    items = sorted(months.items())
    W, H = 960, 210
    pad_l, pad_r, pad_t, pad_b = 52, 16, 18, 54
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    mx = max(v[0] for _, v in items) or 1
    step = plot_w / len(items)
    bw = min(120, step * 0.62)
    parts = ['<svg viewBox="0 0 %d %d" width="100%%" height="%d" '
             'role="img" aria-label="month trend">' % (W, H, H)]
    for i in range(5):
        y = pad_t + plot_h * i / 4.0
        val = int(mx * (4 - i) / 4.0)
        stroke = "var(--ink)" if i == 4 else "var(--line)"
        parts.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" '
                     'stroke="%s" stroke-width="1"/>'
                     % (pad_l, y, W - pad_r, y, stroke))
        parts.append('<text x="%d" y="%.1f" fill="var(--faint)" font-size="11" '
                     'text-anchor="end" font-family="monospace">%d</text>'
                     % (pad_l - 8, y + 4, val))
    for i, (month, (count, size)) in enumerate(items):
        h = max(1.0, plot_h * count / mx)
        x = pad_l + step * i + (step - bw) / 2
        y = pad_t + plot_h - h
        cx = x + bw / 2
        parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" '
                     'fill="var(--navy)"><title>%s: %d / %s</title></rect>'
                     % (x, y, bw, h, _esc(month), count, _esc(human(size))))
        parts.append('<text x="%.1f" y="%d" fill="var(--muted)" font-size="12" '
                     'text-anchor="middle" font-family="monospace">%s</text>'
                     % (cx, H - 32, _esc(month)))
        parts.append('<text x="%.1f" y="%d" fill="var(--navy)" font-size="13" '
                     'text-anchor="middle" font-family="monospace">%d \u00b7 %s</text>'
                     % (cx, H - 12, count, _esc(human(size))))
    parts.append('</svg>')
    return "".join(parts)


def write_html_report(path, records, by_cat, dupes, old, top, accounts,
                      roots, args, rule_stats=None):
    """生成单文件 HTML 报告。数据全部来自已有统计，不二次扫描/不重算 hash。"""
    total = len(records)
    total_size = sum(r["size"] for r in records)
    recoverable = sum(max(x["size"] for x in rs) * (len(rs) - 1)
                      for rs in dupes.values())
    months = defaultdict(lambda: [0, 0])
    ext_stats = defaultdict(lambda: [0, 0])
    for r in records:
        m = months[r["month"]]
        m[0] += 1
        m[1] += r["size"]
        ext = os.path.splitext(r["path"])[1].lstrip(".").lower() \
            or i18n.t("html.no_ext")
        ext_stats[ext][0] += 1
        ext_stats[ext][1] += r["size"]

    mode = i18n.t("html.mode_apply") if args.apply else i18n.t("html.mode_dry")
    cards = [
        (i18n.t("html.total_files"), str(total), ""),
        (i18n.t("html.total_size"), human(total_size), "sm"),
        (i18n.t("html.account_count"), str(len(accounts)), ""),
        (i18n.t("html.dup_groups"), str(len(dupes)), "accent"),
        (i18n.t("html.reclaimable"), human(recoverable), "sm accent"),
        (i18n.t("html.old_files"), str(len(old)), ""),
    ]
    def _section(num, title, note, body):
        """Fathom 版式的章节：编号 + 标题 + 右对齐注释 + 细分隔线。"""
        return ('<section><div class="sec-head"><span class="sec-num">%s</span>'
                '<h2>%s</h2><span class="sec-note">%s</span></div>%s</section>'
                % (num, _esc(title), _esc(note), body))

    out = ['<!DOCTYPE html><html lang="%s"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width,initial-scale=1">'
           '<title>%s · %s</title><style>%s</style></head><body><div class="wrap">'
           % (_esc(i18n.get_lang()), _esc(i18n.t("html.title")),
              _esc(i18n.t("html.kicker")), _HTML_STYLE)]

    # ---- masthead ----
    out.append('<header class="masthead"><div class="kicker">%s</div>'
               '<h1>%s</h1><p class="dek">%s</p><div class="meta">'
               '<span><b>%s</b> %s</span><span><b>%s</b> %s</span>'
               '<span><b>%s</b> %d</span><span><b>%s</b> %s</span>'
               '</div></header>'
               % (_esc(i18n.t("html.kicker")), _esc(i18n.t("html.title")),
                  _esc(i18n.t("html.dek")),
                  _esc(i18n.t("html.meta_generated")),
                  _esc(datetime.now().strftime("%Y-%m-%d %H:%M")),
                  _esc(i18n.t("html.meta_mode")), _esc(mode),
                  _esc(i18n.t("html.account_count")), len(accounts),
                  _esc(i18n.t("html.meta_lang")), _esc(i18n.t("html.lang_name"))))

    out.append('<div class="http-hint" id="httpHint">%s</div>'
               % _esc(i18n.t("html.http_hint")))

    out.append('<div class="searchbar">'
               '<input id="wfoSearch" type="search" placeholder="%s" '
               'autocomplete="off" spellcheck="false" aria-label="%s">'
               '<span id="wfoStat" class="search-stat"></span>'
               '<button id="wfoClear" type="button" aria-label="%s">\u00d7</button>'
               '</div>'
               % (_esc(i18n.t("html.search")), _esc(i18n.t("html.search")),
                  _esc(i18n.t("html.search_clear"))))

    # ---- stat band（6 数字带，回收/重复用朱红 accent）----
    out.append('<div class="statband">')
    for key, val, cls in cards:
        tokens = cls.split()
        accent = " accent" if "accent" in tokens else ""
        small = ""
        if "sm" in tokens:  # 把 human() 的数值和单位拆开，单位用小字
            m = re.match(r"^([\d.]+)\s*([A-Za-z]+)$", val)
            if m:
                val, small = m.group(1), "<small>%s</small>" % _esc(m.group(2))
        out.append('<div class="stat"><div class="k">%s</div>'
                   '<div class="v%s">%s%s</div></div>'
                   % (_esc(key), accent, _esc(val), small))
    out.append('</div>')

    # ---- 01 按类型 ----
    body = []
    for cat in CATEGORIES:
        if cat not in by_cat:
            continue
        count, size = by_cat[cat]
        pct = 100.0 * size / total_size if total_size else 0
        body.append('<div class="type-row"><div class="lab">%s</div>'
                    '<div class="track"><div class="fill" style="width:%.1f%%"></div>'
                    '</div><div class="num">%d \u00b7 %s</div></div>'
                    % (_esc(i18n.cat_name(cat)), pct, count, _esc(human(size))))
    out.append(_section("01", i18n.t("html.by_type"),
                        i18n.t("html.sec_note_type"), "".join(body)))

    # ---- 02 按扩展名排行（完全动态，无预设清单）----
    ext_sorted = sorted(ext_stats.items(), key=lambda kv: (-kv[1][0], kv[0]))
    body = ['<table><thead><tr><th>%s</th><th class="r">%s</th>'
            '<th class="r">%s</th><th class="r">%s</th></tr></thead><tbody>'
            % (_esc(i18n.t("html.ext")), _esc(i18n.t("report.total_files")),
               _esc(i18n.t("html.size")), _esc(i18n.t("html.size_pct")))]
    for ext, (cnt, sz) in ext_sorted:
        pct = 100.0 * sz / total_size if total_size else 0
        body.append('<tr><td><span class="ext-badge">%s</span></td>'
                    '<td class="r">%d</td><td class="r">%s</td>'
                    '<td class="r"><span class="extbar" style="width:%.0fpx"></span>'
                    '<span class="extpct">%.1f%%</span></td></tr>'
                    % (_esc(ext), cnt, _esc(human(sz)), 70.0 * pct / 100.0, pct))
    body.append('</tbody></table>')
    out.append(_section("02", i18n.t("html.by_ext"),
                        i18n.t("html.sec_note_ext"), "".join(body)))

    # ---- 03 按月份 ----
    out.append(_section("03", i18n.t("html.by_month"),
                        i18n.t("html.sec_note_month"),
                        '<div class="chart-wrap">%s</div>' % _svg_month_chart(months)))

    # ---- 04 重复明细 ----
    body = []
    if dupes:
        for h, rs in sorted(dupes.items(),
                            key=lambda kv: max(x["size"] for x in kv[1])
                            * (len(kv[1]) - 1), reverse=True):
            sz = max(x["size"] for x in rs)
            body.append('<details><summary><span class="hash">%s\u2026</span>'
                        '<span>%d %s \u00b7 %s / %s</span></summary>'
                        % (_esc(h[:12]), len(rs), _esc(i18n.t("html.copies")),
                           _esc(human(sz)), _esc(human(sz * (len(rs) - 1)))))
            body.append('<table><thead><tr><th>%s</th><th>%s</th></tr></thead><tbody>'
                        % (_esc(i18n.t("html.account")), _esc(i18n.t("html.path"))))
            for r in sorted(rs, key=lambda x: x["path"]):
                body.append('<tr><td><span class="acct-tag">%s</span></td>'
                            '<td class="path">%s</td></tr>'
                            % (_esc(r["account"]), _openable_path(r["path"])))
            body.append('</tbody></table></details>')
    else:
        body.append('<p class="empty">%s</p>' % _esc(i18n.t("html.no_dupes")))
    out.append(_section("04", i18n.t("html.dup_detail"),
                        i18n.t("html.sec_note_dup"), "".join(body)))

    # ---- 05 规则命中（仅使用规则时显示）----
    if rule_stats is not None:
        body = []
        if rule_stats:
            body.append('<table><thead><tr><th>%s</th><th class="r">%s</th></tr>'
                        '</thead><tbody>' % (_esc(i18n.t("html.rule_name")),
                                             _esc(i18n.t("html.hits"))))
            for name, n in sorted(rule_stats.items(), key=lambda kv: -kv[1]):
                body.append('<tr><td>%s</td><td class="r">%d</td></tr>'
                            % (_esc(name), n))
            body.append('</tbody></table>')
        else:
            body.append('<p class="empty">%s</p>' % _esc(i18n.t("html.no_rules")))
        out.append(_section("05", i18n.t("html.rule_stats"),
                            i18n.t("html.sec_note_rule"), "".join(body)))

    # ---- 06 最大的文件 ----
    if top:
        body = ['<table><thead><tr><th class="r">%s</th><th>%s</th>'
                '<th>%s</th><th>%s</th></tr></thead><tbody>'
                % (_esc(i18n.t("html.size")), _esc(i18n.t("html.type_short")),
                   _esc(i18n.t("html.account")), _esc(i18n.t("html.path")))]
        for r in top:
            body.append('<tr><td class="r">%s</td><td>%s</td>'
                        '<td><span class="acct-tag">%s</span></td>'
                        '<td class="path">%s</td></tr>'
                        % (_esc(human(r["size"])), _esc(i18n.cat_name(r["cat"])),
                           _esc(r["account"]), _openable_path(r["path"])))
        body.append('</tbody></table>')
        out.append(_section("06", i18n.t("html.top_files"),
                            i18n.t("html.sec_note_top"), "".join(body)))

    # ---- colophon ----
    out.append('<footer class="colophon">%s<br>%s %s: %s</footer>'
               % (_esc(i18n.t("html.colophon_1")), _esc(i18n.t("html.colophon_2")),
                  _esc(i18n.t("report.source")), _esc(" | ".join(roots))))
    # 用 json.dumps 生成带引号的 JS 字符串字面量（i18n 文案含中文/空格需正确引用）
    out.append(_HTML_SCRIPT % (json.dumps(i18n.t("html.copied")),
                               json.dumps(i18n.t("html.search_hits")),
                               json.dumps(i18n.t("html.search_nomatch"))))
    out.append('</div></body></html>')

    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(out))


def main():
    ap = argparse.ArgumentParser(description=i18n.t("app.desc"))
    ap.add_argument("--source", help=i18n.t("arg.source"))
    ap.add_argument("--dest", help=i18n.t("arg.dest"))
    ap.add_argument("--scheme", choices=["type", "month", "type-month"], default="type",
                    help=i18n.t("arg.scheme"))
    ap.add_argument("--apply", action="store_true", help=i18n.t("arg.apply"))
    ap.add_argument("--trash", action="store_true",
                    help=i18n.t("arg.trash") % trash_label())
    ap.add_argument("--dedupe", action="store_true", help=i18n.t("arg.dedupe"))
    ap.add_argument("--include-media", action="store_true",
                    help=i18n.t("arg.include_media"))
    ap.add_argument("--scan-all", action="store_true", help=i18n.t("arg.scan_all"))
    ap.add_argument("--top", type=int, default=10, help=i18n.t("arg.top"))
    ap.add_argument("--old-days", type=int, default=365, help=i18n.t("arg.old_days"))
    ap.add_argument("--json", action="store_true", help=i18n.t("arg.json"))
    ap.add_argument("--rules", metavar="FILE", help=i18n.t("arg.rules"))
    ap.add_argument("--html", metavar="FILE", help=i18n.t("arg.html"))
    ap.add_argument("--lang", choices=i18n.LANGS, default=i18n.get_lang(),
                    help=i18n.t("arg.lang"))
    args = ap.parse_args()
    # --lang 也要能覆盖 argv 预解析的结果（例如写在其它参数之后）
    if args.lang != i18n.get_lang():
        i18n.set_lang(args.lang)

    rules = None
    if args.rules:
        try:
            rules = load_rules(args.rules)
        except RuleError as e:
            log(str(e))
            return 2

    roots = [args.source] if args.source else find_all_wechat_dirs()
    roots = [r for r in roots if r and os.path.isdir(r)]
    if not roots:
        msg = {"ok": False, "error": i18n.t("err.no_dir"),
               "hint": i18n.t("err.no_dir_hint")}
        log(json.dumps(msg, ensure_ascii=False) if args.json
            else i18n.t("err.no_dir_text"))
        return 2

    files = collect_files(roots, include_media=args.include_media,
                          scan_all=args.scan_all)
    if not files:
        msg = {"ok": True, "files": 0, "note": i18n.t("skip.none")}
        log(json.dumps(msg, ensure_ascii=False) if args.json
            else i18n.t("skip.none_text"))
        return 0

    records = []
    rule_stats = defaultdict(int) if rules else None
    for p, acct in files:
        try:
            st = os.stat(p)
            rec = {
                "path": p, "account": acct, "cat": cat_of(p), "month": month_of(p),
                "size": st.st_size, "hash": sha256_of(p), "mtime": st.st_mtime,
            }
            if rules:
                hit = match_rule(rules, rec)
                if hit:
                    rec["rule"] = hit["name"]
                    rec["rule_dir"] = expand_rule_dest(hit["dest"], rec)
                    rule_stats[hit["name"]] += 1
            records.append(rec)
        except OSError:
            continue

    total = len(records)
    total_size = sum(r["size"] for r in records)
    accounts = sorted({r["account"] for r in records})

    by_cat = {}
    for r in records:
        c = by_cat.setdefault(r["cat"], [0, 0])
        c[0] += 1
        c[1] += r["size"]

    groups = {}
    for r in records:
        groups.setdefault(r["hash"], []).append(r)
    dupes = {h: rs for h, rs in groups.items() if len(rs) > 1}
    dup_count = sum(len(rs) - 1 for rs in dupes.values())
    dup_recover = sum(max(x["size"] for x in rs) * (len(rs) - 1) for rs in dupes.values())

    now = datetime.now().timestamp()
    old = [r for r in records if now - r["mtime"] > args.old_days * 86400]
    top = sorted(records, key=lambda r: r["size"], reverse=True)[:max(0, args.top)]

    copied = skipped_dup = trashed = 0
    trash_failures = []
    if args.apply:
        dest = args.dest or os.path.join(
            os.path.dirname(os.path.abspath(roots[0])), "WeChatFiles_Organized")
        os.makedirs(dest, exist_ok=True)
        used = set()
        seen_hash = set()
        to_trash = []
        for r in records:
            if args.dedupe and r["hash"] in seen_hash:
                skipped_dup += 1
                continue
            seen_hash.add(r["hash"])
            dp = dest_path(dest, args.scheme, r["cat"], r["month"],
                           os.path.basename(r["path"]), used,
                           rule_dir=r.get("rule_dir"))
            try:
                os.makedirs(os.path.dirname(dp), exist_ok=True)
                shutil.copy2(r["path"], dp)
                copied += 1
                if args.trash:
                    to_trash.append(r["path"])
            except OSError as e:
                log(i18n.t("warn.copy_failed") % (r["path"], e))
        if args.trash and to_trash:
            trashed, trash_failures = send_to_recycle_bin(to_trash)
            for p, reason in trash_failures:
                log(i18n.t("warn.trash_failed") % (p, trash_label(), reason))

    if args.json:
        out = {
            "ok": True, "applied": bool(args.apply), "scheme": args.scheme,
            "platform": PLATFORM, "sources": roots,
            "accounts": accounts, "account_count": len(accounts),
            "total_files": total, "total_size": total_size,
            "by_category": {k: {"count": v[0], "size": v[1]} for k, v in by_cat.items()},
            "duplicates": {"groups": len(dupes), "extra_files": dup_count,
                           "recoverable_bytes": dup_recover},
            "old_files": len(old),
            "top_files": [{"path": r["path"], "size": r["size"],
                           "cat": r["cat"], "account": r["account"]} for r in top],
        }
        if args.apply:
            out["result"] = {"dest": dest, "copied": copied,
                             "skipped_duplicates": skipped_dup,
                             "trashed": trashed,
                             "trash_failures": len(trash_failures)}
        if rule_stats is not None:
            out["rules"] = {"file": args.rules,
                            "count": len(rules),
                            "hits": dict(rule_stats)}
        if args.html:
            out["html_report"] = args.html
        log(json.dumps(out, ensure_ascii=False, indent=2))

    # HTML 报告与 JSON/文本互不排斥：显式指定才写，属于输出产物而非改动源文件
    html_line = None
    if args.html:
        try:
            write_html_report(args.html, records, by_cat, dupes, old, top,
                              accounts, roots, args,
                              rule_stats=dict(rule_stats) if rule_stats is not None
                              else None)
            html_line = i18n.t("report.html_saved") % args.html
        except OSError as e:
            html_line = i18n.t("warn.html_failed") % (args.html, e)

    if not args.json:
        if rule_stats is not None:
            log(i18n.t("report.rules_loaded")
                % (args.rules, len(rules), sum(rule_stats.values())))
        log("=" * 50)
        log(i18n.t("report.title")
            % (i18n.t("report.apply") if args.apply else i18n.t("report.dryrun")))
        log("%s: %s" % (i18n.t("report.source"),
                        roots[0] if len(roots) == 1
                        else i18n.t("report.multi_source") % len(roots)))
        if len(accounts) > 1:
            log(i18n.t("report.accounts_line")
                % (i18n.t("report.accounts"), len(accounts),
                   i18n.join_list(accounts)))
        log("-" * 50)
        log("%s: %d" % (wpad(i18n.t("report.total_files"), 14), total))
        log("%s: %s" % (wpad(i18n.t("report.total_size"), 14), human(total_size)))
        log("-" * 50)
        log(i18n.t("report.by_type") + ":")
        for cat in CATEGORIES:
            if cat in by_cat:
                c = by_cat[cat]
                log(i18n.t("report.type_line")
                    % (wpad(i18n.cat_name(cat), 12), c[0], human(c[1])))
        log("-" * 50)
        log("%s: %s" % (wpad(i18n.t("report.dup"), 14),
                        i18n.t("report.dup_line")
                        % (len(dupes), dup_count, human(dup_recover))))
        log("%s: %s" % (wpad(i18n.t("report.old"), 14),
                        i18n.t("report.old_line") % (len(old), args.old_days)))
        if top:
            log("-" * 50)
            log(i18n.t("report.top") % len(top) + ":")
            for r in top:
                acct = ("[%s] " % r["account"]) if len(accounts) > 1 else ""
                log("  %s  %s%s" % (wpad(human(r["size"]), 10), acct, r["path"]))
        log("=" * 50)

        if args.apply:
            log(i18n.t("report.ok") % dest)
            extra = i18n.t("report.dedupe_skip") % skipped_dup if args.dedupe else ""
            log(i18n.t("report.copied") % (copied, extra))
            if args.trash:
                log(i18n.t("report.trashed")
                    % (trash_label(), trashed, len(trash_failures)))
        else:
            log(i18n.t("report.dryrun_hint"))
        if html_line:
            log(html_line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
