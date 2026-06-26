#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全凭证管理器
用于安全地获取和管理微信公众账号凭证
"""

import os
import json
import re
from pathlib import Path
from typing import Optional, Tuple, Dict

class CredentialManager:
    """安全的凭证管理器"""

    def __init__(self, config_dir: str = None):
        """
        初始化凭证管理器

        Args:
            config_dir: 配置文件目录，默认为脚本所在目录的 references/
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path(__file__).parent.parent / "references"

        # 尝试加载环境变量
        try:
            from dotenv import load_dotenv
            # 加载 .env 文件
            env_file = Path(__file__).parent.parent / ".env"
            if env_file.exists():
                load_dotenv(env_file)
        except ImportError:
            # python-dotenv 未安装，跳过
            pass

    def get_credentials(self, account_id: str = None) -> Tuple[Optional[str], Optional[str]]:
        """
        安全获取凭证

        优先级：
        1. 环境变量
        2. 配置文件

        Args:
            account_id: 账号ID，如 'account_1'

        Returns:
            (app_id, app_secret) 元组
        """
        # 方法1：从环境变量获取
        if account_id:
            # 提取账号编号，如 'account_1' -> '1'
            account_num = account_id.split('_')[-1] if '_' in account_id else '1'

            app_id = os.getenv(f'WECHAT_APP_ID_{account_num}')
            app_secret = os.getenv(f'WECHAT_APP_SECRET_{account_num}')

            if app_id and app_secret:
                return app_id, app_secret

        # 方法2：从配置文件获取
        return self._load_from_config(account_id)

    def _load_from_config(self, account_id: str = None) -> Tuple[Optional[str], Optional[str]]:
        """从配置文件加载凭证"""
        # 尝试多个可能的配置文件名
        config_files = [
            'my_accounts.json',
            'config.json',
            'multi_account_config.json',
            'config.template.json'
        ]

        for config_file in config_files:
            config_path = self.config_dir / config_file
            if not config_path.exists():
                continue

            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                # 获取账号列表
                accounts = config.get('accounts', [])
                if not accounts:
                    continue

                # 如果指定了账号ID，查找对应账号
                if account_id:
                    for account in accounts:
                        if account.get('id') == account_id:
                            return account.get('app_id'), account.get('app_secret')
                else:
                    # 未指定账号ID，返回第一个账号
                    current_id = config.get('current_account', 'account_1')
                    for account in accounts:
                        if account.get('id') == current_id:
                            return account.get('app_id'), account.get('app_secret')

            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️ 读取配置文件失败: {e}")
                continue

        return None, None

    def validate_credentials(self, app_id: str, app_secret: str) -> bool:
        """
        验证凭证格式

        Args:
            app_id: 微信AppID
            app_secret: 微信AppSecret

        Returns:
            是否有效
        """
        # AppID 格式：wx + 16位字符
        if not re.match(r'^wx[a-z0-9]{16}$', app_id or ''):
            return False

        # AppSecret 格式：32位字符
        if not re.match(r'^[a-f0-9]{32}$', app_secret or ''):
            return False

        return True

    def get_account_info(self, account_id: str = None) -> Optional[Dict]:
        """
        获取账号完整信息

        Args:
            account_id: 账号ID

        Returns:
            账号信息字典
        """
        config_files = [
            'my_accounts.json',
            'config.json',
            'multi_account_config.json'
        ]

        for config_file in config_files:
            config_path = self.config_dir / config_file
            if not config_path.exists():
                continue

            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                accounts = config.get('accounts', [])
                if not accounts:
                    continue

                # 如果指定了账号ID
                if account_id:
                    for account in accounts:
                        if account.get('id') == account_id:
                            return account
                else:
                    # 返回当前激活的账号
                    current_id = config.get('current_account', 'account_1')
                    for account in accounts:
                        if account.get('id') == current_id:
                            return account

            except (json.JSONDecodeError, IOError):
                continue

        return None


def sanitize_error_message(error_msg: str) -> str:
    """
    脱敏错误信息

    Args:
        error_msg: 原始错误信息

    Returns:
        脱敏后的错误信息
    """
    if not isinstance(error_msg, str):
        error_msg = str(error_msg)

    # 移除可能的AppID (格式：wx + 16位字符)
    error_msg = re.sub(r'wx[a-z0-9]{16}', 'wx****', error_msg)

    # 移除可能的AppSecret (格式：32位十六进制)
    error_msg = re.sub(r'[a-f0-9]{32}', '****', error_msg)

    # 移除IP地址
    error_msg = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '***.***.***.***', error_msg)

    # 移除可能的access_token
    error_msg = re.sub(r'[0-9]{2,3}_[a-zA-Z0-9_-]{20,}', 'ACCESS_TOKEN****', error_msg)

    return error_msg


def safe_print_error(error: Exception, operation: str = "操作"):
    """
    安全地打印错误信息

    Args:
        error: 异常对象
        operation: 操作名称
    """
    error_msg = str(error)
    safe_msg = sanitize_error_message(error_msg)
    print(f"❌ {operation}失败: {safe_msg}")


# 使用示例
if __name__ == "__main__":
    # 创建凭证管理器
    cred_manager = CredentialManager()

    # 获取凭证
    app_id, app_secret = cred_manager.get_credentials('account_1')

    if app_id and app_secret:
        # 验证凭证格式
        if cred_manager.validate_credentials(app_id, app_secret):
            print("✅ 凭证格式正确")
            print(f"AppID: {app_id[:10]}****")
        else:
            print("❌ 凭证格式错误")
    else:
        print("⚠️ 未找到凭证，请检查配置")

    # 测试错误脱敏
    test_error = "获取token失败: appid=wx94029d52b0b25543, ip=45.58.187.66"
    safe_error = sanitize_error_message(test_error)
    print(f"\n原始错误: {test_error}")
    print(f"脱敏后: {safe_error}")
