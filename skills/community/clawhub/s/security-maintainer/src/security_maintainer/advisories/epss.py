"""
Cliente para el sistema EPSS (Exploit Prediction Scoring System) de FIRST.org.
Proporciona la probabilidad cuantitativa (0.0 a 1.0) y percentil de explotación en el corto plazo.
"""

from __future__ import annotations
import json
import logging
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from .cache import AdvisoryCache

logger = logging.getLogger(__name__)

DEFAULT_EPSS_URL = "https://api.first.org/data/v1/epss"


class EpssClient:
    """Consulta la API de FIRST.org para enriquecer CVEs con predicción de exploits (EPSS)."""

    def __init__(self, config: Dict[str, Any], cache: AdvisoryCache, fixture_data: Optional[Dict[str, Any]] = None):
        self.config = config.get("advisories", {}).get("epss", {})
        self.cache = cache
        self.fixture_data = fixture_data
        self.base_url = self.config.get("url", DEFAULT_EPSS_URL)
        self.ttl_hours = self.config.get("cache_ttl_hours", 24)
        self.last_query_failed = False

    def get_scores(self, cve_ids: List[str]) -> Dict[str, Dict[str, float]]:
        """
        Recupera el score EPSS y percentil para una lista de CVEs.
        Devuelve: { "CVE-XXXX-YYYY": { "epss": 0.8523, "percentile": 0.981 } }
        """
        if not cve_ids:
            return {}

        results: Dict[str, Dict[str, float]] = {}

        # 1. Modo pruebas / fixtures
        if self.fixture_data:
            for cve in cve_ids:
                if cve in self.fixture_data:
                    results[cve] = self.fixture_data[cve]
            return results

        # 2. Consultar primero la caché local
        missing: List[str] = []
        for cve in cve_ids:
            cached, is_valid, _ = self.cache.get("epss", cve, ttl_hours=self.ttl_hours)
            if cached and is_valid:
                results[cve] = cached
            else:
                missing.append(cve)

        if not missing:
            return results

        # 3. Consultar la API de FIRST en lotes de hasta 30 CVEs
        batch_size = 30
        for i in range(0, len(missing), batch_size):
            chunk = missing[i:i + batch_size]
            cve_param = ",".join(chunk)
            url = f"{self.base_url}?cve={cve_param}"

            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "OpenClaw-SecurityMaintainer/1.0 (+https://openclaw.dev)"}
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    payload = json.loads(resp.read().decode("utf-8"))

                if payload.get("status") == "OK" and "data" in payload:
                    for row in payload["data"]:
                        cve = row.get("cve")
                        try:
                            score = float(row.get("epss", 0.0))
                            perc = float(row.get("percentile", 0.0))
                            data = {"epss": score, "percentile": perc}
                            results[cve] = data
                            self.cache.set("epss", cve, data)
                        except (ValueError, TypeError):
                            pass
            except Exception as e:
                logger.debug(f"Error consultando API de FIRST EPSS para {chunk}: {e}")
                self.last_query_failed = True

        return results
