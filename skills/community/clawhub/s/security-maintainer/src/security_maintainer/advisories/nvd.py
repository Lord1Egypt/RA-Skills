"""
NIST National Vulnerability Database (NVD) API 2.0 Client.
Retrieves official CVSS v3.1/v4.0 scores, attack vectors, and vulnerability descriptions.
"""

from __future__ import annotations
import json
import logging
import urllib.request
import urllib.error
from typing import Dict, Any, Optional
from .cache import AdvisoryCache

logger = logging.getLogger(__name__)

DEFAULT_NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


class NvdClient:
    """Queries NIST NVD API to enrich CVEs with detailed CVSS metrics."""

    def __init__(self, config: Dict[str, Any], cache: AdvisoryCache, fixture_data: Optional[Dict[str, Any]] = None):
        self.config = config.get("advisories", {}).get("nvd", {})
        self.cache = cache
        self.fixture_data = fixture_data
        self.base_url = self.config.get("url", DEFAULT_NVD_URL)
        self.api_key = self.config.get("api_key")
        self.ttl_hours = self.config.get("cache_ttl_hours", 72)
        self.last_query_failed = False

    def get_cve_details(self, cve_id: str) -> Optional[Dict[str, Any]]:
        """Recupera CVSS score, vector y descripción para un CVE concreto."""
        if not cve_id or not cve_id.upper().startswith("CVE-"):
            return None

        cve_id = cve_id.upper()

        # 1. Modo fixtures
        if self.fixture_data and cve_id in self.fixture_data:
            return self.fixture_data[cve_id]

        # 2. Comprobar caché local
        cached, is_valid, _ = self.cache.get("nvd", cve_id, ttl_hours=self.ttl_hours)
        if cached and is_valid:
            return cached

        # 3. Consulta HTTP remota
        url = f"{self.base_url}?cveId={cve_id}"
        headers = {"User-Agent": "OpenClaw-SecurityMaintainer/1.0 (+https://openclaw.dev)"}
        if self.api_key:
            headers["apiKey"] = self.api_key

        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            vulnerabilities = data.get("vulnerabilities", [])
            if not vulnerabilities:
                return None

            cve_obj = vulnerabilities[0].get("cve", {})
            metrics = cve_obj.get("metrics", {})

            cvss_score = None
            cvss_vector = None
            severity = "UNKNOWN"

            # Intentar CVSS v3.1 -> v3.0 -> v4.0 -> v2
            if "cvssMetricV31" in metrics and metrics["cvssMetricV31"]:
                primary = metrics["cvssMetricV31"][0].get("cvssData", {})
                cvss_score = primary.get("baseScore")
                cvss_vector = primary.get("vectorString")
                severity = primary.get("baseSeverity", "UNKNOWN")
            elif "cvssMetricV40" in metrics and metrics["cvssMetricV40"]:
                primary = metrics["cvssMetricV40"][0].get("cvssData", {})
                cvss_score = primary.get("baseScore")
                cvss_vector = primary.get("vectorString")
                severity = primary.get("baseSeverity", "UNKNOWN")
            elif "cvssMetricV30" in metrics and metrics["cvssMetricV30"]:
                primary = metrics["cvssMetricV30"][0].get("cvssData", {})
                cvss_score = primary.get("baseScore")
                cvss_vector = primary.get("vectorString")
                severity = primary.get("baseSeverity", "UNKNOWN")

            desc = ""
            descriptions = cve_obj.get("descriptions", [])
            for d in descriptions:
                val = d.get("value", "")
                if val:
                    if not desc or d.get("lang") in ("en", "es"):
                        desc = val
                        if d.get("lang") in ("en", "es"):
                            break

            result = {
                "cve_id": cve_id,
                "cvss_score": float(cvss_score) if cvss_score is not None else None,
                "cvss_vector": cvss_vector,
                "severity": severity,
                "description": desc
            }

            self.cache.set("nvd", cve_id, result)
            return result

        except Exception as e:
            logger.debug(f"Error consultando NVD para {cve_id}: {e}")
            self.last_query_failed = True
            return cached # Fallback a caché expirada si existe
