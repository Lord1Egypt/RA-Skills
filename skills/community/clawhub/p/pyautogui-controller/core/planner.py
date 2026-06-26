from typing import List
from core.types import ParsedIntent, TaskStep, ActionType, ElementType


class Planner:
    def plan(self, intent: ParsedIntent) -> List[TaskStep]:
        if intent.action == ActionType.COMPOUND:
            steps = []
            for child in intent.children:
                steps.extend(self.plan(child))
            return steps

        steps: List[TaskStep] = []
        sid = 1
        if intent.action == ActionType.NAVIGATE and intent.url:
            steps.append(TaskStep(id=f"step_{sid:03d}", action=ActionType.NAVIGATE, description=f"导航到 {intent.url}", params={"url": intent.url}, success_criteria={"url_loaded": True}))
        elif intent.action == ActionType.TYPE:
            steps.append(TaskStep(id=f"step_{sid:03d}", action=ActionType.FOCUS_INPUT, description="定位并聚焦输入框", params={"target_text": intent.target_text, "target_type": (intent.target_type or ElementType.INPUT).value, "position_hint": intent.position_hint}, success_criteria={"focused": True}))
            sid += 1
            steps.append(TaskStep(id=f"step_{sid:03d}", action=ActionType.TYPE, description="输入文本", params={"text": intent.input_text or intent.raw_command}, success_criteria={"text_changed": True}))
        elif intent.action == ActionType.CLICK:
            steps.append(TaskStep(id=f"step_{sid:03d}", action=ActionType.CLICK, description="定位并点击目标", params={"target_text": intent.target_text, "target_type": (intent.target_type or ElementType.BUTTON).value, "position_hint": intent.position_hint}, success_criteria={"state_changed": True}))
        elif intent.action == ActionType.WAIT:
            steps.append(TaskStep(id=f"step_{sid:03d}", action=ActionType.WAIT, description="等待界面稳定", params={"seconds": 1.5}))
        elif intent.action == ActionType.SCREENSHOT:
            steps.append(TaskStep(id=f"step_{sid:03d}", action=ActionType.SCREENSHOT, description="截图", params={}))
        elif intent.action == ActionType.OPEN_APP and intent.app_name:
            steps.append(TaskStep(id=f"step_{sid:03d}", action=ActionType.OPEN_APP, description=f"打开应用 {intent.app_name}", params={"app_name": intent.app_name}, success_criteria={"window_changed": True}))
        else:
            steps.append(TaskStep(id=f"step_{sid:03d}", action=ActionType.UNKNOWN, description=f"未识别动作: {intent.raw_command}", params={}))
        return steps
