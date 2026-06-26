#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布文章到微信公众号（安全增强版）
"""

import requests
import json
import os
from typing import Optional, Dict
from credential_manager import CredentialManager, safe_print_error

# 全局凭证管理器
cred_manager = CredentialManager()

def get_access_token(app_id: str = None, app_secret: str = None, account_id: str = None) -> Optional[str]:
    """
    获取微信 access_token

    Args:
        app_id: 微信AppID（可选，如未提供则从配置获取）
        app_secret: 微信AppSecret（可选，如未提供则从配置获取）
        account_id: 账号ID（可选）

    Returns:
        access_token 或 None
    """
    # 如果未提供凭证，从配置获取
    if not app_id or not app_secret:
        app_id, app_secret = cred_manager.get_credentials(account_id)

    if not app_id or not app_secret:
        print("❌ 未找到有效的凭证配置")
        return None

    # 验证凭证格式
    if not cred_manager.validate_credentials(app_id, app_secret):
        safe_print_error(ValueError("凭证格式无效"), "凭证验证")
        return None

    url = "https://api.weixin.qq.com/cgi-bin/token"
    params = {
        'grant_type': 'client_credential',
        'appid': app_id,
        'secret': app_secret
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if 'access_token' in data:
            # 不打印完整token，只显示前10个字符
            token_preview = data['access_token'][:10] + "****"
            print(f"✅ Access Token获取成功: {token_preview}")
            return data['access_token']
        else:
            error_msg = data.get('errmsg', '未知错误')
            safe_print_error(Exception(error_msg), "获取Access Token")
            return None

    except requests.exceptions.Timeout:
        safe_print_error(Exception("网络请求超时"), "API连接")
        return None
    except Exception as e:
        safe_print_error(e, "API请求")
        return None


def upload_cover_image(access_token: str, image_path: str) -> Optional[str]:
    """
    上传封面图到微信服务器

    Args:
        access_token: 访问令牌
        image_path: 图片路径

    Returns:
        media_id 或 None
    """
    if not os.path.exists(image_path):
        print(f"❌ 文件不存在: {image_path}")
        return None

    url = "https://api.weixin.qq.com/cgi-bin/material/add_material"
    params = {
        'access_token': access_token,
        'type': 'image'
    }

    try:
        with open(image_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, params=params, files=files, timeout=30)

        data = response.json()

        if 'media_id' in data:
            print("✅ 封面图上传成功")
            return data['media_id']
        else:
            error_msg = data.get('errmsg', '未知错误')
            safe_print_error(Exception(error_msg), "封面图上传")
            return None

    except Exception as e:
        safe_print_error(e, "上传封面图")
        return None


def publish_draft(access_token: str, article_data: Dict) -> Optional[str]:
    """
    发布文章到草稿箱

    Args:
        access_token: 访问令牌
        article_data: 文章数据

    Returns:
        media_id 或 None
    """
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"

    data = {
        "articles": [article_data]
    }

    try:
        # 使用 ensure_ascii=False 和 utf-8 编码，确保中文正确处理
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            url,
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            headers=headers,
            timeout=30
        )
        result = response.json()

        if 'media_id' in result:
            print("✅ 文章已发布到草稿箱")
            return result['media_id']
        else:
            error_msg = result.get('errmsg', '未知错误')
            safe_print_error(Exception(error_msg), "发布文章")
            return None

    except Exception as e:
        safe_print_error(e, "发布文章")
        return None


def test_connection(account_id: str = None) -> bool:
    """
    测试API连接

    Args:
        account_id: 账号ID（可选）

    Returns:
        是否连接成功
    """
    print("🔄 正在测试API连接...")

    # 获取凭证
    app_id, app_secret = cred_manager.get_credentials(account_id)

    if not app_id or not app_secret:
        print("❌ 未找到凭证配置")
        return False

    # 验证凭证格式
    if not cred_manager.validate_credentials(app_id, app_secret):
        print("❌ 凭证格式无效")
        return False

    # 获取access token
    token = get_access_token(app_id, app_secret)

    if token:
        print("✅ API连接测试成功")
        return True
    else:
        print("❌ API连接测试失败")
        return False


if __name__ == "__main__":
    print("发布脚本已加载（安全增强版）")
    print()
    print("使用方法:")
    print("  1. 配置凭证：复制 .env.example 为 .env 并填写真实信息")
    print("  2. 测试连接：python publish_to_wechat.py --test")
    print("  3. 发布文章：调用相关函数")
    print()

    # 测试命令行参数
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_connection()