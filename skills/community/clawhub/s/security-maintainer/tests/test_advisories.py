"""
Pruebas unitarias para consultas de vulnerabilidades, CISA KEV y parches retroportados.
"""

import unittest
import json
from pathlib import Path

from security_maintainer.advisories.cache import AdvisoryCache
from security_maintainer.advisories.cisa_kev import CisaKevCatalog
from security_maintainer.advisories.distro_trackers import DistroSecurityTracker
from security_maintainer.advisories.osv_client import OSVClient
from security_maintainer.models import InventoryItem, EnvironmentType, ManagerType, SeverityLevel

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestAdvisories(unittest.TestCase):

    def setUp(self):
        with open(FIXTURES_DIR / "osv_sample.json", "r", encoding="utf-8") as f:
            self.osv_data = json.load(f)
        with open(FIXTURES_DIR / "cisa_kev_sample.json", "r", encoding="utf-8") as f:
            self.kev_data = json.load(f)

        self.cache = AdvisoryCache(cache_dir=FIXTURES_DIR / "test_cache")
        self.kev = CisaKevCatalog({}, self.cache, fixture_data=self.kev_data)
        self.kev.load()

        # Fixture de backports: CVE-2024-2511 ya subsanado en versión 3.0.13-0ubuntu3.4
        self.distro_tracker = DistroSecurityTracker(fixture_data={
            "backports": {
                "ubuntu": {
                    "openssl": {
                        "CVE-2024-2511": "3.0.13-0ubuntu3.4"
                    }
                }
            }
        })

        self.osv = OSVClient(
            config={},
            cache=self.cache,
            kev_catalog=self.kev,
            distro_tracker=self.distro_tracker,
            fixture_data=self.osv_data
        )

    def test_cisa_kev_detection(self):
        # CVE-2024-7264 está en el catálogo KEV fixture
        in_kev, info = self.kev.check_cve("CVE-2024-7264")
        self.assertTrue(in_kev)
        self.assertEqual(info["vulnerability_name"], "curl Out-of-Bounds Read Vulnerability")

        # CVE desconocido no debe figurar en KEV
        in_kev_false, _ = self.kev.check_cve("CVE-2099-99999")
        self.assertFalse(in_kev_false)

    def test_osv_vulnerability_mapping_and_kev_elevation(self):
        item = InventoryItem(
            environment=EnvironmentType.WSL,
            target_name="WSL:Ubuntu",
            name="curl",
            id="curl",
            installed_version="8.4.0",
            manager=ManagerType.APT
        )
        vulns = self.osv.query_vulnerabilities(item)
        self.assertTrue(len(vulns) > 0)
        v = vulns[0]
        self.assertEqual(v.cve_id, "CVE-2024-7264")
        self.assertTrue(v.in_cisa_kev)
        # La presencia en CISA KEV eleva la severidad a CRITICAL
        self.assertEqual(v.severity, SeverityLevel.CRITICAL)

    def test_backported_patch_suppresses_false_positive(self):
        # openssl con versión que ya incluye el backport 3.0.13-0ubuntu3.4
        item_fixed = InventoryItem(
            environment=EnvironmentType.WSL,
            target_name="WSL:Ubuntu",
            name="openssl",
            id="openssl",
            installed_version="3.0.13-0ubuntu3.4",
            manager=ManagerType.APT
        )
        vulns = self.osv.query_vulnerabilities(item_fixed)
        # Debe omitir el falso positivo porque el parche retroportado está presente
        self.assertEqual(len(vulns), 0)

    def test_epss_and_vulncheck_enrichment(self):
        from security_maintainer.advisories.epss import EpssClient
        from security_maintainer.advisories.vulncheck import VulnCheckKevCatalog
        from security_maintainer.advisories.nvd import NvdClient
        from security_maintainer.advisories.msrc import MsrcClient
        from security_maintainer.advisories.ubuntu_security import UbuntuSecurityClient
        from security_maintainer.advisories.enricher import ThreatIntelligenceEnricher
        from security_maintainer.models import Vulnerability

        epss_fixture = {
            "CVE-2023-38606": {"epss": 0.9754, "percentile": 0.9998}
        }
        vulncheck_fixture = {
            "vulnerabilities": [
                {"cveID": "CVE-2023-38606", "vendorProject": "Apple", "product": "Kernel"}
            ]
        }
        nvd_fixture = {
            "CVE-2023-38606": {
                "cve_id": "CVE-2023-38606",
                "cvss_score": 7.8,
                "cvss_vector": "CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H",
                "description": "Kernel memory corruption vulnerability."
            }
        }
        msrc_fixture = {
            "KB5044284": {
                "title": "Windows 11 Cumulative Security Update",
                "severity": "Critical",
                "impact": "Remote Code Execution",
                "cves": ["CVE-2024-30078"]
            }
        }
        ubuntu_fixture = {
            "curl": [
                {"cve_id": "CVE-2024-7264", "usn": "USN-6950-1", "status": "released"}
            ]
        }

        epss = EpssClient({}, self.cache, fixture_data=epss_fixture)
        vulncheck = VulnCheckKevCatalog({}, self.cache, fixture_data=vulncheck_fixture)
        vulncheck.load()
        nvd = NvdClient({}, self.cache, fixture_data=nvd_fixture)
        msrc = MsrcClient({}, self.cache, fixture_data=msrc_fixture)
        ubuntu_sec = UbuntuSecurityClient({}, self.cache, fixture_data=ubuntu_fixture)

        enricher = ThreatIntelligenceEnricher(
            config={},
            cache=self.cache,
            cisa_kev=self.kev,
            vulncheck_kev=vulncheck,
            epss_client=epss,
            nvd_client=nvd,
            msrc_client=msrc,
            ubuntu_client=ubuntu_sec
        )

        test_vuln = Vulnerability(
            cve_id="CVE-2023-38606",
            title="Triangulation zero-day",
            summary="Zero-day kernel exploit",
            severity=SeverityLevel.MEDIUM
        )

        enriched = enricher.enrich_vulnerabilities([test_vuln])
        self.assertEqual(len(enriched), 1)
        v = enriched[0]

        # Validar enriquecimiento EPSS
        self.assertAlmostEqual(v.epss_score, 0.9754, places=3)
        self.assertAlmostEqual(v.epss_percentile, 0.9998, places=3)

        # Validar detección VulnCheck KEV
        self.assertTrue(v.in_vulncheck_kev)

        # Validar NVD CVSS y vector
        self.assertEqual(v.cvss_score, 7.8)
        self.assertEqual(v.cvss_vector, "CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H")

        # La severidad debió elevarse a HIGH por EPSS alto y VulnCheck KEV
        self.assertEqual(v.severity, SeverityLevel.HIGH)

    def test_msrc_and_ubuntu_enrichment(self):
        from security_maintainer.advisories.epss import EpssClient
        from security_maintainer.advisories.vulncheck import VulnCheckKevCatalog
        from security_maintainer.advisories.nvd import NvdClient
        from security_maintainer.advisories.msrc import MsrcClient
        from security_maintainer.advisories.ubuntu_security import UbuntuSecurityClient
        from security_maintainer.advisories.enricher import ThreatIntelligenceEnricher
        from security_maintainer.models import Vulnerability

        enricher = ThreatIntelligenceEnricher(
            config={},
            cache=self.cache,
            cisa_kev=self.kev,
            vulncheck_kev=VulnCheckKevCatalog({}, self.cache, fixture_data={"vulnerabilities": []}),
            epss_client=EpssClient({}, self.cache, fixture_data={}),
            nvd_client=NvdClient({}, self.cache, fixture_data={}),
            msrc_client=MsrcClient({}, self.cache, fixture_data={"KB5044284": {"severity": "Critical", "impact": "RCE"}}),
            ubuntu_client=UbuntuSecurityClient({}, self.cache, fixture_data={"curl": [{"cve_id": "CVE-2024-7264", "usn": "USN-6950-1"}]})
        )

        # Probar enriquecimiento Ubuntu
        wsl_item = InventoryItem(
            environment=EnvironmentType.WSL,
            target_name="WSL:Ubuntu",
            name="curl",
            id="curl",
            installed_version="8.4.0",
            manager=ManagerType.APT
        )
        wsl_vuln = Vulnerability(cve_id="CVE-2024-7264")
        enriched_wsl = enricher.enrich_vulnerabilities([wsl_vuln], wsl_item)
        self.assertEqual(enriched_wsl[0].ubuntu_usn, "USN-6950-1")

        # Probar enriquecimiento MSRC Windows
        win_item = InventoryItem(
            environment=EnvironmentType.WINDOWS,
            target_name="Windows Host",
            name="Windows 11 Security Update",
            id="KB5044284",
            installed_version="pending",
            manager=ManagerType.WINDOWS_UPDATE
        )
        win_vuln = Vulnerability(cve_id="CVE-2024-30078")
        enriched_win = enricher.enrich_vulnerabilities([win_vuln], win_item)
        self.assertEqual(enriched_win[0].msrc_severity, "Critical")


if __name__ == "__main__":
    unittest.main()
