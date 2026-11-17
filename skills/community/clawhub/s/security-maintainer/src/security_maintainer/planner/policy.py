"""
Evaluación de políticas de seguridad, exclusiones y restricciones de actualización.
"""

from __future__ import annotations
import re
from typing import Dict, Any, List, Optional, Tuple

from ..models import InventoryItem, FindingCategory, ManagerType


class PolicyEngine:
    """Verifica el cumplimiento de políticas locales antes de añadir una acción al plan."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.mode = config.get("mode", "ask")
        self.windows_cfg = config.get("windows", {})
        self.wsl_cfg = config.get("wsl", {})
        self.allow_major_upgrades = self.windows_cfg.get("allow_major_upgrades", False)
        self.allow_reboots = self.windows_cfg.get("allow_reboots", False) or self.wsl_cfg.get("allow_reboots", False)

    def is_action_permitted(self, item: InventoryItem, category: FindingCategory) -> Tuple[bool, Optional[str]]:
        """Determina si la actualización o remediación de un componente está permitida por política."""
        # 1. Comprobar si el paquete está excluido
        if item.environment.value == "windows":
            excluded = set(self.windows_cfg.get("excluded_packages", []))
            if item.id in excluded or item.name in excluded:
                return False, f"El paquete '{item.name}' está explícitamente excluido en la configuración de Windows."
        elif item.environment.value == "wsl":
            # Exclusiones específicas de la distro
            distro_name = item.target_name.replace("WSL:", "")
            distro_cfg = self.wsl_cfg.get("distributions", {}).get(distro_name, {})
            distro_excluded = set(distro_cfg.get("excluded_packages", []))
            if item.id in distro_excluded or item.name in distro_excluded:
                return False, f"El paquete '{item.name}' está excluido en la configuración de {distro_name}."

        # 2. Comprobar paquetes fijados (pinned)
        if item.is_pinned:
            return False, f"El paquete '{item.name}' está fijado (pinned) por el gestor de paquetes. No se actualiza sin desbloqueo manual."

        # 3. Comprobar si no es gestionable o requiere intervención manual
        if not item.update_mechanism_available or item.requires_manual_intervention:
            return False, f"El componente '{item.name}' no tiene un mecanismo de actualización automático soportado."

        # 4. Comprobar salto de versión mayor si está prohibido
        if not self.allow_major_upgrades and item.latest_version and item.installed_version:
            if self._is_major_upgrade(item.installed_version, item.latest_version):
                return False, (
                    f"Actualización a versión mayor bloqueada por política "
                    f"({item.installed_version} -> {item.latest_version}). Requiere 'allow_major_upgrades: true'."
                )

        return True, None

    def _is_major_upgrade(self, current: str, target: str) -> bool:
        """Detecta si target implica un cambio de versión mayor (ej. 2.1.0 -> 3.0.0)."""
        curr_m = re.match(r"^(\d+)", current)
        targ_m = re.match(r"^(\d+)", target)
        if curr_m and targ_m:
            try:
                curr_major = int(curr_m.group(1))
                targ_major = int(targ_m.group(1))
                return targ_major > curr_major
            except ValueError:
                pass
        return False
