"""
Manejador de avisos oficiales de distribuciones Linux y parches retroportados (backports).
Evita falsos positivos causados por versiones fijadas por la distribución con parches aplicados.
"""

from __future__ import annotations
import re
import logging
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)


def parse_debian_version(version_str: str) -> Tuple[int, str, str]:
    """
    Descompone una versión Debian/Ubuntu en (epoch, upstream_version, debian_revision).
    Formato estándar: [epoch:]upstream_version[-debian_revision]
    """
    epoch = 0
    if ":" in version_str:
        epoch_part, rest = version_str.split(":", 1)
        if epoch_part.isdigit():
            epoch = int(epoch_part)
            version_str = rest

    if "-" in version_str:
        parts = version_str.rsplit("-", 1)
        upstream = parts[0]
        revision = parts[1]
    else:
        upstream = version_str
        revision = ""

    return epoch, upstream, revision


class DistroSecurityTracker:
    """Verifica si un paquete de Debian/Ubuntu incluye un parche retroportado para un CVE."""

    def __init__(self, fixture_data: Optional[Dict[str, Any]] = None):
        self.fixture_data = fixture_data

    def is_cve_backported_fixed(self, distro_id: str, pkg_name: str, installed_version: str, cve_id: str) -> bool:
        """
        Determina si el CVE ya fue subsanado mediante un parche retroportado en la versión instalada.
        """
        if self.fixture_data and "backports" in self.fixture_data:
            distro_backports = self.fixture_data["backports"].get(distro_id.lower(), {})
            pkg_data = distro_backports.get(pkg_name, {})
            fixed_rev = pkg_data.get(cve_id.upper())
            if fixed_rev:
                # Si la versión instalada es igual o posterior a la revisión corregida
                return self._compare_simple_revisions(installed_version, fixed_rev) >= 0

        # Patrones habituales de seguridad de Ubuntu (ej. 3.0.13-0ubuntu3.4 incluye parches de seguridad)
        if "ubuntu" in installed_version.lower() and ("security" in installed_version.lower() or "usn" in installed_version.lower()):
            # Marcador indicativo de compilación de canal de seguridad
            return True

        return False

    def _compare_simple_revisions(self, installed: str, fixed: str) -> int:
        """Comparación simple de cadenas de revisión."""
        if installed == fixed:
            return 0
        return 1 if installed > fixed else -1
