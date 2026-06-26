#!/usr/bin/env python3
"""
云备份凭证管理模块
统一从 ~/.openclaw/credentials/secrets.env 读取凭证
"""

import os
from pathlib import Path


def get_secrets_path() -> Path:
    """获取 secrets.env 路径"""
    return Path.home() / ".openclaw" / "credentials" / "secrets.env"


def load_secrets() -> dict:
    """加载 secrets.env 中的所有凭证"""
    secrets_file = get_secrets_path()
    secrets = {}
    
    if secrets_file.exists():
        for line in secrets_file.read_text().splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                secrets[key.strip()] = value.strip()
    
    return secrets


def get_ima_credentials() -> tuple:
    """获取 IMA 凭证 (client_id, api_key)"""
    secrets = load_secrets()
    
    client_id = os.environ.get("IMA_OPENAPI_CLIENTID") or secrets.get("IMA_OPENAPI_CLIENTID")
    api_key = os.environ.get("IMA_OPENAPI_APIKEY") or secrets.get("IMA_OPENAPI_APIKEY")
    
    # 回退到旧配置位置
    if not client_id or not api_key:
        config_dir = Path.home() / ".config" / "ima"
        if config_dir.exists():
            client_file = config_dir / "client_id"
            api_file = config_dir / "api_key"
            if client_file.exists():
                client_id = client_file.read_text().strip()
            if api_file.exists():
                api_key = api_file.read_text().strip()
    
    return client_id, api_key


def get_samba_credentials() -> dict:
    """获取 Samba 凭证"""
    secrets = load_secrets()
    
    return {
        "host": os.environ.get("SAMBA_HOST") or secrets.get("SAMBA_HOST", ""),
        "user": os.environ.get("SAMBA_USER") or secrets.get("SAMBA_USER", ""),
        "password": os.environ.get("SAMBA_PASS") or secrets.get("SAMBA_PASS", ""),
        "share": os.environ.get("SAMBA_SHARE") or secrets.get("SAMBA_SHARE", "/memory"),
    }


def get_export_dir() -> Path:
    """获取导出目录（cloud-backup 只能操作这个目录）"""
    return Path.home() / ".openclaw" / "workspace" / "memory" / "exports"


def ensure_export_dir() -> Path:
    """确保导出目录存在"""
    export_dir = get_export_dir()
    export_dir.mkdir(parents=True, exist_ok=True)
    return export_dir
