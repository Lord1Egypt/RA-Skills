#!/usr/bin/env python3
"""
工作流引擎核心库
支持多轮对话、状态保持、流程锁定、超时处理
"""

import json
import re
from typing import Optional, Dict, Any, Callable, List, Tuple
from dataclasses import dataclass
from enum import Enum

from state_manager import state_manager, SessionState


class WorkflowResult(Enum):
    """工作流执行结果"""
    CONTINUE = "continue"      # 继续下一步
    COMPLETE = "complete"      # 工作流完成
    EXIT = "exit"              # 用户退出
    TIMEOUT = "timeout"        # 超时
    INVALID = "invalid"        # 无效输入
    ERROR = "error"            # 错误


@dataclass
class WorkflowStep:
    """工作流步骤定义"""
    step_id: int
    prompt: str                # 提示语
    validator: Optional[Callable[[str], Tuple[bool, Any]]] = None  # 验证函数
    on_complete: Optional[Callable[[Dict[str, Any]], str]] = None  # 完成回调


@dataclass
class WorkflowDefinition:
    """工作流定义"""
    workflow_type: str
    name: str
    description: str
    steps: List[WorkflowStep]
    exit_keywords: List[str] = None
    
    def __post_init__(self):
        if self.exit_keywords is None:
            self.exit_keywords = ['q', 'quit', '退出', 'cancel', '取消']


class WorkflowEngine:
    """工作流引擎"""
    
    def __init__(self):
        self.workflows: Dict[str, WorkflowDefinition] = {}
        self.state_manager = state_manager
    
    def register_workflow(self, workflow: WorkflowDefinition):
        """注册工作流"""
        self.workflows[workflow.workflow_type] = workflow
    
    def start_workflow(
        self,
        session_id: str,
        workflow_type: str,
        timeout_seconds: int = 60
    ) -> Optional[str]:
        """启动工作流"""
        if workflow_type not in self.workflows:
            return f"错误：未知的工作流类型 '{workflow_type}'"
        
        workflow = self.workflows[workflow_type]
        state = self.state_manager.create_session(
            session_id=session_id,
            workflow_type=workflow_type,
            timeout_seconds=timeout_seconds
        )
        
        # 返回第一步的提示
        return self._get_step_prompt(workflow, 0)
    
    def process_message(
        self,
        session_id: str,
        message: str
    ) -> Tuple[WorkflowResult, str]:
        """
        处理用户消息
        返回：(结果类型，回复消息)
        """
        # 检查退出命令
        if self._is_exit_command(message):
            self.state_manager.clear_session(session_id)
            return WorkflowResult.EXIT, "已退出当前流程"
        
        # 获取当前会话状态
        state = self.state_manager.get_session(session_id)
        if not state:
            return WorkflowResult.INVALID, "当前没有进行中的工作流"
        
        # 获取工作流定义
        workflow = self.workflows.get(state.workflow_type)
        if not workflow:
            return WorkflowResult.ERROR, f"错误：工作流 '{state.workflow_type}' 未定义"
        
        # 检查是否已完成所有步骤
        if state.current_step >= len(workflow.steps):
            # 工作流已完成，调用完成回调
            final_step = workflow.steps[-1]
            if final_step.on_complete:
                response = final_step.on_complete(state.step_data)
                self.state_manager.clear_session(session_id)
                return WorkflowResult.COMPLETE, response
            else:
                self.state_manager.clear_session(session_id)
                return WorkflowResult.COMPLETE, "工作流已完成"
        
        # 获取当前步骤
        current_step = workflow.steps[state.current_step]
        
        # 验证输入
        user_input = message.strip()
        validated_data = state.step_data.copy()  # 使用副本保存验证后的数据
        if current_step.validator:
            is_valid, result = current_step.validator(user_input)
            if not is_valid:
                return WorkflowResult.INVALID, f"输入无效：{result}\n{current_step.prompt}"
            
            # 保存验证后的数据到副本
            step_key = f"step_{current_step.step_id}"
            validated_data[step_key] = result
        
        # 保存数据到状态管理器
        self.state_manager.update_session(
            session_id=session_id,
            step_data=validated_data
        )
        
        # 推进到下一步（获取更新后的状态）
        updated_state = self.state_manager.advance_step(session_id)
        
        # 检查是否还有下一步（使用更新后的 current_step）
        next_step_index = updated_state.current_step
        if next_step_index < len(workflow.steps):
            # 中间步骤：如果有 on_complete 回调，调用它获取自定义提示
            if current_step.on_complete:
                next_prompt = current_step.on_complete(validated_data)
            else:
                next_prompt = self._get_step_prompt(workflow, next_step_index)
            return WorkflowResult.CONTINUE, next_prompt
        else:
            # 最后一步：调用完成回调
            if current_step.on_complete:
                response = current_step.on_complete(updated_state.step_data)
                self.state_manager.clear_session(session_id)
                return WorkflowResult.COMPLETE, response
            else:
                self.state_manager.clear_session(session_id)
                return WorkflowResult.COMPLETE, "工作流已完成"
    
    def _get_step_prompt(self, workflow: WorkflowDefinition, step_index: int) -> str:
        """获取步骤提示语"""
        if step_index >= len(workflow.steps):
            return ""
        step = workflow.steps[step_index]
        return step.prompt
    
    def _is_exit_command(self, message: str) -> bool:
        """检查是否为退出命令"""
        msg_lower = message.strip().lower()
        # 获取所有已注册工作流的退出关键词
        all_exit_keywords = set()
        for workflow in self.workflows.values():
            all_exit_keywords.update(workflow.exit_keywords)
        
        return msg_lower in all_exit_keywords
    
    def get_session_status(self, session_id: str) -> Optional[Dict]:
        """获取会话状态（用于调试）"""
        return self.state_manager.get_session_info(session_id)
    
    def check_timeouts(self) -> List[str]:
        """检查超时会话"""
        return self.state_manager.check_timeouts()
    
    def list_active_sessions(self) -> List[Dict]:
        """列出活跃会话"""
        return self.state_manager.list_active_sessions()


# 预定义的验证器函数
def validate_mac_address(mac: str) -> Tuple[bool, str]:
    """验证 MAC 地址格式"""
    mac_clean = mac.replace(':', '').replace('-', '').upper()
    if len(mac_clean) != 12 or not all(c in '0123456789ABCDEF' for c in mac_clean):
        return False, "MAC 地址格式不正确（应为 12 位十六进制，如 00:11:22:33:44:55）"
    
    # 标准化格式
    mac_formatted = ':'.join(mac_clean[i:i+2] for i in range(0, 12, 2))
    return True, mac_formatted


def validate_not_empty(text: str) -> Tuple[bool, str]:
    """验证非空"""
    if not text.strip():
        return False, "输入不能为空"
    return True, text.strip()


def validate_device_name(name: str) -> Tuple[bool, str]:
    """验证设备名称"""
    if not name.strip():
        return False, "设备名称不能为空"
    if len(name) > 50:
        return False, "设备名称不能超过 50 个字符"
    return True, name.strip()


# 创建全局引擎实例
engine = WorkflowEngine()


if __name__ == '__main__':
    # 测试代码
    import sys
    
    print("工作流引擎测试")
    print("=" * 50)
    
    # 注册测试工作流
    test_workflow = WorkflowDefinition(
        workflow_type="test_add_device",
        name="添加设备测试",
        description="测试用添加设备工作流",
        steps=[
            WorkflowStep(
                step_id=1,
                prompt="请输入设备名称：",
                validator=validate_device_name
            ),
            WorkflowStep(
                step_id=2,
                prompt="请输入 MAC 地址（如 00:11:22:33:44:55）：",
                validator=validate_mac_address
            ),
            WorkflowStep(
                step_id=3,
                prompt="请输入备注（可选，直接回车跳过）：",
                validator=lambda x: (True, x.strip() if x.strip() else "无")
            )
        ],
        exit_keywords=['q', 'quit', '退出']
    )
    
    engine.register_workflow(test_workflow)
    
    # 测试会话
    test_session = "test_user_001"
    
    print(f"\n1. 启动工作流")
    result = engine.start_workflow(test_session, "test_add_device")
    print(f"   提示：{result}")
    
    print(f"\n2. 输入设备名称 '测试电脑'")
    result_type, result_msg = engine.process_message(test_session, "测试电脑")
    print(f"   结果：{result_type.value}, 回复：{result_msg}")
    
    print(f"\n3. 输入 MAC 地址 '00:11:22:33:44:55'")
    result_type, result_msg = engine.process_message(test_session, "00:11:22:33:44:55")
    print(f"   结果：{result_type.value}, 回复：{result_msg}")
    
    print(f"\n4. 输入备注 '书房'")
    result_type, result_msg = engine.process_message(test_session, "书房")
    print(f"   结果：{result_type.value}, 回复：{result_msg}")
    
    print(f"\n5. 查看会话状态")
    status = engine.get_session_status(test_session)
    if status:
        print(f"   状态：{json.dumps(status, ensure_ascii=False, indent=2)}")
    else:
        print("   会话已结束")
    
    print("\n测试完成")
