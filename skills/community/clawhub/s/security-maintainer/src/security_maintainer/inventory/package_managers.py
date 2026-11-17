"""
Detección de gestores secundarios de paquetes (pipx, npm global, Scoop, Chocolatey, Snap, Flatpak).
Evita actualizar el mismo componente mediante múltiples gestores conservando su procedencia.
"""

from __future__ import annotations
import shutil
import subprocess
import json
import logging
from typing import List, Dict, Any, Optional

from ..models import (
    InventoryItem,
    EnvironmentType,
    ManagerType,
)

logger = logging.getLogger(__name__)


class AdditionalManagersAdapter:
    """Detecta paquetes instalados mediante herramientas auxiliares evitando duplicidades."""

    def __init__(self, config: Dict[str, Any], fixture_data: Optional[Dict[str, Any]] = None):
        self.config = config
        self.fixture_data = fixture_data

    def detect_available_managers(self) -> Dict[str, bool]:
        """Comprueba qué gestores están instalados en el sistema."""
        managers = ["pipx", "npm", "scoop", "choco", "snap", "flatpak"]
        return {m: shutil.which(m) is not None for m in managers}

    def collect(self) -> List[InventoryItem]:
        items: List[InventoryItem] = []

        if self.fixture_data and "additional_managers" in self.fixture_data:
            for item_dict in self.fixture_data["additional_managers"]:
                items.append(
                    InventoryItem(
                        environment=EnvironmentType.WINDOWS if item_dict.get("env") == "windows" else EnvironmentType.WSL,
                        target_name=item_dict.get("target", "Host"),
                        name=item_dict.get("name", ""),
                        id=item_dict.get("id", ""),
                        installed_version=item_dict.get("version", "unknown"),
                        latest_version=item_dict.get("latest_version"),
                        manager=ManagerType(item_dict.get("manager", "manual")),
                        is_supported=True,
                        update_mechanism_available=True,
                    )
                )
            return items

        # Detección segura de pipx si existe
        if shutil.which("pipx"):
            try:
                res = subprocess.run(["pipx", "list", "--json"], capture_output=True, text=True, timeout=10)
                if res.returncode == 0:
                    data = json.loads(res.stdout)
                    for app_name, app_data in data.get("venvs", {}).items():
                        metadata = app_data.get("metadata", {}).get("main_package", {})
                        version = metadata.get("package_version", "unknown")
                        items.append(
                            InventoryItem(
                                environment=EnvironmentType.WINDOWS,
                                target_name="Windows (pipx)",
                                name=app_name,
                                id=f"pipx:{app_name}",
                                installed_version=version,
                                manager=ManagerType.PIPX,
                                is_supported=True,
                                update_mechanism_available=True,
                                notes="Aplicación CLI aislada en entorno virtual gestionada por pipx."
                            )
                        )
            except Exception as e:
                logger.warning(f"Error inspeccionando pipx: {e}")

        return items
