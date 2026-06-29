#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云启智联AI服务 API KEY 配置管理工具
支持加密存储和读取，基于机器特征绑定加密密钥
"""
import argparse
import base64
import getpass
import hashlib
import os
import platform
import sys

try:
    from cryptography.fernet import Fernet
except ImportError:
    print("错误：缺少 cryptography 库。请运行: pip install cryptography")
    sys.exit(1)

# 配置文件路径（使用通用目录，兼容 QoderWork / QClaw 等不同工具）
CONFIG_DIR = os.path.join(os.path.expanduser("~"), "yqzl-ai-service")
CONFIG_FILE = os.path.join(CONFIG_DIR, ".api_key.enc")

# 兼容旧版本：自动迁移 .qoderwork 路径下的配置
_LEGACY_CONFIG = os.path.join(os.path.expanduser("~"), ".qoderwork", "skills", "yqzl-ai-service", ".api_key.enc")
if not os.path.exists(CONFIG_FILE) and os.path.exists(_LEGACY_CONFIG):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    import shutil
    shutil.copy2(_LEGACY_CONFIG, CONFIG_FILE)


def _derive_key():
    """基于机器特征派生加密密钥，确保不同机器加密结果不同"""
    machine_id = f"{platform.node()}:{getpass.getuser()}:yqzl-ai-salt-v1"
    key = hashlib.sha256(machine_id.encode("utf-8")).digest()
    # Fernet 需要 32 字节并经过 base64url 编码的密钥
    return base64.urlsafe_b64encode(key)


def save_api_key(api_key):
    """加密并保存 API KEY"""
    f = Fernet(_derive_key())
    encrypted = f.encrypt(api_key.encode("utf-8"))
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "wb") as fp:
        fp.write(encrypted)
    # 设置文件权限为仅当前用户可读写（Windows 下效果有限，但仍设置）
    try:
        os.chmod(CONFIG_FILE, 0o600)
    except Exception:
        pass
    print("API KEY 已成功加密保存。")
    print(f"存储位置: {CONFIG_FILE}")


def get_api_key():
    """读取并解密 API KEY"""
    if not os.path.exists(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, "rb") as fp:
            encrypted = fp.read()
        f = Fernet(_derive_key())
        return f.decrypt(encrypted).decode("utf-8")
    except Exception:
        return None


def check_config():
    """检查是否已配置 API KEY"""
    key = get_api_key()
    if key:
        length = len(key)
        if length > 12:
            masked = key[:4] + "*" * (length - 8) + key[-4:]
        elif length > 4:
            masked = key[:2] + "*" * (length - 4) + key[-2:]
        else:
            masked = "****"
        print(f"已配置 API KEY: {masked}")
        print(f"存储位置: {CONFIG_FILE}")
        return True
    else:
        print("未配置 API KEY。")
        print("请访问 http://8.135.62.13:5000/ 获取 API KEY 后，运行以下命令配置：")
        print('  python scripts/config_manager.py set "你的API_KEY"')
        return False


def main():
    parser = argparse.ArgumentParser(
        description="云启智联AI服务 API KEY 配置管理"
    )
    subparsers = parser.add_subparsers(dest="command")

    set_parser = subparsers.add_parser("set", help="设置并加密保存 API KEY")
    set_parser.add_argument("api_key", help="从官网获取的 API KEY")

    subparsers.add_parser("check", help="检查是否已配置 API KEY")

    # 集成升级命令
    upgrade_parser = subparsers.add_parser("upgrade", help="检查并升级技能到最新版本")
    upgrade_parser.add_argument("--force", action="store_true", help="强制升级")
    upgrade_parser.add_argument("--url", help="自定义升级源地址")

    args = parser.parse_args()

    if args.command == "set":
        save_api_key(args.api_key)
    elif args.command == "check":
        check_config()
    elif args.command == "upgrade":
        # 延迟导入 updater，避免循环依赖
        try:
            import updater
        except ImportError:
            # Python 3 相对导入兼容性处理
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import updater
        updater.do_update(args.url, force=args.force)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
