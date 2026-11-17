"""零稀泥模式 — 编排层 orchestrator.py

将四阶段闭环封装为可编程 API。

用法（Python API）:
    from orchestrator import Pipeline, PhaseResult, PipelineConfig

    pipe = Pipeline(PipelineConfig(
        session_id="session_abc", bug_id="algo-typ-...",
        bug_type="config_error", module="algorithmic_novel_writer",
        test_cmd="pytest tests/ -v --tb=short", project_type="python", vcs="git",
    ))
    result = pipe.run_full_pipeline(
        root_cause_md=root_cause_text, test_code=test_code_text, fix_type="permanent",
    )
"""

import json, os, sys, time, logging, threading
from datetime import datetime
from typing import Optional, List, Dict

from .config import (TZ, SKILL_VERSION,
                     REGRESSION_TIMEOUT, PIPELINE_TIMEOUT, SUB_PROCESS_TIMEOUT,
                     CIRCUIT_BREAKER_THRESHOLD, CIRCUIT_BREAKER_RESET)
from . import state_manager as sm
from . import uow as _uow
from .env_detector import EnvironDetector
from .test_runner import TestRunner
from .contracts import (build_fix_record, BugType, FixType,
                        PipelineConfigSchema, PhaseResultSchema, PipelinePhase)
from .checkpoint_manager import CheckpointManager
from .transaction_coordinator import TransactionCoordinator
from .validation_chain import ValidationChain
from .archive_pipeline import ArchivePipeline, ArchiveResult

log = logging.getLogger("orchestrator")

DEFAULT_BUGS_DIR = "bugs"


class PhaseResult(PhaseResultSchema):
    """Pipeline phase execution result — Pydantic 契约校验"""
    pass


class PipelineConfig(PipelineConfigSchema):
    """流水线配置 — Pydantic 契约校验"""
    cron_instructions: List[Dict] = []
    lang: str = ""
    model_config = {"extra": "allow"}


class CircuitBreaker:
    """线程安全的熔断器"""
    def __init__(self, threshold: int = CIRCUIT_BREAKER_THRESHOLD,
                 reset_seconds: int = CIRCUIT_BREAKER_RESET):
        self._threshold = threshold
        self._reset_seconds = reset_seconds
        self._lock = threading.Lock()
        self._failures = 0
        self._last_failure_at = 0.0

    def record_failure(self):
        with self._lock:
            self._failures += 1
            self._last_failure_at = time.time()

    def record_success(self):
        with self._lock:
            self._failures = 0
            self._last_failure_at = 0.0

    def is_tripped(self) -> bool:
        with self._lock:
            if self._failures >= self._threshold:
                if time.time() - self._last_failure_at > self._reset_seconds:
                    self._failures = 0
                    self._last_failure_at = 0.0
                    return False
                return True
            return False

    @property
    def failures(self) -> int:
        with self._lock:
            return self._failures


class Pipeline:
    """四阶段闭环编排器"""

    def __init__(self, config: PipelineConfig,
                 checkpoint_mgr=None, breaker=None,
                 tx=None, validation=None):
        self.cfg = config
        if not self.cfg.state_path:
            self.cfg.state_path = sm.locate()

        _detector = EnvironDetector(self.cfg.workspace_root or os.getcwd())
        _env = _detector.detect()
        self._apply_env(_env)

        self.session_id = config.session_id
        self.bug_id = config.bug_id
        self.bug_dir = os.path.join(config.bugs_dir, config.bug_id)

        # 依赖注入（显式 None 检查，避免 __len__=0 导致的 falsy 陷阱）
        self._ckm = checkpoint_mgr if checkpoint_mgr is not None else CheckpointManager(config.state_path)
        self._breaker = breaker if breaker is not None else CircuitBreaker()
        self._tx = tx if tx is not None else TransactionCoordinator()
        self._validation = validation if validation is not None else ValidationChain()

        self._checkpoint = self._ckm.get(config.bug_id)

        if self._breaker.is_tripped():
            log.error("Pipeline 熔断已激活 (%d 次连续失败)", self._breaker.failures)
            raise RuntimeError(
                f"Pipeline 熔断: 连续 {self._breaker.failures} 次失败，请修复后重试"
            )

    def _apply_env(self, env: dict):
        if not self.cfg.project_type or self.cfg.project_type == "unknown":
            self.cfg.project_type = env.get("project_type", "unknown")
        if not self.cfg.test_cmd:
            self.cfg.test_cmd = env.get("test_cmd", "")
        if not self.cfg.vcs or self.cfg.vcs == "none":
            self.cfg.vcs = env.get("vcs", "none")
        if not self.cfg.lang:
            self.cfg.lang = env.get("lang", "")

    # ── Phase 0 ──

    def phase0_prepare(self) -> PhaseResult:
        try:
            sm.register(self.session_id, self.bug_id, self.cfg.state_path)
            self._tx.register("phase0", "session_unregister",
                              lambda: sm.unregister(self.session_id, self.cfg.state_path))
            os.makedirs(self.bug_dir, exist_ok=True)
            self._tx.register("phase0", f"rmdir_{self.bug_dir}", _uow.undo_rmdir(self.bug_dir))
            os.makedirs(os.path.join(self.bug_dir, "evidence"), exist_ok=True)

            ts = datetime.now(TZ).isoformat(timespec="seconds")
            files = {"bug_dir": self.bug_dir, "evidence_dir": os.path.join(self.bug_dir, "evidence")}
            self._ckm.save(self.bug_id, "phase0", {"ts": ts})
            self._refresh_checkpoint()

            self._breaker.record_success()
            return PhaseResult(phase=PipelinePhase.PHASE0, success=True,
                               details="session ok", output_files=files,
                               compensation_journal=[{"phase": "phase0", "entries": len(self._tx)}])
        except Exception as e:
            self._breaker.record_failure()
            rolled = self._tx.compensate_from("phase0")
            log.error("Phase 0 fail(rollback %d): %s", len(rolled), e)
            return PhaseResult(phase=PipelinePhase.PHASE0, success=False,
                               blocking=True, details=str(e),
                               compensation_journal=[{"rolled_back": rolled}])

    # ── Phase 1 ──

    def phase1_root_cause(self, root_cause_md: str) -> PhaseResult:
        bug_root_cause_path = os.path.join(self.bug_dir, "BUG_ROOT_CAUSE.md")
        try:
            with open(bug_root_cause_path, "w", encoding="utf-8") as f:
                f.write(root_cause_md)
            self._tx.register("phase1", f"rmfile_{os.path.basename(bug_root_cause_path)}",
                              _uow.undo_rmfile(bug_root_cause_path))

            vr = self._validation.validate_root_cause(bug_root_cause_path)
            if vr.blocking:
                rolled = self._tx.compensate_from("phase1")
                self._breaker.record_failure()
                return PhaseResult(phase=PipelinePhase.PHASE1, success=False, blocking=True,
                                   details=vr.details,
                                   output_files={"BUG_ROOT_CAUSE.md": bug_root_cause_path},
                                   compensation_journal=[{"rolled_back": rolled}])

            self._ckm.save(self.bug_id, "phase1", vr.root_cause_analysis or {})
            self._refresh_checkpoint()
            self._breaker.record_success()
            return PhaseResult(phase=PipelinePhase.PHASE1, success=True,
                               details=vr.details,
                               output_files={"BUG_ROOT_CAUSE.md": bug_root_cause_path},
                               compensation_journal=[{"phase": "phase1", "entries": len(self._tx)}])
        except Exception as e:
            self._breaker.record_failure()
            rolled = self._tx.compensate_from("phase1")
            log.error("Phase 1 失败(已回滚 %d): %s", len(rolled), e)
            return PhaseResult(phase=PipelinePhase.PHASE1, success=False,
                               blocking=True, details=str(e),
                               compensation_journal=[{"rolled_back": rolled}])

    # ── Phase 2 ──

    def phase2_test(self, test_code: str, test_cmd: str = "") -> PhaseResult:
        test_name = f"test_{self.cfg.module}_fix_{self.bug_id}.py"
        try:
            root = (self.cfg.workspace_root or os.getcwd()).strip()
            test_path = os.path.join(root, "tests", "regression", test_name)
            bug_test_path = os.path.join(self.bug_dir, test_name)
            os.makedirs(os.path.join(root, "tests", "regression"), exist_ok=True)

            with open(test_path, "w", encoding="utf-8") as f:
                f.write(test_code)
            self._tx.register("phase2", f"rmfile_{test_name}", _uow.undo_rmfile(test_path))
            with open(bug_test_path, "w", encoding="utf-8") as f:
                f.write(test_code)
            self._tx.register("phase2", f"rmfile_bug_{test_name}", _uow.undo_rmfile(bug_test_path))

            vr = self._validation.validate_test(test_path, root)
            if vr.blocking:
                rolled = self._tx.compensate_from("phase2")
                self._breaker.record_failure()
                return PhaseResult(phase=PipelinePhase.PHASE2, success=False, blocking=True,
                                   details=vr.details, output_files={"test_file": test_path},
                                   compensation_journal=[{"rolled_back": rolled}])

            _test_runner = TestRunner(workspace_root=root)
            actual_cmd = test_cmd or self.cfg.test_cmd
            regression_ok = True
            regr_pass = 0
            regr_fail = 0

            if actual_cmd and actual_cmd != "skip":
                regression_log = os.path.join(self.bug_dir, "regression_output.log")
                result = _test_runner.run(actual_cmd)
                with open(regression_log, "w", encoding="utf-8") as f:
                    f.write(f"CMD: {actual_cmd}\nRC: {result.returncode}\n")
                    f.write("---STDOUT---\n")
                    f.write(result.stdout)
                    f.write("\n---STDERR---\n")
                    f.write(result.stderr)
                if not result.success:
                    regression_ok = False
                    regr_fail = 1
                else:
                    regr_pass = 1
                s = result.summary()
                if s["total"] > 0:
                    regr_pass, regr_fail = s["pass"], s["fail"]

            if not regression_ok:
                rolled = self._tx.compensate_from("phase2")
                self._breaker.record_failure()
                rc_info = getattr(result, 'returncode', '?') if 'result' in dir() else '?'
                return PhaseResult(phase=PipelinePhase.PHASE2, success=False, blocking=True,
                                   details=f"回归失败 (rc={rc_info})",
                                   output_files={"test_file": test_path},
                                   compensation_journal=[{"rolled_back": rolled}])

            test_result_path = os.path.join(self.bug_dir, "TEST_RESULT.md")
            now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M (%Z)")
            result_content = (
                f"# 测试验证结果 — {self.bug_id}\n\n"
                f"## 环境\n"
                f"- 测试时间: {now}\n"
                f"- 项目类型: {self.cfg.project_type}\n"
                f"- VCS: {self.cfg.vcs}\n"
                f"- 测试命令: {actual_cmd or 'N/A'}\n\n"
                f"## 结果\n"
                f"| 测试 | 结果 |\n"
                f"|------|------|\n"
                f"| 新增测试 | {test_name} |\n"
                f"| 是否通过 | {'PASS' if regression_ok else 'FAIL'} |\n"
                f"| 回归通过 | {regr_pass} |\n"
                f"| 回归失败 | {regr_fail} |\n"
                f"| blocking | {'true' if not regression_ok else 'false'} |\n"
            )
            with open(test_result_path, "w", encoding="utf-8") as f:
                f.write(result_content)
            self._tx.register("phase2", "rmfile_test_result", _uow.undo_rmfile(test_result_path))

            self._ckm.save(self.bug_id, "phase2", {"regr_pass": regr_pass, "regr_fail": regr_fail})
            self._refresh_checkpoint()
            self._breaker.record_success()
            return PhaseResult(phase=PipelinePhase.PHASE2, success=True,
                               details="回归通过" if regression_ok else "skip",
                               output_files={"test_file": test_path, "TEST_RESULT.md": test_result_path},
                               compensation_journal=[{"phase": "phase2", "entries": len(self._tx)}])
        except Exception as e:
            self._breaker.record_failure()
            rolled = self._tx.compensate_from("phase2")
            log.error("Phase 2 失败(已回滚 %d): %s", len(rolled), e)
            return PhaseResult(phase=PipelinePhase.PHASE2, success=False,
                               blocking=True, details=str(e),
                               compensation_journal=[{"rolled_back": rolled}])

    # ── Phase 3 ──

    def phase3_closure(self, root_cause_summary: str = "",
                       test_skipped: bool = False,
                       regr_pass: int = 0, regr_fail: int = 0,
                       fallback_mode: bool = False) -> PhaseResult:
        cp = self._checkpoint
        regr_pass = regr_pass or cp.get("phase2", {}).get("regr_pass", 0)
        regr_fail = regr_fail or cp.get("phase2", {}).get("regr_fail", 0)

        try:
            ap = ArchivePipeline(
                state_path=self.cfg.state_path, bug_id=self.bug_id,
                session_id=self.session_id, bug_dir=self.bug_dir,
                bug_type=str(self.cfg.bug_type),
                module=self.cfg.module or self.cfg.project_type,
                fix_type=str(self.cfg.fix_type), vcs=self.cfg.vcs,
            )
            pre = ap.run_pre_checks(root_cause_summary)
            if pre["blocking"]:
                self._breaker.record_failure()
                return PhaseResult(phase=PipelinePhase.PHASE3, success=False, blocking=True,
                                   details=pre["details"],
                                   output_files={"loop_report": pre.get("loop_file")} if pre.get("loop_file") else {})

            fr = build_fix_record(
                bug_id=self.bug_id, bug_type=self.cfg.bug_type,
                module=self.cfg.module or self.cfg.project_type,
                fix_type=self.cfg.fix_type, root_cause=root_cause_summary[:255],
                test_count=1 if not test_skipped else 0,
                regression_pass=regr_pass, regression_fail=regr_fail,
                blocking=False, details='fallback' if fallback_mode else '',
                vcs_hash=self.cfg.vcs, test_skipped=test_skipped,
                was_blocking_issue=False,
                skip_reason=self.cfg.skip_reason if test_skipped else '',
            )
            ar = ap.execute(
                record=fr, tx=self._tx, root_cause_summary=root_cause_summary,
                fallback_mode=fallback_mode, test_skipped=test_skipped,
                regr_pass=regr_pass, regr_fail=regr_fail,
                filtered_contents=pre.get("filtered"),
                original_contents=pre.get("original"),
            )
            if not ar.success:
                self._breaker.record_failure()
                return PhaseResult(phase=PipelinePhase.PHASE3, success=False, blocking=True,
                                   details=ar.details)

            self._tx.clear()
            self._ckm.save(self.bug_id, "phase3",
                           {"completed_at": datetime.now(TZ).isoformat()})
            self._refresh_checkpoint()
            self._breaker.record_success()
            return PhaseResult(phase=PipelinePhase.PHASE3, success=True,
                               details="归档完成, 循环检测=未触发",
                               compensation_journal=[{"phase": "phase3", "cleared": True}])
        except Exception as e:
            self._breaker.record_failure()
            rolled = self._tx.compensate_from("phase3")
            log.error("Phase 3 失败(已回滚 %d): %s", len(rolled), e)
            return PhaseResult(phase=PipelinePhase.PHASE3, success=False,
                               blocking=True, details=str(e),
                               compensation_journal=[{"rolled_back": rolled}])
        finally:
            try:
                sm.cleanup_bugs(path=self.cfg.state_path)
            except Exception as ce:
                log.warning("自动清理失败（非关键）: %s", ce)

    # ── Phase 4 ──

    def phase4_verify(self, test_cmd: str = "", hours: List[int] = None) -> PhaseResult:
        if hours is None:
            hours = [24, 168, 720]
        try:
            cmd = test_cmd or self.cfg.test_cmd
            sm.schedule_verification(self.bug_id, hours, path=self.cfg.state_path)
            instructions = sm.generate_cron_instructions(
                self.bug_id, cmd, path=self.cfg.state_path)
            return PhaseResult(phase=PipelinePhase.PHASE4, success=True,
                               details=f"验证计划 {hours} 已安排",
                               cron_instructions=instructions)
        except Exception as e:
            log.error("Phase 4 失败: %s", e)
            return PhaseResult(phase=PipelinePhase.PHASE4, success=False,
                               blocking=False, details=str(e))

    # ── 完整流水线 ──

    def run_full_pipeline(
        self, root_cause_md: str, test_code: str = "", test_cmd: str = "",
        bug_type: str = "", fix_type: str = "permanent", module: str = "",
        root_cause_summary: str = "", skip_regression: bool = False,
        skip_reason: str = "", project_name: str = "",
        verify_hours: List[int] = None, fallback_mode: bool = False,
        timeout_seconds: int = PIPELINE_TIMEOUT,
    ) -> List[PhaseResult]:
        if bug_type:
            self.cfg.bug_type = bug_type
        if module:
            self.cfg.module = module
        if fix_type:
            self.cfg.fix_type = fix_type
        if project_name:
            self.cfg.project_name = project_name
        if skip_regression:
            self.cfg.skip_regression = True
            self.cfg.skip_reason = skip_reason or "手动跳过"

        self._validate_inputs()
        self._tx.reset()

        _deadline = time.time() + timeout_seconds
        results: List[PhaseResult] = []

        for phase_name, phase_fn, args_getter in [
            ("phase0", self.phase0_prepare, lambda: []),
            ("phase1", self.phase1_root_cause, lambda: [root_cause_md]),
            ("phase2", self.phase2_test, lambda: [test_code, test_cmd]),
            ("phase3", self.phase3_closure, lambda: [
                root_cause_summary, skip_regression,
                self._checkpoint.get("phase2", {}).get("regr_pass", 0),
                self._checkpoint.get("phase2", {}).get("regr_fail", 0),
                fallback_mode,
            ]),
            ("phase4", self.phase4_verify, lambda: [test_cmd]),
        ]:
            if time.time() > _deadline:
                log.error("Pipeline 全局超时 (%ds)", timeout_seconds)
                return results
            if phase_name == "phase2" and skip_regression:
                self._ckm.save(self.bug_id, "phase2", {"skipped": True, "reason": skip_reason})
                self._refresh_checkpoint()
                results.append(PhaseResult(phase=PipelinePhase.PHASE2, success=True,
                                           details=f"跳过回归: {skip_reason}"))
                continue
            if phase_name == "phase4" and verify_hours is None and self._ckm.has(self.bug_id, "phase4"):
                continue
            if phase_name != "phase4" and self._ckm.has(self.bug_id, phase_name):
                continue

            if phase_name == "phase4":
                r = phase_fn(verify_hours if verify_hours is not None else [24])
            else:
                r = phase_fn(*args_getter())
            results.append(r)
            if phase_name != "phase4" and not r.success:
                return results
            if phase_name == "phase4" and r.success and r.cron_instructions:
                self.cfg.cron_instructions.extend(r.cron_instructions)
                _cj = os.path.join(self.bug_dir, ".cron-jobs.json")
                try:
                    with open(_cj, "w") as _f:
                        json.dump(r.cron_instructions, _f)
                except Exception:
                    pass

        self._tx.clear()
        return results

    # ── 内部方法 ──

    def _validate_inputs(self):
        errors = []
        if not self.cfg.session_id or len(self.cfg.session_id) < 1:
            errors.append("session_id 不能为空")
        if not self.cfg.bug_id or len(self.cfg.bug_id) < 5:
            errors.append(f"bug_id 无效: '{self.cfg.bug_id}'")
        else:
            import re
            if not re.match(r"^[a-z]{3,4}-[a-z]{3}-\d{10,12}-[a-f0-9]{4}$", self.cfg.bug_id) \
               and not re.match(r"^(resume_|cli_)\d+$", self.cfg.bug_id):
                errors.append(f"bug_id 格式无效: '{self.cfg.bug_id}'")
        if not self.cfg.bug_type or str(self.cfg.bug_type) == "":
            errors.append("bug_type 不能为空")
        if not self.cfg.module or self.cfg.module == "":
            errors.append("module 不能为空")
        if errors:
            raise ValueError(f"输入校验失败: {'; '.join(errors)}")

    def _refresh_checkpoint(self):
        self._checkpoint = self._ckm.get(self.bug_id)

    def status(self) -> dict:
        return {
            "bug_id": self.bug_id, "session_id": self.session_id,
            "checkpoints": self._checkpoint,
            "completed_phases": [k for k in ("phase0", "phase1", "phase2", "phase3", "phase4")
                                 if k in self._checkpoint],
        }

    def resume(self) -> List[str]:
        completed = set(k for k in ("phase0", "phase1", "phase2", "phase3", "phase4")
                        if k in self._checkpoint)
        all_phases = ["phase0", "phase1", "phase2", "phase3", "phase4"]
        pending = [p for p in all_phases if p not in completed]
        if "phase0" in pending:
            r = self.phase0_prepare()
            if not r.success:
                log.error("resume: Phase 0 自动补全失败: %s", r.details)
                return pending  # 保留 phase0 在 pending 中，不静默移除
            pending.remove("phase0")
            log.info("resume: Phase 0 已自动补全")
        return pending
