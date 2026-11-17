"""零稀泥模式 — 数据契约层 (Pydantic Models)

所有跨层数据传递必须经过 Pydantic 模型校验。
每个模型都定义了严格的类型/范围/格式约束，杜绝运行时类型爆炸。

Usage:
    from .contracts import FixRecord, BugType
    record = FixRecord(bug_id="algo-typ-17000001-abc", ...)
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List, Dict, Any, Callable
from enum import Enum


# ── 枚举 ──

class BugType(str, Enum):
    CONFIG_ERROR = "config_error"
    TYPE_MISMATCH = "type_mismatch"
    NULL_POINTER = "null_pointer"
    LOGIC_ERROR = "logic_error"
    RESOURCE_LEAK = "resource_leak"
    DEAD_CODE = "dead_code"
    PERFORMANCE = "performance"
    DATA_CORRUPTION = "data_corruption"
    RACE_CONDITION = "race_condition"
    EDGE_CASE = "edge_case"
    SYNTAX_ERROR = "syntax_error"
    WORKFLOW_BREAK = "workflow_break"
    UNKNOWN = "unknown"
    MULTIPLE = "multiple"


class FixType(str, Enum):
    PERMANENT = "permanent"
    WORKAROUND = "workaround"
    REVERTED = "reverted"


class FixStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class PipelinePhase(str, Enum):
    PHASE0 = "phase0"
    PHASE1 = "phase1"
    PHASE2 = "phase2"
    PHASE3 = "phase3"
    PHASE4 = "phase4"


class BackendCheckVerdict(str, Enum):
    """backend_checker.full_check() 返回的整体判定"""
    PASS = "PASS"
    WARN = "WARN"
    BLOCKING = "BLOCKING"


# ── 核心记录 ──

class FixRecord(BaseModel):
    """FIX_CLOSURE_LOG.ndjson 的单条记录契约"""
    timestamp: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",
                           description="ISO8601 时间戳（秒级）")
    bug_id: str = Field(min_length=5, max_length=64,
                        description="Bug 唯一 ID")
    module: str = Field(min_length=1, max_length=128,
                        description="模块名或项目类型")
    bug_type: BugType = Field(description="Bug 类型枚举")
    fix_type: FixType = Field(description="修复类型")
    root_cause: str = Field(default="", max_length=500,
                            description="根因摘要")
    test_count: int = Field(default=0, ge=0, le=10000,
                            description="测试用例数")
    regression_pass: int = Field(default=0, ge=0, le=10000,
                                 description="回归通过数")
    regression_fail: int = Field(default=0, ge=0, le=10000,
                                 description="回归失败数")
    blocking: bool = Field(default=False,
                           description="是否阻塞性 bug")
    test_skipped: bool = Field(default=False,
                               description="是否跳过测试")
    vcs_hash: str = Field(default="none", max_length=64,
                          description="版本控制 hash")
    details: str = Field(default="", max_length=1000,
                         description="附加详情")
    was_blocking_issue: bool = Field(default=False,
                                     description="是否是阻塞性问题（归档标记）")
    skip_reason: str = Field(default="", max_length=200,
                             description="跳过测试的原因")
    validated: bool = Field(default=True,
                            description="是否通过 schema 校验")
    legacy_fix_type: Optional[str] = Field(default=None,
                                           description="迁移前的 fix_type")
    bug_type_secondary: Optional[List[str]] = Field(default=None,
                                                    description="次要 bug 类型")
    migrated: bool = Field(default=False,
                           description="是否从 v1 迁移")
    sensitive_filtered: bool = Field(default=False, alias="_sensitive_filtered",
                                     description="是否已通过敏感数据过滤")

    @field_validator("regression_pass", "regression_fail")
    @classmethod
    def check_skip_consistency(cls, v, info):
        if info.data.get("test_skipped") and v > 0:
            raise ValueError(f"test_skipped=True but {info.field_name}={v} — 矛盾状态")
        return v

    @field_validator("root_cause")
    @classmethod
    def root_cause_not_empty_for_blocking(cls, v, info):
        if info.data.get("blocking") and not v:
            raise ValueError("blocking=True 但 root_cause 为空")
        return v


# ── State 相关 ──

class SessionInfo(BaseModel):
    """Session 信息契约"""
    bug_id: str = Field(min_length=1)
    started_at: str = Field(pattern=r"\d{4}-\d{2}-\d{2}")
    updated_at: str = Field(pattern=r"\d{4}-\d{2}-\d{2}")
    status: FixStatus = Field(default=FixStatus.IN_PROGRESS)
    completed_at: Optional[str] = None
    re_registered: Optional[str] = None


class PipelineCheckpoint(BaseModel):
    """Pipeline 阶段 checkpoint"""
    phase0: Optional[dict] = None
    phase1: Optional[dict] = None
    phase2: Optional[dict] = None
    phase3: Optional[dict] = None
    phase4: Optional[dict] = None
    updated_at: str = ""


class StateSchema(BaseModel):
    """state.json 顶层契约"""
    version: str = Field(default="1.0.0")
    format_version: int = Field(default=2, ge=1)
    total_fixes: int = Field(default=0, ge=0)
    active_session_ids: List[str] = Field(default_factory=list)
    sessions: Dict[str, SessionInfo] = Field(default_factory=dict)
    bug_id_registry: List[str] = Field(default_factory=list)
    bug_type_counter: Dict[str, int] = Field(default_factory=dict)
    fix_history: List[dict] = Field(default_factory=list,
                                    description="从 ndjson 重建，不持久化")
    verifications: Dict[str, dict] = Field(default_factory=dict)
    last_weekly_report: Optional[str] = None
    ndjson_line_count: int = Field(default=0, ge=0)
    ndjson_last_rotate: Optional[str] = None
    project_env: dict = Field(default_factory=lambda: {
        "project_type": "unknown", "test_cmd": "", "vcs": "none"})
    projects: Dict[str, dict] = Field(default_factory=dict)
    deprecated_fix_history: bool = Field(default=True, alias="_deprecated_fix_history")
    ndjson_is_primary: bool = Field(default=True, alias="_ndjson_is_primary")
    pipeline_checkpoints: Dict[str, PipelineCheckpoint] = Field(default_factory=dict, alias="_pipeline_checkpoints")
    orphan_sessions: List[dict] = Field(default_factory=list, alias="_orphan_sessions")
    verify_needs_cron: List[dict] = Field(default_factory=list, alias="_verify_needs_cron")
    state_size_bytes: int = Field(default=0, ge=0, alias="_state_size_bytes")
    updated_at: str = ""


# ── Pipeline 相关 ──

class PipelineConfigSchema(BaseModel):
    """PipelineConfig 的 Pydantic 版 — 严格契约校验"""
    session_id: str = Field(min_length=1, description="Session 唯一 ID")
    bug_id: str = Field(
        min_length=5, max_length=64,
        pattern=r"^[a-z]{3,4}-[a-z]{3}-\d{10,12}-[a-f0-9]{4}$",
        description="Bug ID，格式: {mod_prefix}-{type_prefix}-{timestamp}-{rand_suffix}",
    )
    workspace_root: str = ""
    bugs_dir: str = "bugs"
    state_path: str = ""
    project_type: str = "unknown"
    test_cmd: str = ""
    vcs: str = "none"
    bug_type: BugType = BugType.UNKNOWN
    module: str = Field(default="", description="模块名（构造时可为空，run_full_pipeline 时填充）")
    fix_type: FixType = FixType.PERMANENT
    project_name: str = ""
    skip_regression: bool = False
    skip_reason: str = ""

    @field_validator("bug_id")
    @classmethod
    def validate_bug_id_format(cls, v):
        """bug_id 必须符合 §0.8 定义的格式，或为回退格式（resume_*/cli_* 等）"""
        import re
        # 标准格式: {mod}-{type}-{timestamp}-{hex}
        if re.match(r"^[a-z]{3,4}-[a-z]{3}-\d{10,12}-[a-f0-9]{4}$", v):
            return v
        # 回退格式（resume/cli + 时间戳）
        if re.match(r"^(resume_|cli_)\d+$", v):
            return v
        raise ValueError(
            f"bug_id 格式无效: '{v}'。"
            f"期望格式: {{mod_prefix}}-{{type_prefix}}-{{timestamp}}-{{rand_suffix}}"
        )
    model_config = {"extra": "allow"}


# ── 检测结果契约 ──

class FakeDataResult(BaseModel):
    """fake_data_detector 返回契约"""
    path: str = ""
    language: str = "python"
    L1: dict = Field(default_factory=dict)
    L2: Optional[dict] = None
    L3: dict = Field(default_factory=dict)
    blocking: bool = False


class LoopDetectionResult(BaseModel):
    """loop_detector 返回契约"""
    loop_detected: bool = False
    same_type_count: int = 0
    max_similarity: float = 0.0
    triggered: bool = False
    error: Optional[str] = None


class RootCauseAnalysis(BaseModel):
    """root_cause_validator 返回契约"""
    max_level: int = 0
    min_required: int = 3
    shallow: bool = True
    has_l4: bool = False
    missing_levels: List[str] = Field(default_factory=list)
    blocking: bool = False



class RootCauseDoc(BaseModel):
    """BUG_ROOT_CAUSE.md 结构与层级验证契约"""
    max_level: int = 0
    has_l4: bool = False
    missing_levels: List[str] = Field(default_factory=list)
    shallow: bool = True
    blocking: bool = False

class EnvDetectionResult(BaseModel):
    """env_detector 返回契约"""
    project_type: str = "unknown"
    test_cmd: str = ""
    vcs: str = "none"
    lang: str = "unknown"


# ── 测试结果契约（新增 Phase 3）──

class TestResultContract(BaseModel):
    """TestResult 的 Pydantic 版本 — 替代裸 dataclass"""
    cmd: str = ""
    returncode: int = Field(default=0, ge=-2,
                            description="-2=异常, -1=超时, >=0=正常")
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False

    @field_validator("timed_out")
    @classmethod
    def check_timeout_consistency(cls, v, info):
        if v and info.data.get("returncode") != -1:
            raise ValueError("timed_out=True 但 returncode != -1")
        return v

    @property
    def success(self) -> bool:
        return self.returncode == 0 and not self.timed_out

    @property
    def output(self) -> str:
        return self.stdout + self.stderr


class BackendCheckResult(BaseModel):
    """backend_checker.full_check() 返回契约"""
    backend_online: dict = Field(default_factory=dict)
    gateway_available: dict = Field(default_factory=dict)
    test_code_check: dict = Field(default_factory=dict)
    project_data: dict = Field(default_factory=dict)
    test_output_check: dict = Field(default_factory=dict)
    overall_verdict: BackendCheckVerdict = BackendCheckVerdict.PASS
    blocking_issues: List[str] = Field(default_factory=list)


class CheckpointData(BaseModel):
    """Checkpoint 数据契约，替代裸 dict"""
    phase: PipelinePhase
    data: dict = Field(default_factory=dict)
    saved_at: str = ""


class UoWAction(BaseModel):
    """UnitOfWork 操作契约"""
    action_id: str = Field(description="操作标识符")
    resource_path: str = Field(default="", description="关联资源路径")


# ── 增强 PhaseResult ──

class PhaseResultSchema(BaseModel):
    """PhaseResult 的 Pydantic 版 — 严格契约校验"""
    phase: PipelinePhase
    success: bool
    blocking: bool = False
    details: str = ""
    output_files: Dict[str, str] = Field(default_factory=dict)
    cron_instructions: List[Dict[str, Any]] = Field(default_factory=list)
    compensation_journal: List[dict] = Field(default_factory=list,
                                              description="补偿日志")
    undo_required: bool = Field(default=False,
                                description="标记是否需要全局回滚")


# ── 工厂方法 ──

def build_fix_record(bug_id: str, bug_type: BugType, module: str,
                     fix_type: FixType = FixType.PERMANENT,
                     root_cause: str = "", **kwargs) -> FixRecord:
    """用当前时间戳构建 FixRecord"""
    from datetime import datetime
    from .config import TZ
    ts = datetime.now(TZ).isoformat(timespec="seconds")
    return FixRecord(
        timestamp=ts, bug_id=bug_id, bug_type=bug_type,
        module=module, fix_type=fix_type, root_cause=root_cause, **kwargs
    )
