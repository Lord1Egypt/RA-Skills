#!/usr/bin/env python3
"""
OpenClaw Security Scanner - Main Scan Script

Performs comprehensive security audit of OpenClaw deployment by
analyzing local configuration files (no network probing, no subprocess calls).

Checks:
1. Network configuration analysis (ports, bindings)
2. Channel policy audit
3. Permission analysis
4. Risk assessment and remediation guidance

Usage:
    python3 security_scan.py [--ports-only | --channels-only | --full]
    python3 security_scan.py --help
"""

import argparse
import json
import os
import platform
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

OPENCLAW_CONFIG_PATHS = [
    Path.home() / ".openclaw" / "openclaw.json",
    Path.home() / ".openclaw" / "config.json",
    Path.home() / ".openclaw" / "gateway.config.json",
    Path("/etc/openclaw/openclaw.json"),
]

DEFAULT_PORTS = {
    "gateway": 18789,
    "web": 8080,
    "https": 443,
    "http": 80,
    "ssh": 22,
}

WELL_KNOWN_DEFAULT_PORTS = {18789, 8080, 80, 443}

RISK_LEVELS = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]


class Finding:
    """Security finding with risk assessment"""

    def __init__(self, level: str, category: str, title: str,
                 description: str, impact: str, remediation: str,
                 risk_of_fix: str = "LOW", rollback: str = ""):
        self.level = level
        self.category = category
        self.title = title
        self.description = description
        self.impact = impact
        self.remediation = remediation
        self.risk_of_fix = risk_of_fix
        self.rollback = rollback
        self.evidence = []

    def to_dict(self) -> Dict:
        return {
            "level": self.level,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "impact": self.impact,
            "remediation": self.remediation,
            "risk_of_fix": self.risk_of_fix,
            "rollback": self.rollback,
            "evidence": self.evidence,
        }


class SecurityScanner:
    """Main security scanner — pure config-based static analysis.

    All checks derive from local configuration files only.
    No network sockets, no subprocess calls, no system command execution.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.findings: List[Finding] = []
        self.config: Dict = {}
        self.config_path: Optional[Path] = None
        self.scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.hostname = platform.node()

    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

    def find_config(self) -> Optional[Path]:
        for path in OPENCLAW_CONFIG_PATHS:
            if path.exists():
                self.log(f"Found config: {path}")
                return path

        if "OPENCLAW_CONFIG" in os.environ:
            path = Path(os.environ["OPENCLAW_CONFIG"])
            if path.exists():
                self.log(f"Found config via env: {path}")
                return path

        self.log("No config file found", "WARN")
        return None

    def load_config(self) -> bool:
        self.config_path = self.find_config()
        if not self.config_path:
            return False

        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            self.log(f"Loaded config from {self.config_path}")
            return True
        except Exception as e:
            self.log(f"Failed to load config: {e}", "ERROR")
            return False

    # ------------------------------------------------------------------
    # Port / network configuration analysis (config-only, no probing)
    # ------------------------------------------------------------------

    def get_port_from_config(self) -> int:
        if not self.config:
            return DEFAULT_PORTS["gateway"]
        return self.config.get("gateway", {}).get("port", DEFAULT_PORTS["gateway"])

    def get_bind_address_from_config(self) -> str:
        """Read the configured bind address. Returns 'unknown' when absent."""
        gw = self.config.get("gateway", {})
        return gw.get("bind", gw.get("host", gw.get("listenAddress", "unknown")))

    def scan_ports(self) -> List[Finding]:
        """Analyze network configuration from config file only."""
        findings = []

        self.log("Analyzing network configuration from config...")

        config_port = self.get_port_from_config()
        bind_address = self.get_bind_address_from_config()

        if bind_address == "0.0.0.0":
            finding = Finding(
                level="CRITICAL",
                category="NETWORK",
                title=f"Gateway configured to bind to all interfaces (0.0.0.0:{config_port})",
                description=f"Gateway bind address is set to 0.0.0.0:{config_port}, making it accessible from any network interface",
                impact="Attackers on the network can access gateway API, potentially leading to unauthorized access",
                remediation=f"Set bind address to 127.0.0.1:{config_port} or use firewall rules to restrict access",
                risk_of_fix="MEDIUM - may break remote access if not careful",
                rollback="Restore previous bind address in config and restart gateway",
            )
            finding.evidence.append(f"Config bind address: {bind_address}")
            findings.append(finding)
        elif bind_address in ("unknown", ""):
            finding = Finding(
                level="MEDIUM",
                category="NETWORK",
                title="Gateway bind address not explicitly configured",
                description="No explicit bind/host/listenAddress found in gateway config; default behaviour depends on the OpenClaw version",
                impact="Gateway may default to 0.0.0.0, exposing it to all interfaces",
                remediation="Explicitly set bind address to 127.0.0.1 in gateway config",
                risk_of_fix="LOW",
                rollback="Remove the bind address setting to revert to defaults",
            )
            findings.append(finding)

        if config_port in WELL_KNOWN_DEFAULT_PORTS:
            finding = Finding(
                level="LOW",
                category="NETWORK",
                title=f"Using default port {config_port}",
                description=f"Gateway uses well-known default port {config_port}",
                impact="Attackers can easily guess the service port",
                remediation="Consider using a non-standard port (security through obscurity, not a primary defense)",
                risk_of_fix="HIGH - changing port will break all existing connections",
                rollback="Revert port configuration",
            )
            findings.append(finding)

        # TLS / SSL configuration check
        gw = self.config.get("gateway", {})
        tls_config = gw.get("tls", gw.get("ssl", {}))
        if not tls_config.get("enabled", False):
            finding = Finding(
                level="HIGH",
                category="NETWORK",
                title="TLS not enabled for gateway",
                description="Gateway does not have TLS/SSL enabled in configuration",
                impact="Traffic between clients and gateway is unencrypted, vulnerable to eavesdropping",
                remediation="Enable TLS in gateway config with a valid certificate",
                risk_of_fix="MEDIUM - requires certificate provisioning",
                rollback="Disable TLS setting to revert",
            )
            findings.append(finding)

        return findings

    # ------------------------------------------------------------------
    # Channel policy audit
    # ------------------------------------------------------------------

    def scan_channels(self) -> List[Finding]:
        """Audit channel configurations"""
        findings = []

        self.log("Scanning channel configurations...")

        channels = self.config.get("channels", {})

        # Telegram
        telegram = channels.get("telegram", {})
        if telegram.get("enabled"):
            group_policy = telegram.get("groupPolicy", "deny")

            if group_policy == "allow":
                finding = Finding(
                    level="CRITICAL",
                    category="CHANNEL",
                    title="Telegram allows all group messages",
                    description="Telegram channel configured with groupPolicy='allow', permitting messages from any group",
                    impact="Anyone can send messages to your OpenClaw instance, potential for spam, abuse, or prompt injection attacks",
                    remediation="Set groupPolicy='allowlist' or 'deny' and explicitly configure allowedGroups",
                    risk_of_fix="LOW - won't break existing 1:1 chats",
                    rollback="Revert groupPolicy to 'allow'",
                )
                finding.evidence.append(f"groupPolicy: {group_policy}")
                findings.append(finding)

            if group_policy == "allowlist":
                allowed_groups = telegram.get("allowedGroups", [])
                if not allowed_groups:
                    finding = Finding(
                        level="HIGH",
                        category="CHANNEL",
                        title="Telegram allowlist is empty",
                        description="groupPolicy='allowlist' but allowedGroups is empty or not configured",
                        impact="No groups can message the bot, may indicate misconfiguration",
                        remediation="Add group IDs to allowedGroups or change groupPolicy",
                        risk_of_fix="LOW",
                        rollback="N/A",
                    )
                    findings.append(finding)

        # WhatsApp
        whatsapp = channels.get("whatsapp", {})
        if whatsapp.get("enabled"):
            if not whatsapp.get("webhookSecret"):
                finding = Finding(
                    level="HIGH",
                    category="CHANNEL",
                    title="WhatsApp webhook missing secret",
                    description="WhatsApp channel enabled without webhookSecret for request validation",
                    impact="Attackers could forge WhatsApp messages",
                    remediation="Generate and configure webhookSecret",
                    risk_of_fix="LOW",
                    rollback="N/A",
                )
                findings.append(finding)

        # Web channel
        web = channels.get("web", {})
        if web.get("enabled"):
            auth_enabled = web.get("authentication", {}).get("enabled", False)
            if not auth_enabled:
                finding = Finding(
                    level="CRITICAL",
                    category="CHANNEL",
                    title="Web channel has no authentication",
                    description="Web UI is accessible without authentication",
                    impact="Anyone with network access can use the web interface",
                    remediation="Enable authentication in web channel config",
                    risk_of_fix="MEDIUM - will require login",
                    rollback="Disable authentication (not recommended)",
                )
                findings.append(finding)

        # Generic allow-all policy check
        for channel_name, channel_config in channels.items():
            if isinstance(channel_config, dict):
                policy = channel_config.get("policy", channel_config.get("groupPolicy", ""))
                if policy == "allow" and channel_name not in ["telegram"]:
                    finding = Finding(
                        level="HIGH",
                        category="CHANNEL",
                        title=f"{channel_name} channel allows all messages",
                        description=f"Channel {channel_name} has permissive policy",
                        impact="Unauthorized users may interact with the bot",
                        remediation=f"Configure allowlist or denylist for {channel_name}",
                        risk_of_fix="LOW",
                        rollback=f"Revert {channel_name} policy",
                    )
                    findings.append(finding)

        return findings

    # ------------------------------------------------------------------
    # Permission analysis
    # ------------------------------------------------------------------

    def scan_permissions(self) -> List[Finding]:
        """Analyze tool and execution permissions"""
        findings = []

        self.log("Analyzing permissions...")

        tools = self.config.get("tools", {})

        exec_policy = tools.get("exec", {}).get("policy", "deny")
        if exec_policy == "allow":
            finding = Finding(
                level="CRITICAL",
                category="PERMISSION",
                title="Tool execution policy is 'allow'",
                description="All tools can execute without restrictions (tools.exec.policy='allow')",
                impact="Any tool can run arbitrary commands, high risk of abuse or accidental damage",
                remediation="Set tools.exec.policy='deny' or 'allowlist' and configure allowedCommands",
                risk_of_fix="HIGH - may break existing workflows",
                rollback="Revert exec policy to 'allow'",
            )
            finding.evidence.append(f"exec.policy: {exec_policy}")
            findings.append(finding)

        fs_config = tools.get("fs", {})
        workspace_only = fs_config.get("workspaceOnly", True)
        if not workspace_only:
            finding = Finding(
                level="HIGH",
                category="PERMISSION",
                title="Filesystem access not restricted to workspace",
                description="tools.fs.workspaceOnly=false allows access to entire filesystem",
                impact="Tools can read/write sensitive files outside workspace",
                remediation="Set tools.fs.workspaceOnly=true",
                risk_of_fix="MEDIUM - may break tools needing broader access",
                rollback="Set workspaceOnly=false",
            )
            findings.append(finding)

        dangerous_tools = ["exec", "shell", "system.run", "canvas.eval"]
        enabled_tools = tools.get("enabled", [])
        for tool in dangerous_tools:
            if tool in enabled_tools:
                finding = Finding(
                    level="MEDIUM",
                    category="PERMISSION",
                    title=f"Dangerous tool enabled: {tool}",
                    description=f"Tool '{tool}' can execute arbitrary code",
                    impact="Potential for code execution attacks if tool is compromised",
                    remediation=f"Disable {tool} if not needed, or restrict via allowlist",
                    risk_of_fix="MEDIUM - may break functionality",
                    rollback=f"Re-enable {tool}",
                )
                findings.append(finding)

        if not self.config.get("contexts", {}).get("enabled"):
            finding = Finding(
                level="LOW",
                category="PERMISSION",
                title="Context-aware permissions not enabled",
                description="No dynamic permission switching based on context (user, channel, time)",
                impact="Cannot implement least-privilege per scenario",
                remediation="Consider implementing context-aware permissions for flexible security",
                risk_of_fix="LOW",
                rollback="N/A",
            )
            findings.append(finding)

        return findings

    # ------------------------------------------------------------------
    # Report generation
    # ------------------------------------------------------------------

    def generate_report(self, output_path: Optional[Path] = None) -> str:
        level_counts = {level: 0 for level in RISK_LEVELS}
        for finding in self.findings:
            level_counts[finding.level] = level_counts.get(finding.level, 0) + 1

        if level_counts["CRITICAL"] > 0:
            overall_risk = "CRITICAL"
        elif level_counts["HIGH"] > 0:
            overall_risk = "HIGH"
        elif level_counts["MEDIUM"] > 0:
            overall_risk = "MEDIUM"
        elif level_counts["LOW"] > 0:
            overall_risk = "LOW"
        else:
            overall_risk = "INFO"

        report = f"""# OpenClaw Security Audit Report

**Scan Date**: {self.scan_time}
**Hostname**: {self.hostname}
**Config Path**: {self.config_path or 'Not found'}
**Overall Risk Level**: {overall_risk}

---

## Executive Summary

Security scan identified **{len(self.findings)} findings**:
- 🔴 CRITICAL: {level_counts['CRITICAL']}
- 🟠 HIGH: {level_counts['HIGH']}
- 🟡 MEDIUM: {level_counts['MEDIUM']}
- 🔵 LOW: {level_counts['LOW']}
- ⚪ INFO: {level_counts['INFO']}

"""

        if overall_risk in ["CRITICAL", "HIGH"]:
            report += """⚠️ **IMMEDIATE ACTION REQUIRED**

Critical or high-risk vulnerabilities detected. Review and remediate immediately.
Some fixes may require staged rollout to avoid breaking remote access.

"""

        report += """---

## Findings

"""

        for level in RISK_LEVELS:
            level_findings = [f for f in self.findings if f.level == level]
            if level_findings:
                emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵", "INFO": "⚪"}[level]
                report += f"### {emoji} {level} ({len(level_findings)})\n\n"

                for i, finding in enumerate(level_findings, 1):
                    report += f"""#### {i}. {finding.title}

**Category**: {finding.category}  
**Impact**: {finding.impact}  
**Risk of Fix**: {finding.risk_of_fix}

**Description**:  
{finding.description}

**Remediation**:  
{finding.remediation}

"""
                    if finding.rollback:
                        report += f"""**Rollback Plan**:  
{finding.rollback}

"""
                    if finding.evidence:
                        report += "**Evidence**:  \n"
                        for ev in finding.evidence:
                            report += f"- {ev}\n"
                        report += "\n"

                    report += "---\n\n"

        report += """---

## Remediation Plan

### Immediate Actions (< 24h)

"""
        immediate = [f for f in self.findings if f.level in ["CRITICAL", "HIGH"] and f.risk_of_fix in ["LOW", "MEDIUM"]]
        if immediate:
            for finding in immediate:
                report += f"- [ ] **{finding.title}**\n"
                report += f"  - Fix: {finding.remediation}\n"
                report += f"  - Risk: {finding.risk_of_fix}\n\n"
        else:
            report += "No immediate low-risk actions identified.\n\n"

        report += """### Staged Rollout Required

⚠️ These fixes may break remote access. Follow staged rollout protocol:

1. Backup current configuration
2. Verify alternative access (SSH, console)
3. Test in staging environment
4. Apply with monitoring
5. Keep rollback ready

"""
        staged = [f for f in self.findings if f.risk_of_fix in ["HIGH", "MEDIUM"]]
        if staged:
            for finding in staged:
                report += f"- [ ] **{finding.title}**\n"
                report += f"  - Fix: {finding.remediation}\n"
                report += f"  - Rollback: {finding.rollback}\n\n"
        else:
            report += "No staged rollout required.\n\n"

        report += f"""---

## Appendix

### Scan Configuration
- Verbose: {self.verbose}
- Config loaded: {self.config_path is not None}
- Total findings: {len(self.findings)}

### Recommendations

1. **Regular Scans**: Run this scan weekly or after major changes
2. **Backup Configs**: Always backup before changes
3. **Least Privilege**: Default to minimal permissions
4. **Defense in Depth**: Multiple security layers

### Contact

For security emergencies, contact your security team immediately.

---

*Report generated by OpenClaw Security Scanner v1.0.4*
"""

        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
            self.log(f"Report saved to {output_path}")

        return report

    def run_full_scan(self) -> List[Finding]:
        self.log("=" * 60)
        self.log("OpenClaw Security Scanner v1.0.4")
        self.log("=" * 60)

        if not self.load_config():
            self.log("Continuing scan without config (limited checks)", "WARN")

        self.log("\n[1/3] Network configuration analysis...")
        self.findings.extend(self.scan_ports())

        self.log("\n[2/3] Channel policy audit...")
        self.findings.extend(self.scan_channels())

        self.log("\n[3/3] Permission analysis...")
        self.findings.extend(self.scan_permissions())

        self.log(f"\n{'=' * 60}")
        self.log(f"Scan complete. {len(self.findings)} findings.")
        self.log(f"{'=' * 60}")

        return self.findings


def main():
    parser = argparse.ArgumentParser(description="OpenClaw Security Scanner")
    parser.add_argument("--ports-only", action="store_true", help="Only scan ports")
    parser.add_argument("--channels-only", action="store_true", help="Only audit channels")
    parser.add_argument("--permissions-only", action="store_true", help="Only analyze permissions")
    parser.add_argument("--output", "-o", type=Path, help="Output report path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--full", action="store_true", help="Full scan (default)")

    args = parser.parse_args()

    scanner = SecurityScanner(verbose=args.verbose)

    if args.ports_only:
        scanner.load_config()
        scanner.findings.extend(scanner.scan_ports())
    elif args.channels_only:
        scanner.load_config()
        scanner.findings.extend(scanner.scan_channels())
    elif args.permissions_only:
        scanner.load_config()
        scanner.findings.extend(scanner.scan_permissions())
    else:
        scanner.run_full_scan()

    output_path = args.output or Path(f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    report = scanner.generate_report(output_path)

    print("\n" + "=" * 60)
    print("SCAN SUMMARY")
    print("=" * 60)

    level_counts = {}
    for finding in scanner.findings:
        level_counts[finding.level] = level_counts.get(finding.level, 0) + 1

    for level in RISK_LEVELS:
        count = level_counts.get(level, 0)
        if count > 0:
            print(f"{level}: {count}")

    print(f"\nFull report: {output_path}")

    if level_counts.get("CRITICAL", 0) > 0 or level_counts.get("HIGH", 0) > 0:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
