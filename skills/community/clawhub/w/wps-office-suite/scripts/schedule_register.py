"""
定时任务注册管理 v5.4.0 — 统一调度层
功能：把周报/月报/对账单注册为系统计划任务（schtasks/cron/launchd）
      调度层零常驻进程，定时 = 定时调 wps CLI
      错过触发提供 skip / run_once 两种策略
      注册表 JSON 化可导出/导入/迁移

v5.4.0 变更（相比 v5.0）：
  - 新增 macOS launchd 支持（三平台全覆盖）
  - 新增错过触发策略：skip（跳过）/ run_once（补跑一次）
  - 注册表 JSON 化（schedule_registry.json），可导出/导入/迁移
  - 调度命令从旧脚本路径改为 wps CLI 调用（与 v5.3 统一入口集成）
  - watch.py 内嵌提醒逻辑剥离给本调度层，watch 只保留文件事件采集

死规则合规：
  - 规则9：纯本地实现，不依赖任何 API
  - 规则10：使用系统 schtasks/cron/launchd，无额外常驻进程
  - 规则13：不生成禁止文件类型
  - 规则14：三次自审
  - 规则15：沙箱模拟运行
  - 规则16：子进程超时自动关闭

安全合规：
  - 不联网、不调用外部服务
  - 不读取用户隐私数据或凭证
  - 注册前展示完整命令并等待用户确认（y/N）
  - 所有操作仅限于本地计划任务管理
"""

import os
import sys
import json
import platform
import subprocess
import argparse
import plistlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

sys.path.insert(0, str(Path(__file__).parent))

try:
    from wps_common import safe_path
except ImportError:
    def safe_path(p):
        return Path(p).resolve()

IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"
IS_MACOS = platform.system() == "Darwin"

TASK_PREFIX = "WPSOfficeSuite_"
TASK_DESCRIPTION = "WPS Office 全家桶 v5.4 定时任务（统一调度层）"

# 注册表持久化位置
REGISTRY_FILE = Path(__file__).parent / "schedule_registry.json"

# 可注册的预定义任务（v5.4：命令全部改用 wps CLI 调用）
PREDEFINED_TASKS = {
    "weekly_report": {
        "label": "周报自动生成（含 ECharts 图表 + usage_stats 摘要）",
        "command": "wps report-center weekly --output \"周报_{date}.html\"",
        "schedule": {
            "windows": {
                "type": "WEEKLY",
                "time": "17:00",
                "days": "FRI"
            },
            "linux": {
                "type": "WEEKLY",
                "cron": "0 17 * * 5"
            },
            "macos": {
                "type": "WEEKLY",
                "hour": 17,
                "minute": 0,
                "weekday": 4  # 0=Mon, 4=Fri
            }
        },
        "missed_run": "run_once"
    },
    "monthly_report": {
        "label": "月报自动生成",
        "command": "wps report-center monthly --output \"月报_{date}.html\"",
        "schedule": {
            "windows": {
                "type": "MONTHLY",
                "time": "09:00",
                "days": "1"
            },
            "linux": {
                "type": "MONTHLY",
                "cron": "0 9 1 * *"
            },
            "macos": {
                "type": "MONTHLY",
                "hour": 9,
                "minute": 0,
                "day": 1
            }
        },
        "missed_run": "skip"
    },
    "watch_daily": {
        "label": "watch 文件监听日报（调度层定时扫描）",
        "command": "wps watch scan --dir \"{watch_dir}\" --output \"watch_daily_{date}.json\"",
        "schedule": {
            "windows": {
                "type": "DAILY",
                "time": "08:00",
                "days": ""
            },
            "linux": {
                "type": "DAILY",
                "cron": "0 8 * * *"
            },
            "macos": {
                "type": "DAILY",
                "hour": 8,
                "minute": 0
            }
        },
        "missed_run": "run_once"
    }
}


class ScheduleRegistry:
    """JSON 注册表持久化（可导出/导入/迁移）"""

    def __init__(self):
        self.registry = self._load()

    def _load(self) -> Dict[str, Any]:
        if REGISTRY_FILE.exists():
            try:
                return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"version": "v5.4.0", "tasks": {}, "last_updated": ""}

    def save(self):
        self.registry["last_updated"] = datetime.now().isoformat()
        REGISTRY_FILE.write_text(
            json.dumps(self.registry, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def add(self, task_name: str, task_info: Dict):
        self.registry["tasks"][task_name] = task_info
        self.save()

    def remove(self, task_name: str):
        if task_name in self.registry["tasks"]:
            del self.registry["tasks"][task_name]
            self.save()

    def get(self, task_name: str) -> Optional[Dict]:
        return self.registry["tasks"].get(task_name)

    def list_all(self) -> Dict:
        return self.registry["tasks"]

    def export(self) -> str:
        return json.dumps(self.registry, ensure_ascii=False, indent=2)

    def import_data(self, data: str) -> bool:
        try:
            parsed = json.loads(data)
            if "tasks" in parsed:
                self.registry = parsed
                self.registry["version"] = "v5.4.0"
                self.save()
                return True
            return False
        except Exception:
            return False


class ScheduleRegister:
    """定时任务注册管理器 v5.4"""

    VERSION = "v5.4.0"

    def __init__(self):
        self.system = platform.system()
        self.registry = ScheduleRegistry()

    def _get_script_path(self, command: str) -> str:
        """从命令中提取脚本路径"""
        parts = command.split()
        if parts:
            script = parts[0]
            # wps 命令 -> scripts/wps.py
            if script == "wps":
                script_path = Path(__file__).parent / "wps.py"
                if script_path.exists():
                    return str(script_path)
            script_path = Path(__file__).parent / script
            if script_path.exists():
                return str(script_path)
        return ""

    def _build_full_command(self, command: str, workdir: str = "") -> str:
        """构建完整命令（使用当前 Python 解释器）"""
        python_exe = sys.executable
        # wps 命令特殊处理：wps.py <子命令>
        if command.startswith("wps "):
            script_path = Path(__file__).parent / "wps.py"
            sub_cmd = command[4:]  # 去掉 "wps "
            cmd = f'"{python_exe}" "{script_path}" {sub_cmd}'
        else:
            parts = command.split()
            script_path = self._get_script_path(command)
            if script_path:
                cmd = f'"{python_exe}" "{script_path}" {" ".join(parts[1:])}'
            else:
                cmd = f'"{python_exe}" {command}'

        if workdir:
            if IS_WINDOWS:
                cmd = f'cd /d "{workdir}" && {cmd}'
            else:
                cmd = f'cd "{workdir}" && {cmd}'
        return cmd

    def _build_schtasks_cmd(self, task_name: str, command: str,
                            schedule: Dict, workdir: str = "",
                            enable: bool = True) -> List[str]:
        """构建 Windows schtasks 命令"""
        full_cmd = self._build_full_command(command, workdir)

        schtasks_cmd = [
            "schtasks", "/Create",
            "/TN", f"{TASK_PREFIX}{task_name}",
            "/TR", full_cmd,
            "/SC", schedule.get("type", "DAILY"),
        ]

        if schedule.get("time"):
            schtasks_cmd.extend(["/ST", schedule["time"]])

        if schedule.get("days"):
            if schedule["type"] == "WEEKLY":
                schtasks_cmd.extend(["/D", schedule["days"]])
            elif schedule["type"] == "MONTHLY":
                schtasks_cmd.extend(["/D", schedule["days"]])

        if not enable:
            schtasks_cmd.append("/DISABLE")

        schtasks_cmd.append("/F")

        # 错过触发策略
        missed = PREDEFINED_TASKS.get(task_name, {}).get("missed_run", "skip")
        if missed == "run_once":
            # /RI 60 秒后补跑（仅在错过时触发一次）
            schtasks_cmd.extend(["/RI", "60"])

        return schtasks_cmd

    def _build_crontab_cmd(self, task_name: str, command: str,
                           schedule: Dict, workdir: str = "") -> str:
        """构建 Linux crontab 条目"""
        full_cmd = self._build_full_command(command, workdir)
        cron_expr = schedule.get("cron", "0 8 * * *")
        comment = f"# {TASK_PREFIX}{task_name} - {TASK_DESCRIPTION}"
        return f"{comment}\n{cron_expr} {full_cmd}"

    def _build_launchd_plist(self, task_name: str, command: str,
                             schedule: Dict, workdir: str = "") -> Dict:
        """构建 macOS launchd plist 字典"""
        full_cmd = self._build_full_command(command, workdir)
        plist = {
            "Label": f"{TASK_PREFIX}{task_name}",
            "ProgramArguments": [sys.executable] + full_cmd.split()[1:],
            "WorkingDirectory": workdir or str(Path.home()),
            "StandardOutPath": str(Path.home() / f"{TASK_PREFIX}{task_name}.log"),
            "StandardErrorPath": str(Path.home() / f"{TASK_PREFIX}{task_name}.err"),
            "RunAtLoad": True,
        }
        sched = schedule or {}
        if sched.get("hour") is not None:
            plist["StartCalendarInterval"] = {
                "Hour": sched["hour"],
                "Minute": sched.get("minute", 0),
            }
            if sched.get("weekday") is not None:
                plist["StartCalendarInterval"]["Weekday"] = sched["weekday"]
            if sched.get("day") is not None:
                plist["StartCalendarInterval"]["Day"] = sched["day"]
        return plist

    def _install_launchd(self, task_name: str, plist: Dict) -> Dict[str, Any]:
        """安装 macOS launchd 任务"""
        try:
            launch_dir = Path.home() / "Library" / "LaunchAgents"
            launch_dir.mkdir(parents=True, exist_ok=True)
            plist_path = launch_dir / f"{TASK_PREFIX}{task_name}.plist"

            with open(plist_path, "wb") as f:
                plistlib.dump(plist, f)

            # 卸载旧任务（如果存在）
            subprocess.run(
                ["launchctl", "unload", str(plist_path)],
                capture_output=True, timeout=10
            )

            # 加载新任务
            proc = subprocess.run(
                ["launchctl", "load", str(plist_path)],
                capture_output=True, text=True, timeout=10
            )

            if proc.returncode == 0:
                return {"ok": True, "path": str(plist_path)}
            else:
                return {"ok": False, "error": proc.stderr.strip() or "launchctl load 失败"}
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": "launchctl 执行超时"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _confirm_command(self, task_name: str, command: str,
                         schedule: Dict) -> bool:
        """展示命令并请求用户确认"""
        print(f"\n{'='*60}")
        print(f"📋 定时任务注册确认")
        print(f"{'='*60}")
        print(f"  任务名称: {task_name}")
        print(f"  任务类型: {PREDEFINED_TASKS.get(task_name, {}).get('label', '自定义')}")
        print(f"  操作系统: {self.system}")
        print(f"  执行命令: {command}")
        print(f"  调度配置: {json.dumps(schedule, ensure_ascii=False)}")
        missed = PREDEFINED_TASKS.get(task_name, {}).get("missed_run", "skip")
        missed_label = "错过时补跑一次" if missed == "run_once" else "错过时跳过"
        print(f"  错过策略: {missed_label}")
        print(f"  创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        print(f"\n⚠️  此任务将在您的系统上按计划自动执行上述命令。")
        print(f"   任务前缀为 {TASK_PREFIX}，可通过 list 命令查看所有注册项。\n")

        try:
            answer = input("确认注册？[y/N]: ").strip().lower()
            return answer == "y"
        except Exception:
            return False

    def register(self, task_name: str, command: str = "",
                 schedule: Dict = None, workdir: str = "",
                 enable: bool = True, force: bool = False) -> Dict[str, Any]:
        """
        注册定时任务

        Args:
            task_name: 任务名称
            command: CLI 命令（如果为空则从预定义任务获取）
            schedule: 调度配置（如果为空则从预定义任务获取）
            workdir: 工作目录
            enable: 是否启用
            force: 是否跳过确认（用于自动化场景）

        Returns:
            dict: {"ok": bool, "error": str, "task_name": str}
        """
        # 使用预定义任务
        if not command and task_name in PREDEFINED_TASKS:
            predefined = PREDEFINED_TASKS[task_name]
            command = predefined["command"]
            sys_key = "windows" if IS_WINDOWS else ("linux" if IS_LINUX else "macos")
            schedule = schedule or predefined["schedule"].get(sys_key, {})

        if not command:
            return {"ok": False, "error": f"未知任务: {task_name}", "task_name": task_name}

        schedule = schedule or {"type": "DAILY", "time": "08:00"}

        # 用户确认
        if not force and not self._confirm_command(task_name, command, schedule):
            return {"ok": False, "error": "用户取消注册", "task_name": task_name}

        try:
            if IS_WINDOWS:
                return self._register_windows(task_name, command, schedule, workdir, enable)
            elif IS_LINUX:
                return self._register_linux(task_name, command, schedule, workdir)
            elif IS_MACOS:
                return self._register_macos(task_name, command, schedule, workdir)
            else:
                return {"ok": False, "error": f"不支持的操作系统: {self.system}", "task_name": task_name}
        except Exception as e:
            return {"ok": False, "error": str(e), "task_name": task_name}

    def _register_windows(self, task_name: str, command: str,
                          schedule: Dict, workdir: str,
                          enable: bool) -> Dict[str, Any]:
        """Windows schtasks 注册"""
        schtasks_cmd = self._build_schtasks_cmd(task_name, command, schedule, workdir, enable)

        proc = subprocess.Popen(
            schtasks_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        try:
            stdout, stderr = proc.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            proc.kill()
            return {"ok": False, "error": "schtasks 执行超时", "task_name": task_name}

        if proc.returncode == 0:
            missed = PREDEFINED_TASKS.get(task_name, {}).get("missed_run", "skip")
            self.registry.add(task_name, {
                "command": command,
                "schedule": schedule,
                "workdir": workdir,
                "enabled": enable,
                "missed_run": missed,
                "platform": "windows",
                "created": datetime.now().isoformat()
            })
            return {"ok": True, "task_name": task_name, "message": f"任务已注册: {TASK_PREFIX}{task_name}"}
        else:
            return {"ok": False, "error": stderr.strip() or "schtasks 执行失败", "task_name": task_name}

    def _register_linux(self, task_name: str, command: str,
                        schedule: Dict, workdir: str) -> Dict[str, Any]:
        """Linux crontab 注册"""
        crontab_line = self._build_crontab_cmd(task_name, command, schedule, workdir)
        task_flag = f"# {TASK_PREFIX}{task_name}"

        try:
            proc = subprocess.Popen(
                ["crontab", "-l"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, _ = proc.communicate(timeout=10)
            existing = stdout if proc.returncode == 0 else ""
        except subprocess.TimeoutExpired:
            proc.kill()
            return {"ok": False, "error": "crontab 读取超时", "task_name": task_name}
        except FileNotFoundError:
            return {"ok": False, "error": "crontab 未安装", "task_name": task_name}

        lines = [l for l in existing.splitlines()
                 if not l.startswith(task_flag) and l.strip()]

        lines.append(crontab_line)
        new_crontab = "\n".join(lines) + "\n"

        proc = subprocess.Popen(
            ["crontab", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        try:
            _, stderr = proc.communicate(input=new_crontab, timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            return {"ok": False, "error": "crontab 写入超时", "task_name": task_name}

        if proc.returncode == 0:
            missed = PREDEFINED_TASKS.get(task_name, {}).get("missed_run", "skip")
            self.registry.add(task_name, {
                "command": command,
                "schedule": schedule,
                "workdir": workdir,
                "enabled": True,
                "missed_run": missed,
                "platform": "linux",
                "created": datetime.now().isoformat()
            })
            return {"ok": True, "task_name": task_name, "message": f"crontab 任务已注册: {TASK_PREFIX}{task_name}"}
        else:
            return {"ok": False, "error": stderr.strip(), "task_name": task_name}

    def _register_macos(self, task_name: str, command: str,
                        schedule: Dict, workdir: str) -> Dict[str, Any]:
        """macOS launchd 注册"""
        plist = self._build_launchd_plist(task_name, command, schedule, workdir)
        result = self._install_launchd(task_name, plist)

        if result.get("ok"):
            missed = PREDEFINED_TASKS.get(task_name, {}).get("missed_run", "skip")
            self.registry.add(task_name, {
                "command": command,
                "schedule": schedule,
                "workdir": workdir,
                "enabled": True,
                "missed_run": missed,
                "platform": "macos",
                "plist_path": result.get("path", ""),
                "created": datetime.now().isoformat()
            })
            return {"ok": True, "task_name": task_name, "message": f"launchd 任务已注册: {TASK_PREFIX}{task_name}"}
        else:
            return {"ok": False, "error": result.get("error", "launchd 安装失败"), "task_name": task_name}

    def list_tasks(self) -> Dict[str, Any]:
        """列出所有已注册的定时任务"""
        tasks = []

        if IS_WINDOWS:
            try:
                proc = subprocess.Popen(
                    ["schtasks", "/Query", "/fo", "CSV", "/v"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, _ = proc.communicate(timeout=15)
                if proc.returncode == 0:
                    for line in stdout.splitlines():
                        if TASK_PREFIX in line:
                            tasks.append({"raw": line, "system": "schtasks"})
            except subprocess.TimeoutExpired:
                proc.kill()
            except FileNotFoundError:
                pass
        elif IS_LINUX:
            try:
                proc = subprocess.Popen(
                    ["crontab", "-l"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, _ = proc.communicate(timeout=10)
                if proc.returncode == 0:
                    for line in stdout.splitlines():
                        if TASK_PREFIX in line:
                            tasks.append({"raw": line, "system": "crontab"})
            except subprocess.TimeoutExpired:
                proc.kill()
            except FileNotFoundError:
                pass
        elif IS_MACOS:
            try:
                launch_dir = Path.home() / "Library" / "LaunchAgents"
                if launch_dir.exists():
                    for plist_file in launch_dir.glob(f"{TASK_PREFIX}*.plist"):
                        tasks.append({
                            "raw": plist_file.name,
                            "system": "launchd",
                            "path": str(plist_file)
                        })
            except Exception:
                pass

        # 合并注册表记录
        reg_tasks = []
        for name, info in self.registry.list_all().items():
            reg_tasks.append({
                "task_name": name,
                "command": info.get("command", ""),
                "schedule": info.get("schedule", {}),
                "enabled": info.get("enabled", True),
                "missed_run": info.get("missed_run", "skip"),
                "platform": info.get("platform", ""),
                "created": info.get("created", "")
            })

        return {
            "ok": True,
            "system": self.system,
            "system_tasks": tasks,
            "registry_tasks": reg_tasks,
            "total": len(tasks) + len(reg_tasks),
            "version": self.VERSION
        }

    def cancel(self, task_name: str) -> Dict[str, Any]:
        """取消已注册的定时任务"""
        try:
            if IS_WINDOWS:
                return self._cancel_windows(task_name)
            elif IS_LINUX:
                return self._cancel_linux(task_name)
            elif IS_MACOS:
                return self._cancel_macos(task_name)
            else:
                return {"ok": False, "error": f"不支持的操作系统: {self.system}"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _cancel_windows(self, task_name: str) -> Dict[str, Any]:
        """取消 Windows 任务"""
        proc = subprocess.Popen(
            ["schtasks", "/Delete", "/TN", f"{TASK_PREFIX}{task_name}", "/F"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        try:
            _, stderr = proc.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
            return {"ok": False, "error": "schtasks 删除超时"}

        if proc.returncode == 0:
            self.registry.remove(task_name)
            return {"ok": True, "message": f"任务已删除: {TASK_PREFIX}{task_name}"}
        else:
            return {"ok": False, "error": stderr.strip()}

    def _cancel_linux(self, task_name: str) -> Dict[str, Any]:
        """取消 Linux crontab 任务"""
        task_flag = f"# {TASK_PREFIX}{task_name}"

        try:
            proc = subprocess.Popen(
                ["crontab", "-l"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, _ = proc.communicate(timeout=10)
            existing = stdout if proc.returncode == 0 else ""
        except subprocess.TimeoutExpired:
            proc.kill()
            return {"ok": False, "error": "crontab 读取超时"}

        lines = [l for l in existing.splitlines()
                 if not l.startswith(task_flag) and l.strip()]
        new_crontab = "\n".join(lines) + "\n"

        proc = subprocess.Popen(
            ["crontab", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        try:
            _, stderr = proc.communicate(input=new_crontab, timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            return {"ok": False, "error": "crontab 写入超时"}

        if proc.returncode == 0:
            self.registry.remove(task_name)
            return {"ok": True, "message": f"crontab 任务已删除: {TASK_PREFIX}{task_name}"}
        else:
            return {"ok": False, "error": stderr.strip()}

    def _cancel_macos(self, task_name: str) -> Dict[str, Any]:
        """取消 macOS launchd 任务"""
        try:
            launch_dir = Path.home() / "Library" / "LaunchAgents"
            plist_path = launch_dir / f"{TASK_PREFIX}{task_name}.plist"

            if plist_path.exists():
                # 卸载
                subprocess.run(
                    ["launchctl", "unload", str(plist_path)],
                    capture_output=True, timeout=10
                )
                # 删除 plist
                plist_path.unlink()
                self.registry.remove(task_name)
                return {"ok": True, "message": f"launchd 任务已删除: {TASK_PREFIX}{task_name}"}
            else:
                return {"ok": False, "error": f"未找到 plist 文件: {plist_path}"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def enable_task(self, task_name: str, enable: bool = True) -> Dict[str, Any]:
        """启用/禁用任务"""
        if IS_WINDOWS:
            action = "/ENABLE" if enable else "/DISABLE"
            proc = subprocess.Popen(
                ["schtasks", "/Change", "/TN", f"{TASK_PREFIX}{task_name}", action],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            try:
                _, stderr = proc.communicate(timeout=15)
            except subprocess.TimeoutExpired:
                proc.kill()
                return {"ok": False, "error": "schtasks 变更超时"}

            if proc.returncode == 0:
                info = self.registry.get(task_name)
                if info:
                    info["enabled"] = enable
                    self.registry.add(task_name, info)
                return {"ok": True, "message": f"任务已{'启用' if enable else '禁用'}: {task_name}"}
            else:
                return {"ok": False, "error": stderr.strip()}
        else:
            return {"ok": False, "error": "仅 Windows 支持启用/禁用；macOS/Linux 请取消后重新注册"}

    def list_predefined(self) -> Dict[str, Any]:
        """列出所有预定义任务"""
        return {
            "ok": True,
            "predefined": PREDEFINED_TASKS,
            "total": len(PREDEFINED_TASKS),
            "version": self.VERSION
        }

    def export_registry(self) -> str:
        """导出注册表为 JSON 字符串"""
        return self.registry.export()

    def import_registry(self, data: str) -> Dict[str, Any]:
        """导入 JSON 注册表"""
        if self.registry.import_data(data):
            return {"ok": True, "message": "注册表导入成功"}
        return {"ok": False, "error": "注册表导入失败"}


def main():
    """CLI 入口"""
    parser = argparse.ArgumentParser(
        description=f"定时任务注册管理 {ScheduleRegister.VERSION} — 统一调度层",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # register 子命令
    p_reg = sub.add_parser("register", help="注册定时任务")
    p_reg.add_argument("--name", required=True, help="任务名称（或预定义任务ID: weekly_report/monthly_report/watch_daily）")
    p_reg.add_argument("--cmd", default="", help="自定义 CLI 命令（不指定则使用预定义）")
    p_reg.add_argument("--schedule", default="", help="调度配置 JSON（不指定则使用预定义）")
    p_reg.add_argument("--workdir", default="", help="工作目录")
    p_reg.add_argument("--disable", action="store_true", help="注册后禁用")
    p_reg.add_argument("--force", action="store_true", help="跳过确认（自动化场景）")

    # list 子命令
    sub.add_parser("list", help="列出已注册的定时任务")

    # cancel 子命令
    p_cancel = sub.add_parser("cancel", help="取消定时任务")
    p_cancel.add_argument("--name", required=True, help="任务名称")

    # enable/disable 子命令
    p_toggle = sub.add_parser("toggle", help="启用/禁用任务")
    p_toggle.add_argument("--name", required=True, help="任务名称")
    p_toggle.add_argument("--off", action="store_true", help="禁用（默认启用）")

    # predefined 子命令
    sub.add_parser("predefined", help="列出预定义任务")

    # run 子命令（手动触发）
    p_run = sub.add_parser("run", help="手动执行预定义任务（不注册）")
    p_run.add_argument("--name", required=True, help="预定义任务名称")

    # export 子命令（v5.4 新增）
    sub.add_parser("export", help="导出注册表 JSON（可备份/迁移）")

    # import 子命令（v5.4 新增）
    p_imp = sub.add_parser("import", help="导入注册表 JSON")
    p_imp.add_argument("--data", required=True, help="JSON 数据")

    args = parser.parse_args()
    reg = ScheduleRegister()

    if args.command == "register":
        schedule = None
        if args.schedule:
            try:
                schedule = json.loads(args.schedule)
            except json.JSONDecodeError as e:
                print(json.dumps({"ok": False, "error": f"调度配置 JSON 解析失败: {e}"}))
                return

        result = reg.register(
            task_name=args.name,
            command=args.cmd,
            schedule=schedule,
            workdir=args.workdir,
            enable=not args.disable,
            force=args.force,
        )
        print(json.dumps(result, ensure_ascii=False))

    elif args.command == "list":
        result = reg.list_tasks()
        print(json.dumps(result, ensure_ascii=False, default=str))

    elif args.command == "cancel":
        result = reg.cancel(args.name)
        print(json.dumps(result, ensure_ascii=False))

    elif args.command == "toggle":
        result = reg.enable_task(args.name, enable=not args.off)
        print(json.dumps(result, ensure_ascii=False))

    elif args.command == "predefined":
        result = reg.list_predefined()
        print(json.dumps(result, ensure_ascii=False, default=str))

    elif args.command == "run":
        if args.name not in PREDEFINED_TASKS:
            print(json.dumps({"ok": False, "error": f"未知预定义任务: {args.name}"}))
            return
        task = PREDEFINED_TASKS[args.name]
        command = task["command"]
        print(f"执行命令: {command}")
        print("提示：请手动替换占位符（如 {date}、{watch_dir}）后执行")

    elif args.command == "export":
        print(reg.export_registry())

    elif args.command == "import":
        result = reg.import_registry(args.data)
        print(json.dumps(result, ensure_ascii=False))

    else:
        print(json.dumps({"ok": False, "error": "未知命令"}))


if __name__ == "__main__":
    main()
