#!/usr/bin/env python3
"""
WoL 工作流实现
使用工作流引擎实现多轮对话添加/删除设备
"""

import sys
from pathlib import Path
from typing import Tuple, Any

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from workflow_engine import (
    WorkflowEngine, 
    WorkflowDefinition, 
    WorkflowStep,
    WorkflowResult,
    validate_mac_address,
    validate_device_name,
    validate_not_empty,
    engine
)
from wol_manager import add_device, remove_device, list_devices


def create_add_device_workflow() -> WorkflowDefinition:
    """创建添加设备工作流"""
    
    def on_add_complete(step_data: dict) -> str:
        """添加设备完成回调"""
        name = step_data.get('step_1', '')
        mac = step_data.get('step_2', '')
        note = step_data.get('step_3', '无')
        
        success, msg = add_device(name, mac, note)
        if success:
            return (
                f"✅ 设备添加成功！\n\n"
                f"名称：{name}\n"
                f"MAC: {mac}\n"
                f"备注：{note}\n\n"
                f"现在可以使用 '开机 -{name}' 唤醒设备"
            )
        else:
            return f"❌ 添加失败：{msg}"
    
    return WorkflowDefinition(
        workflow_type="wol_add_device",
        name="添加 WoL 设备",
        description="通过多轮对话添加 Wake-on-LAN 设备",
        steps=[
            WorkflowStep(
                step_id=1,
                prompt="📝 第一步：请输入设备名称（如：书房电脑）\n（输入 q 退出）",
                validator=validate_device_name
            ),
            WorkflowStep(
                step_id=2,
                prompt="📝 第二步：请输入 MAC 地址\n格式：00:11:22:33:44:55\n（输入 q 退出）",
                validator=validate_mac_address
            ),
            WorkflowStep(
                step_id=3,
                prompt="📝 第三步：请输入备注信息（可选）\n直接回车可跳过\n（输入 q 退出）",
                validator=lambda x: (True, x.strip() if x.strip() else "无"),
                on_complete=on_add_complete
            )
        ],
        exit_keywords=['q', 'quit', '退出', 'cancel', '取消']
    )


def validate_device_selection(user_input: str) -> Tuple[bool, Any]:
    """
    验证设备选择（支持编号或名称）
    返回：(是否有效，设备名称或错误信息)
    """
    from wol_manager import load_devices
    
    user_input = user_input.strip()
    if not user_input:
        return False, "输入不能为空"
    
    devices = load_devices()
    if not devices:
        return False, "当前没有设备，请先添加设备"
    
    # 尝试按编号查找
    try:
        dev_id = int(user_input)
        device = next((d for d in devices if d['id'] == dev_id), None)
        if device:
            return True, device['name']
        else:
            return False, f"未找到编号为 {dev_id} 的设备"
    except ValueError:
        pass
    
    # 尝试按名称精确匹配
    device = next((d for d in devices if d['name'].lower() == user_input.lower()), None)
    if device:
        return True, device['name']
    
    # 尝试模糊匹配（包含匹配）
    matches = [d for d in devices if user_input.lower() in d['name'].lower()]
    if len(matches) == 1:
        return True, matches[0]['name']
    elif len(matches) > 1:
        match_names = ', '.join([d['name'] for d in matches])
        return False, f"匹配到多个设备：{match_names}，请输入更具体的名称或编号"
    
    return False, f"未找到设备：{user_input}"


def create_remove_device_workflow() -> WorkflowDefinition:
    """创建删除设备工作流"""
    
    def on_step1_complete(step_data: dict) -> str:
        """第一步完成：显示确认提示"""
        device_name = step_data.get('step_1', '')
        from wol_manager import load_devices
        devices = load_devices()
        device = next((d for d in devices if d['name'] == device_name), None)
        
        if device:
            return (
                f"⚠️ 确认删除操作\n\n"
                f"设备：{device['name']}\n"
                f"MAC: {device['mac']}\n"
                f"备注：{device.get('note', '无')}\n\n"
                f"回复 yes 确认删除，回复 q 取消"
            )
        else:
            return "❌ 设备不存在，请重新开始"
    
    def on_remove_complete(step_data: dict) -> str:
        """删除设备完成回调"""
        device_name = step_data.get('step_1', '')
        confirm = step_data.get('step_2', '')
        
        if confirm.lower() != 'yes':
            return "已取消删除操作"
        
        success, msg = remove_device(device_name)
        if success:
            return f"✅ 删除成功\n已移除设备：{device_name}"
        else:
            return f"❌ 删除失败：{msg}"
    
    # 获取设备列表提示
    from wol_manager import list_devices as list_all_devices
    device_list = list_all_devices()
    
    return WorkflowDefinition(
        workflow_type="wol_remove_device",
        name="删除 WoL 设备",
        description="通过多轮对话删除 Wake-on-LAN 设备",
        steps=[
            WorkflowStep(
                step_id=1,
                prompt=(
                    f"📋 请选择要删除的设备：\n\n"
                    f"{device_list}\n"
                    f"输入设备编号或名称（支持模糊匹配）\n"
                    f"（输入 q 退出）"
                ),
                validator=validate_device_selection,
                on_complete=on_step1_complete
            ),
            WorkflowStep(
                step_id=2,
                prompt="请确认是否删除",
                validator=lambda x: (
                    (True, x.strip()) if x.strip().lower() in ['yes', 'y', '是', '确认'] 
                    else (False, "请输入 yes 确认，或 q 取消")
                ),
                on_complete=on_remove_complete
            )
        ],
        exit_keywords=['q', 'quit', '退出', 'cancel', '取消']
    )


def init_wol_workflows():
    """初始化 WoL 工作流"""
    engine.register_workflow(create_add_device_workflow())
    engine.register_workflow(create_remove_device_workflow())
    return engine


# 命令行接口
def main():
    """命令行测试接口"""
    if len(sys.argv) < 2:
        print("WoL 工作流测试工具")
        print("=" * 50)
        print("用法：wol_workflow.py <command> [args]")
        print("")
        print("命令:")
        print("  test-add              - 测试添加设备工作流")
        print("  test-remove           - 测试删除设备工作流")
        print("  list-sessions         - 列出活跃会话")
        print("  session-info <id>     - 查看会话信息")
        print("  check-timeouts        - 检查超时")
        print("")
        print("交互式测试:")
        print("  interactive-add       - 交互式测试添加设备")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    # 初始化工作流
    init_wol_workflows()
    test_session = "cli_test_session"
    
    if cmd == 'test-add':
        print("测试添加设备工作流")
        print("-" * 50)
        
        # 启动工作流
        result = engine.start_workflow(test_session, "wol_add_device", timeout_seconds=60)
        print(f"引擎：{result}")
        
        # 模拟用户输入
        test_inputs = [
            ("测试电脑", "设备名称"),
            ("00:11:22:33:44:55", "MAC 地址"),
            ("测试备注", "备注信息")
        ]
        
        for user_input, description in test_inputs:
            print(f"\n用户输入 ({description}): {user_input}")
            result_type, result_msg = engine.process_message(test_session, user_input)
            print(f"引擎回复 [{result_type.value}]: {result_msg}")
            
            if result_type == WorkflowResult.COMPLETE:
                break
        
        print("\n测试完成")
    
    elif cmd == 'test-remove':
        print("测试删除设备工作流（按名称）")
        print("-" * 50)
        
        result = engine.start_workflow(test_session, "wol_remove_device")
        print(f"引擎：{result}")
        
        # 第一步：选择设备（按名称）
        print(f"\n用户输入 (选择设备): 测试电脑")
        result_type, result_msg = engine.process_message(test_session, "测试电脑")
        print(f"引擎回复 [{result_type.value}]: {result_msg}")
        
        if result_type == WorkflowResult.CONTINUE:
            # 第二步：确认删除
            print(f"\n用户输入 (确认): yes")
            result_type, result_msg = engine.process_message(test_session, "yes")
            print(f"引擎回复 [{result_type.value}]: {result_msg}")
        
        print("\n测试完成")
    
    elif cmd == 'test-remove-by-id':
        print("测试删除设备工作流（按编号）")
        print("-" * 50)
        
        test_session_id = "cli_test_session_id"
        result = engine.start_workflow(test_session_id, "wol_remove_device")
        print(f"引擎：{result}")
        
        # 第一步：选择设备（按编号）
        print(f"\n用户输入 (选择设备): 2")
        result_type, result_msg = engine.process_message(test_session_id, "2")
        print(f"引擎回复 [{result_type.value}]: {result_msg}")
        
        if result_type == WorkflowResult.CONTINUE:
            # 第二步：确认删除
            print(f"\n用户输入 (确认): yes")
            result_type, result_msg = engine.process_message(test_session_id, "yes")
            print(f"引擎回复 [{result_type.value}]: {result_msg}")
        
        print("\n测试完成")
    
    elif cmd == 'test-remove-fuzzy':
        print("测试删除设备工作流（模糊匹配）")
        print("-" * 50)
        
        test_session_id = "cli_test_session_fuzzy"
        result = engine.start_workflow(test_session_id, "wol_remove_device")
        print(f"引擎：{result}")
        
        # 第一步：选择设备（模糊匹配 "测试" 应该匹配 "测试电脑"）
        print(f"\n用户输入 (选择设备): 测试")
        result_type, result_msg = engine.process_message(test_session_id, "测试")
        print(f"引擎回复 [{result_type.value}]: {result_msg}")
        
        if result_type == WorkflowResult.CONTINUE:
            # 第二步：确认删除
            print(f"\n用户输入 (确认): yes")
            result_type, result_msg = engine.process_message(test_session_id, "yes")
            print(f"引擎回复 [{result_type.value}]: {result_msg}")
        
        print("\n测试完成")
    
    elif cmd == 'test-remove-cancel':
        print("测试删除设备工作流（取消）")
        print("-" * 50)
        
        test_session_id = "cli_test_session_cancel"
        result = engine.start_workflow(test_session_id, "wol_remove_device")
        print(f"引擎：{result}")
        
        # 第一步：选择设备
        print(f"\n用户输入 (选择设备): 测试电脑")
        result_type, result_msg = engine.process_message(test_session_id, "测试电脑")
        print(f"引擎回复 [{result_type.value}]: {result_msg}")
        
        if result_type == WorkflowResult.CONTINUE:
            # 第二步：取消删除
            print(f"\n用户输入 (取消): q")
            result_type, result_msg = engine.process_message(test_session_id, "q")
            print(f"引擎回复 [{result_type.value}]: {result_msg}")
        
        print("\n测试完成")
    
    elif cmd == 'interactive-add':
        print("交互式添加设备测试")
        print("-" * 50)
        print("输入 q 随时退出\n")
        
        result = engine.start_workflow(test_session, "wol_add_device")
        print(f"引擎：{result}")
        
        while True:
            try:
                user_input = input("\n你：").strip()
                if not user_input:
                    continue
                
                result_type, result_msg = engine.process_message(test_session, user_input)
                print(f"引擎 [{result_type.value}]: {result_msg}")
                
                if result_type in [WorkflowResult.COMPLETE, WorkflowResult.EXIT]:
                    break
            except (KeyboardInterrupt, EOFError):
                print("\n已退出")
                engine.state_manager.clear_session(test_session)
                break
    
    elif cmd == 'list-sessions':
        sessions = engine.list_active_sessions()
        if not sessions:
            print("暂无活跃会话")
        else:
            print(f"活跃会话数：{len(sessions)}")
            for s in sessions:
                print(f"  - {s['session_id']}: {s['workflow_type']} (步骤 {s['current_step']})")
    
    elif cmd == 'session-info' and len(sys.argv) >= 3:
        session_id = sys.argv[2]
        info = engine.get_session_status(session_id)
        if info:
            import json
            print(json.dumps(info, ensure_ascii=False, indent=2))
        else:
            print(f"未找到会话：{session_id}")
    
    elif cmd == 'check-timeouts':
        timed_out = engine.check_timeouts()
        if timed_out:
            print(f"超时会话：{', '.join(timed_out)}")
        else:
            print("无超时会话")
    
    else:
        print(f"未知命令：{cmd}")
        sys.exit(1)


if __name__ == '__main__':
    main()
