# -*- coding: utf-8 -*-
"""
skill_fix_workflow - 工作流固化技能 V3.0

主入口：用户主动触发固化 → 拼接器读取对话 → 生成可运行程序
"""

import os
import sys
from typing import List, Dict, Any, Optional

# 添加技能目录到路径
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)

from joiner import WorkflowJoiner, join_workflow


# ==================== 技能主入口 ====================

def skill_fix_workflow(user_command: str, conversation: List[Dict[str, str]],
                       current_topic: str = None) -> Dict[str, Any]:
    """
    固化技能核心入口
    
    Args:
        user_command: 用户指令，如"固化当前主题的工作流"
        conversation: 当前对话历史
        current_topic: 当前主题名称
        
    Returns:
        固化结果
    """
    # 1. 提取主题名称
    topic = _extract_topic(user_command, current_topic)
    
    if not topic:
        return {
            "status": "error",
            "message": "无法确定主题，请使用：固化「XXX」的工作流"
        }
    
    # 2. 询问输出方式（如果指令中未指定）
    output_config = _parse_output_config(user_command)
    
    if not output_config.get("confirmed"):
        # 需要用户确认输出方式
        return {
            "status": "need_confirmation",
            "topic": topic,
            "prompt": f"""
已识别主题：「{topic}」

请选择输出方式：
A) 屏幕输出 - 直接显示结果
B) 文件输出 - 保存到文件（请指定路径）
C) API 输出 - 发送到 API（请提供 URL）
D) 网页输出 - 生成 HTML 页面

或直接告诉我定时规则，如：每天 9 点执行
""",
            "conversation": conversation
        }
    
    # 3. 拼接工作流
    result = join_workflow(
        conversation=conversation,
        task_name=topic,
        output_type=output_config.get("type", "screen"),
        output_path=output_config.get("path"),
        api_url=output_config.get("api_url")
    )
    
    if result["status"] == "success":
        return {
            "status": "success",
            "message": f"""
✅ 已成功固化「{topic}」主题工作流！

━━━━━━━━━━━━━━━━━━━━━━
📋 固化信息
━━━━━━━━━━━━━━━━━━━━━━
• 主题名称：{topic}
• 输出方式：{output_config.get("type", "screen")}
• 程序路径：{result["program_path"]}
• 识别参数：{len([k for k in result["params"].keys() if not k.startswith("_")])} 个
• 执行步骤：{len(result["execution_chain"])} 步

━━━━━━━━━━━━━━━━━━━━━━
📝 下一步
━━━━━━━━━━━━━━━━━━━━━━
1. 查看生成的程序：打开 {result["program_path"]}
2. 实现 Skill/Tool 函数：编辑文件中的占位函数
3. 测试运行：python {result["program_path"]}

━━━━━━━━━━━━━━━━━━━━━━
⚠️ 注意事项
━━━━━━━━━━━━━━━━━━━━━━
• 首次运行前需实现 Skill/Tool 函数
• 确保参数配置正确
• 查看日志：./task_logs/{topic}*.log
""",
            "program_path": result["program_path"],
            "code": result["code"],
            "params": result["params"]
        }
    else:
        return {
            "status": "error",
            "message": result.get("message", "固化失败")
        }


def _extract_topic(command: str, current_topic: str = None) -> Optional[str]:
    """从指令中提取主题"""
    import re
    
    # 匹配「XXX」或"XXX"
    match = re.search(r'[「"](.+?)[」"]', command)
    if match:
        topic = match.group(1).strip()
        # 去除后缀
        topic = re.sub(r'(主题 | 的工作流 | 流程)$', '', topic)
        return topic
    
    # 当前主题
    if "当前" in command and current_topic:
        return current_topic
    
    # 尝试从命令中提取第一个名词短语
    if "固化" in command:
        # 简单处理：取"固化"后的内容
        parts = command.split("固化")
        if len(parts) > 1:
            topic = parts[1].strip()
            topic = re.sub(r'(主题 | 的工作流 | 流程 |，|,|。).*', '', topic)
            if topic and len(topic) > 0:
                return topic
    
    return None


def _parse_output_config(command: str) -> Dict[str, Any]:
    """解析输出配置"""
    config = {"confirmed": False, "type": "screen"}
    
    # 检查是否指定输出方式
    if "屏幕" in command or "screen" in command.lower():
        config["confirmed"] = True
        config["type"] = "screen"
    elif "文件" in command or "file" in command.lower():
        config["confirmed"] = True
        config["type"] = "file"
        # 提取路径
        import re
        match = re.search(r'文件 [到至]\s*["\']?([^\s"\']+)["\']?', command)
        if match:
            config["path"] = match.group(1)
    elif "API" in command or "api" in command.lower():
        config["confirmed"] = True
        config["type"] = "api"
        # 提取 URL
        import re
        match = re.search(r'https?://[^\s]+', command)
        if match:
            config["api_url"] = match.group(0)
    elif "网页" in command or "web" in command.lower():
        config["confirmed"] = True
        config["type"] = "web"
    
    # 检查定时规则（暂不处理，留给 cron）
    if any(kw in command for kw in ["每天", "每小时", "每周", "定时"]):
        config["has_schedule"] = True
    
    return config


def confirm_workflow(topic: str, conversation: List[Dict[str, str]],
                     output_type: str, output_path: str = None,
                     api_url: str = None) -> Dict[str, Any]:
    """
    确认并固化工作流（用户选择输出方式后调用）
    
    Args:
        topic: 主题名称
        conversation: 对话历史
        output_type: 输出方式
        output_path: 输出路径（文件类型需要）
        api_url: API URL（API 类型需要）
        
    Returns:
        固化结果
    """
    return skill_fix_workflow(
        user_command=f"固化「{topic}」的工作流，{output_type}输出",
        conversation=conversation,
        current_topic=topic
    )


# ==================== 测试入口 ====================

if __name__ == "__main__":
    # 测试对话
    test_conversation = [
        {"role": "user", "content": "帮我监控 Kickstarter 的 AI 分类项目"},
        {"role": "assistant", "content": "已调用 skill_fetch_data(url='https://kickstarter.com/ai')"},
        {"role": "user", "content": "提取项目名称和金额，limit=20"},
        {"role": "assistant", "content": "已调用 tool_parse(data, limit=20)"},
        {"role": "user", "content": "保存到 projects.json"},
        {"role": "assistant", "content": "已调用 tool_file_save(result, path='projects.json')"}
    ]
    
    print("="*60)
    print("skill_fix_workflow V3.0 测试")
    print("="*60)
    
    # 测试固化
    result = skill_fix_workflow(
        user_command="固化「Kickstarter 监控」的工作流，文件输出到 projects.json",
        conversation=test_conversation,
        current_topic="Kickstarter 监控"
    )
    
    print(f"\n状态：{result['status']}")
    print(f"\n消息：{result.get('message', 'N/A')}")
    
    if result["status"] == "success":
        print(f"\n程序已保存：{result['program_path']}")
        print(f"\n识别的参数:")
        for key, value in result.get("params", {}).items():
            if not key.startswith("_"):
                print(f"  {key}: {value}")
