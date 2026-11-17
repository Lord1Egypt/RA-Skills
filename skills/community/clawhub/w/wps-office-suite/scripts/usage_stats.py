"""
使用统计与稳定性中心 v5.0.0
功能：在四引擎入口埋点（文档数、耗时、引擎命中、失败降级次数、重试成功率）写 SQLite
      stats 子命令输出日/周报表与引擎健康度提示
      合并原先分散的三个脚本级 engine-info 命令为全局 wps engine-info
      新增引擎偏好优先级配置（用户可固定某引擎或恢复自动）

v5.0.0 变更：
  - 🎯 初始版本

死规则合规：
  - 规则9：纯本地实现，不依赖任何外部 API
  - 规则10：SQLite 本地存储，无额外进程
  - 规则13：不生成任何禁止文件类型
  - 规则14：三次自审
  - 规则15：沙箱模拟运行
  - 规则16：子进程超时自动关闭

安全合规：
  - 不联网、不调用外部服务
  - 不读取用户隐私数据或凭证
  - 所有数据本地 SQLite 存储
"""

import os
import sys
import json
import sqlite3
import platform
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

sys.path.insert(0, str(Path(__file__).parent))

try:
    from wps_common import safe_path
except ImportError:
    def safe_path(p):
        return Path(p).resolve()


IS_WINDOWS = platform.system() == "Windows"

# SQLite 数据库路径
DB_PATH = Path(__file__).parent / "wps_stats.db"

# 引擎偏好配置文件
ENGINE_PREF_FILE = Path(__file__).parent / "engine_preference.json"

# 引擎列表
ALL_ENGINES = ["wps", "ms_office", "libreoffice", "pure_python"]

# 引擎显示名
ENGINE_LABELS = {
    "wps": "WPS Office",
    "ms_office": "Microsoft Office",
    "libreoffice": "LibreOffice",
    "pure_python": "纯 Python"
}


class StatsDB:
    """SQLite 统计数据库"""

    VERSION = "v5.0.0"
    SCHEMA_VERSION = 1

    def __init__(self, db_path: str = ""):
        self.db_path = Path(db_path) if db_path else DB_PATH
        self._init_db()

    def _init_db(self):
        """初始化数据库表"""
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usage_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    script TEXT NOT NULL,
                    action TEXT NOT NULL,
                    engine TEXT DEFAULT '',
                    duration_ms INTEGER DEFAULT 0,
                    success INTEGER DEFAULT 1,
                    error_type TEXT DEFAULT '',
                    retry_count INTEGER DEFAULT 0,
                    file_type TEXT DEFAULT '',
                    file_size INTEGER DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS engine_health (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    engine TEXT NOT NULL,
                    available INTEGER DEFAULT 1,
                    response_time_ms INTEGER DEFAULT 0,
                    error_message TEXT DEFAULT ''
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS daily_summary (
                    date TEXT PRIMARY KEY,
                    total_operations INTEGER DEFAULT 0,
                    total_duration_ms INTEGER DEFAULT 0,
                    success_count INTEGER DEFAULT 0,
                    fail_count INTEGER DEFAULT 0,
                    retry_count INTEGER DEFAULT 0,
                    most_used_engine TEXT DEFAULT '',
                    most_used_action TEXT DEFAULT ''
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS meta (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            conn.execute(
                "INSERT OR IGNORE INTO meta (key, value) VALUES (?, ?)",
                ("schema_version", str(self.SCHEMA_VERSION))
            )
            conn.commit()

    def log_usage(self, script: str, action: str, engine: str = "",
                  duration_ms: int = 0, success: bool = True,
                  error_type: str = "", retry_count: int = 0,
                  file_type: str = "", file_size: int = 0):
        """记录使用日志"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.execute("""
                    INSERT INTO usage_log 
                    (timestamp, script, action, engine, duration_ms, success, 
                     error_type, retry_count, file_type, file_size)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    datetime.now().isoformat(),
                    script, action, engine, duration_ms,
                    1 if success else 0,
                    error_type, retry_count, file_type, file_size
                ))
                conn.commit()
        except Exception:
            pass

    def log_engine_health(self, engine: str, available: bool,
                          response_time_ms: int = 0, error_message: str = ""):
        """记录引擎健康状态"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.execute("""
                    INSERT INTO engine_health 
                    (timestamp, engine, available, response_time_ms, error_message)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    datetime.now().isoformat(),
                    engine, 1 if available else 0,
                    response_time_ms, error_message
                ))
                conn.commit()
        except Exception:
            pass

    def get_daily_stats(self, date: str = "") -> Dict[str, Any]:
        """获取指定日期统计（默认今天）"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success,
                        SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failed,
                        SUM(duration_ms) as total_duration,
                        SUM(retry_count) as total_retries,
                        AVG(duration_ms) as avg_duration
                    FROM usage_log
                    WHERE DATE(timestamp) = ?
                """, (date,))
                row = cursor.fetchone()

                # 引擎使用分布
                cursor = conn.execute("""
                    SELECT engine, COUNT(*) as count
                    FROM usage_log
                    WHERE DATE(timestamp) = ? AND engine != ''
                    GROUP BY engine
                    ORDER BY count DESC
                """, (date,))
                engine_dist = {r["engine"]: r["count"] for r in cursor.fetchall()}

                # 动作使用分布
                cursor = conn.execute("""
                    SELECT action, COUNT(*) as count
                    FROM usage_log
                    WHERE DATE(timestamp) = ?
                    GROUP BY action
                    ORDER BY count DESC
                    LIMIT 10
                """, (date,))
                action_dist = {r["action"]: r["count"] for r in cursor.fetchall()}

                # 错误分布
                cursor = conn.execute("""
                    SELECT error_type, COUNT(*) as count
                    FROM usage_log
                    WHERE DATE(timestamp) = ? AND success = 0 AND error_type != ''
                    GROUP BY error_type
                    ORDER BY count DESC
                    LIMIT 5
                """, (date,))
                error_dist = {r["error_type"]: r["count"] for r in cursor.fetchall()}

                return {
                    "ok": True,
                    "date": date,
                    "total_operations": row["total"] or 0,
                    "success_count": row["success"] or 0,
                    "fail_count": row["failed"] or 0,
                    "total_duration_ms": row["total_duration"] or 0,
                    "avg_duration_ms": round(row["avg_duration"] or 0, 1),
                    "total_retries": row["total_retries"] or 0,
                    "engine_distribution": engine_dist,
                    "action_distribution": action_dist,
                    "error_distribution": error_dist,
                    "success_rate": round(
                        (row["success"] or 0) / max(row["total"] or 1, 1) * 100, 1
                    )
                }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_weekly_stats(self, weeks: int = 1) -> Dict[str, Any]:
        """获取最近 N 周统计"""
        try:
            since = (datetime.now() - timedelta(weeks=weeks)).strftime("%Y-%m-%d")
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT 
                        DATE(timestamp) as day,
                        COUNT(*) as total,
                        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success,
                        SUM(duration_ms) as duration
                    FROM usage_log
                    WHERE DATE(timestamp) >= ?
                    GROUP BY DATE(timestamp)
                    ORDER BY day
                """, (since,))
                daily = []
                for row in cursor.fetchall():
                    daily.append({
                        "date": row["day"],
                        "total": row["total"],
                        "success": row["success"],
                        "duration_ms": row["duration"]
                    })

                return {
                    "ok": True,
                    "period": f"最近 {weeks} 周",
                    "daily": daily,
                    "total_operations": sum(d["total"] for d in daily),
                    "total_success": sum(d["success"] for d in daily)
                }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_engine_health_report(self) -> Dict[str, Any]:
        """获取引擎健康度报告"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.row_factory = sqlite3.Row

                health = {}
                for engine in ALL_ENGINES:
                    # 最近 24 小时健康检查
                    since = (datetime.now() - timedelta(hours=24)).isoformat()
                    cursor = conn.execute("""
                        SELECT 
                            COUNT(*) as total,
                            SUM(CASE WHEN available = 1 THEN 1 ELSE 0 END) as available_count,
                            AVG(response_time_ms) as avg_response
                        FROM engine_health
                        WHERE engine = ? AND timestamp >= ?
                    """, (engine, since))
                    row = cursor.fetchone()

                    total = row["total"] or 0
                    available = row["available_count"] or 0
                    avg_response = row["avg_response"] or 0

                    health[engine] = {
                        "label": ENGINE_LABELS.get(engine, engine),
                        "total_checks": total,
                        "available_count": available,
                        "availability_rate": round(available / max(total, 1) * 100, 1),
                        "avg_response_ms": round(avg_response, 1),
                        "status": "healthy" if available == total and total > 0 else
                                  "degraded" if available > 0 else "unavailable"
                    }

                return {
                    "ok": True,
                    "period": "最近 24 小时",
                    "engines": health,
                    "overall_health": "healthy" if all(
                        e["status"] == "healthy" for e in health.values()
                    ) else "degraded"
                }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_stats_summary(self) -> Dict[str, Any]:
        """获取统计摘要"""
        today = self.get_daily_stats()
        weekly = self.get_weekly_stats()
        health = self.get_engine_health_report()

        return {
            "ok": True,
            "today": today,
            "weekly": weekly,
            "engine_health": health,
            "version": self.VERSION
        }


class EnginePreference:
    """引擎偏好配置管理"""

    def __init__(self):
        self.pref_file = ENGINE_PREF_FILE
        self.config = self._load_pref()

    def _load_pref(self) -> Dict[str, Any]:
        """加载偏好配置"""
        if self.pref_file.exists():
            try:
                return json.loads(self.pref_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"mode": "auto", "priority": ALL_ENGINES.copy(), "fixed_engine": ""}

    def _save_pref(self):
        """保存偏好配置"""
        try:
            self.pref_file.write_text(
                json.dumps(self.config, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception:
            pass

    def get_mode(self) -> str:
        """获取当前模式：auto/fixed"""
        return self.config.get("mode", "auto")

    def get_fixed_engine(self) -> str:
        """获取固定引擎"""
        return self.config.get("fixed_engine", "")

    def get_priority(self) -> List[str]:
        """获取引擎优先级"""
        return self.config.get("priority", ALL_ENGINES.copy())

    def set_fixed(self, engine: str) -> Dict[str, Any]:
        """设置固定引擎"""
        if engine not in ALL_ENGINES:
            return {"ok": False, "error": f"未知引擎: {engine}，可选: {ALL_ENGINES}"}

        self.config["mode"] = "fixed"
        self.config["fixed_engine"] = engine
        self._save_pref()
        return {"ok": True, "message": f"已固定引擎: {ENGINE_LABELS.get(engine, engine)}"}

    def set_auto(self) -> Dict[str, Any]:
        """恢复自动检测"""
        self.config["mode"] = "auto"
        self.config["fixed_engine"] = ""
        self._save_pref()
        return {"ok": True, "message": "已恢复自动检测模式"}

    def set_priority(self, priority: List[str]) -> Dict[str, Any]:
        """设置引擎优先级"""
        # 验证
        for e in priority:
            if e not in ALL_ENGINES:
                return {"ok": False, "error": f"未知引擎: {e}"}

        self.config["priority"] = priority
        self._save_pref()
        return {"ok": True, "message": f"优先级已设置: {priority}"}

    def get_info(self) -> Dict[str, Any]:
        """获取引擎偏好信息"""
        return {
            "ok": True,
            "mode": self.get_mode(),
            "fixed_engine": self.get_fixed_engine(),
            "priority": self.get_priority(),
            "available_engines": {e: ENGINE_LABELS[e] for e in ALL_ENGINES}
        }


class EngineInfo:
    """全局引擎信息（合并原分散的 engine-info 命令）"""

    def __init__(self):
        self.pref = EnginePreference()

    def get_engine_info(self) -> Dict[str, Any]:
        """获取全局引擎信息"""
        info = {
            "ok": True,
            "system": platform.system(),
            "preference": self.pref.get_info(),
            "engines": {}
        }

        for engine in ALL_ENGINES:
            info["engines"][engine] = {
                "label": ENGINE_LABELS.get(engine, engine),
                "available": self._check_engine_available(engine),
                "status": "available" if self._check_engine_available(engine) else "unavailable"
            }

        # 当前推荐引擎
        if self.pref.get_mode() == "fixed":
            info["recommended_engine"] = self.pref.get_fixed_engine()
            info["selection_method"] = "fixed"
        else:
            info["recommended_engine"] = self._auto_select_engine()
            info["selection_method"] = "auto"

        return info

    def _check_engine_available(self, engine: str) -> bool:
        """检查引擎是否可用"""
        try:
            if engine == "wps":
                if IS_WINDOWS:
                    import win32com.client
                    wps = win32com.client.Dispatch("Kwps.Application")
                    return True
                return False
            elif engine == "ms_office":
                if IS_WINDOWS:
                    import win32com.client
                    word = win32com.client.Dispatch("Word.Application")
                    return True
                return False
            elif engine == "libreoffice":
                proc = subprocess.Popen(
                    ["soffice", "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                try:
                    proc.communicate(timeout=5)
                    return proc.returncode == 0
                except subprocess.TimeoutExpired:
                    proc.kill()
                    return False
            elif engine == "pure_python":
                return True  # 始终可用
        except Exception:
            return False
        return False

    def _auto_select_engine(self) -> str:
        """自动选择最佳引擎"""
        priority = self.pref.get_priority()
        for engine in priority:
            if self._check_engine_available(engine):
                return engine
        return "pure_python"  # 最终兜底


def main():
    """CLI 入口"""
    parser = argparse.ArgumentParser(
        description=f"使用统计与稳定性中心 {StatsDB.VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # stats 子命令
    p_stats = sub.add_parser("stats", help="查看使用统计")
    p_stats.add_argument("--period", default="today",
                         choices=["today", "week", "month"],
                         help="统计周期")
    p_stats.add_argument("--date", default="", help="指定日期 YYYY-MM-DD")

    # health 子命令
    sub.add_parser("health", help="查看引擎健康度")

    # engine-info 子命令（全局）
    sub.add_parser("engine-info", help="查看全局引擎信息")

    # preference 子命令
    p_pref = sub.add_parser("preference", help="引擎偏好配置")
    p_pref.add_argument("--mode", default="", choices=["auto", "fixed"],
                        help="模式：auto/fixed")
    p_pref.add_argument("--engine", default="", help="固定引擎名称")
    p_pref.add_argument("--priority", default="", help="优先级排序（逗号分隔）")

    # log 子命令（手动埋点，供其他脚本调用）
    p_log = sub.add_parser("log", help="记录使用日志")
    p_log.add_argument("--script", required=True, help="脚本名称")
    p_log.add_argument("--action", required=True, help="动作名称")
    p_log.add_argument("--engine", default="", help="使用的引擎")
    p_log.add_argument("--duration", type=int, default=0, help="耗时毫秒")
    p_log.add_argument("--success", type=int, default=1, help="是否成功 0/1")
    p_log.add_argument("--error", default="", help="错误类型")
    p_log.add_argument("--retries", type=int, default=0, help="重试次数")

    # reset 子命令
    p_reset = sub.add_parser("reset", help="重置统计数据")
    p_reset.add_argument("--days", type=int, default=30, help="保留最近N天")

    args = parser.parse_args()
    db = StatsDB()
    engine_info = EngineInfo()

    if args.command == "stats":
        if args.period == "today":
            result = db.get_daily_stats(args.date)
        elif args.period == "week":
            result = db.get_weekly_stats()
        elif args.period == "month":
            result = db.get_weekly_stats(weeks=4)
        else:
            result = db.get_daily_stats()
        print(json.dumps(result, ensure_ascii=False, default=str))

    elif args.command == "health":
        result = db.get_engine_health_report()
        print(json.dumps(result, ensure_ascii=False, default=str))

    elif args.command == "engine-info":
        result = engine_info.get_engine_info()
        print(json.dumps(result, ensure_ascii=False, default=str))

    elif args.command == "preference":
        pref = EnginePreference()
        if args.mode == "fixed" and args.engine:
            result = pref.set_fixed(args.engine)
        elif args.mode == "auto":
            result = pref.set_auto()
        elif args.priority:
            priority_list = [e.strip() for e in args.priority.split(",") if e.strip()]
            result = pref.set_priority(priority_list)
        else:
            result = pref.get_info()
        print(json.dumps(result, ensure_ascii=False))

    elif args.command == "log":
        db.log_usage(
            script=args.script,
            action=args.action,
            engine=args.engine,
            duration_ms=args.duration,
            success=bool(args.success),
            error_type=args.error,
            retry_count=args.retries
        )
        print(json.dumps({"ok": True, "message": "日志已记录"}))

    elif args.command == "reset":
        try:
            cutoff = (datetime.now() - timedelta(days=args.days)).isoformat()
            with sqlite3.connect(str(DB_PATH)) as conn:
                conn.execute("DELETE FROM usage_log WHERE timestamp < ?", (cutoff,))
                conn.execute("DELETE FROM engine_health WHERE timestamp < ?", (cutoff,))
                conn.commit()
            print(json.dumps({"ok": True, "message": f"已清理 {args.days} 天前的数据"}))
        except Exception as e:
            print(json.dumps({"ok": False, "error": str(e)}))

    else:
        print(json.dumps({"ok": False, "error": "未知命令"}))


if __name__ == "__main__":
    main()
