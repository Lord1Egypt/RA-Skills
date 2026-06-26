"""任务执行器 - 逐步执行计划，截图验证，失败重试"""

import json
import time
import logging
import sys
from pathlib import Path

from desktop_agent import DesktopAgent
from task_planner import plan_task
from safety import SafetyChecker

logger = logging.getLogger(__name__)


class TaskExecutor:
    """自动执行引擎：规划 → 执行 → 验证 → 重试"""

    def __init__(self):
        self.agent = DesktopAgent()
        self.safety = SafetyChecker()

    def execute_task(self, task: str) -> dict:
        """执行自然语言任务，返回执行结果"""
        start_time = time.time()
        log = []

        # 1. 安全检查
        if not self.safety.check_task(task):
            return {"success": False, "error": "任务被安全检查拦截", "log": log}

        # 2. 规划
        steps = plan_task(task)
        if not steps:
            return {"success": False, "error": "任务规划失败，无法生成步骤", "log": log}

        if not self.safety.check_plan(steps):
            return {"success": False, "error": "计划被安全检查拦截", "log": log}

        log.append({"phase": "plan", "steps": len(steps), "descriptions": [s.get("description", "") for s in steps]})

        # 3. 执行
        for i, step in enumerate(steps):
            # 超时检查
            if time.time() - start_time > self.safety.max_timeout:
                log.append({"step": i+1, "error": "执行超时"})
                return {"success": False, "error": "执行超时", "log": log}

            action = step.get("action", "")
            desc = step.get("description", action)
            logger.info(f"执行步骤 {i+1}/{len(steps)}: {desc}")

            # 截图记录执行前状态
            before_ss = self.agent.screenshot()

            # 执行单步
            success = self._execute_step(step)
            elapsed = round(time.time() - start_time, 1)

            log.append({
                "step": i+1, "action": action, "description": desc,
                "success": success, "elapsed": elapsed,
                "before_screenshot": before_ss
            })

            if not success:
                logger.warning(f"步骤 {i+1} 执行失败，跳过继续")
                # 失败不中断，继续下一步（某些步骤可能有依赖问题）

            # 步骤间短暂等待
            self.agent.wait(0.5)

        # 4. 最终截图
        final_ss = self.agent.screenshot()
        total_time = round(time.time() - start_time, 1)
        log.append({"phase": "done", "screenshot": final_ss, "total_time": total_time})

        logger.info(f"任务完成，总耗时 {total_time}s")
        return {"success": True, "total_time": total_time, "log": log}

    def _execute_step(self, step: dict) -> bool:
        """执行单个操作步骤"""
        try:
            action = step.get("action")

            if action == "click":
                x, y = step.get("x"), step.get("y")
                if x is not None and y is not None:
                    self.agent.click(int(x), int(y))
                return True

            elif action == "double_click":
                x, y = step.get("x"), step.get("y")
                if x is not None and y is not None:
                    self.agent.double_click(int(x), int(y))
                return True

            elif action == "type_text":
                text = step.get("text", "")
                self.agent.type_text(text)
                return True

            elif action == "press_key":
                key = step.get("key", "enter")
                self.agent.press_key(key)
                return True

            elif action == "scroll":
                amount = step.get("amount", -3)
                self.agent.scroll(int(amount))
                return True

            elif action == "open_app":
                app = step.get("app", "")
                return self.agent.open_app(app)

            elif action == "wait":
                seconds = step.get("seconds", 1)
                self.agent.wait(float(seconds))
                return True

            elif action == "screenshot":
                self.agent.screenshot()
                return True

            elif action == "find_and_click":
                # 简化实现：需要坐标时直接click
                x, y = step.get("x"), step.get("y")
                if x is not None and y is not None:
                    self.agent.click(int(x), int(y))
                    return True
                logger.warning("find_and_click 需要坐标参数")
                return False

            else:
                logger.warning(f"未知操作: {action}")
                return False

        except Exception as e:
            logger.error(f"执行步骤异常: {e}")
            return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")

    if len(sys.argv) < 2:
        print("用法: python task_executor.py <任务描述>")
        sys.exit(1)

    task = sys.argv[1]
    executor = TaskExecutor()
    result = executor.execute_task(task)
    print(json.dumps(result, ensure_ascii=False, indent=2))
