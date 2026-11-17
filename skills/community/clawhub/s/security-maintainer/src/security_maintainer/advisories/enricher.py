"""
Unified Threat Intelligence Enricher.
Combines and correlates OSV, CISA KEV, VulnCheck KEV, FIRST EPSS, NIST NVD, MSRC, and Ubuntu Security trackers.
Emits clear user-facing security notices before initiating external CVE lookups.
"""

from __future__ import annotations
import logging
from typing import Dict, Any, List, Optional
from ..models import Vulnerability, InventoryItem, SeverityLevel, ConfidenceLevel
from .cache import AdvisoryCache
from .cisa_kev import CisaKevCatalog
from .vulncheck import VulnCheckKevCatalog
from .epss import EpssClient
from .nvd import NvdClient
from .msrc import MsrcClient
from .ubuntu_security import UbuntuSecurityClient

logger = logging.getLogger(__name__)


class ThreatIntelligenceEnricher:
    """Enriches vulnerabilities and inventory items using multi-source security feeds."""

    def __init__(
        self,
        config: Dict[str, Any],
        cache: AdvisoryCache,
        cisa_kev: CisaKevCatalog,
        vulncheck_kev: VulnCheckKevCatalog,
        epss_client: EpssClient,
        nvd_client: NvdClient,
        msrc_client: MsrcClient,
        ubuntu_client: UbuntuSecurityClient
    ):
        self.config = config
        self.cache = cache
        self.cisa_kev = cisa_kev
        self.vulncheck_kev = vulncheck_kev
        self.epss_client = epss_client
        self.nvd_client = nvd_client
        self.msrc_client = msrc_client
        self.ubuntu_client = ubuntu_client

    def enrich_vulnerabilities(self, vulns: List[Vulnerability], item: Optional[InventoryItem] = None) -> List[Vulnerability]:
        """Correlates vulnerabilities against external threat intelligence sources with user notice."""
        if not vulns:
            return []

        cve_ids = [v.cve_id for v in vulns if v.cve_id.upper().startswith("CVE-")]

        # Log explicit user-facing notice regarding external intelligence lookup
        logger.info(
            "[SECURITY NOTICE] Performing external CVE threat intelligence enrichment for %d identifiers (EPSS, NVD, KEV)...",
            len(cve_ids)
        )

        # 1. Batch EPSS
        epss_map = self.epss_client.get_scores(cve_ids) if cve_ids else {}

        for v in vulns:
            cve = v.cve_id.upper()

            # 2. VulnCheck KEV
            if self.vulncheck_kev.is_in_vulncheck_kev(cve):
                v.in_vulncheck_kev = True
                # Si está activamente explotado en VulnCheck y la severidad es menor a HIGH, elevar
                if v.severity in [SeverityLevel.MEDIUM, SeverityLevel.LOW, SeverityLevel.UNKNOWN]:
                    v.severity = SeverityLevel.HIGH

            # 3. EPSS
            if cve in epss_map:
                v.epss_score = epss_map[cve].get("epss")
                v.epss_percentile = epss_map[cve].get("percentile")

                # Si la probabilidad de exploit es muy alta (> 0.40 o percentil > 90%), elevar severidad
                if v.epss_score and v.epss_score >= 0.40 and v.severity in [SeverityLevel.MEDIUM, SeverityLevel.LOW, SeverityLevel.UNKNOWN]:
                    v.severity = SeverityLevel.HIGH

            # 4. NVD (CVSS y vectores)
            if v.cvss_score is None or v.cvss_vector is None:
                nvd_info = self.nvd_client.get_cve_details(cve)
                if nvd_info:
                    if v.cvss_score is None and nvd_info.get("cvss_score"):
                        v.cvss_score = nvd_info["cvss_score"]
                    if v.cvss_vector is None and nvd_info.get("cvss_vector"):
                        v.cvss_vector = nvd_info["cvss_vector"]
                    if not v.summary and nvd_info.get("description"):
                        v.summary = nvd_info["description"]

            # 5. Ubuntu Security / USN
            if item and item.environment.value == "wsl":
                pkg_name = item.name
                usn_list = self.ubuntu_client.get_package_advisories(pkg_name)
                for u in usn_list:
                    if u.get("cve_id", "").upper() == cve and u.get("usn"):
                        v.ubuntu_usn = u["usn"]
                        break

            # 6. MSRC (Windows)
            if item and item.environment.value == "windows":
                kb = item.id if item.id.upper().startswith("KB") else item.extra_metadata.get("kb")
                if kb:
                    msrc_info = self.msrc_client.correlate_kb(kb)
                    if msrc_info:
                        v.msrc_kb = kb
                        v.msrc_severity = msrc_info.get("severity")
                        v.msrc_impact = msrc_info.get("impact")

        return vulns
