#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试微信 API

注意：此文件包含敏感信息，请勿上传到公共仓库！
使用前请修改 APPID 和 APPSECRET 为您的测试号配置。
"""

import requests
import json

# ========== 敏感配置区域 ==========
# ⚠️ 请勿将此文件提交到 Git！
# ⚠️ 实际使用时，请从环境变量或安全的配置文件中读取
# ==================================

# 方式 1：直接从环境变量读取（推荐）
APPID = os.environ.get("WECHAT_APPID", "your-wechat-appid")
APPSECRET = os.environ.get("WECHAT_APPSECRET", "your-wechat-appsecret")

# 方式 2：使用测试号（仅用于开发测试）
# 1. 访问 https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login
# 2. 扫码登录获取测试号 AppID 和 AppSecret
# 3. 替换下方的占位符
# APPID = "your-test-appid"
# APPSECRET = "your-test-appsecret"

import os

def get_token():
    """获取 access_token"""
    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        "grant_type": "client_credential",
        "appid": APPID,
        "secret": APPSECRET
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    
    if "access_token" in data:
        print(f"✅ Token 获取成功")
        print(f"   Token: {data['access_token'][:20]}...")
        print(f"   有效期：{data.get('expires_in', 7200)}秒")
        return data['access_token']
    else:
        print(f"❌ Token 获取失败")
        print(f"   错误码：{data.get('errcode')}")
        print(f"   错误信息：{data.get('errmsg')}")
        return None

def get_api_debug(token):
    """获取 API 调试信息"""
    url = "https://api.weixin.qq.com/cgi-bin/get_api_quota"
    params = {"access_token": token}
    data = {"cgi_path": "/cgi-bin/draft/add"}
    resp = requests.post(url, params=params, json=data)
    result = resp.json()
    
    if "quota" in result:
        print(f"\n📊 API 调用额度")
        print(f"   剩余次数：{result['quota']}")
    else:
        print(f"\n❌ 查询失败：{result}")

def main():
    """主函数"""
    print("=" * 60)
    print("微信公众号 API 测试工具")
    print("=" * 60)
    print()
    
    # 检查配置
    if APPID == "your-wechat-appid" or APPSECRET == "your-wechat-appsecret":
        print("⚠️  警告：尚未配置 AppID 和 AppSecret")
        print()
        print("请按以下步骤配置：")
        print("1. 设置环境变量：")
        print("   export WECHAT_APPID='your-appid'")
        print("   export WECHAT_APPSECRET='your-appsecret'")
        print()
        print("2. 或者修改此文件，填入您的测试号配置")
        print()
        print("获取测试号：")
        print("  https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login")
        print()
        return 1
    
    # 获取 Token
    token = get_token()
    
    if token:
        # 获取 API 调试信息
        get_api_debug(token)
        print()
        print("=" * 60)
        print("✅ 测试完成")
        print("=" * 60)
        return 0
    else:
        print()
        print("=" * 60)
        print("❌ 测试失败，请检查配置")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    exit(main())
