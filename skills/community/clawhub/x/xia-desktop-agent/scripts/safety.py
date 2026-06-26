"""安全限制模块 - 防止危险操作"""

import re
import logging

logger = logging.getLogger(__name__)

# 危险操作关键词
DANGEROUS_PATTERNS = [
    r"删除", r"format", r"del\s", r"rm\s", r"rmdir",
    r"reg\s+delete", r"regedit", r"taskkill",
    r"shutdown", r"restart", r"重启", r"关机",
    r"net\s+user", r"net\s+localgroup",
    r"格式化", r"清空", r"擦除",
]

# 只读/安全的应用白名单
SAFE_APPS = {
    "notepad", "calc", "explorer", "chrome", "msedge",
    "code", "微信", "weixin", "钉钉", "dingtalk",
}


class SafetyChecker:
    """安全检查器"""

    def __init__(self, max_steps: int = 20, max_timeout: int = 300):
        self.max_steps = max_steps
        self.max_timeout = max_timeout  # 秒

    def check_task(self, task: str) -> bool:
        """检查任务描述是否包含危险操作"""
        task_lower = task.lower()
        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, task_lower):
                logger.warning(f"任务包含危险操作关键词: {pattern}")
                # 不直接拒绝，但记录警告
                logger.warning(f"⚠️ 任务可能包含危险操作: {task}")
                return True  # 允许但警告
        return True

    def check_plan(self, steps: list[dict]) -> bool:
        """检查执行计划是否安全"""
        if len(steps) > self.max_steps:
            logger.error(f"计划步数 {len(steps)} 超过最大限制 {self.max_steps}")
            return False

        for i, step in enumerate(steps):
            action = step.get("action", "")
            app = step.get("app", "").lower()

            # 检查是否有危险操作
            for key in ("text", "key", "app"):
                val = str(step.get(key, "")).lower()
                for pattern in DANGEROUS_PATTERNS:
                    if re.search(pattern, val):
                        logger.warning(f"步骤 {i+1} 包含危险操作: {pattern}")

        return True

    def is_dangerous(self, text: str) -> bool:
        """判断文本是否包含危险操作"""
        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, text.lower()):
                return True
        return False
