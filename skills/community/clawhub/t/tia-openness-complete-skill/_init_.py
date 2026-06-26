"""
OpenClaw技能：TIA Openness 完整自动化技能
支持项目创建、硬件配置、SCL编程、编译下载完整流程
"""

import logging
from typing import Dict, Any
from .actions import (
    get_tia, close_tia,
    action_create_project,
    action_add_plc,
    action_create_block,
    action_compile_software,
    action_download,
    action_save_project,
    action_close_project,
    action_full_automation
)

logger = logging.getLogger(__name__)

def run(action: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    OpenClaw标准入口函数
    :param action: 操作名称
    :param params: 参数字典
    :return: 结果字典
    """
    try:
        # 路由操作
        if action == "create_project":
            return action_create_project(params)
        elif action == "add_plc":
            return action_add_plc(params)
        elif action == "create_block":
            return action_create_block(params)
        elif action == "compile_software":
            return action_compile_software(params)
        elif action == "download":
            return action_download(params)
        elif action == "save_project":
            return action_save_project(params)
        elif action == "close_project":
            return action_close_project(params)
        elif action == "full_automation":
            return action_full_automation(params)
        else:
            return {"success": False, "message": f"未知操作: {action}"}
    except Exception as e:
        logger.exception("技能执行异常")
        return {"success": False, "message": f"执行异常: {str(e)}"}
    finally:
        if params.get("close_after", False):
            close_tia()