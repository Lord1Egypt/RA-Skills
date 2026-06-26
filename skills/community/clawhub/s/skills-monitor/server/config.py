"""
Skills Monitor 中心化服务器 — 配置文件
=====================================
包括数据库、微信公众号、微信小程序、推送调度等配置。
部署时请通过环境变量覆盖敏感信息。
"""

import os
from pathlib import Path

# ──────── 基础配置 ────────
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
SECRET_KEY = os.environ.get("SM_SECRET_KEY", "skills-monitor-secret-key-change-me")
DEBUG = os.environ.get("SM_DEBUG", "true").lower() == "true"

# ──────── 轻量鉴权（可选） ────────
# 为 dashboard/H5 等“读数据页面”提供一把共享钥匙（生产环境建议设置）。
# 为空则不启用该校验（保持本地开发体验）。
DASHBOARD_TOKEN = os.environ.get("SM_DASHBOARD_TOKEN", "").strip()

# ──────── 数据库配置 ────────
# 使用 SQLite（轻量部署）或 PostgreSQL（生产环境）
DATABASE_TYPE = os.environ.get("SM_DB_TYPE", "sqlite")  # sqlite / postgresql
DATABASE_URL = os.environ.get(
    "SM_DATABASE_URL",
    f"sqlite:///{BASE_DIR / 'data' / 'skills_monitor_server.db'}"
)

# ──────── 微信公众号配置 ────────
WECHAT_OA_APP_ID = os.environ.get("SM_WECHAT_OA_APP_ID", "")
WECHAT_OA_APP_SECRET = os.environ.get("SM_WECHAT_OA_APP_SECRET", "")
WECHAT_OA_TOKEN = os.environ.get("SM_WECHAT_OA_TOKEN", "skills-monitor-wechat")
WECHAT_OA_ENCODING_AES_KEY = os.environ.get("SM_WECHAT_OA_AES_KEY", "")
# 模板消息 ID（需在公众号后台配置）
WECHAT_TEMPLATE_DAILY_REPORT = os.environ.get("SM_WECHAT_TPL_DAILY", "")
WECHAT_TEMPLATE_ALERT = os.environ.get("SM_WECHAT_TPL_ALERT", "")

# ──────── 微信小程序配置 ────────
WECHAT_MP_APP_ID = os.environ.get("SM_WECHAT_MP_APP_ID", "")
WECHAT_MP_APP_SECRET = os.environ.get("SM_WECHAT_MP_APP_SECRET", "")

# ──────── 数据压缩 ────────
# 上报数据超过此大小时自动启用 gzip 压缩
UPLOAD_COMPRESS_THRESHOLD_BYTES = 10 * 1024  # 10KB

# ──────── 推送调度 ────────
DAILY_REPORT_CRON_HOUR = int(os.environ.get("SM_REPORT_HOUR", "21"))
DAILY_REPORT_CRON_MINUTE = int(os.environ.get("SM_REPORT_MINUTE", "0"))

# ──────── 服务器 ────────
SERVER_HOST = os.environ.get("SM_HOST", "0.0.0.0")
SERVER_PORT = int(os.environ.get("SM_PORT", "5100"))

# ──────── H5 页面 ────────
H5_BASE_URL = os.environ.get("SM_H5_BASE_URL", f"http://localhost:{SERVER_PORT}")
