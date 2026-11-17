"""
Adaptador de inventario para distribuciones WSL y la plataforma WSL.
"""

from __future__ import annotations
import json
import logging
import re
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from ..models import (
    InventoryItem,
    EnvironmentType,
    ManagerType,
)

logger = logging.getLogger(__name__)

SCRIPT_PATH = Path(__file__).resolve().parent.parent.parent.parent / "scripts" / "wsl" / "inspect_wsl.sh"


class WSLInventoryAdapter:
    """Inspecciona el subsistema WSL y sus distribuciones de forma segura."""

    def __init__(self, config: Dict[str, Any], fixture_data: Optional[Dict[str, Any]] = None):
        self.config = config.get("wsl", {})
        self.fixture_data = fixture_data
        self.auto_start = self.config.get("auto_start_stopped_distros", False)
        self.distro_configs = self.config.get("distributions", {})

    def is_available(self) -> bool:
        if self.fixture_data is not None:
            return True
        return (shutil.which("wsl.exe") is not None or
                shutil.which("wsl") is not None or
                Path("/etc/os-release").exists())

    def get_wsl_host_status(self) -> Dict[str, str]:
        """Obtiene la versión de la plataforma WSL y su kernel."""
        if self.fixture_data and "wsl_host_status" in self.fixture_data:
            return self.fixture_data["wsl_host_status"]

        wsl_bin = shutil.which("wsl.exe") or shutil.which("wsl")
        if not wsl_bin:
            # Si estamos dentro de WSL, leer el kernel desde uname
            try:
                res = subprocess.run(["uname", "-r"], capture_output=True, text=True, timeout=5)
                if res.returncode == 0:
                    return {"platform": "WSL 2 (Local)", "kernel_version": res.stdout.strip(), "status": "activo"}
            except Exception:
                pass
            return {"platform": "WSL", "kernel_version": "desconocida", "status": "no_disponible"}

        try:
            res = subprocess.run([wsl_bin, "--status"], capture_output=True, timeout=10)
            text = self._decode_wsl_output(res.stdout)
            kernel_match = re.search(r"kernel.*:\s*([0-9\.\-]+)", text, re.IGNORECASE)
            kernel = kernel_match.group(1) if kernel_match else "detectado"
            return {"platform": "WSL 2", "kernel_version": kernel, "status": "activo"}
        except Exception as e:
            logger.warning(f"No se pudo consultar 'wsl --status': {e}")
            return {"platform": "WSL", "kernel_version": "desconocida", "status": "error"}

    def list_distributions(self) -> List[Dict[str, Any]]:
        """Lista las distribuciones instaladas, su estado (Running/Stopped) y versión WSL."""
        if self.fixture_data and "distros" in self.fixture_data:
            return self.fixture_data["distros"]

        wsl_bin = shutil.which("wsl.exe") or shutil.which("wsl")
        if not wsl_bin:
            # Si se ejecuta nativamente dentro de WSL, auto-descubrir la distribución actual
            distro_name = "LocalWSL"
            if Path("/etc/os-release").exists():
                try:
                    with open("/etc/os-release", "r", encoding="utf-8") as f:
                        for line in f:
                            if line.startswith("NAME="):
                                distro_name = line.split("=", 1)[1].strip().strip('"')
                                break
                except Exception:
                    pass
            return [{
                "name": distro_name,
                "state": "Running",
                "version": "2"
            }]

        try:
            res = subprocess.run([wsl_bin, "-l", "-v"], capture_output=True, timeout=10)
            text = self._decode_wsl_output(res.stdout)
            distros = []
            for line in text.splitlines():
                line = line.strip()
                if not line or "NAME" in line or "---" in line:
                    continue
                # Las distros suelen tener formato: [*] Name State Version
                parts = line.replace("*", "").split()
                if len(parts) >= 3:
                    distros.append({
                        "name": parts[0],
                        "state": parts[1], # "Running" o "Stopped"
                        "version": parts[2]
                    })
            return distros
        except Exception as e:
            logger.error(f"Error listando distribuciones WSL: {e}")
            return []

    def collect(self) -> List[InventoryItem]:
        """Inspecciona las distribuciones permitidas."""
        items: List[InventoryItem] = []
        distros = self.list_distributions()

        for d in distros:
            distro_name = d["name"]
            distro_state = d["state"]

            # Si la distribución está configurada específicamente y deshabilitada, omitir
            if distro_name in self.distro_configs and not self.distro_configs[distro_name].get("enabled", True):
                continue

            # Respetar política de no iniciar distribuciones detenidas
            if distro_state.lower() != "running" and not self.auto_start:
                items.append(
                    InventoryItem(
                        environment=EnvironmentType.WSL,
                        target_name=f"WSL:{distro_name}",
                        name=f"Distribución {distro_name}",
                        id=f"wsl-distro-{distro_name}",
                        installed_version=f"WSL v{d.get('version', '2')}",
                        manager=ManagerType.MANUAL,
                        is_supported=False,
                        update_mechanism_available=False,
                        requires_manual_intervention=True,
                        notes="Distribución detenida. No se arranca sin política explícita (auto_start_stopped_distros: true)."
                    )
                )
                continue

            # Inspeccionar paquetes de la distribución activa
            distro_items = self._inspect_active_distro(distro_name)
            items.extend(distro_items)

        return items

    def _inspect_active_distro(self, distro_name: str) -> List[InventoryItem]:
        items: List[InventoryItem] = []
        raw = self._get_distro_raw_info(distro_name)
        if not raw:
            return items

        os_id = raw.get("os_id", "linux")
        pkg_manager_str = raw.get("pkg_manager", "apt")
        manager = ManagerType.APT if pkg_manager_str == "apt" else ManagerType.DPKG

        distro_cfg = self.distro_configs.get(distro_name, {})
        security_only = distro_cfg.get("security_updates_only", True)
        excluded = set(distro_cfg.get("excluded_packages", []))

        # Registrar siempre el sistema base de la distribución como componente inventariado
        distro_ver = raw.get("distro_version") or "Linux"
        all_upgrades = raw.get("upgrades", [])
        status_note = (
            f"Sistema base gestionado por {pkg_manager_str}. Al día (0 actualizaciones pendientes)."
            if not all_upgrades
            else f"Sistema base gestionado por {pkg_manager_str} ({len(all_upgrades)} actualizaciones disponibles)."
        )
        items.append(
            InventoryItem(
                environment=EnvironmentType.WSL,
                target_name=f"WSL:{distro_name}",
                name=f"Sistema Base ({distro_name})",
                id=f"wsl-base-{distro_name.lower().replace(' ', '-')}",
                installed_version=distro_ver,
                manager=manager,
                is_supported=True,
                update_mechanism_available=True,
                requires_manual_intervention=False,
                notes=status_note,
                extra_metadata={
                    "distro": distro_name,
                    "pkg_manager": pkg_manager_str,
                    "upgrades_pending": len(all_upgrades)
                }
            )
        )

        for upg in raw.get("upgrades", []):
            pkg_name = upg.get("name", "")
            is_sec = upg.get("is_security", False)

            if pkg_name in excluded:
                continue

            if security_only and not is_sec:
                continue

            items.append(
                InventoryItem(
                    environment=EnvironmentType.WSL,
                    target_name=f"WSL:{distro_name}",
                    name=pkg_name,
                    id=pkg_name,
                    installed_version=upg.get("installed_version", "current"),
                    latest_version=upg.get("target_version"),
                    manager=manager,
                    is_supported=True,
                    update_mechanism_available=True,
                    requires_manual_intervention=False,
                    notes="Actualización de seguridad oficial de la distribución" if is_sec else "Actualización general de paquete disponible",
                    extra_metadata={
                        "distro": distro_name,
                        "source": upg.get("source", ""),
                        "is_security": is_sec
                    }
                )
            )

        return items

    def _get_distro_raw_info(self, distro_name: str) -> Optional[Dict[str, Any]]:
        if self.fixture_data and "distro_inspect" in self.fixture_data:
            return self.fixture_data["distro_inspect"].get(distro_name)

        wsl_bin = shutil.which("wsl.exe") or shutil.which("wsl")
        raw_cmd = "apt-get -s dist-upgrade 2>/dev/null"
        if wsl_bin:
            cmd = [wsl_bin, "-d", distro_name, "-e", "bash", "-c", raw_cmd]
        elif shutil.which("bash"):
            cmd = ["bash", "-c", raw_cmd]
        else:
            return None

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
            upgrades = []
            if res.returncode == 0 and res.stdout.strip():
                # Formato típico:
                # Inst libaudit1 [1:3.1.2-2.1build1.1] (1:3.1.2-2.1ubuntu0.1 Ubuntu:24.04/noble-updates [amd64])
                # Inst krb5-locales [1.20.1-6ubuntu2.8] (1.20.1-6ubuntu2.10 Ubuntu:24.04/noble-updates [all])
                pattern = re.compile(r"^Inst\s+([^\s]+)\s+\[([^\]]+)\]\s+\(([^ \)]+)\s+([^ \)]+)", re.MULTILINE)
                for match in pattern.finditer(res.stdout):
                    pkg = match.group(1)
                    current_ver = match.group(2)
                    target_ver = match.group(3)
                    source = match.group(4)
                    is_sec = "security" in source.lower()
                    upgrades.append({
                        "name": pkg,
                        "id": pkg,
                        "installed_version": current_ver,
                        "target_version": target_ver,
                        "source": source,
                        "is_security": is_sec
                    })

            distro_version = distro_name
            if Path("/etc/os-release").exists():
                try:
                    with open("/etc/os-release", "r", encoding="utf-8") as f:
                        for line in f:
                            if line.startswith("PRETTY_NAME="):
                                distro_version = line.split("=", 1)[1].strip().strip('"')
                                break
                except Exception:
                    pass

            return {
                "os_id": "ubuntu",
                "pkg_manager": "apt",
                "upgrades": upgrades,
                "distro_version": distro_version
            }
        except Exception as e:
            logger.warning(f"Error inspeccionando distribución {distro_name}: {e}")
        return None

    def _decode_wsl_output(self, raw_bytes: bytes) -> str:
        """Decodifica salida de wsl.exe manejando UTF-16LE de Windows y eliminando caracteres nulos."""
        if not raw_bytes:
            return ""
        try:
            return raw_bytes.decode("utf-16-le").replace("\x00", "")
        except UnicodeDecodeError:
            try:
                return raw_bytes.decode("utf-8", errors="replace").replace("\x00", "")
            except Exception:
                return ""
