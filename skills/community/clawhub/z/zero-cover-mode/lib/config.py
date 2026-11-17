"""零稀泥模式 — 中央配置

所有模块从此文件读取配置，避免各模块分散定义。
"""
from datetime import timezone, timedelta
import os

# ── 版本 ──
SKILL_VERSION = "1.0.0"

# ── 时区 ──
TZ = timezone(timedelta(hours=8))

# ── 文件路径 ──
DEFAULT_STATE_PATH = ".zero-cover-state.json"
DEFAULT_NDJSON_PATH = "FIX_CLOSURE_LOG.ndjson"

# ── NDJSON ──
NDJSON_MAX_LINES = 1000

# ── 锁 ──
LOCK_TIMEOUT = 5  # seconds

# ── 根因深度 ──
ROOT_CAUSE_MIN_LEVEL = 3  # 最低要求 L3（有内容）；L4 为 optional 但鼓励

# ── 清理 ──
BUG_DIR_MAX_AGE_HOURS = 48

# ── 循环检测 ──
LOOP_WINDOW_SIZE = 10
LOOP_THRESHOLD = 3
LOOP_SIM_THRESHOLD = 0.8

# ── 重构警报 ──
MAX_ALERT_BLOCKS = 20

# ── 假数据检测 ──
FAKE_DATA_BLOCKING_PCT = 0.8  # 硬编码断言占 assert 的比例阈值

# ── 标记文件 ──
WORKSPACE_MARKER_FILENAME = ".zerocover-root"

# ── 回归测试 ──
REGRESSION_TIMEOUT = 300  # seconds

# ── 清理 ──
SESSION_MAX_AGE_HOURS = 168
FIX_HISTORY_MAX = 200

# ── 重试 ──
BACKOFF_BASE = 0.05  # 退避基时（秒）
BACKOFF_MAX = 2.0    # 退避最大间隔
MAX_RETRIES = 3       # 默认最大重试次数

# ── 全局超时 ──
PIPELINE_TIMEOUT = 600  # 单次 pipeline 超时（秒）
SUB_PROCESS_TIMEOUT = 300  # 子进程超时

# ── 熔断 ──
CIRCUIT_BREAKER_THRESHOLD = 5  # 连续失败次数触发
CIRCUIT_BREAKER_RESET = 60      # 熔断后重置时间（秒）

# ── 工具函数 ──
def now_iso():
    from datetime import datetime
    return datetime.now(TZ).isoformat(timespec="seconds")
