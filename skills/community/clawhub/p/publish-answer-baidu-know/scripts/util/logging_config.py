"""Re-export unified logging (implementation: jiangchang_skill_core.unified_logging)."""

from jiangchang_skill_core.unified_logging import (
    attach_unified_file_handler,
    ensure_trace_for_process,
    get_skill_log_file_path,
    get_skill_logger,
    get_unified_logs_dir,
    setup_skill_logging,
    subprocess_env_with_trace,
)

__all__ = [
    "attach_unified_file_handler",
    "ensure_trace_for_process",
    "get_skill_log_file_path",
    "get_skill_logger",
    "get_unified_logs_dir",
    "setup_skill_logging",
    "subprocess_env_with_trace",
]
