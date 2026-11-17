"""
Cliente del catálogo CISA KEV (Known Exploited Vulnerabilities).
"""

from __future__ import annotations
import json
import logging
import re
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, Optional, Set, Tuple, List
from .cache import AdvisoryCache
from ..models import Vulnerability, SeverityLevel, ConfidenceLevel, InventoryItem

logger = logging.getLogger(__name__)

DEFAULT_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"


class CisaKevCatalog:
    """Consulta y almacena en caché el catálogo CISA KEV oficial."""

    def __init__(self, config: Dict[str, Any], cache: AdvisoryCache, fixture_data: Optional[Dict[str, Any]] = None):
        self.config = config.get("advisories", {}).get("cisa_kev", {})
        self.cache = cache
        self.fixture_data = fixture_data
        self.url = self.config.get("url", DEFAULT_KEV_URL)
        self.ttl_hours = self.config.get("cache_ttl_hours", 24)
        self._kev_map: Dict[str, Dict[str, Any]] = {}
        self._raw_catalog: List[Dict[str, Any]] = []
        self.last_sync_success = False

    def load(self) -> bool:
        """Carga el catálogo desde fixtures, caché local o consulta HTTP."""
        if self.fixture_data:
            self._parse_catalog(self.fixture_data)
            self.last_sync_success = True
            return True

        # Comprobar caché local
        cached_data, is_valid, age = self.cache.get("cisa_kev", "catalog", ttl_hours=self.ttl_hours)
        if cached_data and is_valid:
            self._parse_catalog(cached_data)
            self.last_sync_success = True
            return True

        # 1. Descargar catálogo oficial con timeout vía urllib
        data = self._fetch_remote()
        if data:
            self._parse_catalog(data)
            self.cache.set("cisa_kev", "catalog", data)
            self.last_sync_success = True
            return True

        # 2. Si falla la red, usar caché existente aunque esté expirada
        if cached_data:
            logger.info("Utilizando catálogo CISA KEV previo almacenado en la caché local.")
            self._parse_catalog(cached_data)
            self.last_sync_success = True
            return True

        # 3. Fallback a snapshot offline embebido en el paquete
        embedded_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "cisa_kev_bundle.json"
        if embedded_path.exists():
            try:
                with open(embedded_path, "r", encoding="utf-8") as f:
                    embedded_data = json.load(f)
                self._parse_catalog(embedded_data)
                logger.info("Utilizando snapshot CISA KEV local embebido (modo resiliencia offline).")
                self.last_sync_success = True
                return True
            except Exception as e:
                logger.warning(f"Error cargando bundle embebido de CISA KEV: {e}")

        self.last_sync_success = False
        return False

    def _fetch_remote(self) -> Optional[Dict[str, Any]]:
        """Downloads official CISA KEV catalog via urllib."""
        try:
            req = urllib.request.Request(
                self.url,
                headers={"User-Agent": "OpenClaw-SecurityMaintainer/1.0 (+https://openclaw.dev)"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            logger.debug(f"urllib request failed for CISA KEV: {e}")
            return None

    def _parse_catalog(self, data: Dict[str, Any]) -> None:
        vulnerabilities = data.get("vulnerabilities", [])
        self._raw_catalog = vulnerabilities
        self._kev_map.clear()
        for v in vulnerabilities:
            cve_id = v.get("cveID")
            if cve_id:
                self._kev_map[cve_id.upper()] = {
                    "due_date": v.get("dueDate"),
                    "vulnerability_name": v.get("vulnerabilityName"),
                    "action": v.get("requiredAction"),
                    "date_added": v.get("dateAdded")
                }

    def check_cve(self, cve_id: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Comprueba si un CVE está activamente explotado en el catálogo KEV."""
        if not self._kev_map:
            self.load()
        info = self._kev_map.get(cve_id.upper())
        return (True, info) if info else (False, None)

    def find_vulnerabilities_for_item(self, item: InventoryItem, max_results: int = 5) -> List[Vulnerability]:
        """Busca vulnerabilidades activas en CISA KEV correlacionadas con el producto."""
        if not self._raw_catalog:
            if not self._kev_map:
                self.load()
            if not self._raw_catalog:
                return []

        name_lower = item.name.lower()
        stopwords = {
            "release", "plus", "profesional", "professional", "edition", "x64", "x86", "64bit", "desktop",
            "software", "client", "app", "version", "community", "corporation", "sistema", "operativo", "windows"
        }
        raw_tokens = re.split(r'[\s\-_\(\)\.\:]+', name_lower)
        keywords = [t for t in raw_tokens if len(t) >= 4 and t not in stopwords]
        if not keywords:
            return []

        matches: List[Dict[str, Any]] = []
        for v in self._raw_catalog:
            prod = v.get("product", "").lower()
            matched = False
            for kw in keywords:
                if kw == prod or prod == kw or (len(kw) >= 5 and (kw in prod or prod in kw)):
                    matched = True
                    break
            if matched:
                matches.append(v)

        matches.sort(key=lambda x: x.get("dateAdded", ""), reverse=True)
        results: List[Vulnerability] = []
        for v in matches[:max_results]:
            cve_id = v.get("cveID", "").upper()
            results.append(
                Vulnerability(
                    cve_id=cve_id,
                    title=v.get("vulnerabilityName", f"Vulnerabilidad conocida en {v.get('product')}"),
                    summary=v.get("shortDescription", ""),
                    severity=SeverityLevel.CRITICAL,
                    confidence=ConfidenceLevel.CONFIRMED,
                    in_cisa_kev=True,
                    cisa_due_date=v.get("dueDate"),
                    source="CISA KEV",
                    evidence=f"Explotación activa reportada en CISA KEV ({v.get('product')}). Acción requerida: {v.get('requiredAction', 'Actualizar software')}."
                )
            )
        return results
