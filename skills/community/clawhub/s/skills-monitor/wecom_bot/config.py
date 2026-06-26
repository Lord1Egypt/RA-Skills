#!/usr/bin/env python3
"""
企业微信双向通信 - 配置文件
============================
所有敏感信息集中在此管理。首次使用请填写以下配置。

配置获取方式：
  1. 登录企业微信管理后台: https://work.weixin.qq.com
  2. 我的企业 → 企业ID (CORP_ID)
  3. 应用管理 → 自建 → 创建应用 → 获取 AGENT_ID 和 SECRET
  4. 应用管理 → 自建应用 → 接收消息 → 设置API接收 → 获取 TOKEN 和 ENCODING_AES_KEY
"""

import os
from pathlib import Path

# ============================================================
# 企业微信配置（必填）
# ============================================================

# 企业ID：我的企业 → 企业信息 → 企业ID
CORP_ID = os.environ.get("WECOM_CORP_ID", "YOUR_CORP_ID_HERE")

# 自建应用 AgentId
AGENT_ID = int(os.environ.get("WECOM_AGENT_ID", "0"))

# 自建应用 Secret
SECRET = os.environ.get("WECOM_SECRET", "YOUR_SECRET_HERE")

# 接收消息 → API接收 → Token（自定义，32位以内英文数字）
CALLBACK_TOKEN = os.environ.get("WECOM_CALLBACK_TOKEN", "YOUR_CALLBACK_TOKEN_HERE")

# 接收消息 → API接收 → EncodingAESKey（43位字符）
CALLBACK_ENCODING_AES_KEY = os.environ.get("WECOM_CALLBACK_AES_KEY", "YOUR_ENCODING_AES_KEY_HERE")

# ============================================================
# 群机器人 Webhook（已有，用于推送报告）
# ============================================================
WEBHOOK_URL = (
    "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"
    "?key=5881dfcd-f771-4756-9b7d-883e0271e212"
)

# ============================================================
# 服务配置
# ============================================================

# Flask 服务端口
SERVER_PORT = int(os.environ.get("WECOM_SERVER_PORT", "5088"))

# 项目根目录
PROJECT_DIR = Path(__file__).resolve().parent.parent

# 日志目录
LOG_DIR = PROJECT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# 报告目录
REPORT_DIR = PROJECT_DIR / "reports"
DATA_DIR = PROJECT_DIR / "report_data"

# ============================================================
# 指令白名单（只有这些用户可以下达指令）
# 留空表示允许所有人
# ============================================================
ALLOWED_USERS = os.environ.get("WECOM_ALLOWED_USERS", "").split(",")
ALLOWED_USERS = [u.strip() for u in ALLOWED_USERS if u.strip()]

# ============================================================
# ngrok 配置
# ============================================================
NGROK_AUTH_TOKEN = os.environ.get("NGROK_AUTH_TOKEN", "")


def validate_config():
    """验证配置是否完整"""
    errors = []
    if CORP_ID == "YOUR_CORP_ID_HERE" or not CORP_ID:
        errors.append("❌ CORP_ID 未配置")
    if AGENT_ID == 0:
        errors.append("❌ AGENT_ID 未配置")
    if SECRET == "YOUR_SECRET_HERE" or not SECRET:
        errors.append("❌ SECRET 未配置")
    if CALLBACK_TOKEN == "YOUR_CALLBACK_TOKEN_HERE" or not CALLBACK_TOKEN:
        errors.append("❌ CALLBACK_TOKEN 未配置")
    if CALLBACK_ENCODING_AES_KEY == "YOUR_ENCODING_AES_KEY_HERE" or not CALLBACK_ENCODING_AES_KEY:
        errors.append("❌ CALLBACK_ENCODING_AES_KEY 未配置")
    return errors


def print_config_status():
    """打印配置状态"""
    errors = validate_config()
    if errors:
        print("⚠️  企业微信配置不完整：")
        for e in errors:
            print(f"   {e}")
        print("\n请编辑 wecom_bot/config.py 或设置环境变量：")
        print("   export WECOM_CORP_ID='your_corp_id'")
        print("   export WECOM_AGENT_ID='your_agent_id'")
        print("   export WECOM_SECRET='your_secret'")
        print("   export WECOM_CALLBACK_TOKEN='your_token'")
        print("   export WECOM_CALLBACK_AES_KEY='your_aes_key'")
        return False
    else:
        print("✅ 企业微信配置完整")
        print(f"   企业ID: {CORP_ID[:6]}****")
        print(f"   应用ID: {AGENT_ID}")
        print(f"   服务端口: {SERVER_PORT}")
        return True
