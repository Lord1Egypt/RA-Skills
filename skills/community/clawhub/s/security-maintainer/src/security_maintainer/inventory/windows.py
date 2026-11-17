"""
Adaptador de inventario para el sistema anfitrión Windows.
"""

from __future__ import annotations
import json
import logging
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional

from ..models import (
    InventoryItem,
    EnvironmentType,
    ManagerType,
    CoverageSummary,
)

logger = logging.getLogger(__name__)

SCRIPT_PATH = Path(__file__).resolve().parent.parent.parent.parent / "scripts" / "windows" / "Get-WindowsInventory.ps1"


class WindowsInventoryAdapter:
    """Recopila el inventario de software de Windows de forma segura y determinista."""

    def __init__(self, config: Dict[str, Any], fixture_data: Optional[Dict[str, Any]] = None):
        self.config = config.get("windows", {})
        self.fixture_data = fixture_data
        self.excluded_packages = set(self.config.get("excluded_packages", []))
        self.allowed_packages = set(self.config.get("allowed_packages", []))

    @classmethod
    def get_powershell_bin(cls) -> Optional[str]:
        """Localiza powershell de forma agnóstica (nativo en Windows o a través de WSL)."""
        import os
        for candidate in ["powershell.exe", "pwsh.exe", "powershell", "pwsh"]:
            bin_path = shutil.which(candidate)
            if bin_path:
                return bin_path

        # Rutas estándar del anfitrión Windows cuando OpenClaw corre en WSL
        wsl_candidates = [
            "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
            "/mnt/c/Program Files/PowerShell/7/pwsh.exe",
            "/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
        ]
        for cp in wsl_candidates:
            p = Path(cp)
            if p.exists() and os.access(cp, os.X_OK):
                return str(p)

        return None

    def is_available(self) -> bool:
        """Comprueba si el entorno Windows es accesible (nativo o desde WSL vía powershell.exe)."""
        if self.fixture_data is not None:
            return True
        return self.get_powershell_bin() is not None

    def collect(self) -> List[InventoryItem]:
        """Obtiene la lista de componentes instalados en Windows."""
        raw_data = self._get_raw_data()
        if not raw_data:
            return []

        items: List[InventoryItem] = []
        target_name = "Windows Host"

        # 0. Registrar siempre el Sistema Operativo Anfitrión como componente evaluado
        os_info = raw_data.get("os_info") or {}
        caption = os_info.get("caption", "Microsoft Windows")
        build = os_info.get("build_number", "")
        os_ver = f"{caption} (Build {build})" if build else caption
        reboot_pending = raw_data.get("reboot_pending", False)
        upg_count = len(raw_data.get("winget_upgrades", [])) + len(raw_data.get("windows_updates_pending", []))

        os_notes = (
            f"Sistema anfitrión Windows al día (0 actualizaciones pendientes)."
            if upg_count == 0
            else f"Sistema anfitrión Windows ({upg_count} actualizaciones pendientes disponibles)."
        )
        if reboot_pending:
            os_notes += " [Reinicio pendiente requerido por el sistema]."

        items.append(
            InventoryItem(
                environment=EnvironmentType.WINDOWS,
                target_name=target_name,
                name="Sistema Operativo Windows",
                id="windows-host-os",
                installed_version=os_ver,
                manager=ManagerType.WINDOWS_UPDATE,
                is_supported=True,
                update_mechanism_available=True,
                requires_manual_intervention=False,
                notes=os_notes,
                extra_metadata={
                    "os_info": os_info,
                    "reboot_pending": reboot_pending
                }
            )
        )

        # 1. Aplicaciones detectadas por WinGet
        winget_upgrades = {u.get("id"): u for u in raw_data.get("winget_upgrades", [])}

        for upg in raw_data.get("winget_upgrades", []):
            pkg_id = upg.get("id", "")
            pkg_name = upg.get("name", pkg_id)
            if self._is_excluded(pkg_id, pkg_name):
                continue

            items.append(
                InventoryItem(
                    environment=EnvironmentType.WINDOWS,
                    target_name=target_name,
                    name=pkg_name,
                    id=pkg_id,
                    installed_version=upg.get("installed_version", "unknown"),
                    latest_version=upg.get("latest_version"),
                    manager=ManagerType.WINGET,
                    is_supported=True,
                    update_mechanism_available=True,
                    requires_manual_intervention=False,
                    extra_metadata={"source": upg.get("source", "winget")}
                )
            )

        # 2. Aplicaciones en Registro (desinstaladores de Windows)
        for reg in raw_data.get("registry_installed", []):
            reg_id = reg.get("id", "")
            reg_name = reg.get("name", reg_id)
            if self._is_excluded(reg_id, reg_name):
                continue

            # Si ya fue registrado por WinGet, evitar duplicar el gestor
            if any(item.id.lower() == reg_id.lower() or item.name.lower() == reg_name.lower() for item in items):
                continue

            # Software detectado solo en el registro: marcado para intervención manual
            items.append(
                InventoryItem(
                    environment=EnvironmentType.WINDOWS,
                    target_name=target_name,
                    name=reg_name,
                    id=reg_id,
                    installed_version=reg.get("installed_version", "desconocida"),
                    manager=ManagerType.REGISTRY,
                    is_supported=False,
                    update_mechanism_available=False,
                    requires_manual_intervention=True,
                    notes="Software sin mecanismo de actualización automática detectado (requiere instalador manual).",
                    extra_metadata={"publisher": reg.get("publisher"), "install_date": reg.get("install_date")}
                )
            )

        # 3. Windows Updates pendientes
        raw_wu = raw_data.get("windows_updates_pending", [])
        if isinstance(raw_wu, dict):
            raw_wu = [raw_wu]
        elif not isinstance(raw_wu, list):
            raw_wu = []

        for wu in raw_wu:
            title = wu.get("title", "")
            kb = wu.get("kb_articles", ["WindowsUpdate"])[0] if wu.get("kb_articles") else "WindowsUpdate"
            items.append(
                InventoryItem(
                    environment=EnvironmentType.WINDOWS,
                    target_name=target_name,
                    name=title,
                    id=kb,
                    installed_version="pending",
                    latest_version="available",
                    manager=ManagerType.WINDOWS_UPDATE,
                    is_supported=True,
                    update_mechanism_available=True,
                    requires_manual_intervention=False,
                    notes=f"Actualización del sistema acumulativa o de seguridad ({kb})",
                    extra_metadata={"is_mandatory": wu.get("is_mandatory", False), "severity": wu.get("severity")}
                )
            )

        return items

    def _is_excluded(self, pkg_id: str, pkg_name: str) -> bool:
        if pkg_id in self.excluded_packages or pkg_name in self.excluded_packages:
            return True
        if self.allowed_packages:
            return pkg_id not in self.allowed_packages and pkg_name not in self.allowed_packages
        return False

    def _get_raw_data(self) -> Optional[Dict[str, Any]]:
        if self.fixture_data is not None:
            return self.fixture_data

        ps_bin = self.get_powershell_bin()
        if not ps_bin or not SCRIPT_PATH.exists():
            logger.warning("PowerShell o script Get-WindowsInventory.ps1 no disponible.")
            return None

        try:
            with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
                script_code = f.read()

            cmd = [
                ps_bin,
                "-NoProfile",
                "-NonInteractive",
                "-ExecutionPolicy", "Bypass",
                "-Command", "-"
            ]

            res = subprocess.run(cmd, input=script_code.encode("utf-8"), capture_output=True, timeout=30)
            if res.returncode == 0 and res.stdout:
                stdout_str = None
                for enc in ["utf-8", "cp1252", "latin1", "cp850"]:
                    try:
                        stdout_str = res.stdout.decode(enc)
                        break
                    except UnicodeDecodeError:
                        continue
                if stdout_str is None:
                    stdout_str = res.stdout.decode("utf-8", errors="replace")

                stdout_str = stdout_str.strip()
                if stdout_str:
                    return json.loads(stdout_str)
            else:
                stderr_str = res.stderr.decode("utf-8", errors="replace") if res.stderr else ""
                logger.error(f"Error ejecutando script de inventario Windows: {stderr_str}")
        except Exception as e:
            logger.error(f"Excepción al recopilar inventario de Windows: {e}")
        return None
