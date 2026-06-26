"""
Skills Monitor 中心化服务器 — Flask 应用入口
=============================================
启动方式：
  python -m server.app               # 开发模式
  gunicorn server.app:create_app()   # 生产模式
"""

import os
import logging
from pathlib import Path

# 加载 .env 环境变量（生产环境配置 AppID/Secret 等）
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

from flask import Flask

from server.config import (
    SECRET_KEY, DEBUG, DATABASE_URL, SERVER_HOST, SERVER_PORT,
    DAILY_REPORT_CRON_HOUR, DAILY_REPORT_CRON_MINUTE,
)
from server.models.database import init_db
from server.api import register_blueprints


def create_app(config_override: dict = None) -> Flask:
    """创建 Flask 应用实例"""

    # 确保数据目录存在
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)

    app = Flask(
        __name__,
        template_folder=str(Path(__file__).parent / "templates"),
        static_folder=str(Path(__file__).parent / "static"),
    )

    # ──────── 配置 ────────
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
    }
    app.config["JSON_AS_ASCII"] = False

    if config_override:
        app.config.update(config_override)

    # ──────── 日志 ────────
    logging.basicConfig(
        level=logging.DEBUG if DEBUG else logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ──────── 初始化数据库 ────────
    init_db(app)

    # ──────── 注册蓝图 ────────
    register_blueprints(app)

    # ──────── 健康检查 ────────
    @app.route("/health")
    def health():
        return {"status": "ok", "service": "skills-monitor-server"}

    @app.route("/")
    def index():
        return {
            "service": "Skills Monitor Server",
        "version": "0.6.1",
        "endpoints": {
            "agent_api": "/api/agent/",
            "benchmark_dashboard": "/benchmark",
            "benchmark_api": "/api/benchmark/",
            "wechat_callback": "/api/wechat/callback",
            "miniprogram_api": "/api/mp/",
            "h5_pages": "/h5/",
            "pwa": "/pwa/",
            "health": "/health",
            "alerts": "/api/mp/push-analytics",
        },
        }

    # ──────── 定时任务 ────────
    _setup_scheduler(app)

    app.logger.info(f"Skills Monitor Server 已启动 (DEBUG={DEBUG})")
    return app


def _setup_scheduler(app: Flask):
    """设置定时推送调度器"""
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from server.services.push_scheduler import push_daily_reports

        scheduler = BackgroundScheduler()

        # 每小时检查一次是否有用户需要推送
        # v0.6.0: 使用增强版推送（含告警检查）
        try:
            from server.services.operation_tracker import enhanced_push_daily_reports
            push_func = lambda: enhanced_push_daily_reports(app)
        except ImportError:
            push_func = lambda: push_daily_reports(app)

        scheduler.add_job(
            func=push_func,
            trigger="cron",
            minute=DAILY_REPORT_CRON_MINUTE,
            id="daily_push",
            name="每日报告推送+告警",
            replace_existing=True,
        )

        scheduler.start()
        app.logger.info(
            f"推送调度器已启动 (每小时 :{DAILY_REPORT_CRON_MINUTE:02d} 检查)"
        )

    except ImportError:
        app.logger.warning(
            "APScheduler 未安装，定时推送功能不可用。"
            "请运行: pip install apscheduler"
        )


# ──────── 直接运行 ────────

if __name__ == "__main__":
    app = create_app()
    app.run(
        host=SERVER_HOST,
        port=SERVER_PORT,
        debug=DEBUG,
    )
