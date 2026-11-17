"""零稀泥模式 — 持久化门面 persistence_facade.py

所有 ndjson + state 写入的唯一入口。
合并之前三条独立写入路径（ndjson_schema / state_manager / repository），
确保校验、去重、轮转逻辑统一。

Usage:
    from .persistence_facade import PersistenceFacade
    facade = PersistenceFacade(state_path)
    facade.save_fix(record_dict, uow=None)
"""

import json, os, time, logging
from typing import Optional, Tuple

from .config import DEFAULT_NDJSON_PATH, NDJSON_MAX_LINES, MAX_RETRIES, BACKOFF_BASE, BACKOFF_MAX
from . import file_ops as _fo
from . import ndjson_schema as _ns
from . import sensitive_filter as _sf

log = logging.getLogger("persistence")

# P10: 运维可观测性 — 静默降级计数器
_silent_degrade_counters = {
    "duplicate_bug_id": 0,
    "oserror_conservative": 0,
    "ndjson_read_fail": 0,
}


def get_degrade_stats() -> dict:
    """返回静默降级统计，供运维监控"""
    return dict(_silent_degrade_counters)


class PersistenceFacade:
    """持久化门面 — ndjson + state 写入的唯一入口

    架构位置: 持久化层 (Layer 3)，所有模块通过此门面写入。
    """

    def __init__(self, state_path: str):
        from . import state_manager as _sm
        self.state_path = state_path or _sm.locate()
        self.ndjson_path = os.path.join(
            os.path.dirname(self.state_path), DEFAULT_NDJSON_PATH
        )

    # ── 写入 ndjson（严格模式 + 重试 + 单次扫描）──

    def write_ndjson(self, record_dict: dict,
                     strict: bool = True,
                     dedup_bug_id: bool = True,
                     retries: int = MAX_RETRIES) -> Tuple[bool, int]:
        """写入一条记录到 ndjson（严格模式默认开启，带重试 + 文件锁）"""
        # Step 1: 敏感过滤
        for field in ("root_cause", "details"):
            if field in record_dict and isinstance(record_dict[field], str):
                record_dict[field] = _sf.filter_sensitive(record_dict[field])

        # Step 2: 校验（严格模式）
        if strict:
            valid, errs = _ns.validate_row(record_dict)
            if not valid:
                raise ValueError(f"ndjson 校验失败: {'; '.join(errs)}")
            record_dict["validated"] = True

        # Step 3: 获取文件锁 → 扫描 → 写入（原子窗口）
        lock_held = _fo.acquire_file_lock(self.ndjson_path)
        try:
            bug_id = record_dict.get("bug_id", "")
            line_count = 0
            already_exists = False
            if os.path.exists(self.ndjson_path):
                try:
                    with open(self.ndjson_path, "r", encoding="utf-8-sig",
                              errors="replace") as f:
                        for line in f:
                            line_count += 1
                            if dedup_bug_id and bug_id and not already_exists:
                                try:
                                    if json.loads(line.strip()).get("bug_id") == bug_id:
                                        already_exists = True
                                except json.JSONDecodeError:
                                    continue
                except OSError as _e:
                    log.warning("ndjson 读取失败，保守拒绝写入: %s", _e)
                    _silent_degrade_counters["oserror_conservative"] += 1
                    return False, 0

            if already_exists:
                log.warning("重复 bug_id %s — 跳过写入（已存在）", bug_id)
                _silent_degrade_counters["duplicate_bug_id"] += 1
                return False, 0

            # Step 4: 轮转检查
            if line_count >= NDJSON_MAX_LINES:
                _fo.safe_rotate_with_backup(self.ndjson_path)
                line_count = 0

            # Step 5: 追加写入（带重试）
            for attempt in range(retries):
                try:
                    with open(self.ndjson_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps(record_dict, ensure_ascii=False) + "\n")
                    return True, line_count + 1
                except OSError as e:
                    if attempt < retries - 1:
                        wait = min(BACKOFF_BASE * (2 ** attempt), BACKOFF_MAX)
                        log.warning("ndjson 写入重试 %d/%d (%.2fs): %s",
                                    attempt + 1, retries, wait, e)
                        time.sleep(wait)
                    else:
                        raise
        finally:
            if lock_held:
                _fo.release_file_lock(self.ndjson_path)

        return False, 0

    # ── 同步 state ──

    def sync_state(self, record_dict: dict) -> None:
        """同步 state 文件（影子状态）"""
        from . import state_manager as _sm
        lock_held = _fo.acquire_file_lock(self.state_path)
        try:
            state = _sm.read(self.state_path)
            state["updated_at"] = _sm.now_iso()
            _sm.write(state, self.state_path)
        finally:
            if lock_held:
                _fo.release_file_lock(self.state_path)

    # ── 事务性双写 ──

    def save_fix(self, record_dict: dict, uow=None) -> dict:
        """原子保存：ndjson + state 双写

        如果外部传入 uow，操作注册到外部事务中。
        返回 {bug_id, success, existed, error}。

        P5-FIX: undo 在 ndjson 写入成功后立即注册（而非 sync_state 之后），
        确保 sync_state 失败时 ndjson 也能被回滚。
        """
        bug_id = record_dict.get("bug_id", "?")
        try:
            # 写入 ndjson
            ok, _ = self.write_ndjson(record_dict, strict=True, dedup_bug_id=True)
            if not ok:
                return {"bug_id": bug_id, "success": False,
                        "existed": True, "error": "duplicate bug_id"}

            # 立即注册 undo（在 sync_state 之前）
            if uow is not None:
                def _make_undo(ndjson_p, rid):
                    def _u():
                        if os.path.exists(ndjson_p):
                            with open(ndjson_p, "r", encoding="utf-8") as f:
                                lines = f.readlines()
                            if lines and rid in lines[-1]:
                                with open(ndjson_p, "w", encoding="utf-8") as f:
                                    f.writelines(lines[:-1])
                    return _u
                uow.register(
                    do=lambda: None,
                    undo=_make_undo(self.ndjson_path, bug_id),
                )

            # 同步 state（失败时 undo 会回滚 ndjson）
            self.sync_state(record_dict)

            log.info("fix 已持久化: bug_id=%s", bug_id)
            return {"bug_id": bug_id, "success": True, "existed": False}

        except Exception as e:
            log.error("fix 持久化失败: %s", e)
            return {"bug_id": bug_id, "success": False, "error": str(e)}

    # ── 验证 ──

    def verify_integrity(self) -> dict:
        """验证 ndjson 与 state 的一致性"""
        from . import state_manager as _sm
        issues = []

        if not os.path.exists(self.ndjson_path):
            return {"ok": True, "issues": [], "note": "ndjson 不存在（首次运行）"}

        ndjson_count = 0
        with open(self.ndjson_path, "r", encoding="utf-8-sig",
                  errors="replace") as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    try:
                        json.loads(stripped)
                        ndjson_count += 1
                    except json.JSONDecodeError:
                        issues.append(
                            f"ndjson 第 {ndjson_count + 1} 行 JSON 损坏")

        state = _sm.read(self.state_path)
        state_count = state.get("ndjson_line_count", 0)

        if ndjson_count != state_count:
            issues.append(
                f"计数不一致: ndjson={ndjson_count}, state={state_count}")

        return {
            "ok": len(issues) == 0,
            "issues": issues,
            "ndjson_count": ndjson_count,
            "state_count": state_count,
        }
