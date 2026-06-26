#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
凭证加密工具
用于加密和解密微信公众号凭证
"""

import sys
import os
import io
import argparse
import getpass

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wechat.encryption import CredentialManager, EncryptionManager


def encrypt_credentials(app_id: str, app_secret: str, config_file: str, password: str = None):
    """
    加密凭证并保存到配置文件
    
    Args:
        app_id: App ID
        app_secret: App Secret
        config_file: 配置文件路径
        password: 可选的密码
    """
    try:
        manager = CredentialManager(config_file)
        manager.save_encrypted_config(app_id, app_secret, password=password)
        
        print("✅ 凭证加密成功！")
        print(f"📁 配置文件: {config_file}")
        print(f"🔑 密钥文件: .secret_key")
        print("\n⚠️  重要提示:")
        print("  1. 请妥善保管 .secret_key 文件，不要提交到版本控制")
        print("  2. 如果使用密码，请牢记密码，丢失将无法恢复")
        print("  3. 建议将 .secret_key 添加到 .gitignore")
        
    except Exception as e:
        print(f"❌ 加密失败: {str(e)}")
        sys.exit(1)


def decrypt_credentials(config_file: str, password: str = None):
    """
    解密并显示凭证
    
    Args:
        config_file: 配置文件路径
        password: 可选的密码
    """
    try:
        manager = CredentialManager(config_file)
        
        # 检查是否加密
        if not manager.is_encrypted():
            print("ℹ️  配置文件未加密")
            return
        
        # 解密凭证
        creds = manager.load_config(password)
        
        print("✅ 凭证解密成功！")
        print(f"App ID: {creds['app_id']}")
        print(f"App Secret: {creds['app_secret'][:8]}...{creds['app_secret'][-8:]}")
        
    except Exception as e:
        print(f"❌ 解密失败: {str(e)}")
        print("提示: 如果使用了密码，请确保输入正确的密码")
        sys.exit(1)


def check_encryption_status(config_file: str):
    """
    检查配置文件的加密状态
    
    Args:
        config_file: 配置文件路径
    """
    try:
        manager = CredentialManager(config_file)
        
        if manager.is_encrypted():
            print("🔒 配置文件已加密")
            print(f"📁 配置文件: {config_file}")
            print(f"🔑 密钥文件: .secret_key")
        else:
            print("🔓 配置文件未加密")
            print(f"📁 配置文件: {config_file}")
            print("\n建议: 使用 'python encrypt_credentials.py encrypt' 加密凭证")
        
    except FileNotFoundError:
        print(f"❌ 配置文件不存在: {config_file}")
    except Exception as e:
        print(f"❌ 检查失败: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description="微信公众号凭证加密工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 加密凭证（交互式输入）
  python encrypt_credentials.py encrypt
  
  # 加密凭证（命令行参数）
  python encrypt_credentials.py encrypt --app-id "wx123456" --app-secret "abc123"
  
  # 解密并查看凭证
  python encrypt_credentials.py decrypt
  
  # 检查加密状态
  python encrypt_credentials.py status
  
  # 使用密码加密（更安全）
  python encrypt_credentials.py encrypt --use-password
        """
    )
    
    parser.add_argument(
        "command",
        choices=["encrypt", "decrypt", "status"],
        help="操作命令: encrypt(加密), decrypt(解密), status(状态)"
    )
    
    parser.add_argument(
        "--config",
        default="config.json",
        help="配置文件路径 (默认: config.json)"
    )
    
    parser.add_argument(
        "--app-id",
        help="App ID (可选，不提供则交互式输入)"
    )
    
    parser.add_argument(
        "--app-secret",
        help="App Secret (可选，不提供则交互式输入)"
    )
    
    parser.add_argument(
        "--password",
        help="加密密码 (可选，不提供则交互式输入)"
    )
    
    parser.add_argument(
        "--use-password",
        action="store_true",
        help="使用密码加密（更安全）"
    )
    
    args = parser.parse_args()
    
    # 执行命令
    if args.command == "encrypt":
        # 获取 App ID
        app_id = args.app_id
        if not app_id:
            app_id = input("请输入 App ID: ").strip()
        
        # 获取 App Secret
        app_secret = args.app_secret
        if not app_secret:
            app_secret = getpass.getpass("请输入 App Secret: ").strip()
        
        # 获取密码（可选）
        password = None
        if args.use_password or args.password:
            password = args.password
            if not password:
                password = getpass.getpass("请输入加密密码（用于额外保护）: ").strip()
                password_confirm = getpass.getpass("请再次输入密码确认: ").strip()
                if password != password_confirm:
                    print("❌ 两次密码输入不一致")
                    sys.exit(1)
        
        encrypt_credentials(app_id, app_secret, args.config, password)
    
    elif args.command == "decrypt":
        # 获取密码（可选）
        password = args.password
        if not password:
            # 尝试无密码解密
            try:
                manager = CredentialManager(args.config)
                if manager.is_encrypted():
                    # 检查是否需要密码
                    try:
                        manager.load_config(None)
                    except:
                        password = getpass.getpass("请输入解密密码: ").strip()
            except:
                pass
        
        decrypt_credentials(args.config, password)
    
    elif args.command == "status":
        check_encryption_status(args.config)


if __name__ == "__main__":
    main()
