"""
定时任务管理 CLI v0.5.0 — 首次启动交互式确认 + 定时任务管理
==========================================================
提供 CLI 子命令用于:
  - skills-monitor schedule install  — 安装定时上报
  - skills-monitor schedule remove   — 卸载定时上报
  - skills-monitor schedule status   — 查看定时任务状态
  - skills-monitor consent           — 管理数据收集同意

首次运行诊断报告后，交互式询问用户是否开启每日定时上报。

使用方式:
  from skills_monitor.core.scheduler import ScheduleManager
  mgr = ScheduleManager()
  mgr.interactive_first_run()
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# 首次运行标记
FIRST_RUN_FLAG = os.path.expanduser("~/.skills_monitor/.first_run_completed")
CONSENT_FLAG = os.path.expanduser("~/.skills_monitor/.consent_shown")


class ScheduleManager:
    """定时任务管理器 — 首次启动交互式确认"""

    def __init__(self, server_url: str = "http://localhost:5100"):
        self.server_url = server_url

    # ──────── 首次运行交互式确认 ────────

    def interactive_first_run(self, force: bool = False) -> Dict[str, Any]:
        """
        首次运行后的交互式确认流程

        流程:
          1. 显示数据收集声明
          2. 询问是否同意数据收集
          3. 询问是否开启每日定时上报
          4. 设置上报时间

        Args:
            force: 强制重新走首次确认流程

        Returns:
            {"consent": bool, "schedule_installed": bool, ...}
        """
        result = {
            "consent": False,
            "schedule_installed": False,
            "skipped": False,
        }

        # 检查是否已完成首次运行
        if not force and os.path.exists(FIRST_RUN_FLAG):
            result["skipped"] = True
            result["message"] = "首次运行确认已完成"
            return result

        # 检查是否在交互式终端
        if not sys.stdin.isatty():
            result["skipped"] = True
            result["message"] = "非交互式终端，跳过确认（可通过 skills-monitor schedule install 手动安装）"
            return result

        print()
        print("=" * 60)
        print("  🏥 Skills Monitor v0.5.0 — 首次运行配置")
        print("=" * 60)
        print()

        # Step 1: 数据收集声明
        consent = self._ask_consent()
        result["consent"] = consent

        if not consent:
            print("\n❌ 您拒绝了数据收集。您仍可使用本地诊断功能。")
            print("   如需更改，运行: skills-monitor consent --agree")
            self._mark_first_run()
            return result

        # Step 2: 询问定时上报
        schedule = self._ask_schedule()
        result["schedule_installed"] = schedule

        # 标记首次运行完成
        self._mark_first_run()

        print()
        print("✅ 配置完成！")
        if schedule:
            print("   每日诊断报告将自动生成并上报。")
        print("   随时可通过 `skills-monitor schedule status` 查看状态。")
        print()

        return result

    def _ask_consent(self) -> bool:
        """显示数据收集声明并获取用户同意"""
        print("📋 数据收集声明")
        print("-" * 40)
        print("Skills Monitor 会收集以下匿名数据用于改进服务:")
        print()
        print("  ✅ 收集内容:")
        print("     • Skill 运行成功率、响应时间等聚合指标")
        print("     • Skill 使用频率统计")
        print("     • 系统健康度评分")
        print()
        print("  ❌ 绝不收集:")
        print("     • 您的代码或文件内容")
        print("     • 个人身份信息（姓名、邮箱等）")
        print("     • API Key 或密码")
        print("     • Skill 的输入/输出数据")
        print()
        print("  🔒 安全保障:")
        print("     • 所有数据上报前自动脱敏")
        print("     • 支持数据导出和删除（GDPR 合规）")
        print("     • 可随时撤销同意")
        print()

        while True:
            answer = input("是否同意数据收集？(y/n): ").strip().lower()
            if answer in ("y", "yes", "是"):
                # 记录同意
                try:
                    from skills_monitor.core.identity import IdentityManager
                    mgr = IdentityManager()
                    mgr.record_consent(True)
                except Exception:
                    pass
                return True
            elif answer in ("n", "no", "否"):
                try:
                    from skills_monitor.core.identity import IdentityManager
                    mgr = IdentityManager()
                    mgr.record_consent(False)
                except Exception:
                    pass
                return False
            else:
                print("请输入 y 或 n")

    def _ask_schedule(self) -> bool:
        """询问是否开启定时上报"""
        print()
        print("⏰ 每日定时上报")
        print("-" * 40)
        print("Skills Monitor 可以每天自动:")
        print("  1. 生成诊断报告")
        print("  2. 上报数据到中心服务器")
        print("  3. 记录系统健康度趋势")
        print()

        while True:
            answer = input("是否开启每日定时上报？(y/n) [默认: y]: ").strip().lower()
            if answer in ("", "y", "yes", "是"):
                break
            elif answer in ("n", "no", "否"):
                print("跳过定时上报安装。您可以随时通过 `skills-monitor schedule install` 开启。")
                return False
            else:
                print("请输入 y 或 n")

        # 询问时间
        hour = 12
        minute = 0
        time_input = input(f"上报时间 (HH:MM) [默认: 12:00]: ").strip()
        if time_input:
            try:
                parts = time_input.split(":")
                hour = int(parts[0])
                minute = int(parts[1]) if len(parts) > 1 else 0
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    print(f"时间无效，使用默认 12:00")
                    hour, minute = 12, 0
            except (ValueError, IndexError):
                print(f"格式无效，使用默认 12:00")
                hour, minute = 12, 0

        # 安装
        from skills_monitor.core.auto_reporter import AutoReporter
        reporter = AutoReporter(server_url=self.server_url, hour=hour, minute=minute)
        result = reporter.install_schedule(hour=hour, minute=minute)

        if result.get("ok"):
            print(f"\n✅ 定时上报已安装: {result.get('schedule')}")
        else:
            print(f"\n⚠️ 安装定时上报失败: {result.get('error')}")
            if result.get("crontab_hint"):
                print(f"\n手动安装 crontab:\n{result['crontab_hint']}")

        return result.get("ok", False)

    def _mark_first_run(self):
        """标记首次运行已完成"""
        try:
            Path(os.path.dirname(FIRST_RUN_FLAG)).mkdir(parents=True, exist_ok=True)
            Path(FIRST_RUN_FLAG).write_text(
                json.dumps({"completed_at": __import__("datetime").datetime.now().isoformat()}),
                encoding="utf-8",
            )
        except Exception:
            pass

    # ──────── CLI 子命令 ────────

    def cmd_install(self, hour: int = 12, minute: int = 0, weekdays_only: bool = False) -> Dict[str, Any]:
        """CLI: skills-monitor schedule install"""
        from skills_monitor.core.auto_reporter import AutoReporter
        reporter = AutoReporter(server_url=self.server_url, hour=hour, minute=minute)
        return reporter.install_schedule(hour=hour, minute=minute, weekdays_only=weekdays_only)

    def cmd_remove(self) -> Dict[str, Any]:
        """CLI: skills-monitor schedule remove"""
        from skills_monitor.core.auto_reporter import AutoReporter
        reporter = AutoReporter(server_url=self.server_url)
        return reporter.uninstall_schedule()

    def cmd_status(self) -> Dict[str, Any]:
        """CLI: skills-monitor schedule status"""
        from skills_monitor.core.auto_reporter import AutoReporter
        reporter = AutoReporter(server_url=self.server_url)
        return reporter.get_schedule_status()

    def cmd_consent(self, agree: bool = None) -> Dict[str, Any]:
        """CLI: skills-monitor consent"""
        from skills_monitor.core.identity import IdentityManager
        mgr = IdentityManager()

        if agree is None:
            # 查询状态
            return {
                "has_consent": mgr.has_consent(),
                "consent_info": mgr._config.get("consent", {}),
            }

        mgr.record_consent(agree)
        return {
            "ok": True,
            "consent": agree,
            "message": f"数据收集已{'同意' if agree else '拒绝'}",
        }

    def cmd_run_now(self) -> Dict[str, Any]:
        """CLI: skills-monitor schedule run — 立即执行一次上报"""
        from skills_monitor.core.auto_reporter import AutoReporter
        reporter = AutoReporter(server_url=self.server_url)
        return reporter.run_daily(trigger="manual")

    # ──────── 重置首次运行 ────────

    @staticmethod
    def reset_first_run():
        """重置首次运行标记（用于测试）"""
        for f in (FIRST_RUN_FLAG, CONSENT_FLAG):
            try:
                os.remove(f)
            except FileNotFoundError:
                pass
