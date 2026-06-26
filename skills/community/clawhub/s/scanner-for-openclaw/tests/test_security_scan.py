"""Tests for scripts/security_scan.py"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from security_scan import (
    DEFAULT_PORTS,
    RISK_LEVELS,
    WELL_KNOWN_DEFAULT_PORTS,
    Finding,
    SecurityScanner,
)

# ---------------------------------------------------------------------------
# Finding
# ---------------------------------------------------------------------------

class TestFinding:
    def test_construction_defaults(self):
        f = Finding(
            level="HIGH",
            category="NETWORK",
            title="title",
            description="desc",
            impact="impact",
            remediation="fix",
        )
        assert f.level == "HIGH"
        assert f.risk_of_fix == "LOW"
        assert f.rollback == ""
        assert f.evidence == []

    def test_to_dict_round_trip(self):
        f = Finding(
            level="CRITICAL",
            category="CHANNEL",
            title="t",
            description="d",
            impact="i",
            remediation="r",
            risk_of_fix="HIGH",
            rollback="rollback plan",
        )
        f.evidence.append("ev1")
        d = f.to_dict()
        assert d["level"] == "CRITICAL"
        assert d["rollback"] == "rollback plan"
        assert d["evidence"] == ["ev1"]

    def test_evidence_isolation(self):
        """Each Finding instance should have its own evidence list."""
        f1 = Finding("LOW", "A", "t", "d", "i", "r")
        f2 = Finding("LOW", "A", "t", "d", "i", "r")
        f1.evidence.append("only-f1")
        assert f2.evidence == []


# ---------------------------------------------------------------------------
# SecurityScanner — helpers
# ---------------------------------------------------------------------------

class TestGetPortFromConfig:
    def test_returns_default_when_config_empty(self):
        scanner = SecurityScanner()
        assert scanner.get_port_from_config() == DEFAULT_PORTS["gateway"]

    def test_reads_port_from_config(self):
        scanner = SecurityScanner()
        scanner.config = {"gateway": {"port": 9999}}
        assert scanner.get_port_from_config() == 9999

    def test_falls_back_when_gateway_key_missing(self):
        scanner = SecurityScanner()
        scanner.config = {"other": "stuff"}
        assert scanner.get_port_from_config() == DEFAULT_PORTS["gateway"]


class TestGetBindAddressFromConfig:
    def test_returns_unknown_when_config_empty(self):
        scanner = SecurityScanner()
        assert scanner.get_bind_address_from_config() == "unknown"

    def test_reads_bind_field(self):
        scanner = SecurityScanner()
        scanner.config = {"gateway": {"bind": "127.0.0.1"}}
        assert scanner.get_bind_address_from_config() == "127.0.0.1"

    def test_reads_host_field(self):
        scanner = SecurityScanner()
        scanner.config = {"gateway": {"host": "0.0.0.0"}}
        assert scanner.get_bind_address_from_config() == "0.0.0.0"

    def test_reads_listenAddress_field(self):
        scanner = SecurityScanner()
        scanner.config = {"gateway": {"listenAddress": "192.168.1.1"}}
        assert scanner.get_bind_address_from_config() == "192.168.1.1"

    def test_bind_takes_precedence_over_host(self):
        scanner = SecurityScanner()
        scanner.config = {"gateway": {"bind": "127.0.0.1", "host": "0.0.0.0"}}
        assert scanner.get_bind_address_from_config() == "127.0.0.1"


# ---------------------------------------------------------------------------
# SecurityScanner — config loading
# ---------------------------------------------------------------------------

class TestFindConfig:
    @patch("security_scan.OPENCLAW_CONFIG_PATHS", [])
    def test_returns_none_when_no_paths_and_no_env(self):
        scanner = SecurityScanner()
        with patch.dict("os.environ", {}, clear=True):
            assert scanner.find_config() is None

    @patch("security_scan.OPENCLAW_CONFIG_PATHS", [])
    def test_finds_config_via_env(self, tmp_path):
        cfg = tmp_path / "env_config.json"
        cfg.write_text("{}")
        scanner = SecurityScanner()
        with patch.dict("os.environ", {"OPENCLAW_CONFIG": str(cfg)}):
            assert scanner.find_config() == cfg

    def test_finds_first_existing_path(self, tmp_path):
        p1 = tmp_path / "a.json"
        p2 = tmp_path / "b.json"
        p1.write_text("{}")
        p2.write_text("{}")
        with patch("security_scan.OPENCLAW_CONFIG_PATHS", [p1, p2]):
            scanner = SecurityScanner()
            assert scanner.find_config() == p1


class TestLoadConfig:
    def test_loads_valid_json(self, tmp_path):
        cfg = tmp_path / "config.json"
        cfg.write_text(json.dumps({"gateway": {"port": 1234}}))
        scanner = SecurityScanner()
        with patch("security_scan.OPENCLAW_CONFIG_PATHS", [cfg]):
            assert scanner.load_config() is True
            assert scanner.config["gateway"]["port"] == 1234

    def test_returns_false_when_no_config(self):
        scanner = SecurityScanner()
        with patch("security_scan.OPENCLAW_CONFIG_PATHS", []):
            with patch.dict("os.environ", {}, clear=True):
                assert scanner.load_config() is False

    def test_returns_false_on_invalid_json(self, tmp_path):
        cfg = tmp_path / "bad.json"
        cfg.write_text("not json")
        scanner = SecurityScanner()
        with patch("security_scan.OPENCLAW_CONFIG_PATHS", [cfg]):
            assert scanner.load_config() is False


# ---------------------------------------------------------------------------
# SecurityScanner — scan_ports (config-only)
# ---------------------------------------------------------------------------

class TestScanPorts:
    def _make_scanner(self, config=None):
        scanner = SecurityScanner()
        scanner.config = config or {}
        return scanner

    def test_default_port_finding(self):
        scanner = self._make_scanner({"gateway": {"port": 18789}})
        findings = scanner.scan_ports()
        port_findings = [f for f in findings if "default port" in f.title.lower()]
        assert len(port_findings) == 1
        assert "18789" in port_findings[0].title

    def test_no_finding_for_non_default_port(self):
        scanner = self._make_scanner({"gateway": {"port": 31337}})
        findings = scanner.scan_ports()
        port_findings = [f for f in findings if "default port" in f.title.lower()]
        assert len(port_findings) == 0

    def test_bind_0000_is_critical(self):
        scanner = self._make_scanner({"gateway": {"bind": "0.0.0.0", "port": 9999}})
        findings = scanner.scan_ports()
        critical = [f for f in findings if f.level == "CRITICAL" and "bind" in f.title.lower()]
        assert len(critical) == 1

    def test_bind_localhost_no_critical(self):
        scanner = self._make_scanner({"gateway": {"bind": "127.0.0.1", "port": 9999}})
        findings = scanner.scan_ports()
        critical = [f for f in findings if f.level == "CRITICAL" and f.category == "NETWORK"]
        assert len(critical) == 0

    def test_missing_bind_address_warning(self):
        scanner = self._make_scanner({"gateway": {"port": 31337}})
        findings = scanner.scan_ports()
        bind_findings = [f for f in findings if "not explicitly configured" in f.title.lower()]
        assert len(bind_findings) == 1
        assert bind_findings[0].level == "MEDIUM"

    def test_tls_not_enabled_is_high(self):
        scanner = self._make_scanner({"gateway": {"port": 31337, "bind": "127.0.0.1"}})
        findings = scanner.scan_ports()
        tls_findings = [f for f in findings if "TLS" in f.title]
        assert len(tls_findings) == 1
        assert tls_findings[0].level == "HIGH"

    def test_tls_enabled_no_finding(self):
        scanner = self._make_scanner({"gateway": {"port": 31337, "bind": "127.0.0.1", "tls": {"enabled": True}}})
        findings = scanner.scan_ports()
        tls_findings = [f for f in findings if "TLS" in f.title]
        assert len(tls_findings) == 0

    def test_empty_config_still_produces_findings(self):
        scanner = self._make_scanner({})
        findings = scanner.scan_ports()
        assert len(findings) > 0


# ---------------------------------------------------------------------------
# SecurityScanner — scan_channels
# ---------------------------------------------------------------------------

class TestScanChannels:
    def _make_scanner(self, config):
        scanner = SecurityScanner()
        scanner.config = config
        return scanner

    def test_telegram_allow_all_is_critical(self):
        config = {"channels": {"telegram": {"enabled": True, "groupPolicy": "allow"}}}
        findings = self._make_scanner(config).scan_channels()
        assert any(f.level == "CRITICAL" and "Telegram" in f.title for f in findings)

    def test_telegram_allowlist_empty_is_high(self):
        config = {"channels": {"telegram": {"enabled": True, "groupPolicy": "allowlist", "allowedGroups": []}}}
        findings = self._make_scanner(config).scan_channels()
        assert any(f.level == "HIGH" and "allowlist" in f.title.lower() for f in findings)

    def test_telegram_deny_no_finding(self):
        config = {"channels": {"telegram": {"enabled": True, "groupPolicy": "deny"}}}
        findings = self._make_scanner(config).scan_channels()
        telegram_findings = [f for f in findings if "Telegram" in f.title]
        assert len(telegram_findings) == 0

    def test_telegram_disabled_no_finding(self):
        config = {"channels": {"telegram": {"enabled": False, "groupPolicy": "allow"}}}
        findings = self._make_scanner(config).scan_channels()
        assert len(findings) == 0

    def test_whatsapp_missing_secret(self):
        config = {"channels": {"whatsapp": {"enabled": True}}}
        findings = self._make_scanner(config).scan_channels()
        assert any(f.level == "HIGH" and "WhatsApp" in f.title for f in findings)

    def test_whatsapp_with_secret_no_finding(self):
        config = {"channels": {"whatsapp": {"enabled": True, "webhookSecret": "s3cret"}}}
        findings = self._make_scanner(config).scan_channels()
        whatsapp_findings = [f for f in findings if "WhatsApp" in f.title]
        assert len(whatsapp_findings) == 0

    def test_web_no_auth_is_critical(self):
        config = {"channels": {"web": {"enabled": True}}}
        findings = self._make_scanner(config).scan_channels()
        assert any(f.level == "CRITICAL" and "Web" in f.title for f in findings)

    def test_web_with_auth_no_finding(self):
        config = {"channels": {"web": {"enabled": True, "authentication": {"enabled": True}}}}
        findings = self._make_scanner(config).scan_channels()
        web_findings = [f for f in findings if "Web" in f.title]
        assert len(web_findings) == 0

    def test_generic_channel_allow_policy(self):
        config = {"channels": {"slack": {"enabled": True, "policy": "allow"}}}
        findings = self._make_scanner(config).scan_channels()
        assert any(f.level == "HIGH" and "slack" in f.title for f in findings)

    def test_empty_channels_no_findings(self):
        findings = self._make_scanner({"channels": {}}).scan_channels()
        assert len(findings) == 0


# ---------------------------------------------------------------------------
# SecurityScanner — scan_permissions
# ---------------------------------------------------------------------------

class TestScanPermissions:
    def _make_scanner(self, config):
        scanner = SecurityScanner()
        scanner.config = config
        return scanner

    def test_exec_allow_is_critical(self):
        config = {"tools": {"exec": {"policy": "allow"}}}
        findings = self._make_scanner(config).scan_permissions()
        assert any(f.level == "CRITICAL" and "execution policy" in f.title.lower() for f in findings)

    def test_exec_deny_no_critical(self):
        config = {"tools": {"exec": {"policy": "deny"}}}
        findings = self._make_scanner(config).scan_permissions()
        assert not any(f.level == "CRITICAL" and "execution policy" in f.title.lower() for f in findings)

    def test_fs_not_workspace_only(self):
        config = {"tools": {"fs": {"workspaceOnly": False}}}
        findings = self._make_scanner(config).scan_permissions()
        assert any(f.level == "HIGH" and "Filesystem" in f.title for f in findings)

    def test_fs_workspace_only_no_finding(self):
        config = {"tools": {"fs": {"workspaceOnly": True}}}
        findings = self._make_scanner(config).scan_permissions()
        assert not any("Filesystem" in f.title for f in findings)

    def test_dangerous_tools_detected(self):
        config = {"tools": {"enabled": ["exec", "shell"]}}
        findings = self._make_scanner(config).scan_permissions()
        dangerous = [f for f in findings if "Dangerous tool" in f.title]
        assert len(dangerous) == 2

    def test_no_dangerous_tools(self):
        config = {"tools": {"enabled": ["search", "read"]}}
        findings = self._make_scanner(config).scan_permissions()
        dangerous = [f for f in findings if "Dangerous tool" in f.title]
        assert len(dangerous) == 0

    def test_context_aware_not_enabled(self):
        config = {}
        findings = self._make_scanner(config).scan_permissions()
        assert any("Context-aware" in f.title for f in findings)

    def test_context_aware_enabled_no_finding(self):
        config = {"contexts": {"enabled": True}}
        findings = self._make_scanner(config).scan_permissions()
        assert not any("Context-aware" in f.title for f in findings)


# ---------------------------------------------------------------------------
# SecurityScanner — generate_report
# ---------------------------------------------------------------------------

class TestGenerateReport:
    def test_report_contains_header(self):
        scanner = SecurityScanner()
        report = scanner.generate_report()
        assert "# OpenClaw Security Audit Report" in report
        assert "Overall Risk Level" in report

    def test_overall_risk_critical(self):
        scanner = SecurityScanner()
        scanner.findings = [
            Finding("CRITICAL", "NET", "t", "d", "i", "r"),
        ]
        report = scanner.generate_report()
        assert "CRITICAL" in report
        assert "IMMEDIATE ACTION REQUIRED" in report

    def test_overall_risk_info_when_no_findings(self):
        scanner = SecurityScanner()
        report = scanner.generate_report()
        assert "**Overall Risk Level**: INFO" in report
        assert "IMMEDIATE ACTION REQUIRED" not in report

    def test_report_saved_to_file(self, tmp_path):
        out = tmp_path / "report.md"
        scanner = SecurityScanner()
        scanner.generate_report(output_path=out)
        assert out.exists()
        content = out.read_text()
        assert "OpenClaw Security Audit Report" in content

    def test_findings_grouped_by_level(self):
        scanner = SecurityScanner()
        scanner.findings = [
            Finding("HIGH", "A", "high1", "d", "i", "r"),
            Finding("LOW", "A", "low1", "d", "i", "r"),
            Finding("HIGH", "A", "high2", "d", "i", "r"),
        ]
        report = scanner.generate_report()
        high_pos = report.index("high1")
        low_pos = report.index("low1")
        assert high_pos < low_pos


# ---------------------------------------------------------------------------
# SecurityScanner — run_full_scan
# ---------------------------------------------------------------------------

class TestRunFullScan:
    @patch.object(SecurityScanner, "scan_permissions", return_value=[])
    @patch.object(SecurityScanner, "scan_channels", return_value=[])
    @patch.object(SecurityScanner, "scan_ports", return_value=[])
    @patch.object(SecurityScanner, "load_config", return_value=False)
    def test_runs_all_scans_even_without_config(self, mock_lc, mock_sp, mock_sc, mock_perm):
        scanner = SecurityScanner()
        scanner.run_full_scan()
        mock_sp.assert_called_once()
        mock_sc.assert_called_once()
        mock_perm.assert_called_once()

    @patch.object(SecurityScanner, "scan_permissions", return_value=[])
    @patch.object(SecurityScanner, "scan_channels", return_value=[])
    @patch.object(SecurityScanner, "scan_ports")
    @patch.object(SecurityScanner, "load_config", return_value=True)
    def test_aggregates_findings(self, mock_lc, mock_sp, mock_sc, mock_perm):
        f1 = Finding("HIGH", "A", "t1", "d", "i", "r")
        f2 = Finding("LOW", "B", "t2", "d", "i", "r")
        mock_sp.return_value = [f1, f2]
        scanner = SecurityScanner()
        result = scanner.run_full_scan()
        assert len(result) == 2


# ---------------------------------------------------------------------------
# No risky imports — verify subprocess/socket not imported
# ---------------------------------------------------------------------------

class TestNoRiskyImports:
    def test_no_subprocess_import(self):
        import security_scan
        assert not hasattr(security_scan, "subprocess"), "subprocess must not be imported"

    def test_no_socket_import(self):
        import security_scan
        assert not hasattr(security_scan, "socket"), "socket must not be imported"

    def test_no_shutil_import(self):
        import security_scan
        assert not hasattr(security_scan, "shutil"), "shutil must not be imported"
