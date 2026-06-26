#!/usr/bin/env python3
"""
云服务自动检测模块
自动识别用户环境中已配置的云服务

检测策略：
1. 检测本地同步客户端（iCloud、Dropbox、OneDrive等）
2. 检测配置文件（WebDAV、Samba、S3等）
3. 检测环境变量
4. 检测开放端口
5. 智能推荐
"""

import os
import re
import socket
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ============================================================================
# 检测结果
# ============================================================================

@dataclass
class DetectedService:
    """检测到的服务"""
    name: str                    # 服务名称
    provider: str                 # 提供商类型
    detected_path: str            # 检测到的路径
    config_status: str            # 配置状态: detected(检测到) / configured(已配置) / recommended(推荐)
    confidence: float = 0.0      # 置信度 0-1
    auto_adapt: bool = False     # 是否可自动适配
    setup_hint: str = ""          # 设置提示


@dataclass
class DetectionReport:
    """检测报告"""
    services: List[DetectedService] = field(default_factory=list)
    total_detected: int = 0
    total_configured: int = 0
    recommendations: List[str] = field(default_factory=list)


# ============================================================================
# 检测器基类
# ============================================================================

class CloudServiceDetector:
    """云服务检测器基类"""
    
    def __init__(self):
        self.name = "base"
        self.provider = "unknown"
    
    def detect(self) -> List[DetectedService]:
        """检测服务"""
        return []
    
    def get_recommendation(self) -> str:
        """获取推荐文本"""
        return ""


# ============================================================================
# 本地云同步客户端检测
# ============================================================================

class ICloudDetector(CloudServiceDetector):
    """iCloud Drive 检测"""
    
    def __init__(self):
        super().__init__()
        self.name = "iCloud Drive"
        self.provider = "icloud"
    
    def detect(self) -> List[DetectedService]:
        services = []
        
        # 检测 iCloud 文档目录
        icloud_paths = [
            Path.home() / "Library/Mobile Documents/com~apple~CloudDocs",
            Path("/Users") / os.environ.get("USER", "") / "Library/Mobile Documents/com~apple~CloudDocs",
        ]
        
        for path in icloud_paths:
            if path.exists():
                # 检测是否有内容
                has_content = any(path.iterdir())
                
                service = DetectedService(
                    name=self.name,
                    provider=self.provider,
                    detected_path=str(path),
                    config_status="detected" if has_content else "recommended",
                    confidence=0.9 if has_content else 0.3,
                    auto_adapt=True,
                    setup_hint="iCloud 已开启，建议将记忆目录链接到 iCloud Drive"
                )
                services.append(service)
                break
        
        return services
    
    def get_recommendation(self) -> str:
        return "💡 建议：iCloud Drive 是 macOS 最便捷的云同步方案，适合 Apple 生态用户"


class DropboxDetector(CloudServiceDetector):
    """Dropbox 检测"""
    
    def __init__(self):
        super().__init__()
        self.name = "Dropbox"
        self.provider = "dropbox"
    
    def detect(self) -> List[DetectedService]:
        services = []
        
        dropbox_paths = [
            Path.home() / "Dropbox",
            Path.home() / ".dropbox-dist",
        ]
        
        for path in dropbox_paths:
            if path.exists():
                has_content = any(path.iterdir()) if path.is_dir() else True
                
                service = DetectedService(
                    name=self.name,
                    provider=self.provider,
                    detected_path=str(path),
                    config_status="detected" if has_content else "recommended",
                    confidence=0.95,
                    auto_adapt=True,
                    setup_hint="Dropbox 已安装，可将记忆目录链接到 Dropbox"
                )
                services.append(service)
                break
        
        return services
    
    def get_recommendation(self) -> str:
        return "💡 建议：Dropbox 是成熟的云存储方案，跨平台支持好"


class OneDriveDetector(CloudServiceDetector):
    """OneDrive 检测"""
    
    def __init__(self):
        super().__init__()
        self.name = "OneDrive"
        self.provider = "onedrive"
    
    def detect(self) -> List[DetectedService]:
        services = []
        
        onedrive_paths = [
            Path.home() / "OneDrive",
            Path.home() / "OneDrive - 个人",
            Path.home() / "OneDrive - 商业",
        ]
        
        for path in onedrive_paths:
            if path.exists():
                has_content = any(path.iterdir())
                
                service = DetectedService(
                    name=self.name,
                    provider=self.provider,
                    detected_path=str(path),
                    config_status="detected" if has_content else "recommended",
                    confidence=0.9,
                    auto_adapt=True,
                    setup_hint="OneDrive 已登录，可将记忆目录链接到 OneDrive"
                )
                services.append(service)
                break
        
        return services
    
    def get_recommendation(self) -> str:
        return "💡 建议：OneDrive 集成在 Windows系统中，适合 Windows 用户"


class GoogleDriveDetector(CloudServiceDetector):
    """Google Drive 检测"""
    
    def __init__(self):
        super().__init__()
        self.name = "Google Drive"
        self.provider = "gdrive"
    
    def detect(self) -> List[DetectedService]:
        services = []
        
        gdrive_paths = [
            Path.home() / "Google Drive",
            Path.home() / "My Drive",
        ]
        
        for path in gdrive_paths:
            if path.exists():
                service = DetectedService(
                    name=self.name,
                    provider=self.provider,
                    detected_path=str(path),
                    config_status="detected",
                    confidence=0.85,
                    auto_adapt=True,
                    setup_hint="Google Drive 已挂载，可将记忆目录链接到 Google Drive"
                )
                services.append(service)
                break
        
        return services
    
    def get_recommendation(self) -> str:
        return "💡 建议：Google Drive 适合已使用 Google 生态的用户"


class NextcloudDetector(CloudServiceDetector):
    """Nextcloud 检测"""
    
    def __init__(self):
        super().__init__()
        self.name = "Nextcloud"
        self.provider = "webdav"
    
    def detect(self) -> List[DetectedService]:
        services = []
        
        # 检测 Nextcloud 客户端
        nextcloud_paths = [
            Path.home() / ".local/share/nextcloud",
            Path.home() / "Nextcloud",
            Path.home() / ".config/Nextcloud",
        ]
        
        for path in nextcloud_paths:
            if path.exists():
                service = DetectedService(
                    name=self.name,
                    provider=self.provider,
                    detected_path=str(path),
                    config_status="detected",
                    confidence=0.9,
                    auto_adapt=True,
                    setup_hint="Nextcloud 客户端已安装，可通过 WebDAV 连接"
                )
                services.append(service)
                break
        
        # 也检测 WebDAV URL 配置
        webdav_urls = self._detect_webdav_url()
        services.extend(webdav_urls)
        
        return services
    
    def _detect_webdav_url(self) -> List[DetectedService]:
        """检测 WebDAV URL 配置"""
        services = []
        
        # 检测浏览器配置的 Nextcloud
        config_dirs = [
            Path.home() / ".config/Nextcloud",
            Path.home() / ".local/share/Nextcloud",
        ]
        
        for config_dir in config_dirs:
            if not config_dir.exists():
                continue
            
            # 搜索 .ini 或 .cfg 文件
            for config_file in config_dir.rglob("*.cfg"):
                try:
                    content = config_file.read_text()
                    # 查找 URL
                    matches = re.findall(r'https?://[^\s]+', content)
                    for url in matches:
                        if 'webdav' in url.lower() or 'nextcloud' in url.lower():
                            services.append(DetectedService(
                                name="Nextcloud (WebDAV)",
                                provider="webdav",
                                detected_path=url,
                                config_status="detected",
                                confidence=0.85,
                                auto_adapt=True,
                                setup_hint=f"发现 WebDAV 配置: {url}"
                            ))
                except:
                    pass
        
        return services
    
    def get_recommendation(self) -> str:
        return "💡 建议：Nextcloud 是开源私有云方案，适合注重隐私的用户"


class NutstoreDetector(CloudServiceDetector):
    """坚果云检测"""
    
    def __init__(self):
        super().__init__()
        self.name = "坚果云"
        self.provider = "webdav"
    
    def detect(self) -> List[DetectedService]:
        services = []
        
        nutstore_paths = [
            Path.home() / ".nutstore",
            Path.home() / ".local/share/nutstore",
            Path.home() / "坚果云",
        ]
        
        for path in nutstore_paths:
            if path.exists():
                service = DetectedService(
                    name=self.name,
                    provider=self.provider,
                    detected_path=str(path),
                    config_status="detected",
                    confidence=0.9,
                    auto_adapt=True,
                    setup_hint="坚果云已安装，可通过 WebDAV 连接"
                )
                services.append(service)
                break
        
        return services
    
    def get_recommendation(self) -> str:
        return "💡 建议：坚果云是国内可用的 WebDAV 云盘，稳定性好"


# ============================================================================
# 服务器/存储检测
# ============================================================================

class SambaDetector(CloudServiceDetector):
    """Samba/NAS 检测"""
    
    def __init__(self):
        super().__init__()
        self.name = "Samba/NAS"
        self.provider = "samba"
    
    def detect(self) -> List[DetectedService]:
        services = []
        
        # 检测已挂载的 Samba 共享
        proc_mounts = Path("/proc/mounts")
        if proc_mounts.exists():
            try:
                content = proc_mounts.read_text()
                # 查找 cifs 或 smbfs 挂载
                for line in content.splitlines():
                    if 'cifs' in line or 'smbfs' in line or '//' in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            mount_point = parts[1]
                            share_path = parts[0]
                            
                            if Path(mount_point).exists():
                                service = DetectedService(
                                    name=f"Samba 共享 ({Path(share_path).name})",
                                    provider=self.provider,
                                    detected_path=mount_point,
                                    config_status="detected",
                                    confidence=0.95,
                                    auto_adapt=True,
                                    setup_hint=f"检测到已挂载的 Samba 共享: {share_path}"
                                )
                                services.append(service)
            except:
                pass
        
        # 检测 smb.conf
        smb_conf_paths = [
            Path("/etc/samba/smb.conf"),
            Path.home() / ".smb/smb.conf",
        ]
        
        for conf_path in smb_conf_paths:
            if conf_path.exists():
                try:
                    content = conf_path.read_text()
                    # 提取共享名称
                    shares = re.findall(r'\[([^\]]+)\]', content)
                    for share in shares:
                        if share not in ['global', 'printers', 'print$']:
                            services.append(DetectedService(
                                name=f"Samba 共享 ({share})",
                                provider=self.provider,
                                detected_path=f"smb://.../{share}",
                                config_status="detected",
                                confidence=0.8,
                                auto_adapt=False,
                                setup_hint=f"发现 Samba 配置: [{share}]"
                            ))
                except:
                    pass
        
        return services
    
    def get_recommendation(self) -> str:
        return "💡 建议：Samba 适合局域网 NAS 存储，高速稳定"


class SFTPDetector(CloudServiceDetector):
    """SFTP 检测"""
    
    def __init__(self):
        super().__init__()
        self.name = "SFTP"
        self.provider = "sftp"
    
    def detect(self) -> List[DetectedService]:
        services = []
        
        # 检测 SSH 配置
        ssh_config = Path.home() / ".ssh" / "config"
        if ssh_config.exists():
            try:
                content = ssh_config.read_text()
                # 查找 Host 配置
                hosts = re.findall(r'Host\s+(\S+)', content)
                for host in hosts:
                    # 检测是否是服务器（非 github/gitlab）
                    if host not in ['github.com', 'gitlab.com', 'bitbucket.org']:
                        services.append(DetectedService(
                            name=f"SFTP ({host})",
                            provider=self.provider,
                            detected_path=f"sftp://{host}",
                            config_status="detected",
                            confidence=0.75,
                            auto_adapt=False,
                            setup_hint=f"发现 SSH 配置: {host}"
                        ))
            except:
                pass
        
        # 检测 known_hosts 中的服务器
        known_hosts = Path.home() / ".ssh" / "known_hosts"
        if known_hosts.exists():
            try:
                content = known_hosts.read_text()
                # 提取主机名（非 IP）
                hosts = set()
                for line in content.splitlines():
                    parts = line.split()
                    if parts:
                        host = parts[0].split(',')[0]
                        # 过滤掉 IP 和已知服务
                        if not host[0].isdigit() and host not in ['github.com', 'gitlab.com']:
                            hosts.add(host)
                
                for host in list(hosts)[:5]:  # 最多 5 个
                    services.append(DetectedService(
                        name=f"SFTP 服务器 ({host})",
                        provider=self.provider,
                        detected_path=f"sftp://{host}",
                        config_status="detected",
                        confidence=0.6,
                        auto_adapt=False,
                        setup_hint=f"发现 SFTP 服务器: {host}"
                    ))
            except:
                pass
        
        return services
    
    def get_recommendation(self) -> str:
        return "💡 建议：SFTP 适合有自己服务器的用户，安全可靠"


class FTPDetector(CloudServiceDetector):
    """FTP 检测"""
    
    def __init__(self):
        super().__init__()
        self.name = "FTP"
        self.provider = "ftp"
    
    def detect(self) -> List[DetectedService]:
        # FTP 通常需要用户主动配置，不主动检测
        return []
    
    def get_recommendation(self) -> str:
        return "💡 建议：FTP 是传统文件传输方案，配置简单"


# ============================================================================
# 云 API 检测
# ============================================================================

class IMAClientDetector(CloudServiceDetector):
    """IMA 客户端检测"""
    
    def __init__(self):
        super().__init__()
        self.name = "IMA 知识库"
        self.provider = "ima"
    
    def detect(self) -> List[DetectedService]:
        services = []
        
        # 检测环境变量
        client_id = os.environ.get("IMA_OPENAPI_CLIENTID", "")
        api_key = os.environ.get("IMA_OPENAPI_APIKEY", "")
        
        if client_id and api_key:
            service = DetectedService(
                name=self.name,
                provider=self.provider,
                detected_path="环境变量",
                config_status="configured",
                confidence=1.0,
                auto_adapt=True,
                setup_hint="IMA 凭证已配置"
            )
            services.append(service)
        
        # 检测 secrets.env
        secrets_file = Path.home() / ".openclaw" / "credentials" / "secrets.env"
        if secrets_file.exists():
            try:
                content = secrets_file.read_text()
                if "IMA_OPENAPI_CLIENTID" in content:
                    service = DetectedService(
                        name=self.name,
                        provider=self.provider,
                        detected_path=str(secrets_file),
                        config_status="configured",
                        confidence=1.0,
                        auto_adapt=True,
                        setup_hint="IMA 凭证已在 secrets.env 中配置"
                    )
                    services.append(service)
            except:
                pass
        
        return services
    
    def get_recommendation(self) -> str:
        return "💡 建议：IMA 知识库适合腾讯生态用户，支持知识库管理"


class OSSDetector(CloudServiceDetector):
    """阿里云 OSS 检测"""
    
    def __init__(self):
        super().__init__()
        self.name = "阿里云 OSS"
        self.provider = "s3"
    
    def detect(self) -> List[DetectedService]:
        services = []
        
        # 检测环境变量
        if os.environ.get("OSS_ACCESS_KEY_ID") and os.environ.get("OSS_ACCESS_KEY_SECRET"):
            service = DetectedService(
                name=self.name,
                provider=self.provider,
                detected_path="环境变量",
                config_status="configured",
                confidence=1.0,
                auto_adapt=True,
                setup_hint="阿里云 OSS 凭证已配置"
            )
            services.append(service)
        
        return services
    
    def get_recommendation(self) -> str:
        return "💡 建议：阿里云 OSS 是国内成熟的云存储方案，成本低、稳定性好"


class COSDetector(CloudServiceDetector):
    """腾讯云 COS 检测"""
    
    def __init__(self):
        super().__init__()
        self.name = "腾讯云 COS"
        self.provider = "s3"
    
    def detect(self) -> List[DetectedService]:
        services = []
        
        if os.environ.get("COS_SECRET_ID") and os.environ.get("COS_SECRET_KEY"):
            service = DetectedService(
                name=self.name,
                provider=self.provider,
                detected_path="环境变量",
                config_status="configured",
                confidence=1.0,
                auto_adapt=True,
                setup_hint="腾讯云 COS 凭证已配置"
            )
            services.append(service)
        
        return services
    
    def get_recommendation(self) -> str:
        return "💡 建议：腾讯云 COS 与 IMA 同属腾讯生态，集成方便"


# ============================================================================
# 综合检测器
# ============================================================================

class CloudServiceAutoDetector:
    """云服务综合检测器"""
    
    def __init__(self):
        self.detectors: List[CloudServiceDetector] = [
            # 本地云同步客户端
            ICloudDetector(),
            DropboxDetector(),
            OneDriveDetector(),
            GoogleDriveDetector(),
            NextcloudDetector(),
            NutstoreDetector(),
            # 服务器/存储
            SambaDetector(),
            SFTPDetector(),
            # 云 API
            IMAClientDetector(),
            OSSDetector(),
            COSDetector(),
        ]
    
    def detect_all(self) -> DetectionReport:
        """检测所有云服务"""
        report = DetectionReport()
        
        for detector in self.detectors:
            services = detector.detect()
            for service in services:
                report.services.append(service)
                
                if service.config_status == "configured":
                    report.total_configured += 1
                elif service.config_status == "detected":
                    report.total_detected += 1
        
        # 去重（同一服务可能多次检测）
        seen = set()
        unique_services = []
        for service in report.services:
            key = (service.provider, service.detected_path)
            if key not in seen:
                seen.add(key)
                unique_services.append(service)
        
        report.services = unique_services
        
        # 生成推荐
        report.recommendations = self._generate_recommendations(report)
        
        return report
    
    def _generate_recommendations(self, report: DetectionReport) -> List[str]:
        """生成推荐"""
        recommendations = []
        
        # 已配置的服务
        configured = [s for s in report.services if s.config_status == "configured"]
        if configured:
            recommendations.append(f"✅ 已自动适配 {len(configured)} 个云服务:")
            for s in configured:
                recommendations.append(f"   - {s.name} ({s.setup_hint})")
        
        # 检测到待配置的服务
        detected = [s for s in report.services if s.config_status == "detected"]
        if detected:
            recommendations.append(f"\n🔍 检测到 {len(detected)} 个可用的云服务:")
            for s in detected:
                recommendations.append(f"   - {s.name}: {s.setup_hint}")
        
        # 无检测结果
        if not report.services:
            recommendations.append("🔎 未检测到任何云服务")
            recommendations.append("")
            recommendations.append("📋 推荐方案:")
            recommendations.append("   1. 坚果云（国内 WebDAV，稳定）")
            recommendations.append("   2. Nextcloud（开源私有云）")
            recommendations.append("   3. 阿里云 OSS（企业级存储）")
            recommendations.append("   4. 腾讯云 COS（与 IMA 同一生态）")
            recommendations.append("")
            recommendations.append("💡 输入\"安装 坚果云\"等指令即可快速配置")
        
        return recommendations
    
    def print_report(self, report: DetectionReport):
        """打印检测报告"""
        print("=" * 50)
        print("☁️  云服务自动检测报告")
        print("=" * 50)
        
        if not report.services:
            print("\n🔎 未检测到任何云服务\n")
        else:
            print(f"\n📊 检测结果：{len(report.services)} 个服务")
            print(f"   ✅ 已配置: {report.total_configured}")
            print(f"   🔍 待适配: {report.total_detected}\n")
        
        for service in report.services:
            status_icon = "✅" if service.config_status == "configured" else "🔍"
            auto_icon = "🤖" if service.auto_adapt else "👤"
            print(f"{status_icon} {service.name} {auto_icon}")
            print(f"   路径: {service.detected_path}")
            print(f"   置信度: {service.confidence:.0%}")
            print(f"   提示: {service.setup_hint}")
            print()
        
        # 打印推荐
        print("-" * 50)
        for rec in report.recommendations:
            print(rec)
        
        print("-" * 50)


# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    print("🔍 正在检测云服务...\n")
    
    detector = CloudServiceAutoDetector()
    report = detector.detect_all()
    detector.print_report(report)
    
    # 返回检测到的服务列表（供其他脚本使用）
    configured = [s for s in report.services if s.config_status == "configured"]
    return configured


if __name__ == "__main__":
    main()
