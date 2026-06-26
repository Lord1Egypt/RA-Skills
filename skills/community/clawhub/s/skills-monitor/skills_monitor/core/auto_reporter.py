"""
后台自动上报模块 v0.5.0 — 每日定时诊断 + 增量上报
=================================================
功能:
  - 自动生成诊断报告 + 上报中心服务器
  - macOS LaunchAgent 安装/卸载/状态管理
  - 首次运行交互式确认
  - 日志记录与错误恢复

使用方式:
  from skills_monitor.core.auto_reporter import AutoReporter
  reporter = AutoReporter()
  reporter.run_daily()            # 手动触发一次
  reporter.install_schedule()     # 安装 LaunchAgent
"""

import json
import logging
import os
import platform
import subprocess
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

# LaunchAgent 配置
PLIST_LABEL = "com.codebuddy.auto-upload"
PLIST_FILENAME = f"{PLIST_LABEL}.plist"
DEFAULT_HOUR = 12       # 默认每天中午 12 点
DEFAULT_MINUTE = 0
DEFAULT_SERVER_URL = "http://localhost:5100"

# 日志目录
LOG_DIR = os.path.expanduser("~/.skills_monitor/logs")
STATE_FILE = os.path.expanduser("~/.skills_monitor/auto_report_state.json")


class AutoReporter:
    """
    后台自动上报器

    职责:
      1. 调用 DiagnosticReporter 生成报告
      2. 调用 DataUploader 上报到中心服务器
      3. 管理 macOS LaunchAgent (定时任务)
      4. 记录上报状态（成功/失败/重试）
    """

    def __init__(
        self,
        server_url: str = DEFAULT_SERVER_URL,
        hour: int = DEFAULT_HOUR,
        minute: int = DEFAULT_MINUTE,
        skills_dir: str = "skills",
    ):
        self.server_url = server_url
        self.hour = hour
        self.minute = minute
        self.skills_dir = skills_dir
        self._state = self._load_state()

        # 确保日志目录
        Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

    # ──────── 核心：执行一次上报 ────────

    def run_daily(self, trigger: str = "scheduled") -> Dict[str, Any]:
        """
        执行一次完整的诊断 + 上报流程

        流程:
          1. 检查 GDPR 同意状态
          2. 生成诊断报告
          3. 上报数据到中心服务器
          4. 记录本次上报结果

        Returns:
            {"ok": bool, "report_path": str, "upload_result": dict, ...}
        """
        result = {
            "ok": False,
            "timestamp": datetime.now().isoformat(),
            "trigger": trigger,
            "steps": {},
        }

        try:
            # Step 1: 检查 GDPR 同意
            from skills_monitor.core.identity import IdentityManager
            identity = IdentityManager()

            if not identity.is_initialized:
                result["error"] = "Agent 未初始化，请先运行 skills-monitor init"
                self._save_state(result)
                return result

            if not identity.has_consent():
                result["error"] = "用户未同意数据收集，请先运行 skills-monitor consent"
                self._save_state(result)
                return result

            result["steps"]["consent_check"] = "passed"

            # Step 2: 生成诊断报告
            from skills_monitor.data.store import DataStore
            from skills_monitor.adapters.skill_registry import SkillRegistry
            from skills_monitor.core.diagnostic import DiagnosticReporter

            store = DataStore()
            registry = SkillRegistry(skills_dir=self.skills_dir)
            reporter = DiagnosticReporter(
                store, registry, identity.agent_id,
                reports_dir="reports/diagnostic",
            )
            report_content, report_path = reporter.generate_and_save(trigger=trigger)
            result["steps"]["report"] = "generated"
            result["report_path"] = report_path

            # Step 3: 上报到中心服务器
            from skills_monitor.core.uploader import DataUploader
            uploader = DataUploader(server_url=self.server_url)
            uploader.init()

            # 先注册/心跳
            uploader.register()
            uploader.heartbeat()

            # 先兜底确保首次诊断已存在
            initial_ok, initial_result = uploader.ensure_initial_diagnostic_uploaded()
            result["steps"]["initial_diagnostic"] = "success" if initial_ok else "failed"
            result["initial_diagnostic_result"] = initial_result

            # 上报诊断数据
            ok, upload_result = uploader.upload_diagnostic({
                "collected_at": datetime.now().isoformat(),
                "report_markdown": report_content,
                "trigger": trigger,
                "report_date": date.today().isoformat(),
            })

            result["steps"]["upload"] = "success" if ok else "failed"
            result["upload_result"] = upload_result

            # 同时上报每日数据
            daily_ok, daily_result = uploader.upload_daily(date.today(), trigger=trigger)
            result["steps"]["daily_upload"] = "success" if daily_ok else "failed"
            result["daily_upload_result"] = daily_result
            result["ok"] = bool(initial_ok and ok and daily_ok)

            logger.info(f"自动上报{'成功' if result['ok'] else '失败'}: {result}")

        except Exception as e:
            result["error"] = f"{type(e).__name__}: {e}"
            logger.error(f"自动上报异常: {e}", exc_info=True)

        self._save_state(result)
        return result

    # ──────── macOS LaunchAgent 管理 ────────

    def install_schedule(
        self,
        hour: int = None,
        minute: int = None,
        weekdays_only: bool = False,
    ) -> Dict[str, Any]:
        """
        安装 macOS LaunchAgent 定时任务

        Args:
            hour: 执行小时 (0-23)
            minute: 执行分钟 (0-59)
            weekdays_only: 是否仅工作日

        Returns:
            {"ok": bool, "plist_path": str, "loaded": bool}
        """
        if platform.system() != "Darwin":
            return {
                "ok": False,
                "error": "LaunchAgent 仅支持 macOS，其他系统请使用 crontab",
                "crontab_hint": self._generate_crontab(hour, minute, weekdays_only),
            }

        h = hour or self.hour
        m = minute or self.minute

        plist_content = self._generate_plist(h, m, weekdays_only)
        plist_dir = Path.home() / "Library" / "LaunchAgents"
        plist_dir.mkdir(parents=True, exist_ok=True)
        plist_path = plist_dir / PLIST_FILENAME

        # 先卸载旧的
        self._unload_plist(str(plist_path))

        # 写入 plist
        plist_path.write_text(plist_content, encoding="utf-8")

        # 加载
        loaded = self._load_plist(str(plist_path))

        result = {
            "ok": True,
            "plist_path": str(plist_path),
            "loaded": loaded,
            "schedule": f"每天 {h:02d}:{m:02d}" + (" (仅工作日)" if weekdays_only else ""),
        }

        logger.info(f"LaunchAgent 已安装: {result}")
        return result

    def uninstall_schedule(self) -> Dict[str, Any]:
        """卸载 LaunchAgent 定时任务"""
        plist_path = Path.home() / "Library" / "LaunchAgents" / PLIST_FILENAME

        if not plist_path.exists():
            return {"ok": True, "message": "LaunchAgent 未安装"}

        self._unload_plist(str(plist_path))
        plist_path.unlink(missing_ok=True)

        return {"ok": True, "message": "LaunchAgent 已卸载", "removed": str(plist_path)}

    def get_schedule_status(self) -> Dict[str, Any]:
        """查询定时任务状态"""
        plist_path = Path.home() / "Library" / "LaunchAgents" / PLIST_FILENAME

        if platform.system() != "Darwin":
            return {"installed": False, "reason": "非 macOS 系统"}

        if not plist_path.exists():
            return {"installed": False, "plist_path": str(plist_path)}

        # 检查是否已加载
        try:
            cp = subprocess.run(
                ["launchctl", "list", PLIST_LABEL],
                capture_output=True, text=True, timeout=5,
            )
            loaded = cp.returncode == 0
        except Exception:
            loaded = False

        return {
            "installed": True,
            "loaded": loaded,
            "plist_path": str(plist_path),
            "last_run": self._state.get("timestamp"),
            "last_result": self._state.get("ok"),
        }

    # ──────── plist 生成 ────────

    def _generate_plist(self, hour: int, minute: int, weekdays_only: bool) -> str:
        """生成 macOS LaunchAgent plist XML"""
        python_path = sys.executable
        # 找到 auto_reporter 的入口脚本
        project_dir = str(Path(__file__).resolve().parent.parent.parent)
        script_path = os.path.join(project_dir, "_auto_report_entry.py")

        # 如果入口脚本不存在，自动创建
        self._ensure_entry_script(script_path, project_dir)

        if weekdays_only:
            # 周一到周五
            intervals = ""
            for wd in range(1, 6):  # 1=Monday .. 5=Friday
                intervals += f"""        <dict>
            <key>Weekday</key><integer>{wd}</integer>
            <key>Hour</key><integer>{hour}</integer>
            <key>Minute</key><integer>{minute}</integer>
        </dict>\n"""
            calendar_section = f"""    <key>StartCalendarInterval</key>
    <array>
{intervals}    </array>"""
        else:
            calendar_section = f"""    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key><integer>{hour}</integer>
        <key>Minute</key><integer>{minute}</integer>
    </dict>"""

        return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{PLIST_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>{script_path}</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{project_dir}</string>
{calendar_section}
    <key>StandardOutPath</key>
    <string>{LOG_DIR}/auto_upload_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>{LOG_DIR}/auto_upload_stderr.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:{os.path.dirname(python_path)}</string>
        <key>PYTHONPATH</key>
        <string>{project_dir}</string>
    </dict>
</dict>
</plist>
"""

    def _ensure_entry_script(self, script_path: str, project_dir: str):
        """确保入口脚本存在"""
        if os.path.exists(script_path):
            return

        content = f'''#!/usr/bin/env python3
"""
Skills Monitor 自动上报入口脚本 (由 auto_reporter.py 自动生成)
每日由 LaunchAgent 触发
"""
import sys
import os
sys.path.insert(0, "{project_dir}")
os.chdir("{project_dir}")

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(os.path.expanduser("~/.skills_monitor/logs/auto_upload.log")),
        logging.StreamHandler(),
    ],
)

from skills_monitor.core.auto_reporter import AutoReporter

if __name__ == "__main__":
    reporter = AutoReporter()
    result = reporter.run_daily(trigger="launchagent")
    status = "✅ 成功" if result.get("ok") else f"❌ 失败: {{result.get(\'error\', \'未知错误\')}}"
    logging.info(f"自动上报结果: {{status}}")
'''
        Path(script_path).write_text(content, encoding="utf-8")
        os.chmod(script_path, 0o755)

    def _generate_crontab(self, hour: int = None, minute: int = None, weekdays_only: bool = False) -> str:
        """为非 macOS 系统生成 crontab 提示"""
        h = hour or self.hour
        m = minute or self.minute
        day_part = "1-5" if weekdays_only else "*"
        project_dir = str(Path(__file__).resolve().parent.parent.parent)
        return (
            f"# Skills Monitor 自动上报 (crontab)\n"
            f"{m} {h} * * {day_part} cd {project_dir} && "
            f"{sys.executable} -c 'from skills_monitor.core.auto_reporter import AutoReporter; "
            f"AutoReporter().run_daily(trigger=\"crontab\")'"
        )

    # ──────── launchctl 操作 ────────

    def _load_plist(self, plist_path: str) -> bool:
        """加载 plist 到 launchd"""
        try:
            cp = subprocess.run(
                ["launchctl", "load", plist_path],
                capture_output=True, text=True, timeout=10,
            )
            return cp.returncode == 0
        except Exception as e:
            logger.warning(f"launchctl load 失败: {e}")
            return False

    def _unload_plist(self, plist_path: str) -> bool:
        """从 launchd 卸载 plist"""
        try:
            cp = subprocess.run(
                ["launchctl", "unload", plist_path],
                capture_output=True, text=True, timeout=10,
            )
            return cp.returncode == 0
        except Exception:
            return False

    # ──────── 状态持久化 ────────

    def _load_state(self) -> Dict[str, Any]:
        """加载上次上报状态"""
        try:
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def _save_state(self, result: Dict[str, Any]):
        """保存上报状态"""
        try:
            Path(os.path.dirname(STATE_FILE)).mkdir(parents=True, exist_ok=True)
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"保存上报状态失败: {e}")
        self._state = result

    # ──────── 重试逻辑 ────────

    def retry_last_failed(self) -> Dict[str, Any]:
        """重试上次失败的上报"""
        if self._state.get("ok", True):
            return {"ok": True, "message": "上次上报已成功，无需重试"}
        return self.run_daily(trigger="retry")
