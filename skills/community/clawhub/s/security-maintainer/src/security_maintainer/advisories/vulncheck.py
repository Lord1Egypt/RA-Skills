"""
Cliente para el catálogo VulnCheck KEV (Community Edition).
Extiende CISA KEV detectando tempranamente vulnerabilidades explotadas en ransomware, botnets y exploits armados.
"""

from __future__ import annotations
import json
import logging
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, Optional, Set
from .cache import AdvisoryCache

logger = logging.getLogger(__name__)

DEFAULT_VULNCHECK_URL = "https://raw.githubusercontent.com/vulncheck/vulncheck-kev-community/main/vulncheck-kev.json"


class VulnCheckKevCatalog:
    """Consulta y gestiona el catálogo comunitario de exploits activos de VulnCheck."""

    def __init__(self, config: Dict[str, Any], cache: AdvisoryCache, fixture_data: Optional[Dict[str, Any]] = None):
        self.config = config.get("advisories", {}).get("vulncheck", {})
        self.cache = cache
        self.fixture_data = fixture_data
        self.url = self.config.get("url", DEFAULT_VULNCHECK_URL)
        self.ttl_hours = self.config.get("cache_ttl_hours", 24)
        self._vuln_map: Dict[str, Dict[str, Any]] = {}
        self.last_sync_success = False

    def load(self) -> bool:
        """Carga el catálogo de VulnCheck desde fixtures, caché o remoto con fallback offline."""
        if self.fixture_data:
            self._parse_catalog(self.fixture_data)
            self.last_sync_success = True
            return True

        # Comprobar caché local
        cached, is_valid, _ = self.cache.get("vulncheck", "catalog", ttl_hours=self.ttl_hours)
        if cached and is_valid:
            self._parse_catalog(cached)
            self.last_sync_success = True
            return True

        # Intentar descarga remota
        data = self._fetch_remote()
        if data:
            self._parse_catalog(data)
            self.cache.set("vulncheck", "catalog", data)
            self.last_sync_success = True
            return True

        # Si falla la red, usar caché expirada
        if cached:
            self._parse_catalog(cached)
            self.last_sync_success = True
            return True

        # Fallback a snapshot offline embebido
        embedded_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "vulncheck_kev_bundle.json"
        if embedded_path.exists():
            try:
                with open(embedded_path, "r", encoding="utf-8") as f:
                    self._parse_catalog(json.load(f))
                self.last_sync_success = True
                return True
            except Exception as e:
                logger.debug(f"Error cargando bundle embebido VulnCheck: {e}")

        self.last_sync_success = False
        return False

    def _fetch_remote(self) -> Optional[Dict[str, Any]]:
        try:
            req = urllib.request.Request(
                self.url,
                headers={"User-Agent": "OpenClaw-SecurityMaintainer/1.0 (+https://openclaw.dev)"}
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            logger.debug(f"Error descargando VulnCheck KEV: {e}")
            return None

    def _parse_catalog(self, data: Any):
        self._vuln_map = {}
        items = []
        if isinstance(data, dict):
            items = data.get("data", data.get("vulnerabilities", []))
        elif isinstance(data, list):
            items = data

        for v in items:
            cve = v.get("cve", v.get("cveID"))
            if cve:
                if isinstance(cve, list):
                    for c in cve:
                        self._vuln_map[c.upper()] = v
                else:
                    self._vuln_map[cve.upper()] = v

    def is_in_vulncheck_kev(self, cve_id: str) -> bool:
        return cve_id.upper() in self._vuln_map

    def get_details(self, cve_id: str) -> Optional[Dict[str, Any]]:
        return self._vuln_map.get(cve_id.upper())
