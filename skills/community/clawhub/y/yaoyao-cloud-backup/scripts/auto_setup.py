#!/usr/bin/env python3
"""
云服务快速安装向导
根据用户选择的推荐，自动安装配置对应的云服务

用法：
    python3 scripts/auto_setup.py --install 坚果云
    python3 scripts/auto_setup.py --install 阿里云OSS
"""

import argparse
import sys
import os
import webbrowser
from pathlib import Path


# ============================================================================
# 安装向导
# ============================================================================

class CloudInstaller:
    """云服务安装向导"""
    
    SERVICES = {
        "坚果云": {
            "name": "坚果云",
            "provider": "webdav",
            "url": "https://www.jianguoyun.com/",
            "features": ["国内可用", "WebDAV 支持", "免费额度"],
            "config_vars": {
                "WEBDAV_URL": "https://dav.jianguoyun.com/dav/",
                "WEBDAV_USERNAME": "你的坚果云邮箱",
                "WEBDAV_PASSWORD": "你的坚果云密码",
            },
            "install_hint": """
📋 坚果云配置步骤：

1. 访问 https://www.jianguoyun.com/ 注册/登录
2. 进入「账户信息」→「安全设置」→「第三方应用管理」
3. 创建「应用密码」
4. 复制以下配置到 secrets.env：

WEBDAV_URL=https://dav.jianguoyun.com/dav/
WEBDAV_USERNAME=你的坚果云邮箱
WEBDAV_PASSWORD=刚才创建的应用密码
""",
        },
        "Nextcloud": {
            "name": "Nextcloud",
            "provider": "webdav",
            "url": "https://nextcloud.com/",
            "features": ["开源私有云", "WebDAV 支持", "自托管"],
            "config_vars": {
                "WEBDAV_URL": "https://你的服务器/remote.php/dav/files/用户名/",
                "WEBDAV_USERNAME": "你的用户名",
                "WEBDAV_PASSWORD": "你的密码",
            },
            "install_hint": """
📋 Nextcloud 配置步骤：

1. 如果没有服务器，可以购买低配 VPS 安装
2. 安装后创建用户名密码
3. 复制以下配置到 secrets.env：

WEBDAV_URL=https://你的服务器/remote.php/dav/files/用户名/
WEBDAV_USERNAME=你的用户名
WEBDAV_PASSWORD=你的密码
""",
        },
        "阿里云OSS": {
            "name": "阿里云 OSS",
            "provider": "s3",
            "url": "https://www.aliyun.com/product/oss",
            "features": ["企业级存储", "低成本", "国内高速"],
            "config_vars": {
                "S3_ENDPOINT": "https://oss-cn-hangzhou.aliyuncs.com",
                "S3_ACCESS_KEY": "你的 AccessKey ID",
                "S3_SECRET_KEY": "你的 AccessKey Secret",
                "S3_BUCKET": "你的 bucket 名称",
            },
            "install_hint": """
📋 阿里云 OSS 配置步骤：

1. 访问 https://www.aliyun.com/product/oss 开通服务
2. 进入控制台 → 访问密钥 → 创建 AccessKey
3. 创建一个 Bucket（存储桶）
4. 复制以下配置到 secrets.env：

S3_ENDPOINT=https://oss-cn-hangzhou.aliyuncs.com
S3_ACCESS_KEY=你的 AccessKey ID
S3_SECRET_KEY=你的 AccessKey Secret
S3_BUCKET=你的 bucket 名称
""",
        },
        "腾讯云COS": {
            "name": "腾讯云 COS",
            "provider": "s3",
            "url": "https://cloud.tencent.com/product/cos",
            "features": ["与 IMA 同属腾讯", "国内高速", "集成方便"],
            "config_vars": {
                "S3_ENDPOINT": "https://cos.ap-guangzhou.myqcloud.com",
                "S3_ACCESS_KEY": "你的 SecretId",
                "S3_SECRET_KEY": "你的 SecretKey",
                "S3_BUCKET": "你的 bucket 名称",
            },
            "install_hint": """
📋 腾讯云 COS 配置步骤：

1. 访问 https://cloud.tencent.com/product/cos 开通服务
2. 进入 COS 控制台 → 访问管理 → 秘钥管理
3. 创建 Bucket（存储桶）
4. 复制以下配置到 secrets.env：

S3_ENDPOINT=https://cos.ap-guangzhou.myqcloud.com
S3_ACCESS_KEY=你的 SecretId
S3_SECRET_KEY=你的 SecretKey
S3_BUCKET=你的 bucket 名称
""",
        },
        "Samba": {
            "name": "Samba/NAS",
            "provider": "samba",
            "url": None,
            "features": ["局域网高速", "适合 NAS", "无需互联网"],
            "config_vars": {
                "SAMBA_HOST": "192.168.1.100",
                "SAMBA_USER": "你的用户名",
                "SAMBA_PASSWORD": "你的密码",
                "SAMBA_SHARE": "/memory",
            },
            "install_hint": """
📋 Samba/NAS 配置步骤：

1. 确保 NAS 已开启 SMB/Samba 服务
2. 在 NAS 上创建共享文件夹（如 memory）
3. 复制以下配置到 secrets.env：

SAMBA_HOST=192.168.1.100
SAMBA_USER=你的用户名
SAMBA_PASSWORD=你的密码
SAMBA_SHARE=/memory
""",
        },
        "SFTP": {
            "name": "SFTP",
            "provider": "sftp",
            "url": None,
            "features": ["SSH 加固", "安全可靠", "适合有服务器的用户"],
            "config_vars": {
                "SFTP_HOST": "你的服务器地址",
                "SFTP_PORT": "22",
                "SFTP_USERNAME": "你的用户名",
                "SFTP_PASSWORD": "你的密码",
            },
            "install_hint": """
📋 SFTP 配置步骤：

1. 确保服务器已开启 SSH 服务
2. 创建专用用户或使用现有用户
3. 复制以下配置到 secrets.env：

SFTP_HOST=你的服务器地址
SFTP_PORT=22
SFTP_USERNAME=你的用户名
SFTP_PASSWORD=你的密码
""",
        },
    }
    
    @classmethod
    def list_services(cls) -> list:
        """列出所有可安装的服务"""
        return list(cls.SERVICES.keys())
    
    @classmethod
    def get_install_hint(cls, service_name: str) -> str:
        """获取安装提示"""
        service = cls.SERVICES.get(service_name)
        if not service:
            return f"❌ 未知的云服务: {service_name}"
        return service.get("install_hint", "")
    
    @classmethod
    def open_signup_page(cls, service_name: str):
        """打开注册页面"""
        service = cls.SERVICES.get(service_name)
        if service and service.get("url"):
            print(f"🌐 正在打开 {service['name']} 官网...")
            webbrowser.open(service["url"])
        else:
            print("❌ 该服务无需在线注册")
    
    @classmethod
    def generate_config(cls, service_name: str) -> str:
        """生成配置模板"""
        service = cls.SERVICES.get(service_name)
        if not service:
            return ""
        
        lines = [f"\n# {service['name']} 配置"]
        lines.append("#" + "=" * 50)
        
        for key, value in service.get("config_vars", {}).items():
            lines.append(f"{key}={value}")
        
        lines.append("")
        return "\n".join(lines)


# ============================================================================
# 主函数
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="云服务快速安装向导")
    parser.add_argument("--list", action="store_true", help="列出所有可安装的云服务")
    parser.add_argument("--install", type=str, help="安装指定云服务")
    parser.add_argument("--hint", type=str, help="显示安装提示")
    parser.add_argument("--config", type=str, help="生成配置模板")
    parser.add_argument("--open", type=str, help="打开服务官网")
    args = parser.parse_args()
    
    if args.list:
        print("📋 支持快速安装的云服务：\n")
        for name, info in CloudInstaller.SERVICES.items():
            features = "、".join(info.get("features", []))
            print(f"  ☁️  {name}")
            print(f"     特点: {features}\n")
        print("💡 用法: python3 scripts/auto_setup.py --install 坚果云")
        return
    
    if args.hint:
        print(CloudInstaller.get_install_hint(args.hint))
        return
    
    if args.config:
        config = CloudInstaller.generate_config(args.config)
        if config:
            print(config)
        return
    
    if args.open:
        CloudInstaller.open_signup_page(args.open)
        return
    
    if args.install:
        hint = CloudInstaller.get_install_hint(args.install)
        print(hint)
        
        service = CloudInstaller.SERVICES.get(args.install)
        if service and service.get("url"):
            response = input("\n🌐 是否打开官网注册？(y/n): ")
            if response.lower() == "y":
                CloudInstaller.open_signup_page(args.install)
        return
    
    # 默认显示帮助
    parser.print_help()
    print("\n📋 示例：")
    print("  python3 scripts/auto_setup.py --list                    # 列出所有服务")
    print("  python3 scripts/auto_setup.py --install 坚果云          # 查看安装步骤")
    print("  python3 scripts/auto_setup.py --config 坚果云          # 生成配置模板")


if __name__ == "__main__":
    main()
