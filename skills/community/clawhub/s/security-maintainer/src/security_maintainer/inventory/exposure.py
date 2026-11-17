"""
Exposure surface auditor and network process/port mapping module.
Correlates active listening sockets with installed software packages.
"""

from __future__ import annotations
import re
import shutil
import subprocess
import logging
from typing import Dict, Any, List, Optional, Set

logger = logging.getLogger(__name__)


class ExposureAuditor:
    """Detects active network listening ports and correlates them with installed packages."""

    def __init__(self, fixture_data: Optional[Dict[str, Any]] = None):
        self.fixture_data = fixture_data

    def audit_wsl_ports(self, distro_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Audits listening sockets (TCP/UDP) in Linux/WSL via 'ss -tulpn'."""
        if self.fixture_data and "wsl_ports" in self.fixture_data:
            return self.fixture_data["wsl_ports"]

        wsl_bin = shutil.which("wsl.exe") or shutil.which("wsl")
        cmd = []
        if wsl_bin and distro_name:
            cmd = [wsl_bin, "-d", distro_name, "-e", "bash", "-c", "ss -tulpn 2>/dev/null || netstat -tulpn 2>/dev/null"]
        elif shutil.which("ss"):
            cmd = ["ss", "-tulpn"]

        if not cmd:
            return []

        open_sockets = []
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if res.returncode == 0:
                for line in res.stdout.splitlines():
                    line = line.strip()
                    if not line or line.startswith("Netid") or line.startswith("Active"):
                        continue
                    parts = line.split()
                    if len(parts) >= 5:
                        proto = parts[0]
                        local_addr = parts[4] if "LISTEN" not in parts[1] else parts[3]
                        # Extraer proceso si está visible
                        proc_info = ""
                        for part in parts[5:]:
                            if "users:" in part:
                                proc_info = part
                                break

                        open_sockets.append({
                            "protocol": proto,
                            "local_address": local_addr,
                            "process_info": proc_info,
                            "is_public": not local_addr.startswith("127.") and not local_addr.startswith("[::1]")
                        })
        except Exception as e:
            logger.debug(f"Error analizando sockets en WSL: {e}")

        return open_sockets

    def is_package_exposed(self, pkg_name: str, open_sockets: List[Dict[str, Any]]) -> bool:
        """Determina si un paquete está asociado a un proceso escuchando en red."""
        pkg_lower = pkg_name.lower()
        for sock in open_sockets:
            p_info = sock.get("process_info", "").lower()
            if pkg_lower in p_info:
                return True
        return False
