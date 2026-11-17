"""零稀泥模式 — 归档流水线 archive_pipeline.py

从 Pipeline.phase3_closure() 抽取的归档逻辑：
ndjson 写入 + 事件发布 + state 同步 + session 注销。

Usage:
    from .archive_pipeline import ArchivePipeline, ArchiveResult
    ap = ArchivePipeline(state_path, bug_id, session_id, bug_dir)
    pre = ap.run_pre_checks(root_cause_summary)
    result = ap.execute(record, tx, root_cause_summary=root_cause_summary)
"""

import json, os, logging
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .config import TZ
from .contracts import FixRecord
from . import state_manager as sm
from . import sensitive_filter as sf
from . import loop_detector as ld
from .repository import FixRepository
from .event_publisher import EventPublisher

log = logging.getLogger("archive")


class ArchiveResult(BaseModel):
    """归档结果 — Pydantic 契约"""
    success: bool
    blocking: bool = False
    details: str = ""
    output_files: dict = Field(default_factory=dict)
    existed: bool = False


class ArchivePipeline:
    """归档流水线 — ndjson + 事件 + state 同步的事务组合

    从 Pipeline.phase3_closure() 抽取。
    职责：
    1. 敏感数据过滤（只读阶段）
    2. 循环检测（只读阶段）
    3. ndjson 写入 + 事件发布 + session 注销（TransactionCoordinator 管理）
    """

    def __init__(self, state_path: str, bug_id: str, session_id: str, bug_dir: str,
                 bug_type: str, module: str, fix_type: str = "permanent",
                 vcs: str = "none"):
        self.state_path = state_path
        self.bug_id = bug_id
        self.session_id = session_id
        self.bug_dir = bug_dir
        self.bug_type = bug_type
        self.module = module
        self.fix_type = fix_type
        self.vcs = vcs

    def run_pre_checks(self, root_cause_summary: str) -> dict:
        """执行只读预检查（敏感过滤 + 循环检测）

        Returns:
            {"ok": bool, "blocking": bool, "details": str,
             "filtered": dict, "original": dict, "loop_file": str}
        """
        filtered_contents = {}
        original_contents = {}
        files_to_filter = [
            os.path.join(self.bug_dir, "BUG_ROOT_CAUSE.md"),
            os.path.join(self.bug_dir, "TEST_RESULT.md"),
        ]
        for fpath in files_to_filter:
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    raw = f.read()
                original_contents[fpath] = raw
                filtered_contents[fpath] = sf.filter_sensitive(raw)

        ndjson_path = os.path.join(
            os.path.dirname(self.state_path or "."),
            "FIX_CLOSURE_LOG.ndjson",
        )
        if not root_cause_summary:
            rc_file = os.path.join(self.bug_dir, "BUG_ROOT_CAUSE.md")
            if os.path.exists(rc_file):
                with open(rc_file, "r", encoding="utf-8") as f:
                    root_cause_summary = f.read()[:255]

        loop_result = ld.detect_loop(ndjson_path, self.bug_type, root_cause_summary)
        if loop_result.get("loop_detected"):
            loop_file = os.path.join(self.bug_dir, "LOOP_DETECTION.json")
            with open(loop_file, "w", encoding="utf-8") as f:
                json.dump(loop_result, f, ensure_ascii=False, indent=2)
            return {
                "ok": False,
                "blocking": True,
                "details": (f"循环检测触发: type={self.bug_type} "
                           f"sim={loop_result.get('max_similarity', 0):.3f}"),
                "filtered": filtered_contents,
                "original": original_contents,
                "loop_file": loop_file,
            }

        return {
            "ok": True,
            "blocking": False,
            "details": "预检查通过",
            "filtered": filtered_contents,
            "original": original_contents,
            "loop_file": None,
        }

    def execute(self, record: FixRecord, tx,  # tx: TransactionCoordinator
                root_cause_summary: str = "",
                fallback_mode: bool = False,
                test_skipped: bool = False,
                regr_pass: int = 0, regr_fail: int = 0,
                filtered_contents: dict = None,
                original_contents: dict = None) -> ArchiveResult:
        """执行归档（TransactionCoordinator 统一管理副作用）

        tx 参数替代了旧的 uow 参数，所有副作用注册到 tx 中。
        cleanup_bugs 移到事务外（在调用方 finally 中执行）。
        """
        try:
            # ndjson 写入（内部使用 UoW，但不影响外部 tx）
            repo = FixRepository(self.state_path)
            result = repo.save_fix(record, None)  # 不再传 uow
            if not result.get("success"):
                return ArchiveResult(
                    success=False, blocking=True,
                    details=f"ndjson 写入失败: {result.get('error', 'unknown')}",
                    existed=result.get("existed", False),
                )

            # 注册 ndjson 回滚到外部 tx
            def _undo_ndjson():
                ndjson_path = os.path.join(
                    os.path.dirname(self.state_path), "FIX_CLOSURE_LOG.ndjson")
                if os.path.exists(ndjson_path):
                    try:
                        with open(ndjson_path, "r", encoding="utf-8") as f:
                            lines = f.readlines()
                        # 精确匹配 bug_id（JSON key 查找，避免 substring 误判）
                        if lines:
                            try:
                                import json as _j
                                last_record = _j.loads(lines[-1].strip())
                                if last_record.get("bug_id") == self.bug_id:
                                    with open(ndjson_path, "w", encoding="utf-8") as f:
                                        f.writelines(lines[:-1])
                            except Exception:
                                pass
                    except OSError:
                        pass
            tx.register("phase3", f"ndjson_{self.bug_id}", _undo_ndjson)

            # 事件发布（非关键，不注册回滚）
            _pub = EventPublisher(state_path=self.state_path)
            learn_event = {
                "kind": "fix_closure",
                "bug_id": self.bug_id,
                "bug_type": self.bug_type,
                "module": self.module,
                "root_cause": sf.filter_sensitive(root_cause_summary[:120]),
                "fix_type": self.fix_type,
                "fallback": fallback_mode,
                "timestamp": datetime.now(TZ).isoformat(timespec="seconds"),
            }
            try:
                _pub.publish_learn(learn_event)
            except Exception as pe:
                log.warning("事件发布失败（非关键，继续）: %s", pe)

            # 写回过滤后的文件
            if filtered_contents and original_contents:
                for fpath, filtered_text in filtered_contents.items():
                    if fpath in original_contents:
                        orig = original_contents[fpath]
                        with open(fpath, "w", encoding="utf-8") as f:
                            f.write(filtered_text)
                        tx.register(
                            "phase3", f"filter_restore_{os.path.basename(fpath)}",
                            (lambda p, o: (
                                lambda: (_fh := open(p, "w", encoding="utf-8"),
                                         _fh.write(o), _fh.close())[-1]
                                if os.path.exists(p) else None
                            ))(fpath, orig),
                        )

            # 注销 session（先注册回滚，再执行——防止 tx.register 失败导致不可恢复）
            tx.register(
                "phase3", "session_reregister",
                lambda: sm.register(self.session_id, self.bug_id, self.state_path),
            )
            sm.unregister(self.session_id, self.state_path)

            log.info("归档完成: bug_id=%s", self.bug_id)
            return ArchiveResult(
                success=True,
                details="归档完成",
            )

        except Exception as e:
            log.error("归档失败: %s", e)
            return ArchiveResult(
                success=False, blocking=True,
                details=str(e),
            )
