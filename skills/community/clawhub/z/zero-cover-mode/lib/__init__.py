"""零稀泥模式 — 工具库 v1.0.0

模块清单:
- config.py                  — 中央配置（版本/时区/常量）
- contracts.py               — 数据契约层（Pydantic 模型）
- state_manager.py           — .zero-cover-state.json 的原子读写、session 管理
- ndjson_schema.py           — FIX_CLOSURE_LOG.ndjson 的校验、追加与旋转
- root_cause_validator.py    — BUG_ROOT_CAUSE.md 的 5-Whys 深度验证
- sensitive_filter.py        — API key/密码等敏感数据过滤
- fake_data_detector.py      — 假数据检测（L1/L2/L3）
- loop_detector.py           — 跨修复模式循环检测
- weekly_report.py           — 周报聚合
- refactoring_alert.py       — 重构警报 upsert
- ndjson_migrate_v1_to_v2.py — ndjson schema 数据迁移
- event_publisher.py         — 事件发布器
- test_runner.py             — 测试执行器
- uow.py                     — Unit of Work / Saga 事务模式
- orchestrator.py            — 四阶段闭环编排器
- transaction_coordinator.py — 统一事务协调器
- checkpoint_manager.py      — Checkpoint 持久化管理器
- validation_chain.py        — 校验链
- archive_pipeline.py        — 归档流水线
- persistence_facade.py      — 持久化门面
- repository.py              — 持久化仓库
- file_ops.py                — 文件操作 Sidecar
- env_detector.py            — 项目环境检测器
- backend_checker.py         — 活代码验证后端检查器

用法: python -m lib.<module> <action> <args...>
"""

import sys, os, logging
from . import file_ops
from . import contracts
from . import repository
from . import event_publisher
from . import test_runner
from .config import SKILL_VERSION

__all__ = [
    "config", "contracts", "file_ops", "repository",
    "state_manager", "ndjson_schema", "orchestrator",
    "fake_data_detector", "loop_detector", "root_cause_validator",
    "sensitive_filter", "refactoring_alert", "weekly_report",
    "env_detector", "backend_checker", "uow", "persistence_facade",
    "checkpoint_manager", "validation_chain", "archive_pipeline",
    "transaction_coordinator", "cli",
]
__version__ = SKILL_VERSION

_logging_initialized = False


def setup_logging(level=logging.WARNING):
    global _logging_initialized
    if _logging_initialized:
        return
    logging.basicConfig(
        stream=sys.stderr, level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    _logging_initialized = True
