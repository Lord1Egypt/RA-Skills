#!/usr/bin/env python3
"""
企业微信添加用户 - Skill 处理器

这个脚本被 OpenClaw Skill 调用，处理添加用户命令
"""

import sys
import os
import json

# 添加父目录到路径（add_user_mini.py 在父目录）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入自动激活功能
from auto_activate import check_and_activate

from add_user_mini import (
    parse_command,
    search_stores,
    generate_confirm_card,
    handle_callback,
    on_user_login,
    ROLE_DISPLAY
)


def check_permission(userid: str) -> tuple:
    """检查用户权限"""
    from permission_manager import get_permission_manager
    
    pm = get_permission_manager()
    
    if userid not in pm.users:
        return False, "❌ 您没有权限添加用户\n\n请联系管理员为您配置权限"
    
    user = pm.users[userid]
    allowed_types = ["headquarter", "region", "province"]
    
    if user.user_type.value not in allowed_types:
        return False, f"❌ 您的角色没有权限添加用户"
    
    return True, "OK"


def handle_message(text: str, from_userid: str):
    """处理消息"""
    # 检查权限
    has_perm, msg = check_permission(from_userid)
    if not has_perm:
        return {"type": "text", "content": msg}
    
    # 解析命令
    parsed = parse_command(text)
    
    if not parsed.get("userid"):
        return {
            "type": "text",
            "content": "❌ 命令格式错误\n\n请使用：添加用户 <UserID> <角色> <门店/地区>\n\n示例：添加用户 zhangsan 店长 正义路"
        }
    
    # 搜索门店
    if parsed.get("store_name"):
        stores = search_stores(parsed["store_name"])
        
        if not stores:
            return {
                "type": "text",
                "content": f"❌ 未找到匹配的门店：{parsed['store_name']}\n\n请检查门店名称，或输入关键词（如'正义路'）"
            }
        
        if len(stores) > 1:
            return {
                "type": "text",
                "content": f"⚠️ 找到 {len(stores)} 个匹配门店，请选择其中一个\n\n" + 
                "\n".join([f"{i+1}. {s['store_name']} ({s['province']}{s['city']})" for i, s in enumerate(stores[:5])]) +
                "\n\n请回复序号选择门店"
            }
        
        parsed["store_id"] = stores[0]["store_id"]
        parsed["store_name"] = stores[0]["store_name"]
    
    # 生成确认卡片
    card_data = {
        "userid": parsed["userid"],
        "role": parsed["role"],
        "role_display": parsed["role_display"],
        "store_name": parsed.get("store_name", ""),
        "store_id": parsed.get("store_id", ""),
    }
    
    card = generate_confirm_card(card_data)
    
    return {"type": "card", "content": card}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: handler.py <command> <args...>"}))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "handle_message":
        text = sys.argv[2]
        from_userid = sys.argv[3] if len(sys.argv) > 3 else "unknown"
        result = handle_message(text, from_userid)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))
        sys.exit(1)
