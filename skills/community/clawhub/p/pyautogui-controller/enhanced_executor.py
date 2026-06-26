#!/usr/bin/env python3
"""Legacy compatibility wrapper for the new orchestrator."""

from app.config import AppConfig
from core.orchestrator import Orchestrator


class ExecutionResult:
    def __init__(self, success: bool, data=None, error: str = None):
        self.success = success
        self.data = data
        self.error = error


class EnhancedExecutor:
    def __init__(self):
        self.runner = Orchestrator(AppConfig())

    def execute_plan(self, steps):
        results = []
        success_count = 0
        failed_count = 0
        for step in steps:
            result = self.execute_step(step)
            results.append({"step": step, "result": result})
            if result.success:
                success_count += 1
            else:
                failed_count += 1
        return {
            "success": failed_count == 0,
            "total": len(steps),
            "success_count": success_count,
            "failed_count": failed_count,
            "results": results,
        }

    def execute_step(self, step):
        action = getattr(step, "action", None) or getattr(step, "step_type", None)
        params = getattr(step, "params", {}) or {}
        description = getattr(step, "description", "")
        try:
            if hasattr(action, "value"):
                action = action.value
            if action in {"navigate", "ActionType.NAVIGATE"} and params.get("url"):
                out = self.runner.execute(f"打开浏览器访问 {params['url']}")
            elif action in {"type", "ActionType.TYPE"} and params.get("text"):
                out = self.runner.execute(f"在输入框输入 '{params['text']}'")
            elif action in {"click", "ActionType.CLICK"}:
                target = params.get("target_text") or params.get("description") or description or "按钮"
                out = self.runner.execute(f"点击{target}")
            elif action in {"open_app", "ActionType.OPEN_APP", "start"} and params.get("app_name"):
                out = self.runner.execute(f"打开 {params['app_name']}")
            else:
                out = {"success": False, "error": f"unsupported legacy step: {description or action}"}
            return ExecutionResult(bool(out.get("success")), data=out, error=out.get("error"))
        except Exception as exc:
            return ExecutionResult(False, error=str(exc))
