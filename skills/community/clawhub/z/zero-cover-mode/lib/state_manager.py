"""零稀泥模式 — 状态管理器 state_manager.py

管理 .zero-cover-state.json 的原子读写、session 注册/注销。

Usage:
    python state_manager.py read [--path <path>]
    python state_manager.py register <session_id> <bug_id>
    python state_manager.py unregister <session_id>
    python state_manager.py add-fix <bug_id> <bug_type> [--project <project>]
    python state_manager.py set-env <project> <json_env>
    python state_manager.py set-env <project> --key key1=val1 --key key2=val2
    python state_manager.py schedule-verify <bug_id> [--hours 24,168,720]
    python state_manager.py pending-verify
    python state_manager.py mark-verify <bug_id> <hours> <result>
    python state_manager.py cron-instructions <bug_id> <test_cmd>
    python state_manager.py cleanup-bugs [--max-age 48]
    python state_manager.py compact
    python state_manager.py info
"""

import json, os, sys, time, threading, shutil, platform, tempfile
import logging
from datetime import datetime, timezone, timedelta

from . import ndjson_schema as _ns
from .config import (
    TZ, DEFAULT_STATE_PATH, DEFAULT_NDJSON_PATH, SKILL_VERSION,
    LOCK_TIMEOUT, BUG_DIR_MAX_AGE_HOURS, WORKSPACE_MARKER_FILENAME,
    FIX_HISTORY_MAX,
    now_iso,
)

log = logging.getLogger("state")

# P2-v11.3: _WRITE_LOCK 已移除 — 文件锁 _acquire_file_lock 已覆盖跨进程互斥
# 线程锁 + 文件锁共存可能引发 ABBA 死锁，且文件锁 O_EXCL 本身就是互斥的
# 所有 register/unregister/add_fix 均已使用文件锁保护


# ------------------------------------------------------------
#  路径探测
# ------------------------------------------------------------

# P2-3: locate() 结果缓存 — 进程生命周期内有效
# 避免每次 read()/register()/add_fix() 都重复 20 级路径探测
_LOCATE_CACHE = None
_LOCATE_CACHE_CWD = None
_LOCATE_CACHE_AT = 0.0
_LOCATE_CACHE_TTL = 300  # 5 minutes


def _try_create_marker(result_dir):
    """在非临时目录创建 .zerocover-root 标记文件"""
    temp_dirs = {tempfile.gettempdir().lower()}
    try:
        for k in ('TEMP', 'TMP', 'TMPDIR'):
            v = os.environ.get(k, '').lower()
            if v:
                temp_dirs.add(v)
    except Exception:
        pass
    is_temp = any(td and result_dir.lower().startswith(td) for td in temp_dirs if td)
    if not is_temp:
        marker = os.path.join(result_dir, WORKSPACE_MARKER_FILENAME)
        if not os.path.exists(marker):
            try:
                with open(marker, "w", encoding="utf-8") as f:
                    f.write("# zero-cover workspace root\n")
            except OSError as _e:
                log.warning("无法创建 workspace 标记文件: %s", _e)


def locate(*, force_refresh=False):
    """从环境变量 / CWD / 标记文件 / 脚本路径 探测 workspace 根

    优先级:
    1. STATE_PATH 环境变量（最高优先级，如果路径存在或父目录存在则使用）
    2. CWD 中的 state 文件（同时创建标记文件）
    3. CWD 向上查找 .zerocover-root 标记文件
    4. 从脚本路径多级退避推理
    5. 回退 CWD（默认位置）

    TTL: 缓存 300 秒后自动失效。使用 force_refresh=True 可强制刷新。
    注意: STATE_PATH 虽最高优先，但仅当路径存在或父目录存在时才生效。
          否则回退到后续优先级。
    """
    global _LOCATE_CACHE, _LOCATE_CACHE_CWD, _LOCATE_CACHE_AT
    now = time.time()
    if _LOCATE_CACHE is not None and _LOCATE_CACHE_CWD == os.getcwd() and not force_refresh:
        if now - _LOCATE_CACHE_AT < _LOCATE_CACHE_TTL:
            return _LOCATE_CACHE
    result = None

    # 1. 环境变量
    env = os.environ.get("STATE_PATH")
    if env:
        abspath = os.path.abspath(env)
        if os.path.exists(abspath):
            result = abspath
        elif os.path.isdir(os.path.dirname(abspath)):
            result = abspath

    # 2. CWD — 找到后创建标记文件（让下游 locate 能快速定位）
    if result is None:
        cwd_state = os.path.join(os.getcwd(), DEFAULT_STATE_PATH)
        if os.path.exists(cwd_state):
            result = cwd_state
            _try_create_marker(os.path.dirname(cwd_state))

    # 3. 从 CWD 向上查找 .zerocover-root 标记文件（含循环检测防止死循环）
    if result is None:
        current = os.path.abspath(os.getcwd())
        visited = set()
        while current not in visited:
            visited.add(current)
            marker = os.path.join(current, WORKSPACE_MARKER_FILENAME)
            if os.path.exists(marker):
                result = os.path.join(current, DEFAULT_STATE_PATH)
                break
            parent = os.path.dirname(current)
            if parent == current:
                break
            current = parent

    # 4. 从脚本路径多级退避推理
    if result is None:
        script_path = os.path.abspath(__file__)
        parts = script_path.split(os.sep)
        for depth in range(len(parts), 0, -1):
            candidate = os.sep.join(parts[:depth])
            if not candidate or not os.path.isdir(candidate):
                continue
            marker = os.path.join(candidate, WORKSPACE_MARKER_FILENAME)
            if os.path.exists(marker):
                result = os.path.join(candidate, DEFAULT_STATE_PATH)
                break
            skills_dir = os.path.join(candidate, "skills")
            if os.path.isdir(skills_dir):
                result = os.path.join(candidate, DEFAULT_STATE_PATH)
                break

    # 5. 回退 CWD
    if result is None:
        result = os.path.join(os.getcwd(), DEFAULT_STATE_PATH)

    # 缓存结果
    _LOCATE_CACHE = result
    _LOCATE_CACHE_CWD = os.getcwd()
    _LOCATE_CACHE_AT = now

    # 创建标记文件
    result_dir = os.path.dirname(os.path.abspath(result))
    _try_create_marker(result_dir)

    return result


# ------------------------------------------------------------
#  跨进程文件锁（Windows 兼容）
# ------------------------------------------------------------

# Phase 1: 锁逻辑委托到 file_ops.py
from . import file_ops as _fo
_acquire_file_lock = _fo.acquire_file_lock
_release_file_lock = _fo.release_file_lock


#  公开锁 API
# ------------------------------------------------------------

def acquire_lock(path=None, timeout=LOCK_TIMEOUT):
    """公开锁获取接口（委托到 file_ops）"""
    fp = path or locate()
    return _fo.acquire_file_lock(fp, timeout)


def acquire_lock_for_path(path, timeout=LOCK_TIMEOUT):
    """公开锁获取接口 — 强制要求显式路径"""
    if not path:
        raise ValueError("acquire_lock_for_path: path is required")
    return _fo.acquire_file_lock(path, timeout)


def release_lock(path=None):
    """公开锁释放接口（委托到 file_ops）

    参数:
        path: 与 acquire_lock 一致的路径。传 None 时调用 locate() 自动定位。
            建议使用与 acquire_lock 相同的 path 参数避免 locate() 重复执行。
    """
    fp = path or locate()
    _release_file_lock(fp)


# ------------------------------------------------------------
#  核心状态操作
# ------------------------------------------------------------




def read(path=None):
    """读取 state 文件，然后从 ndjson 重建可计算字段

    P6-SINGLE-SOURCE: ndjson 是 fix_history/bug_type_counter/total_fixes
    的唯一事实源。read() 每次读取后从 ndjson 重建这些字段。
    """
    path = path or locate()
    if not os.path.exists(path):
        s = _default_state(path)
        _rebuild_from_ndjson(s, state_path=path)
        _update_format_versions(s)
        return s
    try:
        with open(path, "r", encoding="utf-8") as f:
            s = json.load(f)
            # P6-CONTRACT: StateSchema 运行时校验
            try:
                from .contracts import StateSchema
                StateSchema(**s)
            except Exception as _sce:
                log.warning("StateSchema 校验失败: %s — 尝试修复", _sce)
                # 让读取继续，auto_repair 会处理
    except json.JSONDecodeError:
        backup = path + ".bak"
        if os.path.exists(backup):
            log.warning("state 文件损坏，从备份恢复: %s", path)
            try:
                with open(backup, "r", encoding="utf-8") as f:
                    s = json.load(f)
                shutil.copy2(backup, path)
                log.warning("已用备份覆盖损坏的 state 文件: %s", path)
            except json.JSONDecodeError:
                corruption_ts = datetime.now().strftime("%Y%m%d%H%M%S")
                corruption_bak = f"{path}.corrupted.{corruption_ts}"
                try:
                    shutil.copy2(path, corruption_bak)
                    log.critical("state 文件及其备份均损坏！已保存损坏文件至: %s", corruption_bak)
                except OSError as _ce:
                    log.critical("无法保存损坏的 state 文件备份: %s", _ce)
                s = _default_state(path)
                write(s, path)
                log.warning("已创建空白 state 文件并覆盖主路径: %s", path)
        else:
            log.warning("state 文件损坏 (%s), 重建默认", path)
            s = _default_state(path)
            write(s, path)
    # P6-SINGLE-SOURCE: 从 ndjson（唯一事实源）重建可计算字段
    _rebuild_from_ndjson(s, path)
    _update_format_versions(s)
    return s


def _default_state(path):
    return {
        "version": SKILL_VERSION,
        "format_version": 2,
        "total_fixes": 0,
        "active_session_ids": [],
        "sessions": {},
        "bug_id_registry": [],
        "bug_type_counter": {},
        "fix_history": [],
        "verifications": {},
        "last_weekly_report": None,
        "ndjson_line_count": 0,
        "ndjson_last_rotate": None,
        "project_env": {"project_type": "unknown", "test_cmd": "", "vcs": "none"},
        "projects": {},
        "_deprecated_fix_history": True,
        "_ndjson_is_primary": True,
        "updated_at": now_iso(),
    }


def _update_format_versions(state):
    """从 fix_history 计算 bug_id 格式分布"""
    import re as _re
    new_fmt = _re.compile(r'^[a-z]{3,4}-[a-z]{3}-\d{10,12}-[a-f0-9]{4}$')
    history = state.get("fix_history", [])
    new_count = sum(1 for h in history
                    if new_fmt.match(str(h.get("bug_id", ""))))
    old_count = len(history) - new_count
    state["bug_id_format_versions"] = {
        "new_format_regex": "^[a-z]{3,4}-[a-z]{3}-\\d{10,12}-[a-f0-9]{4}$",
        "new_count": new_count,
        "old_count": old_count,
        "transition_policy": "旧ID保留不迁移; 新写入强制使用格式; 事实来源为ndjson",
    }


# ------------------------------------------------------------
#  单源重建（P6-SINGLE-SOURCE: ndjson 是唯一事实源）
# ------------------------------------------------------------

def _rebuild_from_ndjson(state, state_path):
    """Public alias: rebuild_state_from_ndjson = _rebuild_from_ndjson"""
    """从 ndjson 重建 state 的可计算字段

    ndjson 是 fix_history / bug_type_counter / total_fixes / bug_id_registry
    的唯一事实源。state.json 只存储 session/verification 等非持久类数据。
    每次 read() 后调用此函数确保 state 与 ndjson 完全一致。
    """
    ndjson_dir = os.path.dirname(os.path.abspath(state_path))
    ndjson_path = os.path.join(ndjson_dir, DEFAULT_NDJSON_PATH)

    if not os.path.exists(ndjson_path):
        # ndjson 不存在时不覆盖 state 中可能已有的数据
        # （测试场景或全新环境需要保留现有状态）
        return

    line_count = 0
    fix_history = []
    bug_type_counter = {}
    bug_id_set = set()

    with open(ndjson_path, "r", encoding="utf-8-sig", errors="replace") as f:
        for line in f:
            try:
                row = json.loads(line.strip())
                bid = row.get("bug_id", "")
                if not bid:
                    continue
                line_count += 1
                fix_history.append({
                    "bug_id": bid,
                    "bug_type": row.get("bug_type", "unknown"),
                    "timestamp": row.get("timestamp", ""),
                })
                bt = row.get("bug_type", "unknown")
                bug_type_counter[bt] = bug_type_counter.get(bt, 0) + 1
                bug_id_set.add(bid)
            except (json.JSONDecodeError, ValueError):
                continue

    state["fix_history"] = fix_history
    state["bug_type_counter"] = bug_type_counter
    state["total_fixes"] = line_count
    state["bug_id_registry"] = sorted(bug_id_set)[-1000:]
    state["ndjson_line_count"] = line_count
    # P6-VERSION: 同步版本号（config.py 是单一事实源）
    from .config import SKILL_VERSION
    state["version"] = SKILL_VERSION


def write(state, path=None):
    """原子写入：写临时文件 -> 备份 -> rename -> 后验证（P2-v7.1: 后验证 + 自动恢复）"""
    path = path or locate()
    tmp = path + ".tmp." + str(os.getpid())
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    if os.path.exists(path):
        try:
            # 验证旧文件完整性
            with open(path, "r", encoding="utf-8") as f:
                json.load(f)
            shutil.copy2(path, path + ".bak")
        except (json.JSONDecodeError, OSError, IOError) as e:
            log.warning("旧文件验证或备份失败: %s — 仍进行替换", e)
            try:
                os.replace(path, path + ".bak")
            except OSError:
                pass
    # P6-SINGLE-SOURCE: auto-compact 已移除——write() 只负责写入，不负责清理。
    # compact 逻辑已迁移到独立的 compact() 函数。
    os.replace(tmp, path)
    # 后验证：确认新文件有效
    try:
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        log.error("新写入的 state 文件无效! 尝试从备份恢复: %s", e)
        bak_file = path + ".bak"
        if os.path.exists(bak_file):
            try:
                shutil.copy2(bak_file, path)
                log.warning("已从备份恢复: %s", path)
            except (OSError, IOError) as e2:
                log.error("备份恢复失败: %s", e2)
    # P5: 只有文件仍存在时才尝试删除
    # os.replace(tmp, path) 已经移动/替换了文件，通常 tmp 不再存在
    if os.path.exists(tmp):
        try:
            os.unlink(tmp)
        except OSError as _e:
            log.warning("tempfile unlink failed: %s - %s", tmp, _e)


# Public alias for repository.py
rebuild_state_from_ndjson = _rebuild_from_ndjson


# ------------------------------------------------------------
#  Session 管理
# ------------------------------------------------------------

def register(session_id, bug_id, path=None):
    fp = path or locate()
    lock_held = _acquire_file_lock(fp)
    try:
        state = read(fp)
        existing = state.get("sessions", {}).get(session_id, {})
        if existing.get("bug_id") and existing.get("bug_id") != bug_id:
            log.warning(
                "session %s 正在修复 %s (in_progress), 覆盖为 %s — "
                "旧修复将留下孤立 bug 目录",
                session_id, existing.get("bug_id"), bug_id,
            )
            import sys as _sys
            _sys.stderr.write(
                "WARNING: session %s overwrites bug %s -> %s\n"
                "The old bug dir will be orphaned unless cleanup runs.\n"
                "Use cleanup_bugs() or manually delete the old dir.\n"
            )
            log.warning("返回 (state, was_orphan=True, old_bug_id=%s)", existing.get("bug_id"))
            # P1-7: 记录孤立 session，便于 cleanup_bugs 追踪
            orphans = state.setdefault("_orphan_sessions", [])
            orphans.append({
                "session_id": session_id,
                "old_bug_id": existing["bug_id"],
                "new_bug_id": bug_id,
                "replaced_at": now_iso(),
            })
            # 限制 orphan_sessions 上限，防止无限增长
            _MAX_ORPHANS = 200
            if len(orphans) > _MAX_ORPHANS:
                state["_orphan_sessions"] = orphans[-_MAX_ORPHANS:]
        state.setdefault("sessions", {})[session_id] = {
            **existing,                                       # 保留旧字段
            "bug_id": bug_id,                                 # 覆盖 bug_id
            "started_at": existing.get("started_at", now_iso()),  # 保留最早 start
            "updated_at": now_iso(),
            "re_registered": now_iso() if existing.get("bug_id") else None,
            "status": "in_progress",
        }
        if session_id not in state.get("active_session_ids", []):
            state.setdefault("active_session_ids", []).append(session_id)
        if bug_id not in state.setdefault("bug_id_registry", []):
            state["bug_id_registry"].append(bug_id)
        state["updated_at"] = now_iso()
        # register: 文件锁保护下的直接写入
        execute_write(state, fp)
    finally:
        if lock_held:
            _release_file_lock(fp)
    return state


def unregister(session_id, path=None):
    fp = path or locate()
    lock_held = _acquire_file_lock(fp)
    try:
        state = read(fp)
        state["active_session_ids"] = [
            s for s in state.get("active_session_ids", [])
            if s != session_id
        ]
        if session_id in state.get("sessions", {}):
            state["sessions"][session_id]["status"] = "completed"
            state["sessions"][session_id]["completed_at"] = now_iso()
        state["updated_at"] = now_iso()
        # unregister: 文件锁保护下的直接写入
        execute_write(state, fp)
    finally:
        if lock_held:
            _release_file_lock(fp)
    return state


# ------------------------------------------------------------
#  修复记录管理（以 ndjson 为事实来源）
# ------------------------------------------------------------


def execute_write(state, fp):
    """简化写入：文件锁已保证互斥，直接写入
    _acquire_file_lock() 的 O_EXCL 已经是操作系统级跨进程互斥。"""
    state["updated_at"] = now_iso()
    write(state, fp)
    return True




def _write_ndjson_record(ndjson_path, fix_record):
    """Write fix record to ndjson. Returns (ok, already_existed).

    P2-REFACTOR: 委托 PersistenceFacade（唯一写入入口），移除三层降级逻辑。
    校验失败即拒绝写入，不再静默降级。
    """
    from .persistence_facade import PersistenceFacade
    # 从 ndjson_path 反推 state_path
    state_dir = os.path.dirname(os.path.abspath(ndjson_path))
    state_path = os.path.join(state_dir, DEFAULT_STATE_PATH)
    facade = PersistenceFacade(state_path)

    try:
        ok, _ = facade.write_ndjson(fix_record, strict=True, dedup_bug_id=True)
        if ok:
            return True, False
        # 唯一可能失败的原因：bug_id 去重
        return False, True  # existed
    except ValueError as e:
        log.error("ndjson 校验失败（拒绝写入）: %s", e)
        return False, False


def add_fix(bug_id, bug_type, project=None, path=None, record=None):
    """Add fix record -- ndjson is the single source of truth.

    P6-SINGLE-SOURCE: add_fix 只写 ndjson。state.json 的 fix_history /
    bug_type_counter / total_fixes 等字段在 read() 时从 ndjson 重建。
    """
    fp = path or locate()
    lock_held = _acquire_file_lock(fp)
    try:
        state = read(fp)
        ndjson_path = os.path.join(os.path.dirname(fp), DEFAULT_NDJSON_PATH)
        if record:
            fix_record = record
        else:
            fix_record = {
                "timestamp": now_iso(),
                "bug_id": bug_id,
                "bug_type": bug_type,
                "module": state.get("project_env", {}).get("project_type", "unknown"),
                "fix_type": "permanent",
                "blocking": False,
                "test_count": 0,
                "regression_pass": 0,
                "regression_fail": 0,
                "vcs_hash": "none",
                "test_skipped": False,
            }
        ndjson_ok, existed = _write_ndjson_record(ndjson_path, fix_record)
        if not ndjson_ok:
            raise RuntimeError(
                f"ndjson write failed (bug_id={bug_id})"
            )
        if existed:
            log.info("ndjson already has bug_id=%s — done", bug_id)
            return state
        # P6-SINGLE-SOURCE: 不再同步到 state.json（ndjson 是事实源）
        log.info("fix added to ndjson: bug_id=%s, type=%s", bug_id, bug_type)
        return state
    finally:
        if lock_held:
            _release_file_lock(fp)


def set_project_env(project, env_dict, path=None):
    state = read(path)
    state.setdefault("projects", {})[project] = env_dict
    state["project_env"] = env_dict
    state["updated_at"] = now_iso()
    write(state, path)
    return state


def schedule_verification(bug_id, hours_list=None, path=None):
    """安排验证计划 — 带文件锁保护"""
    if hours_list is None:
        hours_list = [24, 168, 720]
    fp = path or locate()
    lock_held = _acquire_file_lock(fp)
    try:
        state = read(fp)
        state.setdefault("verifications", {})[bug_id] = {
            "scheduled_at": hours_list,
            "checks": {},
            "status": "pending",
            "created_at": now_iso(),
        }
        state.setdefault("_verify_needs_cron", []).append({
            "bug_id": bug_id, "hours": hours_list, "created_at": now_iso(),
        })
        state["updated_at"] = now_iso()
        write(state, fp)
        return state
    finally:
        if lock_held:
            _release_file_lock(fp)


def list_pending_verifications(path=None):
    state = read(path)
    now = datetime.now(TZ)
    pending = []
    for bug_id, vinfo in state.get("verifications", {}).items():
        if vinfo.get("status") == "verified":
            continue
        created = datetime.fromisoformat(vinfo["created_at"])
        elapsed = (now - created).total_seconds() / 3600
        for h in vinfo.get("scheduled_at", []):
            if str(h) not in vinfo.get("checks", {}):
                if elapsed >= h:
                    pending.append({
                        "bug_id": bug_id,
                        "hours": h,
                        "overdue_by": round(elapsed - h, 1),
                    })
    return pending


def mark_verification(bug_id, hours, result, path=None):
    """标记验证结果 — 带文件锁保护"""
    fp = path or locate()
    lock_held = _acquire_file_lock(fp)
    try:
        state = read(fp)
        vinfo = state.get("verifications", {}).get(bug_id)
        if vinfo is None:
            return False
        vinfo.setdefault("checks", {})[str(hours)] = {
            "result": result,
            "checked_at": now_iso(),
        }
        all_done = all(str(h) in vinfo["checks"] for h in vinfo.get("scheduled_at", []))
        if all_done:
            vinfo["status"] = "verified"
        state["updated_at"] = now_iso()
        write(state, fp)
        return True
    finally:
        if lock_held:
            _release_file_lock(fp)


def generate_cron_instructions(bug_id, test_cmd, path=None):
    state = read(path)
    vinfo = state.get("verifications", {}).get(bug_id)
    if vinfo is None:
        log.error("%s 无验证计划", bug_id)
        return []

    instructions = []
    now = datetime.now(TZ)
    for h in vinfo.get("scheduled_at", []):
        future = now + timedelta(hours=h)
        at_iso = future.isoformat(timespec="seconds")
        instructions.append({
            "bug_id": bug_id,
            "hours": h,
            "at": at_iso,
            "message": f"验证 {bug_id} ({h}h复查): 运行 {test_cmd}",
            "sessionTarget": "isolated",
            "hint": f"cron add schedule.kind=at at={at_iso} sessionTarget=isolated",
        })
    return instructions


# ------------------------------------------------------------
#  清理
# ------------------------------------------------------------

def cleanup_bugs(max_age_hours=BUG_DIR_MAX_AGE_HOURS, path=None):
    state_path = path or locate()
    state = read(state_path)
    bugs_dir = os.path.join(os.path.dirname(os.path.abspath(state_path)), "bugs")
    if not os.path.isdir(bugs_dir):
        log.info("bugs 目录不存在 (%s)", bugs_dir)
        return 0

    active_bug_ids = set()
    for s in state.get("sessions", {}).values():
        if s.get("status") == "in_progress" and s.get("bug_id"):
            active_bug_ids.add(s["bug_id"])
    # P5: orphan sessions 中的 old_bug_id 不被保护，超过 max_age 可清理
    orphan_bug_ids = set()
    for orphan in state.get("_orphan_sessions", []):
        old_bid = orphan.get("old_bug_id", "")
        if old_bid:
            orphan_bug_ids.add(old_bid)

    now = time.time()
    cutoff = now - (max_age_hours * 3600)
    removed = 0
    kept = 0
    for entry in os.listdir(bugs_dir):
        candidate = os.path.join(bugs_dir, entry)
        if not os.path.isdir(candidate):
            continue
        if entry in active_bug_ids:
            kept += 1
            continue
        # orphan bug 目录也参与清理（超过 max_age 即可删除）
        try:
            mtime = os.path.getmtime(candidate)
        except OSError:
            kept += 1
            continue
        if mtime < cutoff:
            try:
                shutil.rmtree(candidate)
                removed += 1
                log.info("清理 bugs 目录: %s", entry)
            except (OSError, IOError) as e:
                log.error("删除 %s 失败: %s", entry, e)
        else:
            kept += 1
    # P5: 清理已处理的 _orphan_sessions（对应的 bug 目录在清理范围中已处理）
    _cleanup_orphan_records(state)
    log.info("清理完成: 删除 %d, 保留 %d, orphan 已处理", removed, kept)
    return removed


def _cleanup_orphan_records(state):
    """清理已处理的 _orphan_sessions — orphan 对应的 bug 目录被清理后清除记录"""
    from .config import BUG_DIR_MAX_AGE_HOURS
    now = time.time()
    cutoff = now - (BUG_DIR_MAX_AGE_HOURS * 3600)
    orphans = state.get("_orphan_sessions", [])
    kept = []
    for orphan in orphans:
        replaced_str = orphan.get("replaced_at", "")
        if replaced_str:
            try:
                from datetime import datetime as _dt
                replaced_at = _dt.fromisoformat(replaced_str).timestamp()
                if replaced_at < cutoff:
                    # orphan 记录已过时，删除
                    continue
            except (ValueError, TypeError):
                pass
        kept.append(orphan)
    if len(kept) < len(orphans):
        state["_orphan_sessions"] = kept[-50:]  # 最多保留 50 条


# ------------------------------------------------------------
#  信息显示
# ------------------------------------------------------------

def info(path=None):
    state = read(path)
    print(f"零稀泥模式状态 ({state.get('version', '?')})")
    print(f"  总修复: {state.get('total_fixes', 0)}")
    print(f"  活跃 session: {len(state.get('active_session_ids', []))}")
    print(f"  ndjson 行数: {state.get('ndjson_line_count', 0)}")
    print(f"  上次周报: {state.get('last_weekly_report', '从未')}")
    print(f"  state 体积: {state.get('_state_size_bytes', 0)} bytes")
    print(f"  bug 类型分布:")
    for bt, cnt in sorted(state.get("bug_type_counter", {}).items(),
                           key=lambda x: -x[1]):
        print(f"    {bt}: {cnt}")
    print(f"  待验证: {len(list_pending_verifications(path))}")


def compact(path=None):
    """压缩 state 文件：清理旧 checkpoint 数据，防止无限制膨胀

    保留最近 50 条 checkpoint，其余删除。
    """
    fp = path or locate()
    state = read(fp)
    modified = False

    # 压缩 pipeline checkpoints
    cps = state.get("_pipeline_checkpoints", {})
    if len(cps) > 50:
        sorted_ids = sorted(cps.keys(),
                            key=lambda k: cps[k].get("updated_at", "") or "")
        for old_id in sorted_ids[:-50]:
            del cps[old_id]
        state["_pipeline_checkpoints"] = cps
        modified = True
        log.info("压缩 state: 删除 %d 个旧 checkpoint", len(sorted_ids) - 50)

    # 记录文件体积
    if os.path.exists(fp):
        try:
            state["_state_size_bytes"] = os.path.getsize(fp)
        except OSError:
            pass

    # 清理 _orphan_sessions
    # 清理 stale active_session_ids (Fix D)
    active = state.get("active_session_ids", [])
    sessions = state.get("sessions", {})
    stale = [s for s in active if s in sessions and sessions[s].get("status") == "completed"]
    if stale:
        for s in stale: active.remove(s)
        state["active_session_ids"] = active
        modified = True
        print("OK: stale sessions: " + str(len(stale)))

    # P6-DEAD: bug_id_registry dedup 和 fix_history dedup 已移除。
    # Batch 1 单源改造后，state 的这两个字段在 read() 时从 ndjson 重建，
    # 每次读取后已是干净状态，compact() 中的去重永远不触发。
    orphans = state.get("_orphan_sessions", [])
    bugs_base = os.path.join(os.path.dirname(fp) or ".", "bugs")
    cleaned = 0
    for orphan in orphans:
        old_bid = orphan.get("old_bug_id", "")
        if not old_bid: continue
        bd = os.path.join(bugs_base, old_bid)
        if os.path.isdir(bd):
            try:
                shutil.rmtree(bd)
                cleaned += 1
            except OSError:
                pass
    if cleaned:
        state["_orphan_sessions"] = []
        modified = True
        print(f"OK: 清理 {cleaned} 个 orphan 目录")

    if modified:
        write(state, fp)
        print(f"OK: state 已压缩")
    else:
        print(f"OK: state 无需压缩")
    return state


# ------------------------------------------------------------
#  CLI
# ------------------------------------------------------------

def _build_cli_parser():
    import argparse
    parser = argparse.ArgumentParser(
        description="零稀泥模式状态管理器",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
示例:
  python -m lib.state_manager register session_abc bug-001
  python -m lib.state_manager unregister session_abc
  python -m lib.state_manager add-fix bug-001 config_error --project my-project
  python -m lib.state_manager info
  python -m lib.state_manager compact
""",
    )
    parser.add_argument("--path", help="状态文件路径（默认自动探测）")
    parser.add_argument("--version", action="version",
                        version=f"zero-cover-mode v{SKILL_VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("read", help="读取状态")

    p = sub.add_parser("register", help="注册 session")
    p.add_argument("session_id")
    p.add_argument("bug_id")

    p = sub.add_parser("unregister", help="注销 session")
    p.add_argument("session_id")

    p = sub.add_parser("add-fix", help="添加修复记录")
    p.add_argument("bug_id")
    p.add_argument("bug_type")
    p.add_argument("--project", "-p", help="所属项目")

    p = sub.add_parser("set-env", help="设置项目环境")
    p.add_argument("project")
    p.add_argument("env", nargs="?", help="JSON 格式环境字典")
    p.add_argument("--key", "-k", action="append", dest="keys",
                   help="key=value 格式（可多次）: --key type=python --key vcs=git")

    p = sub.add_parser("schedule-verify", help="安排验证计划")
    p.add_argument("bug_id")
    p.add_argument("--hours", default="24,168,720", help="复查时间点（逗号分隔）")

    sub.add_parser("pending-verify", help="列出待验证项")

    p = sub.add_parser("mark-verify", help="标记验证结果")
    p.add_argument("bug_id")
    p.add_argument("hours", type=int, help="验证时间点")
    p.add_argument("result", help="结果: pass/fail")

    p = sub.add_parser("cron-instructions", help="生成 cron 指令")
    p.add_argument("bug_id")
    p.add_argument("test_cmd")

    p = sub.add_parser("cleanup-bugs", help="清理过期 bugs 目录")
    p.add_argument("--max-age", type=float, default=BUG_DIR_MAX_AGE_HOURS,
                   help=f"最大保留时间（小时，默认 {BUG_DIR_MAX_AGE_HOURS}）")

    sub.add_parser("compact", help="压缩 state 文件（清理旧 checkpoint）")
    sub.add_parser("info", help="显示状态概览")
    return parser


if __name__ == "__main__":
    parser = _build_cli_parser()

    # 统一 argparse 入口（P0-v7.1: 移除旧式位置参数解析，完全使用 argparse）
    args = parser.parse_args()
    path = args.path or os.environ.get("STATE_PATH")

    try:
        if args.command == "read":
            s = read(path)
            write(s, path)
            json.dump(s, sys.stdout, ensure_ascii=False, indent=2)
        elif args.command == "register":
            register(args.session_id, args.bug_id, path)
            print(f"OK: session {args.session_id} registered with bug_id {args.bug_id}")
        elif args.command == "unregister":
            unregister(args.session_id, path)
            print(f"OK: session {args.session_id} unregistered")
        elif args.command == "add-fix":
            add_fix(args.bug_id, args.bug_type, args.project, path)
            print(f"OK: fix {args.bug_id} ({args.bug_type}) added" +
                  (f" [project: {args.project}]" if args.project else ""))
        elif args.command == "set-env":
            if args.env:
                env_dict = json.loads(args.env)
            elif args.keys:
                env_dict = {}
                for kv in args.keys:
                    if "=" in kv:
                        k, v = kv.split("=", 1)
                        env_dict[k] = v
            else:
                parser.error("set-env 需要 env JSON 或 --key 参数")
            set_project_env(args.project, env_dict, path)
            print(f"OK: project env set for {args.project}: {json.dumps(env_dict)}")
        elif args.command == "schedule-verify":
            hours = [int(x) for x in args.hours.split(",")]
            schedule_verification(args.bug_id, hours, path)
            print(f"OK: verification scheduled for {args.bug_id}")
        elif args.command == "pending-verify":
            pending = list_pending_verifications(path)
            if pending:
                print(f"待验证: {len(pending)} 个")
                for p in pending:
                    print(f"  {p['bug_id']}: {p['hours']}h (过期 {p['overdue_by']}h)")
            else:
                print("OK: 无待验证项")
        elif args.command == "mark-verify":
            mark_verification(args.bug_id, args.hours, args.result, path)
            print(f"OK: {args.bug_id} {args.hours}h 验证标记为 {args.result}")
        elif args.command == "cron-instructions":
            generate_cron_instructions(args.bug_id, args.test_cmd, path)
        elif args.command == "cleanup-bugs":
            cleanup_bugs(args.max_age, path)
        elif args.command == "compact":
            compact(path)
        elif args.command == "info":
            info(path)
    except Exception as e:
        log.error("执行失败: %s", e)
        sys.exit(1)
