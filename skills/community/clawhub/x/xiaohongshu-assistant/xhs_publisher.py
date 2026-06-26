#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📕 小红书发布模块 - 基于 CDP
功能：自动发布、图片上传、标签填入
基于 XiaohongshuSkills 项目
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime

# XiaohongshuSkills 路径
XHS_SKILLS_DIR = Path(__file__).parent.parent.parent / "XiaohongshuSkills"
PUBLISH_SCRIPT = XHS_SKILLS_DIR / "scripts" / "publish_pipeline.py"
LOGIN_SCRIPT = XHS_SKILLS_DIR / "scripts" / "cdp_publish.py"

# 账号配置文件
ACCOUNTS_FILE = Path(__file__).parent / "xhs_accounts.json"


def check_xhs_skills():
    """检查 XiaohongshuSkills 是否可用"""
    if not XHS_SKILLS_DIR.exists():
        return False, "XiaohongshuSkills 仓库不存在"
    
    if not PUBLISH_SCRIPT.exists():
        return False, "发布脚本不存在"
    
    return True, "就绪"


def check_login(account="default"):
    """
    检查登录状态
    
    Args:
        account: 账号名称
        
    Returns:
        dict: 登录状态信息
    """
    cmd = [
        "python", str(LOGIN_SCRIPT),
        "check-login",
        "--account", account
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return {"logged_in": True, "account": account}
        else:
            return {"logged_in": False, "error": result.stderr}
    except Exception as e:
        return {"logged_in": False, "error": str(e)}


def login(account="default"):
    """
    登录小红书账号
    
    Args:
        account: 账号名称
        
    Returns:
        dict: 登录结果
    """
    cmd = [
        "python", str(LOGIN_SCRIPT),
        "login",
        "--account", account
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return {"success": True, "message": "登录成功"}
        else:
            return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}


def publish(title, content, images=None, account="default", preview=False):
    """
    发布笔记到小红书
    
    Args:
        title: 标题
        content: 正文内容
        images: 图片列表（本地路径或 URL）
        account: 账号名称
        preview: 预览模式（不实际发布）
        
    Returns:
        dict: 发布结果
    """
    # 检查 XiaohongshuSkills
    ok, msg = check_xhs_skills()
    if not ok:
        return {"success": False, "error": msg}
    
    # 构建命令
    cmd = [
        "python", str(PUBLISH_SCRIPT),
        "--account", account,
        "--title", title,
        "--content", content,
    ]
    
    # 预览模式
    if preview:
        cmd.append("--preview")
    else:
        cmd.append("--headless")
    
    # 添加图片
    if images:
        for img in images:
            # 判断是 URL 还是本地路径
            if img.startswith("http"):
                cmd.extend(["--image-urls", img])
            else:
                cmd.extend(["--images", img])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            return {
                "success": True,
                "message": "发布成功",
                "title": title,
                "preview": preview
            }
        else:
            return {
                "success": False,
                "error": result.stderr,
                "output": result.stdout
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_accounts():
    """
    列出所有账号
    
    Returns:
        list: 账号列表
    """
    cmd = [
        "python", str(LOGIN_SCRIPT),
        "list-accounts"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            # 解析输出
            accounts = []
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    accounts.append(line.strip())
            return accounts
        else:
            return []
    except Exception as e:
        return []


def add_account(name, alias=None):
    """
    添加新账号
    
    Args:
        name: 账号名称
        alias: 账号别名
        
    Returns:
        dict: 添加结果
    """
    cmd = [
        "python", str(LOGIN_SCRIPT),
        "add-account", name
    ]
    
    if alias:
        cmd.extend(["--alias", alias])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return {"success": True, "message": "账号添加成功"}
        else:
            return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_feed_detail(feed_id, xsec_token):
    """
    获取笔记详情
    
    Args:
        feed_id: 笔记 ID
        xsec_token: 安全令牌
        
    Returns:
        dict: 笔记详情
    """
    cmd = [
        "python", str(LOGIN_SCRIPT),
        "get-feed-detail",
        "--feed-id", feed_id,
        "--xsec-token", xsec_token
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}


def post_comment(feed_id, xsec_token, content):
    """
    发表评论
    
    Args:
        feed_id: 笔记 ID
        xsec_token: 安全令牌
        content: 评论内容
        
    Returns:
        dict: 评论结果
    """
    cmd = [
        "python", str(LOGIN_SCRIPT),
        "post-comment-to-feed",
        "--feed-id", feed_id,
        "--xsec-token", xsec_token,
        "--content", content
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return {"success": True, "message": "评论成功"}
        else:
            return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}


def note_action(feed_id, xsec_token, action):
    """
    笔记互动（点赞/收藏）
    
    Args:
        feed_id: 笔记 ID
        xsec_token: 安全令牌
        action: 动作 (upvote/unvote/bookmark/unbookmark)
        
    Returns:
        dict: 操作结果
    """
    cmd = [
        "python", str(LOGIN_SCRIPT),
        f"note-{action}",
        "--feed-id", feed_id,
        "--xsec-token", xsec_token
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return {"success": True, "message": f"{action} 成功"}
        else:
            return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}


# 测试
if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("📕 小红书发布模块 - 测试")
    print("=" * 60)
    
    # 检查
    ok, msg = check_xhs_skills()
    print(f"\n检查：{msg}")
    
    # 登录状态
    if ok:
        status = check_login()
        print(f"登录状态：{status}")
