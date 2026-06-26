#!/usr/bin/env python3
"""
企业微信用户自动激活脚本

功能：
1. 检测用户是否需要激活
2. 自动更新用户名（从企业微信获取）
3. 发送欢迎消息

使用方式：
    python3 auto_activate.py check_and_activate "<userid>" "<wecom_name>"
"""

import sys
import os
import json
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from permission_manager import get_permission_manager
from add_user_mini import ROLE_DISPLAY


def check_and_activate(userid: str, wecom_name: str) -> tuple:
    """
    检查并激活用户
    
    Args:
        userid: 企业微信 UserID
        wecom_name: 从企业微信获取的姓名
    
    Returns:
        (activated: bool, message: str)
    """
    pm = get_permission_manager()
    
    # 检查用户是否存在
    if userid not in pm.users:
        return False, f"❌ 用户不存在：{userid}\n\n请联系管理员添加权限"
    
    user = pm.users[userid]
    
    # 检查是否已激活
    if not user.username.startswith("待激活_"):
        # 已激活用户，更新最后登录时间
        user.last_login = datetime.now().isoformat()
        pm._save_users()
        return False, f"欢迎回来，{user.username}！"
    
    # 激活用户
    old_username = user.username
    user.username = wecom_name
    user.last_login = datetime.now().isoformat()
    user.updated_at = datetime.now().isoformat()
    
    # 保存用户
    pm._save_users()
    
    # 获取用户信息
    role_display = ROLE_DISPLAY.get(user.user_type.value, user.user_type.value)
    store_count = len(user.store_ids) if user.store_ids else 0
    
    # 构建欢迎消息
    message = f"👋 欢迎使用红谷门店经营助手！\n\n"
    message += f"检测到您是首次使用，正在激活账户...\n"
    message += f"✅ 账户已激活\n\n"
    message += f"姓名：{wecom_name}\n"
    message += f"企业微信 ID: {userid}\n"
    message += f"角色：{role_display}\n"
    if store_count > 0:
        message += f"门店：{store_count} 家\n"
    if user.province:
        message += f"省份：{user.province}\n"
    if user.city:
        message += f"城市：{user.city}\n"
    if user.region:
        message += f"大区：{user.region}\n"
    message += f"\n现在可以开始使用了！"
    
    return True, message


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python3 auto_activate.py check_and_activate '<userid>' '<wecom_name>'")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check_and_activate":
        if len(sys.argv) < 4:
            print("❌ 缺少参数")
            print("使用方法：python3 auto_activate.py check_and_activate '<userid>' '<wecom_name>'")
            sys.exit(1)
        
        userid = sys.argv[2]
        wecom_name = sys.argv[3]
        
        activated, message = check_and_activate(userid, wecom_name)
        
        result = {
            "activated": activated,
            "message": message
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
