#!/usr/bin/env python3
"""
云服务自动检测模块 v2.0
简化版，专为集成设计

检测策略：
1. 优先检测本地云同步客户端
2. 检测配置文件和 WebDAV URL
3. 检测环境变量和 secrets.env
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional


# ============================================================================
# 检测结果
# ============================================================================

class DetectedService:
    def __init__(self, name: str, provider: str, path: str, configured: bool = False):
        self.name = name
        self.provider = provider
        self.path = path
        self.configured = configured


# ============================================================================
# 简化检测器
# ============================================================================

def detect_local_cloud_clients() -> List[DetectedService]:
    """检测本地云同步客户端"""
    services = []
    
    # iCloud Drive (macOS)
    icloud_path = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs"
    if icloud_path.exists():
        services.append(DetectedService(
            name="iCloud Drive",
            provider="icloud",
            path=str(icloud_path),
            configured=True  # iCloud 只要开启就能用
        ))
    
    # Dropbox
    dropbox_path = Path.home() / "Dropbox"
    if dropbox_path.exists():
        services.append(DetectedService(
            name="Dropbox",
            provider="dropbox",
            path=str(dropbox_path),
            configured=True
        ))
    
    # OneDrive
    onedrive_paths = [
        Path.home() / "OneDrive",
        Path.home() / "OneDrive - 个人",
        Path.home() / "OneDrive - 商业",
    ]
    for path in onedrive_paths:
        if path.exists():
            services.append(DetectedService(
                name="OneDrive",
                provider="onedrive",
                path=str(path),
                configured=True
            ))
            break
    
    # Google Drive
    gdrive_paths = [
        Path.home() / "Google Drive",
        Path.home() / "My Drive",
    ]
    for path in gdrive_paths:
        if path.exists():
            services.append(DetectedService(
                name="Google Drive",
                provider="gdrive",
                path=str(path),
                configured=True
            ))
            break
    
    # 坚果云
    nutstore_paths = [
        Path.home() / ".nutstore",
        Path.home() / "坚果云",
    ]
    for path in nutstore_paths:
        if path.exists():
            services.append(DetectedService(
                name="坚果云",
                provider="webdav",
                path=str(path),
                configured=False  # 需要 WebDAV 配置
            ))
            break
    
    # Nextcloud
    nextcloud_paths = [
        Path.home() / ".local/share/nextcloud",
        Path.home() / "Nextcloud",
    ]
    for path in nextcloud_paths:
        if path.exists():
            services.append(DetectedService(
                name="Nextcloud",
                provider="webdav",
                path=str(path),
                configured=False
            ))
            break
    
    return services


def detect_secrets_config() -> List[DetectedService]:
    """检测 secrets.env 配置"""
    services = []
    
    secrets_file = Path.home() / ".openclaw" / "credentials" / "secrets.env"
    
    if not secrets_file.exists():
        return services
    
    try:
        content = secrets_file.read_text()
    except:
        return services
    
    # IMA
    if "IMA_OPENAPI_CLIENTID" in content and "IMA_OPENAPI_APIKEY" in content:
        services.append(DetectedService(
            name="IMA 知识库",
            provider="ima",
            path="secrets.env",
            configured=True
        ))
    
    # WebDAV
    if "WEBDAV_URL" in content:
        services.append(DetectedService(
            name="WebDAV",
            provider="webdav",
            path="secrets.env",
            configured=True
        ))
    
    # S3/OSS/COS
    if "S3_ENDPOINT" in content:
        services.append(DetectedService(
            name="S3 兼容存储",
            provider="s3",
            path="secrets.env",
            configured=True
        ))
    
    # Samba
    if "SAMBA_HOST" in content:
        services.append(DetectedService(
            name="Samba/NAS",
            provider="samba",
            path="secrets.env",
            configured=True
        ))
    
    # SFTP
    if "SFTP_HOST" in content:
        services.append(DetectedService(
            name="SFTP",
            provider="sftp",
            path="secrets.env",
            configured=True
        ))
    
    return services


def detect_environment_vars() -> List[DetectedService]:
    """检测环境变量"""
    services = []
    
    # IMA
    if os.environ.get("IMA_OPENAPI_CLIENTID") and os.environ.get("IMA_OPENAPI_APIKEY"):
        services.append(DetectedService(
            name="IMA 知识库",
            provider="ima",
            path="环境变量",
            configured=True
        ))
    
    # OSS
    if os.environ.get("OSS_ACCESS_KEY_ID") and os.environ.get("OSS_ACCESS_KEY_SECRET"):
        services.append(DetectedService(
            name="阿里云 OSS",
            provider="s3",
            path="环境变量",
            configured=True
        ))
    
    # COS
    if os.environ.get("COS_SECRET_ID") and os.environ.get("COS_SECRET_KEY"):
        services.append(DetectedService(
            name="腾讯云 COS",
            provider="s3",
            path="环境变量",
            configured=True
        ))
    
    return services


def detect_samba_mounts() -> List[DetectedService]:
    """检测已挂载的 Samba 共享"""
    services = []
    
    proc_mounts = Path("/proc/mounts")
    if not proc_mounts.exists():
        return services
    
    try:
        content = proc_mounts.read_text()
    except:
        return services
    
    for line in content.splitlines():
        if 'cifs' in line or 'smbfs' in line:
            parts = line.split()
            if len(parts) >= 2:
                mount_point = parts[1]
                if Path(mount_point).exists() and "yaoyao" not in mount_point.lower():
                    services.append(DetectedService(
                        name=f"Samba 共享 ({Path(mount_point).name})",
                        provider="samba",
                        path=mount_point,
                        configured=True
                    ))
    
    return services


# ============================================================================
# 综合检测
# ============================================================================

def detect_all() -> Dict[str, List[DetectedService]]:
    """检测所有云服务"""
    result = {
        "configured": [],   # 已配置好可以用的
        "available": [],    # 检测到但未配置（本地客户端等）
    }
    
    # 本地云客户端
    for service in detect_local_cloud_clients():
        if service.configured:
            result["available"].append(service)
        else:
            result["available"].append(service)
    
    # secrets.env 配置
    for service in detect_secrets_config():
        if service.configured:
            result["configured"].append(service)
    
    # 环境变量
    for service in detect_environment_vars():
        if service.configured and service.name not in [s.name for s in result["configured"]]:
            result["configured"].append(service)
    
    # 已挂载的 Samba
    for service in detect_samba_mounts():
        if service.configured and service.name not in [s.name for s in result["configured"]]:
            result["configured"].append(service)
    
    # 去重
    seen = set()
    unique_configured = []
    for s in result["configured"]:
        if s.name not in seen:
            seen.add(s.name)
            unique_configured.append(s)
    result["configured"] = unique_configured
    
    return result


def print_detection_report():
    """打印检测报告（小白友好）"""
    print("\n" + "=" * 50)
    print("☁️  云服务检测报告")
    print("=" * 50)
    
    detected = detect_all()
    configured = detected["configured"]
    available = detected["available"]
    
    if configured:
        print(f"\n✅ 已配置 {len(configured)} 个云服务，可以直接使用：\n")
        for s in configured:
            icon = "📚" if s.provider == "ima" else "🌐" if s.provider == "webdav" else "🪣" if s.provider == "s3" else "🖥️"
            print(f"  {icon} {s.name}")
    else:
        print("\n⚠️  未检测到已配置的云服务")
    
    if available:
        print(f"\n🔍 检测到 {len(available)} 个可用的本地云客户端：\n")
        for s in available:
            icon = "☁️" if s.provider == "icloud" else "📦" if s.provider == "dropbox" else "💾" if s.provider == "onedrive" else "🌐"
            print(f"  {icon} {s.name}")
            print(f"      路径: {s.path}")
            print(f"      提示: 需要配置才能使用\n")
    
    if not configured and not available:
        print("\n🔎 未检测到任何云服务\n")
        print("💡 推荐方案：")
        print("  1. 坚果云（国内 WebDAV，稳定）")
        print("  2. 阿里云 OSS（企业级存储）")
        print("  3. 腾讯云 COS（与 IMA 同属腾讯）")
        print("  4. Samba/NAS（局域网高速）")
        print("\n📖 输入'云同步安装'可查看详细安装指南")
    
    print("=" * 50)


# ============================================================================
# 主函数
# ============================================================================

if __name__ == "__main__":
    print_detection_report()
