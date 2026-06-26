"""
Skill 运行适配器
针对不同 skill 的入口方式，提供统一的运行接口
"""

import importlib
import json
import os
import subprocess
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from typing import Any, Callable, Dict, List, Optional

from skills_monitor.adapters.skill_registry import SkillInfo


class SkillRunner:
    """统一的 Skill 运行器"""

    def __init__(self, skill_info: SkillInfo):
        self.info = skill_info

    def run(self, task_name: str = "", params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        运行 skill
        返回 {"success": bool, "output": ..., "error": ...}
        """
        if params is None:
            params = {}

        if self.info.entry_type == "none":
            return {
                "success": False,
                "output": None,
                "error": f"Skill [{self.info.slug}] 没有可执行入口",
            }

        if self.info.entry_type == "cli":
            return self._run_cli(task_name, params)
        elif self.info.entry_type == "function":
            return self._run_function(task_name, params)
        else:
            return {
                "success": False,
                "output": None,
                "error": f"未知的入口类型: {self.info.entry_type}",
            }

    def _run_cli(self, task_name: str, params: Dict) -> Dict[str, Any]:
        """通过 CLI (subprocess) 运行 skill"""
        entry_path = os.path.join(self.info.dir_path, self.info.entry_file)
        if not os.path.isfile(entry_path):
            return {"success": False, "output": None, "error": f"入口文件不存在: {entry_path}"}

        # 构建命令行参数
        cmd = [sys.executable, entry_path]
        if task_name:
            cmd.append(task_name)
        for k, v in params.items():
            if v is True:
                cmd.append(f"--{k}")
            elif v is not None and v is not False:
                cmd.append(f"--{k}")
                cmd.append(str(v))

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=self.info.dir_path,
                env={**os.environ, "PYTHONPATH": self.info.dir_path},
            )

            output = result.stdout.strip()
            stderr = result.stderr.strip()

            # 尝试解析 JSON 输出
            parsed_output = output
            try:
                parsed_output = json.loads(output)
            except (json.JSONDecodeError, ValueError):
                pass

            if result.returncode == 0:
                return {"success": True, "output": parsed_output, "error": None}
            else:
                return {
                    "success": False,
                    "output": parsed_output,
                    "error": stderr or f"exit code: {result.returncode}",
                }

        except subprocess.TimeoutExpired:
            return {"success": False, "output": None, "error": "执行超时 (120s)"}
        except Exception as e:
            return {"success": False, "output": None, "error": str(e)}

    def _run_function(self, task_name: str, params: Dict) -> Dict[str, Any]:
        """通过直接导入函数运行 skill"""
        entry_path = os.path.join(self.info.dir_path, self.info.entry_file)
        if not os.path.isfile(entry_path):
            return {"success": False, "output": None, "error": f"入口文件不存在: {entry_path}"}

        try:
            # 动态导入
            spec = importlib.util.spec_from_file_location(
                f"skill_{self.info.slug}", entry_path
            )
            module = importlib.util.module_from_spec(spec)
            
            # 添加 skill 目录到 path
            if self.info.dir_path not in sys.path:
                sys.path.insert(0, self.info.dir_path)
            
            spec.loader.exec_module(module)

            # 查找目标函数
            func = None
            if task_name and hasattr(module, task_name):
                func = getattr(module, task_name)
            elif hasattr(module, "main"):
                func = module.main
            elif hasattr(module, "run"):
                func = module.run
            else:
                return {
                    "success": False,
                    "output": None,
                    "error": f"找不到函数: {task_name or 'main/run'}",
                }

            # 捕获 stdout
            stdout_capture = io.StringIO()
            with redirect_stdout(stdout_capture):
                result = func(**params) if params else func()

            stdout_text = stdout_capture.getvalue()
            output = result if result is not None else stdout_text

            return {"success": True, "output": output, "error": None}

        except Exception as e:
            return {"success": False, "output": None, "error": str(e)}


# ──────── 预定义的快捷适配器 ────────

class AShareShortDecisionAdapter:
    """a-share-short-decision 的专用适配器"""
    
    TASKS = [
        "get_market_sentiment",
        "get_sector_rotation",
        "scan_strong_stocks",
        "analyze_capital_flow",
        "short_term_signal_engine",
        "short_term_risk_control",
        "generate_daily_report",
    ]

    def __init__(self, skill_info: SkillInfo):
        self.runner = SkillRunner(skill_info)
        self.info = skill_info

    def list_tasks(self) -> List[str]:
        return self.TASKS

    def run_task(self, task: str, **kwargs) -> Dict[str, Any]:
        return self.runner.run(task_name=task, params=kwargs)


class TradingSignalsAdapter:
    """trading-signals 的专用适配器"""
    
    DEFAULT_SYMBOLS = ["AAPL", "BTC-USD", "0700.HK"]

    def __init__(self, skill_info: SkillInfo):
        self.runner = SkillRunner(skill_info)
        self.info = skill_info

    def list_tasks(self) -> List[str]:
        return ["analyze_signals"]

    def run_task(self, symbol: str = "AAPL") -> Dict[str, Any]:
        return self.runner.run(task_name="", params={})  # 通过 sys.argv 传参
    
    def run_with_symbol(self, symbol: str) -> Dict[str, Any]:
        """直接运行并传入 symbol"""
        entry_path = os.path.join(self.info.dir_path, self.info.entry_file)
        try:
            result = subprocess.run(
                [sys.executable, entry_path, symbol],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=self.info.dir_path,
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip(),
                "error": result.stderr.strip() if result.returncode != 0 else None,
            }
        except Exception as e:
            return {"success": False, "output": None, "error": str(e)}


class StockScreenerAdapter:
    """stock-screener-cn 的专用适配器"""

    STRATEGIES = [
        "均线多头排列", "均线向上", "缩量回踩",
        "放量突破", "金叉", "大帅逼策略", "龙回头",
    ]

    def __init__(self, skill_info: SkillInfo):
        self.runner = SkillRunner(skill_info)
        self.info = skill_info

    def list_tasks(self) -> List[str]:
        return self.STRATEGIES

    def run_task(self, strategy: str = "金叉", limit: int = 10) -> Dict[str, Any]:
        return self.runner.run(params={
            "strategy": strategy,
            "limit": limit,
            "min-price": 5.0,
            "max-price": 100.0,
        })


def get_adapter(skill_info: SkillInfo):
    """工厂函数：为指定 skill 返回专用适配器"""
    adapters = {
        "a-share-short-decision": AShareShortDecisionAdapter,
        "trading-signals": TradingSignalsAdapter,
        "stock-screener-cn": StockScreenerAdapter,
    }
    adapter_class = adapters.get(skill_info.slug)
    if adapter_class:
        return adapter_class(skill_info)
    # 通用 runner
    return SkillRunner(skill_info)
