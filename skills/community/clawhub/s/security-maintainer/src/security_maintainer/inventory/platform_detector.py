"""
Detector inteligente de plataforma, entorno de montaje y sistema operativo anfitrión.
Distingue si OpenClaw corre en WSL, contenedor Docker o anfitrión nativo (Windows, macOS, Linux).
"""

from __future__ import annotations
import sys
import os
import shutil
import subprocess
from pathlib import Path
from enum import Enum
from typing import Dict, Any, Tuple


class RuntimeMountType(str, Enum):
    WSL = "wsl"
    DOCKER = "docker"
    NATIVE = "native"


class HostOSType(str, Enum):
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"


class PlatformDetector:
    """Identifica el entorno de ejecución de OpenClaw y el sistema operativo del anfitrión."""

    @staticmethod
    def detect() -> Dict[str, Any]:
        mount_type = PlatformDetector._detect_mount_type()
        host_os = PlatformDetector._detect_host_os(mount_type)

        return {
            "mount_type": mount_type.value,
            "host_os": host_os.value,
            "platform_raw": sys.platform,
            "description": PlatformDetector._get_description(mount_type, host_os)
        }

    @staticmethod
    def _detect_mount_type() -> RuntimeMountType:
        # 1. Comprobar WSL
        if sys.platform.startswith("linux"):
            proc_version = Path("/proc/version")
            if proc_version.exists():
                try:
                    content = proc_version.read_text(encoding="utf-8").lower()
                    if "microsoft" in content or "wsl" in content:
                        return RuntimeMountType.WSL
                except Exception:
                    pass

        # 2. Comprobar Docker / Contenedor
        if Path("/.dockerenv").exists():
            return RuntimeMountType.DOCKER

        # 3. Nativo
        return RuntimeMountType.NATIVE

    @staticmethod
    def _detect_host_os(mount_type: RuntimeMountType) -> HostOSType:
        if mount_type == RuntimeMountType.WSL:
            # Si OpenClaw está en WSL, el anfitrión siempre es Windows
            return HostOSType.WINDOWS

        if sys.platform == "darwin":
            return HostOSType.MACOS

        if sys.platform == "win32":
            return HostOSType.WINDOWS

        return HostOSType.LINUX

    @staticmethod
    def _get_description(mount_type: RuntimeMountType, host_os: HostOSType) -> str:
        if mount_type == RuntimeMountType.WSL and host_os == HostOSType.WINDOWS:
            return "OpenClaw montado en WSL sobre anfitrión Windows"
        elif mount_type == RuntimeMountType.DOCKER:
            return f"OpenClaw montado en contenedor Docker sobre anfitrión {host_os.value.capitalize()}"
        elif host_os == HostOSType.MACOS:
            return "OpenClaw montado directamente en macOS (Apple Mac)"
        elif host_os == HostOSType.WINDOWS:
            return "OpenClaw montado directamente en Windows nativo"
        else:
            return "OpenClaw montado directamente en Linux nativo (Bare-metal o VM)"
