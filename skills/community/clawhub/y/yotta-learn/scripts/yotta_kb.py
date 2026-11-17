#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yotta_kb.py — 元习知识库（Yuanxi KB）内核。

文件式知识库 v1：分类 / 条目（Markdown + 受控 frontmatter）/ 审计 /
回收站 / 快照 / 备份 / doctor。索引与查询在 yotta_kb_index.py，CLI 在
yotta_learn.py；纯 Python 3.8+ 标准库，Windows + Linux 通用。

数据协议见技能内 references/kb.md（KB v1）。
"""
import hashlib
import json
import os
import re
import shutil
import socket
import tempfile
import time
from datetime import datetime
from pathlib import Path

KB_SCHEMA = "yotta-kb/1"
INDEX_SCHEMA = "yotta-kb-index/1"
GLOBAL_SCHEMA = "yotta-kb-global/1"
STATS_SCHEMA = "yotta-kb-stats/1"
SNAPSHOT_SCHEMA = "yotta-kb-snapshot/1"
BACKUP_SCHEMA = "yotta-kb-backup/1"

ENTRY_STATUSES = ("draft", "verified", "deprecated")
CONFIDENCES = ("high", "medium", "low")
CATEGORY_STATUSES = ("active", "deprecated")
SLUG_RE = re.compile(r"^[a-z][a-z0-9-]{1,38}$")
ENTRY_ID_RE = re.compile(r"^KB-\d{8}-\d{3}$")
TRASH_RETENTION_DAYS = 7
SNAPSHOT_KEEP = 20
LOCK_STALE_SECONDS = 120.0


class KbError(Exception):
    """知识库错误基类：message + 退出码。"""

    def __init__(self, message, code=1):
        super().__init__(message)
        self.message = message
        self.code = code


class KbUsageError(KbError):
    def __init__(self, message):
        super().__init__(message, 4)


class KbGateError(KbError):
    def __init__(self, message):
        super().__init__(message, 5)


class KbIntegrityError(KbError):
    def __init__(self, message):
        super().__init__(message, 6)


class KbNotFound(KbError):
    def __init__(self, message):
        super().__init__(message, 1)


# ── 时间与身份 ──────────────────────────────────────────────────────────────

def now_iso():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _today():
    return datetime.now().strftime("%Y%m%d")


def _timestamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def resolve_actor(explicit=None):
    """身份 = agent@host：--agent 优先，其次 YOTTA_LEARN_AGENT，兜底 unknown。"""
    agent = (explicit or os.environ.get("YOTTA_LEARN_AGENT") or "").strip() or "unknown"
    host = (socket.gethostname() or "").strip() or "unknown-host"
    return "%s@%s" % (agent, host)


def actor_is_unknown(actor):
    return actor.startswith("unknown@")


def _age_days(iso_text):
    try:
        dt = datetime.fromisoformat(iso_text)
    except (TypeError, ValueError):
        return 0.0
    if dt.tzinfo is None:
        dt = dt.astimezone()
    return max(0.0, (datetime.now().astimezone() - dt).total_seconds() / 86400.0)


# ── 配置与位置 ──────────────────────────────────────────────────────────────
#
# 0.4.0 起配置与默认库独立到 ~/.yottalearn/（不再与元阁 ~/.yottaskills/ 混放）。
# 旧路径（~/.yottaskills/yotta-learn.json 与 ~/.yottaskills/knowledge）保留只读
# 兼容 + 迁移引导（回退生效时写操作 fail-closed）；迁移 = migrate_kb（复制 →
# 校验 → 切配置 → 旧库移出原位）。

def config_dir():
    return Path.home() / ".yottalearn"


def config_path():
    return config_dir() / "config.json"


def legacy_config_path():
    return Path.home() / ".yottaskills" / "yotta-learn.json"


def default_kb_root():
    return config_dir() / "knowledge"


def legacy_default_kb_root():
    return Path.home() / ".yottaskills" / "knowledge"


def _read_config_file(p):
    try:
        data = json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise KbIntegrityError("配置文件损坏（%s）：%s；修复或删除后重试" % (p, exc))
    if not isinstance(data, dict):
        raise KbIntegrityError("配置文件格式错误（应为 JSON 对象）：%s" % p)
    return data


def load_config_with_source():
    """读取位置配置：新路径优先，不存在时回退旧路径（0.3.x 兼容）。

    返回 (cfg, path, legacy)。"""
    new = config_path()
    if new.exists():
        return _read_config_file(new), new, False
    old = legacy_config_path()
    if old.exists():
        return _read_config_file(old), old, True
    return {}, new, False


def load_config():
    cfg, _path, _legacy = load_config_with_source()
    return cfg


def save_config(cfg):
    atomic_write_text(config_path(), json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")


def resolve_kb_root(explicit=None):
    """位置优先级：--dir > YOTTA_LEARN_KB > 配置文件 kbDir > 默认。

    兼容回退：新配置不存在时读旧配置（legacy-config）；新默认库未初始化而旧
    默认库已初始化时回退旧默认库（legacy-default），避免已有数据「失联」。"""
    if explicit:
        return Path(explicit).expanduser().resolve(), "flag"
    env = (os.environ.get("YOTTA_LEARN_KB") or "").strip()
    if env:
        return Path(env).expanduser().resolve(), "env"
    cfg, _cfg_path, legacy = load_config_with_source()
    kbdir = str(cfg.get("kbDir") or "").strip()
    if kbdir:
        return Path(kbdir).expanduser().resolve(), ("legacy-config" if legacy else "config")
    new_default = default_kb_root().resolve()
    if is_initialized(new_default):
        return new_default, "default"
    old_default = legacy_default_kb_root().resolve()
    if is_initialized(old_default):
        return old_default, "legacy-default"
    return new_default, "default"


def legacy_location_hint(source):
    """旧版位置的一次性迁移引导（非旧版来源返回空串）。"""
    if source == "legacy-config":
        return ("检测到旧版配置位置（~/.yottaskills/yotta-learn.json）；"
                "建议迁移：yotta-learn kb config set --dir ~/.yottalearn/knowledge --move")
    if source == "legacy-default":
        return ("检测到旧版默认知识库（~/.yottaskills/knowledge）；"
                "建议迁移：yotta-learn kb config set --dir ~/.yottalearn/knowledge --move")
    return ""


LEGACY_SOURCES = ("legacy-config", "legacy-default")


def legacy_source_for_root(root):
    """给定库根是否由旧版位置回退生效；命中返回来源名，否则返回空串。

    仅当未显式指定 --dir / YOTTA_LEARN_KB、解析链确实回退到旧位置且根一致时命中。"""
    resolved, source = resolve_kb_root()
    if source in LEGACY_SOURCES and resolved == Path(root).expanduser().resolve():
        return source
    return ""


def assert_writable(root):
    """写入门：旧版位置只读兼容（fail-closed），命中即拒绝并给出迁移指引。"""
    source = legacy_source_for_root(root)
    if not source:
        return
    raise KbGateError(
        "当前知识库位于旧版位置（%s），0.4.0 起旧位置只读兼容，写入已阻断；请先迁移：%s"
        % (Path(root).expanduser().resolve(), legacy_location_hint(source)))


def location_info(explicit=None):
    """位置解析 + 配置状态（CLI config get / GUI 位置视图同一真源）。"""
    root, source = resolve_kb_root(explicit)
    cfg, cfg_file, _legacy = load_config_with_source()
    info = {"root": str(root), "origin": source, "configFile": str(cfg_file),
            "configExists": cfg_file.exists(), "initialized": is_initialized(root)}
    if info["initialized"]:
        kb_meta = load_kb(root)
        info["schema"] = kb_meta.get("schema")
        info["entries"] = count_entries(root)
    if cfg.get("kbDir"):
        info["kbDir"] = str(cfg["kbDir"])
    if isinstance(cfg.get("unmigrated"), dict):
        info["unmigrated"] = cfg["unmigrated"]
    if isinstance(cfg.get("lastMigration"), dict):
        info["lastMigration"] = cfg["lastMigration"]
    hint = legacy_location_hint(source)
    if hint:
        info["legacyHint"] = hint
    return info


def clear_config():
    """清除位置配置（新 + 旧路径）；返回被删除的文件列表。"""
    removed = []
    for p in (config_path(), legacy_config_path()):
        if p.exists():
            p.unlink()
            removed.append(p)
    return removed


# ── 位置迁移（复制 → 校验 → 旧库移出原位） ─────────────────────────────────

def _is_within(child, parent):
    try:
        Path(child).resolve().relative_to(Path(parent).resolve())
        return True
    except ValueError:
        return False


def kb_tree_digest(root):
    """KB 目录内容摘要（跳过 .lock / 临时文件），用于迁移前后一致性校验。"""
    root = Path(root)
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).as_posix()
        if p.name == ".lock" or p.name.startswith(".ytk-") or p.name.endswith(".tmp"):
            continue
        if p.is_dir():
            h.update(("D\0%s\0" % rel).encode("utf-8"))
        elif p.is_file():
            h.update(("F\0%s\0" % rel).encode("utf-8"))
            with p.open("rb") as fh:
                for chunk in iter(lambda: fh.read(1 << 20), b""):
                    h.update(chunk)
            h.update(b"\0")
    return "sha256:" + h.hexdigest()


def _copy_kb_tree(src, dst):
    def _ignore(_dirpath, names):
        return [n for n in names if n == ".lock"]
    shutil.copytree(str(src), str(dst), ignore=_ignore)


def _verify_migration(src, dst):
    report = doctor(dst)
    if not report.get("ok"):
        first = ""
        for c in report.get("checks", []):
            if c.get("status") == "error":
                first = "：%s" % (c.get("detail") or c.get("name") or "")
                break
        raise KbIntegrityError("迁移校验失败：目标库 doctor 未通过（%d 个错误）%s"
                               % (report.get("errors", 0), first))
    src_digest = kb_tree_digest(src)
    dst_digest = kb_tree_digest(dst)
    if src_digest != dst_digest:
        raise KbIntegrityError("迁移校验失败：源库与目标库内容摘要不一致（源 %s / 目标 %s）"
                               % (src_digest[:19], dst_digest[:19]))
    return {"digest": src_digest,
            "entries": count_entries(dst),
            "categories": len(list_categories(dst))}


def migrate_kb(source_root, target_root, stamp=None):
    """迁移知识库到新位置（复制到暂存 → 校验 → 原子落位）。

    fail-closed：任何一步失败都清理暂存与半成品目标，源库保持不动；本函数
    不切配置、不移旧库（由调用方在成功后再执行）。"""
    source = Path(source_root).expanduser().resolve()
    target = Path(target_root).expanduser().resolve()
    if source == target:
        raise KbUsageError("目标位置与当前库相同：%s" % target)
    if not is_initialized(source):
        raise KbNotFound("当前库未初始化，无法迁移：%s；"
                         "如源库在其他位置，请加 --from <源库> 指定" % source)
    if _is_within(target, source):
        raise KbUsageError("目标位置不能位于源库内部：%s → %s" % (source, target))
    if _is_within(source, target):
        raise KbUsageError("源库不能位于目标位置内部：%s → %s" % (source, target))
    if target.exists():
        if not target.is_dir():
            raise KbIntegrityError("目标已存在且不是目录，拒绝迁移：%s" % target)
        if any(target.iterdir()):
            raise KbIntegrityError("目标目录非空，拒绝迁移（保护现有数据）：%s；"
                                   "请换空目录，或清理后重试" % target)
    stamp = stamp or _timestamp()
    parent = target.parent
    parent.mkdir(parents=True, exist_ok=True)
    staging = parent / ("%s.kb-migrating-%s" % (target.name, stamp))
    for old in parent.glob("%s.kb-migrating-*" % target.name):
        shutil.rmtree(old, ignore_errors=True)
    try:
        _copy_kb_tree(source, staging)
        verify = _verify_migration(source, staging)
        if target.exists():
            target.rmdir()
        _replace_with_retry(staging, target)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return {"from": str(source), "to": str(target), "at": now_iso(),
            "entries": verify["entries"], "categories": verify["categories"],
            "digest": verify["digest"], "stamp": stamp}


def _replace_with_retry(source, destination):
    """Retry Windows sharing violations caused by short-lived scanner handles."""
    for delay in (0.05, 0.1, 0.2, 0.4):
        try:
            os.replace(str(source), str(destination))
            return
        except PermissionError:
            time.sleep(delay)
    os.replace(str(source), str(destination))


def archive_moved_kb(source_root, stamp=None):
    """把旧库移出原位（改名 <原名>.kb-moved-<stamp>），返回新路径。"""
    source = Path(source_root).expanduser().resolve()
    stamp = stamp or _timestamp()
    moved = source.parent / ("%s.kb-moved-%s" % (source.name, stamp))
    n = 2
    while moved.exists():
        moved = source.parent / ("%s.kb-moved-%s-%d" % (source.name, stamp, n))
        n += 1
    _replace_with_retry(source, moved)
    return moved


def _drop_legacy_config():
    """新配置写入成功后清理旧版配置文件（仅位置指针，非知识数据）。"""
    p = legacy_config_path()
    if p.exists():
        p.unlink()
        return p
    return None


def set_location(target_root, move=False, current_root=None):
    """切换 / 迁移知识库位置（CLI 与 GUI 同一真源）。

    move=True：复制 → 校验 → 切配置 → 旧库移出原位（fail-closed：任一步失败
    配置不切、旧库不动、暂存清理）。move=False：只切指针；旧库已初始化且不同
    路径时记录 unmigrated（真实回显，不假成功）。

    返回结果 dict；失败 raise KbError。"""
    target = Path(target_root).expanduser().resolve()
    if current_root is None:
        current_root, _src = resolve_kb_root()
    source = Path(current_root).expanduser().resolve()
    result = {
        "target": str(target), "move": bool(move), "source": str(source),
        "config": str(config_path()), "movedFrom": None, "movedTo": None,
        "sourceLeftAt": None, "entries": 0, "categories": 0, "digest": None,
        "unmigrated": None, "warnings": [], "removedLegacyConfig": None,
    }
    if move:
        report = migrate_kb(source, target)
        cfg = load_config()
        cfg["kbDir"] = str(target)
        cfg["updated_at"] = now_iso()
        cfg["lastMigration"] = {
            "from": report["from"], "to": report["to"], "at": report["at"],
            "entries": report["entries"], "categories": report["categories"],
            "movedTo": None, "sourceLeftAt": None,
        }
        cfg.pop("unmigrated", None)
        save_config(cfg)
        removed = _drop_legacy_config()
        if removed:
            result["removedLegacyConfig"] = str(removed)
        try:
            moved = archive_moved_kb(source, report["stamp"])
            cfg["lastMigration"]["movedTo"] = str(moved)
        except OSError as exc:
            cfg["lastMigration"]["sourceLeftAt"] = str(source)
            result["warnings"].append(
                "旧库未能移出原位：%s（%s）；请手动确认后移动或删除" % (source, exc))
        save_config(cfg)
        result.update({
            "movedFrom": report["from"], "movedTo": cfg["lastMigration"]["movedTo"],
            "sourceLeftAt": cfg["lastMigration"]["sourceLeftAt"],
            "entries": report["entries"], "categories": report["categories"],
            "digest": report["digest"],
        })
        return result

    prev_initialized = is_initialized(source)
    prev_entries = count_entries(source) if prev_initialized else 0
    cfg = load_config()
    cfg["kbDir"] = str(target)
    cfg["updated_at"] = now_iso()
    if prev_initialized and source != target:
        unmigrated = {"from": str(source), "entries": prev_entries, "at": now_iso()}
        cfg["unmigrated"] = unmigrated
        result["unmigrated"] = unmigrated
    else:
        cfg.pop("unmigrated", None)
    save_config(cfg)
    removed = _drop_legacy_config()
    if removed:
        result["removedLegacyConfig"] = str(removed)
    return result


# ── 文件写入（原子）──────────────────────────────────────────────────────────

def atomic_write_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".ytk-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        os.replace(tmp, str(path))
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def atomic_write_json(path, obj):
    atomic_write_text(path, json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def load_json(path, where=None, schema=None):
    where = where or str(path)
    p = Path(path)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise KbIntegrityError("%s 损坏：%s" % (where, exc))
    if not isinstance(data, dict):
        raise KbIntegrityError("%s 格式错误（应为 JSON 对象）" % where)
    if schema and data.get("schema") != schema:
        raise KbIntegrityError("%s schema 不符（期望 %s，实际 %s）"
                               % (where, schema, data.get("schema")))
    return data


# ── 路径布局 ────────────────────────────────────────────────────────────────

def kb_json_path(root):
    return Path(root) / "kb.json"


def categories_dir(root):
    return Path(root) / "categories"


def category_dir(root, slug):
    return categories_dir(root) / slug


def category_json_path(root, slug):
    return category_dir(root, slug) / "category.json"


def entries_dir(root, slug):
    return category_dir(root, slug) / "entries"


def category_index_path(root, slug):
    return category_dir(root, slug) / "index.json"


def index_dir(root):
    return Path(root) / "index"


def global_index_path(root):
    return index_dir(root) / "global.json"


def stats_path(root):
    return index_dir(root) / "stats.json"


def audit_path(root):
    return Path(root) / "audit" / "audit.jsonl"


def trash_dir(root):
    return Path(root) / ".trash"


def snapshots_dir(root):
    return Path(root) / "snapshots"


def lock_path(root):
    return Path(root) / ".lock"


def is_initialized(root):
    return kb_json_path(root).is_file()


def load_kb(root):
    data = load_json(kb_json_path(root), where="kb.json")
    if data is None:
        raise KbNotFound("知识库未初始化：%s（先运行 yotta-learn kb init）" % root)
    if data.get("schema") != KB_SCHEMA:
        raise KbIntegrityError("kb.json schema 不符（期望 %s，实际 %s）"
                               % (KB_SCHEMA, data.get("schema")))
    return data


def init_kb(root, actor):
    """初始化知识库（fail-closed：已存在或目录非空时拒绝覆盖）。"""
    root = Path(root)
    assert_writable(root)
    if kb_json_path(root).exists():
        raise KbIntegrityError("知识库已存在（kb.json），init 拒绝覆盖：%s；如需重建先手动备份" % root)
    if root.exists() and any(root.iterdir()):
        raise KbIntegrityError("目录非空且不含 kb.json，拒绝初始化（保护现有数据）：%s" % root)
    root.mkdir(parents=True, exist_ok=True)
    for d in (categories_dir(root), index_dir(root), root / "audit",
              trash_dir(root), snapshots_dir(root)):
        d.mkdir(parents=True, exist_ok=True)
    kb = {"schema": KB_SCHEMA, "name": root.name, "created": now_iso(), "created_by": actor}
    atomic_write_json(kb_json_path(root), kb)
    atomic_write_json(global_index_path(root),
                      {"schema": GLOBAL_SCHEMA, "built_at": now_iso(),
                       "categories": {}, "terms": {}})
    atomic_write_json(stats_path(root),
                      {"schema": STATS_SCHEMA, "built_at": now_iso(), "total_entries": 0,
                       "by_status": {}, "by_category": {}, "terms": 0})
    audit(root, actor, "kb.init", str(root), "ok", {"schema": KB_SCHEMA})
    return kb


# ── 写锁（跨进程）───────────────────────────────────────────────────────────

class KbLock:
    """跨进程写锁：O_EXCL 锁文件 + 过期接管；默认超时 10s（可用环境变量覆盖）。"""

    def __init__(self, root, timeout=None, stale_after=LOCK_STALE_SECONDS,
                 allow_legacy=False):
        self.root = Path(root)
        self.allow_legacy = allow_legacy
        self.path = lock_path(root)
        if timeout is None:
            try:
                timeout = float(os.environ.get("YOTTA_LEARN_LOCK_TIMEOUT", "10"))
            except ValueError:
                timeout = 10.0
        self.timeout = max(0.0, timeout)
        self.stale_after = stale_after
        self.acquired = False

    def __enter__(self):
        if not self.allow_legacy:
            assert_writable(self.root)
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, ("%d %s\n" % (os.getpid(), now_iso())).encode("utf-8"))
                os.close(fd)
                self.acquired = True
                return self
            except FileExistsError:
                try:
                    age = time.time() - self.path.stat().st_mtime
                except OSError:
                    age = 0.0
                if age > self.stale_after:
                    try:
                        self.path.unlink()
                    except OSError:
                        pass
                    continue
                if time.monotonic() >= deadline:
                    raise KbIntegrityError(
                        "写锁超时：另一进程正在写入（%s）；稍后重试" % self.path)
                time.sleep(0.1)

    def __exit__(self, exc_type, exc, tb):
        if self.acquired:
            try:
                self.path.unlink()
            except OSError:
                pass
        self.acquired = False
        return False


def refresh_index(root, slugs=None):
    """刷新索引（懒加载 yotta_kb_index，避免模块循环依赖）。"""
    try:
        import yotta_kb_index
    except ImportError as exc:
        raise KbIntegrityError("索引组件缺失（yotta_kb_index.py）：%s" % exc)
    yotta_kb_index.refresh(root, slugs=slugs)


# ── frontmatter（受控子集：单行键值 + 单引号字符串 + JSON 数组）──────────────

FM_KEYS = ("id", "title", "category", "tags", "status", "confidence",
           "source", "evidence", "author", "created", "updated",
           "verified_by", "verified_at", "related")
FM_REQUIRED = ("id", "title", "category", "status", "source", "author", "created")
_BARE_FIELDS = frozenset(("id", "category", "status", "confidence", "author"))
_FM_LINE_RE = re.compile(r"^([a-z][a-z0-9_]*):\s?(.*)$")
_QUOTED_RE = re.compile(r"^'((?:[^']|'')*)'(?:\s+#.*)?$")
_BARE_OK_RE = re.compile(r"^[A-Za-z0-9_@][A-Za-z0-9_@.:+/-]*$")


def _parse_scalar(key, raw, where):
    raw = raw.strip()
    if key in ("tags", "related"):
        m = re.match(r"^(\[.*\])(?:\s+#.*)?$", raw)
        if not m:
            raise KbIntegrityError("%s: 字段 %s 需为 JSON 数组" % (where, key))
        try:
            val = json.loads(m.group(1))
        except ValueError as exc:
            raise KbIntegrityError("%s: 字段 %s 数组解析失败：%s" % (where, key, exc))
        if not isinstance(val, list) or not all(isinstance(x, str) for x in val):
            raise KbIntegrityError("%s: 字段 %s 需为字符串数组" % (where, key))
        return val
    if raw.startswith("'"):
        m = _QUOTED_RE.match(raw)
        if not m:
            raise KbIntegrityError("%s: 字段 %s 单引号未闭合" % (where, key))
        return m.group(1).replace("''", "'")
    if raw.startswith("["):
        raise KbIntegrityError("%s: 字段 %s 不是数组字段却以 [ 开头" % (where, key))
    return raw.split(" #", 1)[0].strip()


def parse_entry_text(text, where="<entry>"):
    """解析条目 markdown → (fields, body)；fail-closed。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise KbIntegrityError("%s: 缺少 frontmatter 起始 '---'" % where)
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise KbIntegrityError("%s: frontmatter 未闭合（缺少结束 '---'）" % where)
    fields = {}
    for ln in lines[1:end]:
        if not ln.strip():
            continue
        m = _FM_LINE_RE.match(ln)
        if not m:
            raise KbIntegrityError("%s: 无法解析字段行：%s" % (where, ln[:80]))
        key, raw = m.group(1), m.group(2)
        if key not in FM_KEYS:
            raise KbIntegrityError("%s: 未知字段 '%s'（受控 frontmatter 子集，拒绝解析）"
                                   % (where, key))
        fields[key] = _parse_scalar(key, raw, where)
    body = "\n".join(lines[end + 1:]).strip("\n")
    return fields, body


def _fmt_scalar(key, value):
    if key in ("tags", "related"):
        return json.dumps(list(value or []), ensure_ascii=False)
    s = "" if value is None else str(value)
    if "\n" in s or "\r" in s:
        raise KbUsageError("字段 %s 不允许换行（frontmatter 只允许单行键值）" % key)
    if key in _BARE_FIELDS and s and _BARE_OK_RE.match(s):
        return s
    return "'" + s.replace("'", "''") + "'"


def dump_entry_text(fields, body):
    lines = ["---"]
    for key in FM_KEYS:
        if key in fields:
            lines.append("%s: %s" % (key, _fmt_scalar(key, fields[key])))
    lines.append("---")
    text = "\n".join(lines) + "\n"
    body = (body or "").strip("\n")
    if body:
        text += "\n" + body + "\n"
    return text


def validate_entry_fields(fields, where="<entry>"):
    for key in FM_REQUIRED:
        val = fields.get(key)
        if val is None or (isinstance(val, str) and not val.strip()):
            raise KbIntegrityError("%s: 缺少必填字段 %s" % (where, key))
    if not ENTRY_ID_RE.match(str(fields.get("id"))):
        raise KbIntegrityError("%s: 条目 ID 非法：%s" % (where, fields.get("id")))
    if not SLUG_RE.match(str(fields.get("category"))):
        raise KbIntegrityError("%s: category 非法：%s" % (where, fields.get("category")))
    if fields.get("status") not in ENTRY_STATUSES:
        raise KbIntegrityError("%s: status 非法：%s（可用 %s）"
                               % (where, fields.get("status"), " / ".join(ENTRY_STATUSES)))
    conf = fields.get("confidence", "medium")
    if conf not in CONFIDENCES:
        raise KbIntegrityError("%s: confidence 非法：%s（可用 %s）"
                               % (where, conf, " / ".join(CONFIDENCES)))
    for key in ("tags", "related"):
        val = fields.get(key, [])
        if not isinstance(val, list):
            raise KbIntegrityError("%s: 字段 %s 需为数组" % (where, key))
    return fields


# ── 条目模型 ────────────────────────────────────────────────────────────────

class KbEntry:
    def __init__(self, path, fields, body):
        self.path = Path(path)
        self.fields = fields
        self.body = body

    @property
    def id(self):
        return str(self.fields.get("id", ""))

    @property
    def title(self):
        return str(self.fields.get("title", ""))

    @property
    def category(self):
        return str(self.fields.get("category", ""))

    @property
    def status(self):
        return str(self.fields.get("status", ""))

    @property
    def confidence(self):
        return str(self.fields.get("confidence", "medium"))

    @property
    def tags(self):
        return list(self.fields.get("tags", []))

    @property
    def updated(self):
        return str(self.fields.get("updated", "")) or str(self.fields.get("created", ""))

    def to_dict(self, include_body=False):
        data = dict(self.fields)
        data["path"] = str(self.path)
        if include_body:
            data["body"] = self.body
        return data


def load_entry(path):
    path = Path(path)
    text = read_text(path)
    fields, body = parse_entry_text(text, where=str(path))
    validate_entry_fields(fields, where=str(path))
    return KbEntry(path, fields, body)


def save_entry(entry):
    atomic_write_text(entry.path, dump_entry_text(entry.fields, entry.body))


def new_entry_fields(eid, title, category, tags, source, evidence,
                     confidence, author, created=None):
    created = created or now_iso()
    return {
        "id": eid, "title": title, "category": category,
        "tags": list(tags or []), "status": "draft",
        "confidence": confidence or "medium", "source": source,
        "evidence": evidence or "", "author": author,
        "created": created, "updated": created,
        "verified_by": "", "verified_at": "", "related": [],
    }


def iter_entries(root, category=None):
    """遍历条目（fail-closed：条目损坏时抛错）。category=None 时遍历全部分类。"""
    if category:
        slugs = [category]
    else:
        slugs = [c["slug"] for c in list_categories(root)]
    for slug in slugs:
        d = entries_dir(root, slug)
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.md")):
            yield load_entry(f)


def find_entry(root, eid):
    target = (eid or "").strip().upper()
    for entry in iter_entries(root):
        if entry.id.upper() == target:
            return entry
    return None


def next_entry_id(root):
    prefix = "KB-%s-" % _today()
    used = set()
    cdir = categories_dir(root)
    if cdir.is_dir():
        for f in cdir.glob("*/entries/*.md"):
            if f.stem.startswith(prefix):
                used.add(f.stem)
    tdir = trash_dir(root)
    if tdir.is_dir():
        for f in tdir.glob("*.md"):
            name = f.stem
            idx = name.rfind("KB-")
            if idx >= 0:
                name = name[idx:]
            if name.startswith(prefix):
                used.add(name)
    seq = 1
    while "%s%03d" % (prefix, seq) in used:
        seq += 1
    return "%s%03d" % (prefix, seq)


# ── 分类注册表 ──────────────────────────────────────────────────────────────

def validate_category(cat, where="<category>"):
    slug = str(cat.get("slug") or "")
    if not SLUG_RE.match(slug):
        raise KbIntegrityError("%s: slug 非法：%s" % (where, slug))
    for key in ("name", "description"):
        if not str(cat.get(key) or "").strip():
            raise KbIntegrityError("%s: 缺少 %s" % (where, key))
    if cat.get("status") not in CATEGORY_STATUSES:
        raise KbIntegrityError("%s: status 非法：%s" % (where, cat.get("status")))
    aliases = cat.get("aliases", [])
    if not isinstance(aliases, list) or not all(isinstance(a, str) for a in aliases):
        raise KbIntegrityError("%s: aliases 需为字符串数组" % where)
    return cat


def load_category(root, slug):
    p = category_json_path(root, slug)
    if not p.is_file():
        raise KbNotFound("分类不存在：%s（可用 kb category list 查看）" % slug)
    cat = load_json(p, where="category.json(%s)" % slug)
    validate_category(cat, where=str(p))
    if cat["slug"] != slug:
        raise KbIntegrityError("%s: slug 与目录名不一致（%s != %s）"
                               % (p, cat["slug"], slug))
    return cat


def list_categories(root, include_deprecated=True):
    out = []
    cdir = categories_dir(root)
    if not cdir.is_dir():
        return out
    for d in sorted(cdir.iterdir()):
        if not d.is_dir():
            continue
        p = d / "category.json"
        if not p.is_file():
            continue
        cat = load_json(p, where="category.json(%s)" % d.name)
        validate_category(cat, where=str(p))
        if not include_deprecated and cat.get("status") == "deprecated":
            continue
        out.append(cat)
    return out


def alias_map(root):
    mapping = {}
    for cat in list_categories(root):
        for alias in cat.get("aliases", []):
            mapping[alias] = cat["slug"]
    return mapping


def resolve_category(root, slug):
    """解析分类：别名 → 主分类；已合并 → 目标；已停用（无合并）→ 报错。"""
    slug = (slug or "").strip()
    cats = {c["slug"]: c for c in list_categories(root)}
    if slug in cats:
        cat = cats[slug]
        if cat.get("status") == "deprecated":
            target = cat.get("merged_into")
            if target and target in cats:
                return cats[target]
            raise KbUsageError("分类已停用：%s" % slug)
        return cat
    target = alias_map(root).get(slug)
    if target and target in cats:
        return cats[target]
    raise KbUsageError("分类不存在：%s（先 kb category create 创建，或 kb category list 查看）" % slug)


def create_category(root, slug, name, description, aliases, actor):
    slug = (slug or "").strip()
    if not SLUG_RE.match(slug):
        raise KbUsageError("slug 非法：%s（小写字母开头，2-39 位 a-z0-9-）" % slug)
    name = (name or "").strip()
    description = (description or "").strip()
    if not name:
        raise KbUsageError("分类需要 --name（中文名）")
    if not description:
        raise KbUsageError("分类需要 --description（一句话说明）")
    taken = set(c["slug"] for c in list_categories(root)) | set(alias_map(root))
    if slug in taken:
        raise KbUsageError("分类已存在（或与别名冲突）：%s" % slug)
    aliases = [a.strip() for a in (aliases or []) if a and a.strip()]
    seen = set()
    for alias in aliases:
        if not SLUG_RE.match(alias):
            raise KbUsageError("别名非法：%s（小写字母开头，2-39 位 a-z0-9-）" % alias)
        if alias in taken or alias in seen:
            raise KbUsageError("别名冲突：%s" % alias)
        seen.add(alias)
    cat = {
        "slug": slug, "name": name, "description": description,
        "aliases": aliases, "status": "active",
        "created_by": actor, "created_at": now_iso(), "updated_at": now_iso(),
    }
    with KbLock(root):
        entries_dir(root, slug).mkdir(parents=True, exist_ok=True)
        atomic_write_json(category_json_path(root, slug), cat)
        audit(root, actor, "kb.category.create", slug, "ok", {"name": name})
        refresh_index(root, slugs=[slug])
    return cat


def rename_category(root, slug, new_name, actor):
    cat = load_category(root, slug)
    new_name = (new_name or "").strip()
    if not new_name:
        raise KbUsageError("rename 需要 --name（新中文名）")
    with KbLock(root):
        old = cat["name"]
        cat["name"] = new_name
        cat["updated_at"] = now_iso()
        atomic_write_json(category_json_path(root, slug), cat)
        audit(root, actor, "kb.category.rename", slug, "ok", {"from": old, "to": new_name})
    return cat


def merge_category(root, from_slug, into_slug, actor):
    from_slug = (from_slug or "").strip()
    into_slug = (into_slug or "").strip()
    if from_slug == into_slug:
        raise KbUsageError("merge 的源与目标不能相同")
    source = load_category(root, from_slug)
    if source.get("status") == "deprecated":
        raise KbUsageError("源分类已停用：%s" % from_slug)
    target = resolve_category(root, into_slug)
    into_slug = target["slug"]
    moved = 0
    with KbLock(root):
        create_snapshot(root, "merge-%s-into-%s" % (from_slug, into_slug))
        src_entries = entries_dir(root, from_slug)
        dst_entries = entries_dir(root, into_slug)
        dst_entries.mkdir(parents=True, exist_ok=True)
        for f in sorted(src_entries.glob("*.md")):
            entry = load_entry(f)
            entry.fields["category"] = into_slug
            entry.fields["updated"] = now_iso()
            dest = dst_entries / f.name
            if dest.exists():
                raise KbIntegrityError("合并冲突：目标分类已存在同名条目 %s" % dest.name)
            save_entry(KbEntry(dest, entry.fields, entry.body))
            f.unlink()
            moved += 1
        if from_slug not in target.get("aliases", []):
            target.setdefault("aliases", []).append(from_slug)
        target["updated_at"] = now_iso()
        atomic_write_json(category_json_path(root, into_slug), target)
        source["status"] = "deprecated"
        source["merged_into"] = into_slug
        source["updated_at"] = now_iso()
        atomic_write_json(category_json_path(root, from_slug), source)
        audit(root, actor, "kb.category.merge", from_slug, "ok",
              {"into": into_slug, "moved": moved})
        refresh_index(root, slugs=[from_slug, into_slug])
    return {"from": from_slug, "into": into_slug, "moved": moved}


def deprecate_category(root, slug, actor, reason="", force=False):
    cat = load_category(root, slug)
    if cat.get("status") == "deprecated":
        raise KbUsageError("分类已停用：%s" % slug)
    count = len(list(entries_dir(root, slug).glob("*.md"))) if entries_dir(root, slug).is_dir() else 0
    if count and not force:
        raise KbUsageError("分类下仍有 %d 条条目：%s；先 merge 迁移，或 --force 强制停用" % (count, slug))
    with KbLock(root):
        create_snapshot(root, "deprecate-category-%s" % slug)
        cat["status"] = "deprecated"
        cat["updated_at"] = now_iso()
        atomic_write_json(category_json_path(root, slug), cat)
        audit(root, actor, "kb.category.deprecate", slug, "ok",
              {"reason": reason, "entries": count})
        refresh_index(root, slugs=[slug])
    return cat


# ── 条目操作 ────────────────────────────────────────────────────────────────

def add_entry(root, category, title, message, tags, source, evidence,
              confidence, actor):
    cat = resolve_category(root, category)
    title = (title or "").strip()
    message = (message or "").strip("\n")
    source = (source or "").strip()
    if not title:
        raise KbUsageError("kb add 需要 --title")
    if not message.strip():
        raise KbUsageError("kb add 需要 --message（知识正文）")
    if not source:
        raise KbUsageError("kb add 需要 --source（出处：URL / 文件 / 会话）")
    if confidence not in CONFIDENCES:
        raise KbUsageError("confidence 非法：%s（可用 %s）" % (confidence, " / ".join(CONFIDENCES)))
    tags = [t.strip() for t in (tags or []) if t and t.strip()]
    with KbLock(root):
        eid = next_entry_id(root)
        fields = new_entry_fields(eid, title, cat["slug"], tags, source,
                                  evidence, confidence, actor)
        path = entries_dir(root, cat["slug"]) / (eid + ".md")
        save_entry(KbEntry(path, fields, message))
        audit(root, actor, "kb.add", eid, "ok",
              {"category": cat["slug"], "title": title})
        refresh_index(root, slugs=[cat["slug"]])
    return KbEntry(path, fields, message)


def update_entry(root, eid, changes, actor):
    entry = find_entry(root, eid)
    if entry is None:
        raise KbNotFound("未找到条目：%s" % eid)
    applied = {}
    with KbLock(root):
        if "title" in changes:
            title = (changes["title"] or "").strip()
            if not title:
                raise KbUsageError("title 不能为空")
            entry.fields["title"] = title
            applied["title"] = title
        if "message" in changes:
            message = (changes["message"] or "").strip("\n")
            if not message.strip():
                raise KbUsageError("message 不能为空")
            entry.body = message
            applied["message"] = "updated"
        if "tags" in changes:
            entry.fields["tags"] = [t.strip() for t in (changes["tags"] or []) if t and t.strip()]
            applied["tags"] = entry.fields["tags"]
        if "source" in changes:
            source = (changes["source"] or "").strip()
            if not source:
                raise KbUsageError("source 不能为空")
            entry.fields["source"] = source
            applied["source"] = source
        if "evidence" in changes:
            entry.fields["evidence"] = (changes["evidence"] or "").strip()
            applied["evidence"] = "updated"
        if "confidence" in changes:
            conf = changes["confidence"]
            if conf not in CONFIDENCES:
                raise KbUsageError("confidence 非法：%s" % conf)
            entry.fields["confidence"] = conf
            applied["confidence"] = conf
        if not applied:
            raise KbUsageError("未提供任何更新字段")
        entry.fields["updated"] = now_iso()
        save_entry(entry)
        audit(root, actor, "kb.update", entry.id, "ok",
              {"fields": sorted(applied.keys())})
        refresh_index(root, slugs=[entry.category])
    return entry


def deprecate_entry(root, eid, reason, actor):
    entry = find_entry(root, eid)
    if entry is None:
        raise KbNotFound("未找到条目：%s" % eid)
    if entry.status == "deprecated":
        raise KbUsageError("条目已停用：%s" % eid)
    reason = (reason or "").strip()
    if not reason:
        raise KbUsageError("deprecate 需要 --reason（停用原因）")
    with KbLock(root):
        create_snapshot(root, "deprecate-%s" % entry.id)
        entry.fields["status"] = "deprecated"
        entry.fields["updated"] = now_iso()
        save_entry(entry)
        audit(root, actor, "kb.deprecate", entry.id, "ok", {"reason": reason})
        refresh_index(root, slugs=[entry.category])
    return entry


def move_to_trash(root, entry, actor, reason=""):
    tdir = trash_dir(root)
    tdir.mkdir(parents=True, exist_ok=True)
    base = "%s-%s-%s" % (_timestamp(), entry.category, entry.id)
    dest = tdir / (base + ".md")
    n = 2
    while dest.exists():
        dest = tdir / ("%s-%d.md" % (base, n))
        n += 1
    os.replace(str(entry.path), str(dest))
    audit(root, actor, "kb.trash.add", entry.id, "ok",
          {"category": entry.category, "reason": reason, "path": str(dest)})
    return dest


def list_trash(root):
    tdir = trash_dir(root)
    items = []
    if not tdir.is_dir():
        return items
    for f in sorted(tdir.glob("*.md")):
        try:
            mtime = f.stat().st_mtime
        except OSError:
            continue
        items.append({
            "path": str(f),
            "name": f.name,
            "age_days": max(0.0, (time.time() - mtime) / 86400.0),
        })
    items.sort(key=lambda x: x["name"])
    return items


def purge_trash(root, actor, days=TRASH_RETENTION_DAYS, purge_all=False):
    removed = 0
    kept = 0
    with KbLock(root):
        for item in list_trash(root):
            if purge_all or item["age_days"] >= days:
                try:
                    os.unlink(item["path"])
                    removed += 1
                except OSError:
                    kept += 1
            else:
                kept += 1
        audit(root, actor, "kb.trash.purge", str(root), "ok",
              {"removed": removed, "kept": kept, "days": days, "all": purge_all})
    return {"removed": removed, "kept": kept}


# ── 审计 ────────────────────────────────────────────────────────────────────

def audit(root, actor, action, target="", result="ok", detail=None):
    record = {"ts": now_iso(), "actor": actor, "action": action,
              "target": target, "result": result}
    if detail:
        record["detail"] = detail
    p = audit_path(root)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(str(p), "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_audit(root, limit=20):
    p = audit_path(root)
    if not p.is_file():
        return []
    lines = read_text(p).splitlines()
    out = []
    for line in lines[-limit:]:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


# ── 快照 ────────────────────────────────────────────────────────────────────

def _file_sha256(path):
    h = hashlib.sha256()
    with open(str(path), "rb") as fh:
        while True:
            chunk = fh.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def create_snapshot(root, op, keep=SNAPSHOT_KEEP):
    base = snapshots_dir(root) / ("%s-%s" % (_timestamp(), op))
    n = 2
    while base.exists():
        base = snapshots_dir(root) / ("%s-%s-%d" % (_timestamp(), op, n))
        n += 1
    base.mkdir(parents=True, exist_ok=True)
    if categories_dir(root).is_dir():
        shutil.copytree(str(categories_dir(root)), str(base / "categories"))
    if kb_json_path(root).is_file():
        shutil.copy2(str(kb_json_path(root)), str(base / "kb.json"))
    files = {}
    for f in sorted(base.rglob("*")):
        if f.is_file() and f.name != "manifest.json":
            files[f.relative_to(base).as_posix()] = _file_sha256(f)
    atomic_write_json(base / "manifest.json", {
        "schema": SNAPSHOT_SCHEMA, "op": op, "created": now_iso(),
        "source": str(root), "files": files,
    })
    _prune_snapshots(root, keep)
    return base


def _prune_snapshots(root, keep):
    snaps = sorted([d for d in snapshots_dir(root).iterdir() if d.is_dir()],
                   key=lambda d: d.name)
    while len(snaps) > keep:
        victim = snaps.pop(0)
        shutil.rmtree(str(victim), ignore_errors=True)


def list_snapshots(root):
    out = []
    sdir = snapshots_dir(root)
    if not sdir.is_dir():
        return out
    for d in sorted(sdir.iterdir(), key=lambda x: x.name, reverse=True):
        if not d.is_dir():
            continue
        manifest = d / "manifest.json"
        if not manifest.is_file():
            continue
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        out.append({
            "name": d.name, "op": data.get("op", ""),
            "created": data.get("created", ""),
            "files": len(data.get("files", {})),
            "path": str(d),
        })
    return out


def restore_snapshot(root, name, actor):
    snaps = {s["name"]: s for s in list_snapshots(root)}
    if name not in snaps:
        raise KbNotFound("未找到快照：%s（可用 kb snapshot list 查看）" % name)
    src = Path(snaps[name]["path"])
    if not (src / "categories").is_dir():
        raise KbIntegrityError("快照损坏（缺 categories/）：%s" % src)
    with KbLock(root):
        create_snapshot(root, "pre-restore")
        target = categories_dir(root)
        if target.exists():
            shutil.rmtree(str(target))
        shutil.copytree(str(src / "categories"), str(target))
        audit(root, actor, "kb.snapshot.restore", name, "ok", {"source": str(src)})
        refresh_index(root)
    return name


# ── 备份 ────────────────────────────────────────────────────────────────────

def count_entries(root):
    count = 0
    cdir = categories_dir(root)
    if cdir.is_dir():
        count = len(list(cdir.glob("*/entries/*.md")))
    return count


def backup_create(root, out_dir, actor):
    load_kb(root)
    out = Path(out_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    base = "%s-%s" % (Path(root).name or "kb", _timestamp())
    dest = out / base
    n = 2
    while dest.exists():
        dest = out / ("%s-%d" % (base, n))
        n += 1
    with KbLock(root, allow_legacy=True):
        dest.mkdir(parents=True)
        for item in sorted(Path(root).iterdir()):
            if item.name in ("snapshots", ".lock"):
                continue
            if item.is_dir():
                shutil.copytree(str(item), str(dest / item.name))
            else:
                shutil.copy2(str(item), str(dest / item.name))
        files = {}
        for f in sorted(dest.rglob("*")):
            if f.is_file() and f.name != "manifest.json":
                files[f.relative_to(dest).as_posix()] = _file_sha256(f)
        manifest = {
            "schema": BACKUP_SCHEMA, "name": dest.name, "created": now_iso(),
            "source": str(root), "entries": count_entries(root),
            "files": files,
        }
        atomic_write_json(dest / "manifest.json", manifest)
        audit(root, actor, "kb.backup.create", dest.name, "ok",
              {"out": str(out), "files": len(files)})
    return dest, manifest


def backup_list(out_dir):
    out = Path(out_dir).expanduser().resolve()
    items = []
    if not out.is_dir():
        return items
    for d in sorted(out.iterdir(), key=lambda x: x.name, reverse=True):
        if not d.is_dir():
            continue
        manifest = d / "manifest.json"
        if not manifest.is_file():
            continue
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if data.get("schema") != BACKUP_SCHEMA:
            continue
        items.append({
            "name": data.get("name") or d.name,
            "created": data.get("created", ""),
            "entries": data.get("entries", 0),
            "files": len(data.get("files", {})),
            "path": str(d),
        })
    return items


def backup_restore(out_dir, name, into, actor, force=False):
    out = Path(out_dir).expanduser().resolve()
    src = out / name
    manifest = src / "manifest.json"
    if not src.is_dir() or not manifest.is_file():
        raise KbNotFound("未找到备份：%s（在 %s 下；可用 kb backup list --out 查看）" % (name, out))
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise KbIntegrityError("备份 manifest 损坏：%s" % exc)
    if data.get("schema") != BACKUP_SCHEMA:
        raise KbIntegrityError("备份 schema 不符：%s" % data.get("schema"))
    target = Path(into).expanduser().resolve()
    if target == Path(target.anchor) or target == Path.home().resolve():
        raise KbUsageError("恢复目标不能是盘根或用户主目录：%s" % target)
    if target.exists() and any(target.iterdir()):
        if not force:
            raise KbIntegrityError("目标目录非空，拒绝覆盖：%s（--force 显式允许）" % target)
        shutil.rmtree(str(target))
    if not target.exists():
        target.mkdir(parents=True)
    for item in sorted(src.iterdir()):
        if item.name == "manifest.json":
            continue
        if item.is_dir():
            shutil.copytree(str(item), str(target / item.name))
        else:
            shutil.copy2(str(item), str(target / item.name))
    load_kb(target)
    with KbLock(target):
        audit(target, actor, "kb.backup.restore", name, "ok",
              {"from": str(src), "into": str(target)})
        refresh_index(target)
    return target


# ── 敏感扫描与查重 ──────────────────────────────────────────────────────────

SENSITIVE_PATTERNS = (
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("aws-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("secret-assignment",
     re.compile(r"(?i)\b(api[_-]?key|token|secret|password|passwd|pwd)\b"
                r"\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}")),
    ("windows-user-path", re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+")),
    ("unix-home-path", re.compile(r"/(?:home|Users)/[^/\s]+")),
    ("cn-id-card", re.compile(r"\b\d{17}[\dXx]\b")),
    ("cn-phone", re.compile(r"\b1[3-9]\d{9}\b")),
)


def scan_sensitive(text):
    findings = []
    text = text or ""
    for kind, rx in SENSITIVE_PATTERNS:
        for m in rx.finditer(text):
            findings.append({
                "kind": kind,
                "line": text[:m.start()].count("\n") + 1,
            })
    return findings


def normalize_title(text):
    return re.sub(r"[\s\W_]+", "", (text or "").lower())


def find_duplicate(root, entry):
    norm = normalize_title(entry.title)
    if not norm:
        return None
    for other in iter_entries(root, entry.category):
        if other.id == entry.id or other.status == "deprecated":
            continue
        if normalize_title(other.title) == norm:
            return other
    return None


def similar_titles(root, entry, threshold=0.8):
    base = set(normalize_title(entry.title))
    if not base:
        return []
    out = []
    for other in iter_entries(root, entry.category):
        if other.id == entry.id or other.status == "deprecated":
            continue
        other_set = set(normalize_title(other.title))
        if not other_set:
            continue
        jaccard = len(base & other_set) / float(len(base | other_set))
        if jaccard >= threshold:
            out.append({"id": other.id, "title": other.title, "similarity": round(jaccard, 3)})
    out.sort(key=lambda x: -x["similarity"])
    return out


def review_entry(root, eid, decision, note, evidence, actor, force=False):
    """审核门：三问清单由 CLI 展示；pass / reject 在此执行。"""
    entry = find_entry(root, eid)
    if entry is None:
        raise KbNotFound("未找到条目：%s" % eid)
    if decision == "pass":
        if entry.status == "verified":
            raise KbUsageError("条目已是 verified：%s" % eid)
        if entry.status == "deprecated":
            raise KbUsageError("条目已停用，不能核验：%s" % eid)
        text = "\n".join([entry.title, " ".join(entry.tags),
                          str(entry.fields.get("source", "")), entry.body])
        findings = scan_sensitive(text)
        if findings and not force:
            kinds = ", ".join(sorted(set(f["kind"] for f in findings)))
            raise KbGateError("敏感扫描命中 %d 处（%s）；处理后重试，或 --force --note 说明后放行"
                              % (len(findings), kinds))
        if findings and force and not (note or "").strip():
            raise KbUsageError("--force 放行敏感命中需同时提供 --note 说明")
        evidence = (evidence or "").strip() or str(entry.fields.get("evidence", "")).strip()
        if not evidence:
            raise KbUsageError("核验通过需要 --evidence（或条目已有 evidence）")
        dup = find_duplicate(root, entry)
        if dup is not None and not force:
            raise KbGateError("发现同分类疑似重复条目 %s（标题一致）；确认不重复后 --force 放行"
                              % dup.id)
        similar = similar_titles(root, entry)
        with KbLock(root):
            entry.fields["evidence"] = evidence
            entry.fields["status"] = "verified"
            entry.fields["verified_by"] = actor
            entry.fields["verified_at"] = now_iso()
            entry.fields["updated"] = now_iso()
            save_entry(entry)
            audit(root, actor, "kb.review.pass", entry.id, "ok",
                  {"note": note or "", "forced": bool(force),
                   "sensitive": [f["kind"] for f in findings],
                   "duplicate": dup.id if dup else ""})
            refresh_index(root, slugs=[entry.category])
        return entry, {"findings": findings, "duplicate": dup.id if dup else "",
                       "similar": similar}
    if decision == "reject":
        if not (note or "").strip():
            raise KbUsageError("reject 需要 --note（拒绝原因）")
        with KbLock(root):
            create_snapshot(root, "reject-%s" % entry.id)
            audit(root, actor, "kb.review.reject", entry.id, "ok", {"note": note})
            move_to_trash(root, entry, actor, reason=note)
            refresh_index(root, slugs=[entry.category])
        return entry, {"trashed": True}
    raise KbUsageError("review 需要 --pass 或 --reject（不带时只显示三问清单）")


# ── doctor ──────────────────────────────────────────────────────────────────

def _dir_size(path):
    total = 0
    p = Path(path)
    if not p.is_dir():
        return 0
    for f in p.rglob("*"):
        try:
            if f.is_file():
                total += f.stat().st_size
        except OSError:
            continue
    return total


def doctor(root, backup_dir=None):
    checks = []
    errors = 0
    warnings = 0

    def add(name, status, detail=""):
        nonlocal errors, warnings
        if status == "error":
            errors += 1
        elif status == "warn":
            warnings += 1
        checks.append({"name": name, "status": status, "detail": detail})

    try:
        kb = load_kb(root)
        add("kb.json", "ok", "schema %s" % kb.get("schema"))
    except KbError as exc:
        add("kb.json", "error", exc.message)
        return {"checks": checks, "errors": errors, "warnings": warnings,
                "ok": False, "root": str(root)}

    cats = []
    cdir = categories_dir(root)
    if cdir.is_dir():
        for d in sorted(cdir.iterdir()):
            if not d.is_dir():
                continue
            try:
                cats.append(load_category(root, d.name))
            except KbError as exc:
                add("category:%s" % d.name, "error", exc.message)
    add("categories", "ok", "%d 个分类" % len(cats))

    entry_count = 0
    entry_errors = 0
    for cat in cats:
        d = entries_dir(root, cat["slug"])
        if not d.is_dir():
            add("entries:%s" % cat["slug"], "error", "缺少 entries/ 目录")
            continue
        for f in sorted(d.glob("*.md")):
            entry_count += 1
            try:
                load_entry(f)
            except KbError as exc:
                entry_errors += 1
                add("entry:%s" % f.name, "error", exc.message)
        for f in sorted(d.iterdir()):
            if f.is_file() and f.suffix != ".md":
                add("entry-file:%s/%s" % (cat["slug"], f.name), "warn",
                    "entries/ 下存在非 .md 文件（忽略）")
    if entry_errors == 0:
        add("entries", "ok", "%d 条" % entry_count)

    try:
        import yotta_kb_index
        status = yotta_kb_index.index_status(root)
        if status.get("drift"):
            drifted = [c["slug"] for c in status["categories"] if c["drift"]]
            if status.get("global_drift"):
                drifted.append("global")
            add("index", "warn", "索引漂移：%s；运行 kb index rebuild" % ", ".join(drifted))
        else:
            add("index", "ok", "与条目一致")
    except KbError as exc:
        add("index", "error", exc.message)
    except ImportError as exc:
        add("index", "error", "索引组件缺失：%s" % exc)

    lock = lock_path(root)
    if lock.exists():
        try:
            age = time.time() - lock.stat().st_mtime
        except OSError:
            age = 0.0
        if age > LOCK_STALE_SECONDS:
            add("lock", "warn", "存在过期锁文件（%s，%.0fs）；可删除后重试" % (lock, age))
        else:
            add("lock", "warn", "存在锁文件（可能有进程正在写入）：%s" % lock)
    else:
        add("lock", "ok", "无锁文件")

    trash = list_trash(root)
    if trash:
        oldest = max(t["age_days"] for t in trash)
        status = "warn" if oldest > TRASH_RETENTION_DAYS else "ok"
        add("trash", status, "%d 项；最旧 %.1f 天（保留 %d 天）"
            % (len(trash), oldest, TRASH_RETENTION_DAYS))
    else:
        add("trash", "ok", "空")

    snaps = list_snapshots(root)
    add("snapshots", "ok", "%d 个（保留最近 %d 个）" % (len(snaps), SNAPSHOT_KEEP))
    add("capacity", "ok", "%.1f KB" % (_dir_size(root) / 1024.0))

    if backup_dir:
        backups = backup_list(backup_dir)
        if not backups:
            add("backup", "warn", "备份目录无可用备份：%s" % backup_dir)
        else:
            add("backup", "ok", "%d 份；最新 %s（%s）"
                % (len(backups), backups[0]["name"], backups[0]["created"]))

    return {"checks": checks, "errors": errors, "warnings": warnings,
            "ok": errors == 0, "root": str(root)}
