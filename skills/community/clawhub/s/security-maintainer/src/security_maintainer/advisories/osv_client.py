"""
Client for the OSV (Open Source Vulnerabilities, https://osv.dev) API with caching and retry logic.
"""

from __future__ import annotations
import json
import logging
import urllib.request
import urllib.error
import time
from typing import List, Dict, Any, Optional

from ..models import (
    InventoryItem,
    Vulnerability,
    SeverityLevel,
    ConfidenceLevel,
    EnvironmentType,
    ManagerType,
)
from .cache import AdvisoryCache
from .cisa_kev import CisaKevCatalog
from .distro_trackers import DistroSecurityTracker

logger = logging.getLogger(__name__)

OSV_QUERY_URL = "https://api.osv.dev/v1/query"


class OSVClient:
    """Queries known package vulnerabilities against the distributed OSV database."""

    def __init__(
        self,
        config: Dict[str, Any],
        cache: AdvisoryCache,
        kev_catalog: CisaKevCatalog,
        distro_tracker: DistroSecurityTracker,
        fixture_data: Optional[Dict[str, Any]] = None
    ):
        self.config = config.get("advisories", {}).get("osv", {})
        self.cache = cache
        self.kev = kev_catalog
        self.distro_tracker = distro_tracker
        self.fixture_data = fixture_data
        self.timeout = self.config.get("timeout_seconds", 15)
        self.max_retries = self.config.get("max_retries", 3)
        self.last_query_failed = False

    def query_vulnerabilities(self, item: InventoryItem) -> List[Vulnerability]:
        """Queries vulnerabilities for a target component and deduplicates advisory identifiers."""
        ecosystem = self._map_ecosystem(item)
        if not ecosystem:
            # Component does not map to an OSV ecosystem
            return []

        cache_key = f"{ecosystem}_{item.name}_{item.installed_version}"

        # 1. Check test fixtures
        if self.fixture_data and "osv" in self.fixture_data:
            mock_res = self.fixture_data["osv"].get(cache_key) or self.fixture_data["osv"].get(item.name)
            if mock_res is not None:
                return self._parse_osv_response(mock_res, item)

        # 2. Check local advisory cache
        cached_data, is_valid, age = self.cache.get("osv", cache_key, ttl_hours=12)
        if cached_data and is_valid:
            return self._parse_osv_response(cached_data, item)

        # 3. Perform network query with exponential retries
        payload = {
            "version": item.installed_version,
            "package": {
                "name": item.name,
                "ecosystem": ecosystem
            }
        }

        raw_resp = self._execute_request(payload)
        if raw_resp is not None:
            self.cache.set("osv", cache_key, raw_resp)
            self.last_query_failed = False
            return self._parse_osv_response(raw_resp, item)
        else:
            self.last_query_failed = True
            if cached_data:
                logger.info(f"Using cached advisory data for {item.name} due to network unreachable.")
                return self._parse_osv_response(cached_data, item)
            return []

    def _execute_request(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "OpenClaw-SecurityMaintainer/1.0 (+https://openclaw.dev)"
        }
        for attempt in range(self.max_retries):
            try:
                req = urllib.request.Request(OSV_QUERY_URL, data=body, headers=headers)
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    if resp.status == 200:
                        return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as he:
                if he.code == 404:
                    return {"vulns": []}
                logger.warning(f"HTTP error querying OSV ({he.code}): attempt {attempt+1}/{self.max_retries}")
            except Exception as e:
                logger.warning(f"Connection failure connecting to OSV: {e} (attempt {attempt+1}/{self.max_retries})")
            time.sleep(1.0 * (attempt + 1))
        return None

    def _map_ecosystem(self, item: InventoryItem) -> Optional[str]:
        if item.manager == ManagerType.NODE_ENV or item.id.startswith("npm:"):
            return "npm"
        if item.manager == ManagerType.PYTHON_ENV or item.id.startswith("pypi:"):
            return "PyPI"
        if item.environment == EnvironmentType.WSL:
            # Distro Linux
            if "ubuntu" in item.target_name.lower():
                return "Ubuntu"
            elif "debian" in item.target_name.lower():
                return "Debian"
            return "Linux"
        return None

    def _parse_osv_response(self, data: Dict[str, Any], item: InventoryItem) -> List[Vulnerability]:
        vulns_data = data.get("vulns", [])
        results: List[Vulnerability] = []
        seen_cves: set = set()

        for v in vulns_data:
            primary_id = v.get("id", "")
            aliases = v.get("aliases", [])
            all_ids = [primary_id] + aliases

            # Extraer identificador CVE si existe
            cve_candidates = [i for i in all_ids if i.startswith("CVE-")]
            cve_id = cve_candidates[0] if cve_candidates else primary_id

            if cve_id in seen_cves:
                continue
            seen_cves.add(cve_id)

            # Comprobar si aplica parche retroportado de distribución
            if item.environment == EnvironmentType.WSL:
                distro_id = "ubuntu" if "ubuntu" in item.target_name.lower() else "debian"
                if self.distro_tracker.is_cve_backported_fixed(distro_id, item.name, item.installed_version, cve_id):
                    logger.debug(f"CVE {cve_id} subsanado por parche retroportado en {item.name} {item.installed_version}")
                    continue

            # Comprobar presencia en CISA KEV
            in_kev, kev_info = self.kev.check_cve(cve_id)

            # Severidad
            severity = SeverityLevel.UNKNOWN
            cvss_val = None
            if in_kev:
                severity = SeverityLevel.CRITICAL
            else:
                for sev in v.get("severity", []):
                    if sev.get("type") == "CVSS_V3":
                        score_str = sev.get("score", "")
                        # Parse CVSS score or severity text
                        if "AV:" in score_str:
                            severity = SeverityLevel.HIGH # Score estándar CVSS3
                        break
                if severity == SeverityLevel.UNKNOWN and v.get("database_specific", {}).get("severity"):
                    s_str = str(v["database_specific"]["severity"]).upper()
                    if s_str in SeverityLevel.__members__:
                        severity = SeverityLevel[s_str]

            # Versión que corrige
            fixed_version = None
            for affected in v.get("affected", []):
                for rng in affected.get("ranges", []):
                    for evt in rng.get("events", []):
                        if "fixed" in evt:
                            fixed_version = evt["fixed"]
                            break

            evidence_txt = f"Vulnerabilidad registrada en OSV ({primary_id})."
            if in_kev:
                evidence_txt += f" Confirmada en CISA KEV (Fecha límite: {kev_info.get('due_date')})."

            results.append(
                Vulnerability(
                    cve_id=cve_id,
                    aliases=aliases,
                    title=v.get("summary", ""),
                    summary=v.get("details", "")[:300] if v.get("details") else "",
                    severity=severity,
                    cvss_score=cvss_val,
                    in_cisa_kev=in_kev,
                    cisa_due_date=kev_info.get("due_date") if in_kev and kev_info else None,
                    fixed_version=fixed_version,
                    source="OSV + CISA KEV" if in_kev else "OSV",
                    confidence=ConfidenceLevel.CONFIRMED,
                    evidence=evidence_txt
                )
            )

        return results
