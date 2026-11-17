"""零稀泥模式 — 文件操作 Sidecar (file_ops.py)

集中管理所有 I/O 副作用：文件锁、目录操作、备份、轮转安全。
所有模块不得绕过此层直接执行文件操作。

提取自 state_manager.py 的锁逻辑，消除 TOCTOU 竞态。
"""

import os, sys, time, platform, tempfile, shutil, logging, random

from .config import LOCK_TIMEOUT

log = logging.getLogger("file_ops")

_LOCK_GENERATION = random.randint(0, 2**31)


# ════════════════════════════════════════════════════════════
#  跨进程文件锁
# ════════════════════════════════════════════════════════════

def _process_exists(pid):
    """跨平台检查 PID 是否存在"""
    if platform.system() == "Windows":
        try:
            import ctypes
            handle = ctypes.windll.kernel32.OpenProcess(0x400, False, pid)
            if handle == 0:
                return False
            ctypes.windll.kernel32.CloseHandle(handle)
            return True
        except (ImportError, AttributeError, OSError):
            try:
                os.kill(pid, 0)
                return True
            except ProcessLookupError:
                return False
            except PermissionError:
                return True
            except OSError:
                return True
    else:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False


def acquire_file_lock(path, timeout=LOCK_TIMEOUT):
    """基于 O_EXCL 的跨进程文件锁（Phase 1: TOCTOU 修复版）

    修复架构审查 1.4 号问题：
    清理死锁前先读取 stale 文件确认 generation，
    只有确认锁是旧进程的才删除，防止误删其他进程的新锁。

    返回 True 表示成功获取锁，False 表示超时。
    """
    lockpath = path + ".lock"
    deadline = time.time() + timeout
    attempt = 0
    while time.time() < deadline:
        try:
            fd = os.open(lockpath, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, 'w') as f:
                f.write(f"{os.getpid()}:{_LOCK_GENERATION}")
            return True
        except FileExistsError:
            try:
                with open(lockpath, 'r') as f:
                    content = f.read().strip()
                if ":" in content:
                    pid_str, gen_str = content.split(":", 1)
                    pid = int(pid_str)
                    lock_gen = int(gen_str)
                else:
                    pid = int(content)
                    lock_gen = None

                if not _process_exists(pid):
                    # TOCTOU fix: rename first (atomic), then verify generation
                    stale_path = lockpath + f".stale.{os.getpid()}"
                    try:
                        os.rename(lockpath, stale_path)
                        # Read stale to confirm generation is old
                        try:
                            with open(stale_path, 'r') as _sf:
                                _sc = _sf.read().strip()
                            if ":" in _sc:
                                _sg = int(_sc.split(":", 1)[1])
                                if _sg == _LOCK_GENERATION:
                                    # Our own stale lock — safe to delete
                                    os.unlink(stale_path)
                                    continue
                                # Old process's lock — safe to delete
                                os.unlink(stale_path)
                                continue
                            # Old format (no generation) — safe to delete
                            os.unlink(stale_path)
                            continue
                        except (ValueError, OSError, IOError):
                            try:
                                os.unlink(stale_path)
                            except OSError:
                                pass
                            continue
                    except OSError:
                        pass
                    continue
            except (ValueError, OSError, IOError):
                pass
            attempt += 1
            time.sleep(min(0.05 * (2 ** min(attempt, 5)), 1.0))
    return False


def release_file_lock(path):
    """释放文件锁"""
    lockpath = path + ".lock"
    try:
        if os.path.exists(lockpath):
            os.unlink(lockpath)
    except OSError as e:
        log.warning("释放锁文件失败 %s: %s", lockpath, e)


# ════════════════════════════════════════════════════════════
#  文件备份与安全轮转
# ════════════════════════════════════════════════════════════

def safe_rotate_with_backup(path, backup_suffix=None):
    """安全轮转文件：先备份再 rename

    修复架构审查 6 号问题（ndjson rotation 数据丢失）：
    os.replace() 之前先 shutil.copy2 创建快照。

    返回 (rotated_path, backup_path) 或在失败时 raise。

    P6-FIX: os.replace 失败时清理残留的 pre-rotate.bak 文件。
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"轮转目标不存在: {path}")

    from datetime import datetime
    from .config import TZ

    now = datetime.now(TZ)
    week = now.strftime('W%W')
    ts = now.strftime('%H%M%S%f')
    rotated = f"{path}.{week}-{ts}.ndjson"

    # Step 1: 创建快照备份（防轮转中途 crash）
    backup_path = f"{rotated}.pre-rotate.bak"
    try:
        shutil.copy2(path, backup_path)
    except OSError as e:
        log.error("轮转前备份失败: %s — 中断轮转", e)
        raise RuntimeError(f"轮转前备份失败: {e}") from e

    # Step 2: 执行轮转
    try:
        os.replace(path, rotated)
    except OSError as e:
        # 轮转失败时清理备份文件，防止残留
        try:
            os.unlink(backup_path)
        except OSError:
            pass
        log.error("轮转 rename 失败: %s (备份已清理)", e)
        raise RuntimeError(f"轮转 rename 失败: {e}") from e

    log.info("轮转完成: %s -> %s (备份: %s)", path, rotated, backup_path)

    return rotated, backup_path


def safe_atomic_write(path, data_json_func):
    """安全原子写入：写临时文件 → 备份 → rename → 后验证

    data_json_func 是可调用对象，用于获取 JSON 序列化结果。
    """
    tmp = path + ".tmp." + str(os.getpid())
    try:
        # 写入临时文件
        json_data = data_json_func()
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(json_data)
    except Exception as e:
        log.error("临时文件写入失败: %s", e)
        if os.path.exists(tmp):
            try:
                os.unlink(tmp)
            except OSError:
                pass
        raise

    # 备份旧文件
    if os.path.exists(path):
        try:
            shutil.copy2(path, path + ".bak")
        except OSError as e:
            log.warning("备份失败（非关键）: %s", e)

    # rename
    os.replace(tmp, path)

    # 后验证
    try:
        with open(path, "r", encoding="utf-8") as f:
            f.read()
    except (OSError, IOError) as e:
        log.error("文件写入后验证失败: %s", e)
        bak = path + ".bak"
        if os.path.exists(bak):
            try:
                shutil.copy2(bak, path)
                log.info("已从备份恢复: %s", path)
            except OSError as e2:
                log.error("备份恢复也失败: %s", e2)
        raise

    if os.path.exists(tmp):
        try:
            os.unlink(tmp)
        except OSError:
            pass
