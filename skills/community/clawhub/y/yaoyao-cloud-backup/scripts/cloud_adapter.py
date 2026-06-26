#!/usr/bin/env python3
"""
云存储适配器架构
支持多种云存储服务:IMA、WebDAV、S3、FTP/SFTP、Samba等

架构:
- CloudAdapter (ABC) - 抽象基类
- 具体适配器实现各种云服务
- AdapterFactory - 适配器工厂,根据配置创建对应适配器
"""

import os
import json
import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


# ============================================================================
# 配置定义
# ============================================================================

@dataclass
class CloudConfig:
    """云存储配置"""
    provider: str           # 服务类型: ima, webdav, s3, ftp, samba
    enabled: bool = False
    credentials: Dict = None  # 各服务凭证

    def __post_init__(self):
        if self.credentials is None:
            self.credentials = {}


class CloudSyncConfig:
    """云同步统一配置管理器"""

    PROVIDERS = ["ima", "webdav", "s3", "ftp", "sftp", "samba", "icloud", "dropbox", "onedrive"]

    @staticmethod
    def load_from_secrets() -> Dict[str, CloudConfig]:
        """从 secrets.env 加载配置"""
        secrets_file = Path.home() / ".openclaw" / "credentials" / "secrets.env"
        config = {}

        if not secrets_file.exists():
            return config

        # 解析 secrets.env
        secrets = {}
        for line in secrets_file.read_text().splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                # 去除首尾引号和空白
                value = value.strip().strip('"').strip("'")
                secrets[key.strip()] = value

        # IMA
        if "IMA_OPENAPI_CLIENTID" in secrets:
            config["ima"] = CloudConfig(
                provider="ima",
                enabled=True,
                credentials={
                    "client_id": secrets.get("IMA_OPENAPI_CLIENTID", ""),
                    "api_key": secrets.get("IMA_OPENAPI_APIKEY", ""),
                }
            )

        # WebDAV
        if "WEBDAV_URL" in secrets:
            config["webdav"] = CloudConfig(
                provider="webdav",
                enabled=True,
                credentials={
                    "url": secrets.get("WEBDAV_URL", ""),
                    "username": secrets.get("WEBDAV_USERNAME", ""),
                    "password": secrets.get("WEBDAV_PASSWORD", ""),
                }
            )

        # S3/OSS
        if "S3_ENDPOINT" in secrets:
            config["s3"] = CloudConfig(
                provider="s3",
                enabled=True,
                credentials={
                    "endpoint": secrets.get("S3_ENDPOINT", ""),
                    "access_key": secrets.get("S3_ACCESS_KEY", ""),
                    "secret_key": secrets.get("S3_SECRET_KEY", ""),
                    "bucket": secrets.get("S3_BUCKET", ""),
                    "region": secrets.get("S3_REGION", "auto"),
                }
            )

        # FTP/SFTP
        if "FTP_HOST" in secrets:
            config["ftp"] = CloudConfig(
                provider="ftp",
                enabled=True,
                credentials={
                    "host": secrets.get("FTP_HOST", ""),
                    "port": int(secrets.get("FTP_PORT", "21")),
                    "username": secrets.get("FTP_USERNAME", ""),
                    "password": secrets.get("FTP_PASSWORD", ""),
                    "secure": secrets.get("FTP_SECURE", "false").lower() == "true",
                }
            )

        # SFTP
        if "SFTP_HOST" in secrets:
            config["sftp"] = CloudConfig(
                provider="sftp",
                enabled=True,
                credentials={
                    "host": secrets.get("SFTP_HOST", ""),
                    "port": int(secrets.get("SFTP_PORT", "22")),
                    "username": secrets.get("SFTP_USERNAME", ""),
                    "password": secrets.get("SFTP_PASSWORD", ""),
                    "key_file": secrets.get("SFTP_KEY_FILE", ""),
                }
            )

        # Samba/NAS
        if "SAMBA_HOST" in secrets:
            config["samba"] = CloudConfig(
                provider="samba",
                enabled=True,
                credentials={
                    "host": secrets.get("SAMBA_HOST", ""),
                    "port": int(secrets.get("SAMBA_PORT", "445")),
                    "username": secrets.get("SAMBA_USER", ""),
                    "password": secrets.get("SAMBA_PASSWORD", secrets.get("SAMBA_PASS", "")),
                    "share": secrets.get("SAMBA_SHARE", "memory"),
                    "remote_path": secrets.get("SAMBA_REMOTE_PATH", "/"),
                }
            )

        return config

    @staticmethod
    def get_config_template() -> str:
        """返回配置模板"""
        return '''
# ==============================================
# yaoyao-cloud-backup 凭证配置模板
# 复制到 ~/.openclaw/credentials/secrets.env
# ==============================================

# --- IMA 知识库(腾讯)---
IMA_OPENAPI_CLIENTID=your_client_id
IMA_OPENAPI_APIKEY=your_api_key

# --- WebDAV(Nextcloud/坚果云/ownCloud)---
WEBDAV_URL=https://your-server.com/remote.php/dav/files/username/
WEBDAV_USERNAME=your_username
WEBDAV_PASSWORD=your_password

# --- S3 兼容存储(阿里云OSS/腾讯COS/AWS S3)---
S3_ENDPOINT=https://oss-cn-hangzhou.aliyuncs.com
S3_ACCESS_KEY=your_access_key
S3_SECRET_KEY=your_secret_key
S3_BUCKET=your_bucket_name
S3_REGION=oss-cn-hangzhou

# --- FTP ---
FTP_HOST=ftp.example.com
FTP_PORT=21
FTP_USERNAME=your_username
FTP_PASSWORD=your_password
FTP_SECURE=false

# --- SFTP ---
SFTP_HOST=sftp.example.com
SFTP_PORT=22
SFTP_USERNAME=your_username
SFTP_PASSWORD=your_password
SFTP_KEY_FILE=~/.ssh/id_rsa

# --- Samba/NAS ---
SAMBA_HOST=192.168.1.100
SAMBA_USER=your_username
SAMBA_PASSWORD=your_password
SAMBA_SHARE=/memory
'''


# ============================================================================
# 抽象基类
# ============================================================================

class CloudAdapter(ABC):
    """云存储适配器基类"""

    def __init__(self, config: CloudConfig):
        self.config = config
        self.provider = config.provider

    @abstractmethod
    def upload(self, local_path: Path, remote_path: str) -> bool:
        """上传文件"""
        pass

    @abstractmethod
    def download(self, remote_path: str, local_path: Path) -> bool:
        """下载文件"""
        pass

    @abstractmethod
    def list(self, remote_path: str = "/") -> List[Dict]:
        """列出文件"""
        pass

    @abstractmethod
    def delete(self, remote_path: str) -> bool:
        """删除文件"""
        pass

    @abstractmethod
    def exists(self, remote_path: str) -> bool:
        """检查文件是否存在"""
        pass

    def get_name(self) -> str:
        """获取服务名称"""
        return self.provider


# ============================================================================
# 适配器实现
# ============================================================================

class IMAAdapter(CloudAdapter):
    """IMA 知识库适配器"""

    def __init__(self, config: CloudConfig):
        super().__init__(config)
        self.client_id = config.credentials.get("client_id", "")
        self.api_key = config.credentials.get("api_key", "")

    def upload(self, local_path: Path, remote_path: str) -> bool:
        """上传到 IMA"""
        # 已在 sync_ima.py 中实现
        # 这里复用
        pass

    def download(self, remote_path: str, local_path: Path) -> bool:
        """从 IMA 下载"""
        # TODO: 实现 IMA 下载
        return False

    def list(self, remote_path: str = "/") -> List[Dict]:
        """列出 IMA 文件"""
        # TODO: 实现
        return []

    def delete(self, remote_path: str) -> bool:
        """删除 IMA 文件"""
        return False

    def exists(self, remote_path: str) -> bool:
        """检查 IMA 文件是否存在"""
        return False


class WebDAVAdapter(CloudAdapter):
    """WebDAV 适配器(支持 Nextcloud、坚果云、ownCloud 等)"""

    def __init__(self, config: CloudConfig):
        super().__init__(config)
        self.url = config.credentials.get("url", "")
        self.username = config.credentials.get("username", "")
        self.password = config.credentials.get("password", "")

    def _get_client(self):
        """获取 WebDAV 客户端"""
        try:
            import webdav3.client
            options = {
                "webdav_hostname": self.url,
                "webdav_login": self.username,
                "webdav_password": self.password,
            }
            return webdav3.client.Client(options)
        except ImportError:
            # 使用内置实现
            return None

    def upload(self, local_path: Path, remote_path: str) -> bool:
        """上传到 WebDAV"""
        try:
            import requests
            with open(local_path, "rb") as f:
                response = requests.put(
                    f"{self.url.rstrip('/')}/{remote_path}",
                    data=f,
                    auth=(self.username, self.password)
                )
                return response.status_code in [200, 201, 204]
        except Exception as e:
            print(f"WebDAV upload failed: {e}")
            return False

    def download(self, remote_path: str, local_path: Path) -> bool:
        """从 WebDAV 下载"""
        try:
            import requests
            response = requests.get(
                f"{self.url.rstrip('/')}/{remote_path}",
                auth=(self.username, self.password)
            )
            if response.status_code == 200:
                local_path.parent.mkdir(parents=True, exist_ok=True)
                with open(local_path, "wb") as f:
                    f.write(response.content)
                return True
            return False
        except Exception as e:
            print(f"WebDAV download failed: {e}")
            return False

    def list(self, remote_path: str = "/") -> List[Dict]:
        """列出 WebDAV 文件"""
        try:
            import requests
            response = requests.request(
                "PROPFIND",
                f"{self.url.rstrip('/')}/{remote_path}",
                auth=(self.username, self.password),
                headers={"Depth": "1"}
            )
            if response.status_code in [200, 207]:
                # 解析 XML 响应
                # 简化处理
                return []
            return []
        except Exception as e:
            print(f"WebDAV list failed: {e}")
            return []

    def delete(self, remote_path: str) -> bool:
        """删除 WebDAV 文件"""
        try:
            import requests
            response = requests.delete(
                f"{self.url.rstrip('/')}/{remote_path}",
                auth=(self.username, self.password)
            )
            return response.status_code in [200, 204]
        except Exception:
            return False

    def exists(self, remote_path: str) -> bool:
        """检查 WebDAV 文件是否存在"""
        try:
            import requests
            response = requests.head(
                f"{self.url.rstrip('/')}/{remote_path}",
                auth=(self.username, self.password)
            )
            return response.status_code == 200
        except Exception:
            return False


class S3Adapter(CloudAdapter):
    """S3 兼容存储适配器(阿里云OSS、腾讯COS、AWS S3 等)"""

    def __init__(self, config: CloudConfig):
        super().__init__(config)
        self.endpoint = config.credentials.get("endpoint", "")
        self.access_key = config.credentials.get("access_key", "")
        self.secret_key = config.credentials.get("secret_key", "")
        self.bucket = config.credentials.get("bucket", "")
        self.region = config.credentials.get("region", "auto")

    def _get_client(self):
        """获取 S3 客户端"""
        try:
            import boto3
            return boto3.client(
                "s3",
                endpoint_url=self.endpoint,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region,
            )
        except ImportError:
            return None

    def upload(self, local_path: Path, remote_path: str) -> bool:
        """上传到 S3"""
        client = self._get_client()
        if not client:
            return False
        try:
            client.upload_file(str(local_path), self.bucket, remote_path)
            return True
        except Exception as e:
            print(f"S3 upload failed: {e}")
            return False

    def download(self, remote_path: str, local_path: Path) -> bool:
        """从 S3 下载"""
        client = self._get_client()
        if not client:
            return False
        try:
            local_path.parent.mkdir(parents=True, exist_ok=True)
            client.download_file(self.bucket, remote_path, str(local_path))
            return True
        except Exception as e:
            print(f"S3 download failed: {e}")
            return False

    def list(self, remote_path: str = "/") -> List[Dict]:
        """列出 S3 文件"""
        client = self._get_client()
        if not client:
            return []
        try:
            result = client.list_objects_v2(Bucket=self.bucket, Prefix=remote_path)
            files = []
            for obj in result.get("Contents", []):
                files.append({
                    "name": obj["Key"],
                    "size": obj["Size"],
                    "modified": obj["LastModified"].isoformat() if hasattr(obj["LastModified"], "isoformat") else str(obj["LastModified"]),
                })
            return files
        except Exception as e:
            print(f"S3 list failed: {e}")
            return []

    def delete(self, remote_path: str) -> bool:
        """删除 S3 文件"""
        client = self._get_client()
        if not client:
            return False
        try:
            client.delete_object(Bucket=self.bucket, Key=remote_path)
            return True
        except Exception:
            return False

    def exists(self, remote_path: str) -> bool:
        """检查 S3 文件是否存在"""
        client = self._get_client()
        if not client:
            return False
        try:
            client.head_object(Bucket=self.bucket, Key=remote_path)
            return True
        except Exception:
            return False


class FTPAdapter(CloudAdapter):
    """FTP 适配器"""

    def __init__(self, config: CloudConfig):
        super().__init__(config)
        self.host = config.credentials.get("host", "")
        self.port = config.credentials.get("port", 21)
        self.username = config.credentials.get("username", "")
        self.password = config.credentials.get("password", "")
        self.secure = config.credentials.get("secure", False)

    def upload(self, local_path: Path, remote_path: str) -> bool:
        """上传到 FTP"""
        try:
            if self.secure:
                from ftplib import FTP_TLS
                ftp = FTP_TLS()
            else:
                from ftp import FTP
                ftp = FTP()

            ftp.connect(self.host, self.port)
            ftp.login(self.username, self.password)

            # 创建远程目录
            dirs = Path(remote_path).parts[:-1]
            for d in dirs:
                try:
                    ftp.mkd(d)
                except:
                    pass

            with open(local_path, "rb") as f:
                ftp.storbinary(f"STOR {remote_path}", f)

            ftp.quit()
            return True
        except Exception as e:
            print(f"FTP upload failed: {e}")
            return False

    def download(self, remote_path: str, local_path: Path) -> bool:
        """从 FTP 下载"""
        try:
            from ftplib import FTP
            ftp = FTP()
            ftp.connect(self.host, self.port)
            ftp.login(self.username, self.password)

            local_path.parent.mkdir(parents=True, exist_ok=True)
            with open(local_path, "wb") as f:
                ftp.retrbinary(f"RETR {remote_path}", f.write)

            ftp.quit()
            return True
        except Exception as e:
            print(f"FTP download failed: {e}")
            return False

    def list(self, remote_path: str = "/") -> List[Dict]:
        """列出 FTP 文件"""
        try:
            from ftplib import FTP
            ftp = FTP()
            ftp.connect(self.host, self.port)
            ftp.login(self.username, self.password)
            files = ftp.nlst(remote_path)
            ftp.quit()
            return [{"name": f} for f in files]
        except Exception as e:
            print(f"FTP list failed: {e}")
            return []

    def delete(self, remote_path: str) -> bool:
        """删除 FTP 文件"""
        try:
            from ftplib import FTP
            ftp = FTP()
            ftp.connect(self.host, self.port)
            ftp.login(self.username, self.password)
            ftp.delete(remote_path)
            ftp.quit()
            return True
        except Exception:
            return False

    def exists(self, remote_path: str) -> bool:
        """检查 FTP 文件是否存在"""
        try:
            from ftplib import FTP
            ftp = FTP()
            ftp.connect(self.host, self.port)
            ftp.login(self.username, self.password)
            ftp.size(remote_path)
            ftp.quit()
            return True
        except Exception:
            return False


class SFTPAdapter(CloudAdapter):
    """SFTP 适配器"""

    def __init__(self, config: CloudConfig):
        super().__init__(config)
        self.host = config.credentials.get("host", "")
        self.port = config.credentials.get("port", 22)
        self.username = config.credentials.get("username", "")
        self.password = config.credentials.get("password", "")
        self.key_file = config.credentials.get("key_file", "")

    def _get_client(self):
        """获取 SFTP 客户端"""
        try:
            import paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self.key_file:
                ssh.connect(
                    self.host, port=self.port,
                    username=self.username,
                    key_filename=self.key_file
                )
            else:
                ssh.connect(
                    self.host, port=self.port,
                    username=self.username,
                    password=self.password
                )

            return ssh.open_sftp()
        except Exception as e:
            print(f"SFTP connection failed: {e}")
            return None

    def upload(self, local_path: Path, remote_path: str) -> bool:
        """上传到 SFTP"""
        sftp = self._get_client()
        if not sftp:
            return False
        try:
            # 创建远程目录
            dirs = Path(remote_path).parts[:-1]
            current = ""
            for d in dirs:
                current += "/" + d
                try:
                    sftp.mkdir(current)
                except:
                    pass

            sftp.put(str(local_path), remote_path)
            sftp.close()
            return True
        except Exception as e:
            print(f"SFTP upload failed: {e}")
            return False

    def download(self, remote_path: str, local_path: Path) -> bool:
        """从 SFTP 下载"""
        sftp = self._get_client()
        if not sftp:
            return False
        try:
            local_path.parent.mkdir(parents=True, exist_ok=True)
            sftp.get(remote_path, str(local_path))
            sftp.close()
            return True
        except Exception as e:
            print(f"SFTP download failed: {e}")
            return False

    def list(self, remote_path: str = "/") -> List[Dict]:
        """列出 SFTP 文件"""
        sftp = self._get_client()
        if not sftp:
            return []
        try:
            files = sftp.listdir(remote_path)
            sftp.close()
            return [{"name": f} for f in files]
        except Exception as e:
            print(f"SFTP list failed: {e}")
            return []

    def delete(self, remote_path: str) -> bool:
        """删除 SFTP 文件"""
        sftp = self._get_client()
        if not sftp:
            return False
        try:
            sftp.remove(remote_path)
            sftp.close()
            return True
        except Exception:
            return False

    def exists(self, remote_path: str) -> bool:
        """检查 SFTP 文件是否存在"""
        sftp = self._get_client()
        if not sftp:
            return False
        try:
            sftp.stat(remote_path)
            sftp.close()
            return True
        except Exception:
            return False


class SambaAdapter(CloudAdapter):
    """Samba/NAS 适配器(使用 pysmb)"""

    def __init__(self, config: CloudConfig):
        super().__init__(config)
        self.host = config.credentials.get("host", "")
        self.port = int(config.credentials.get("port", 445))
        self.username = config.credentials.get("username", "")
        self.password = config.credentials.get("password", "")
        self.share = config.credentials.get("share", "memory")
        self.remote_path = config.credentials.get("remote_path", "/")
        self._conn = None

    def _get_connection(self):
        """获取 Samba 连接"""
        try:
            from smb.SMBConnection import SMBConnection

            if self._conn is None or not hasattr(self._conn, 'sock') or not self._conn.sock:
                self._conn = SMBConnection(
                    self.username,
                    self.password,
                    "openclaw",
                    self.host,
                    is_direct_tcp=True
                )
                self._conn.connect(self.host, self.port)

            return self._conn
        except ImportError:
            print("pysmb not installed. Run: pip install pysmb")
            return None
        except Exception as e:
            print(f"Samba connection failed: {e}")
            return None

    def upload(self, local_path: Path, remote_path: str) -> bool:
        """上传到 Samba/NAS"""
        conn = self._get_connection()
        if not conn:
            return False
        try:
            # 构造完整路径: remote_path + filename
            # remote_path like "/记忆", filename like "test.txt"
            # result: "/记忆/test.txt"
            full_path = f"{self.remote_path}/{remote_path}"
            with open(local_path, "rb") as f:
                conn.storeFile(self.share, full_path, f)
            return True
        except Exception as e:
            print(f"Samba upload failed: {e}")
            return False

    def download(self, remote_path: str, local_path: Path) -> bool:
        """从 Samba/NAS 下载"""
        conn = self._get_connection()
        if not conn:
            return False
        try:
            import io
            data = io.BytesIO()
            conn.retrieveFile(self.share, remote_path, data)
            data.seek(0)
            local_path.parent.mkdir(parents=True, exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(data.read())
            return True
        except Exception as e:
            print(f"Samba download failed: {e}")
            return False

    def list(self, remote_path: str = "/") -> List[Dict]:
        """列出 Samba 文件(部分NAS不支持QUERY_DIRECTORY)"""
        # 由于部分NAS的SMB实现不完整,list可能失败
        # 返回空列表,依赖exists检查
        return []

    def delete(self, remote_path: str) -> bool:
        """删除 Samba 文件"""
        conn = self._get_connection()
        if not conn:
            return False
        try:
            full_path = f"{self.remote_path}/{remote_path}"
            conn.deleteFiles(self.share, full_path)
            return True
        except Exception:
            return False

    def exists(self, remote_path: str) -> bool:
        """检查 Samba 文件是否存在（通过尝试读取）"""
        conn = self._get_connection()
        if not conn:
            return False
        try:
            import io
            full_path = f"{self.remote_path}/{remote_path}"
            data = io.BytesIO()
            conn.retrieveFile(self.share, full_path, data)
            return True
        except Exception:
            return False

    def close(self):
        """关闭连接"""
        if self._conn:
            try:
                self._conn.close()
            except:
                pass
            self._conn = None


# ============================================================================
# 适配器工厂
# ============================================================================

class AdapterFactory:
    """适配器工厂"""

    _adapters: Dict[str, CloudAdapter] = {}

    @classmethod
    def create_all(cls) -> Dict[str, CloudAdapter]:
        """从配置创建所有适配器"""
        configs = CloudSyncConfig.load_from_secrets()
        adapters = {}

        for name, config in configs.items():
            if not config.enabled:
                continue

            adapter = cls.create(config)
            if adapter:
                adapters[name] = adapter

        cls._adapters = adapters
        return adapters

    @classmethod
    def create(cls, config: CloudConfig) -> Optional[CloudAdapter]:
        """创建单个适配器"""
        provider = config.provider.lower()

        adapters = {
            "ima": IMAAdapter,
            "webdav": WebDAVAdapter,
            "s3": S3Adapter,
            "ftp": FTPAdapter,
            "sftp": SFTPAdapter,
            "samba": SambaAdapter,
        }

        adapter_class = adapters.get(provider)
        if adapter_class:
            return adapter_class(config)

        return None

    @classmethod
    def get_enabled(cls) -> Dict[str, CloudAdapter]:
        """获取所有已启用的适配器"""
        if not cls._adapters:
            cls.create_all()
        return cls._adapters


# ============================================================================
# 主函数
# ============================================================================

def main():
    """测试适配器"""
    print("🧪 云适配器测试")
    print("=" * 50)

    configs = CloudSyncConfig.load_from_secrets()

    if not configs:
        print("⚠️  未检测到云服务配置")
        print()
        print(CloudSyncConfig.get_config_template())
        return

    print(f"✅ 检测到 {len(configs)} 个云服务配置:\n")
    for name, config in configs.items():
        print(f"  - {name}: {config.provider}")

    print()
    print("📋 配置模板(供添加更多服务):")
    print(CloudSyncConfig.get_config_template())


if __name__ == "__main__":
    main()
