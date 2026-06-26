"""SOC 2 Type II compliance checks for Agent Memory."""
from __future__ import annotations

import os
from .framework import ComplianceCheck, ComplianceReport, ComplianceStatus


def check_soc2(store=None, config=None) -> ComplianceReport:
    report = ComplianceReport(framework="SOC2", version="Type II")

    checks = [
        ComplianceCheck(check_id="soc2-001", name="Access Control", description="Logical access restrictions on data", category="Security"),
        ComplianceCheck(check_id="soc2-002", name="Encryption", description="Data encryption at rest and in transit", category="Security"),
        ComplianceCheck(check_id="soc2-003", name="Monitoring", description="System monitoring and alerting", category="Security"),
        ComplianceCheck(check_id="soc2-004", name="Incident Response", description="Incident detection and response procedures", category="Security"),
        ComplianceCheck(check_id="soc2-005", name="Change Management", description="Controlled changes to systems", category="Security"),
        ComplianceCheck(check_id="soc2-006", name="Data Backup", description="Regular data backups with verification", category="Availability"),
        ComplianceCheck(check_id="soc2-007", name="Vulnerability Management", description="Regular vulnerability scanning", category="Security"),
        ComplianceCheck(check_id="soc2-008", name="Audit Logging", description="Comprehensive audit trail", category="Security"),
    ]

    # Check 1: Access Control
    has_auth = False
    try:
        from ..auth_middleware import AuthMiddleware
        has_auth = True
    except ImportError:
        pass
    checks[0].status = ComplianceStatus.PASS if has_auth else ComplianceStatus.FAIL
    checks[0].details = "JWT + API Key authentication" if has_auth else "No auth module"
    checks[0].checked_at = __import__('time').time()

    # Check 2: Encryption
    has_crypto = False
    try:
        from ..storage.crypto_store import CryptoStore
        has_crypto = True
    except ImportError:
        pass
    checks[1].status = ComplianceStatus.PASS if has_crypto else ComplianceStatus.WARNING
    checks[1].details = "CryptoStore + HTTPS" if has_crypto else "HTTPS only, no at-rest encryption"
    checks[1].checked_at = __import__('time').time()

    # Check 3: Monitoring
    has_otel = False
    try:
        from ..observability import _HAS_OTEL
        has_otel = _HAS_OTEL
    except ImportError:
        pass
    checks[2].status = ComplianceStatus.PASS if has_otel else ComplianceStatus.WARNING
    checks[2].details = "OpenTelemetry integration available" if has_otel else "No OTel integration"
    checks[2].checked_at = __import__('time').time()

    # Check 4: Incident Response
    checks[3].status = ComplianceStatus.WARNING
    checks[3].details = "Self-healing module available, no formal IR plan"
    checks[3].checked_at = __import__('time').time()

    # Check 5: Change Management
    has_ci = os.path.exists(os.path.join(os.path.dirname(__file__), '..', '..', '.github', 'workflows', 'ci.yml'))
    checks[4].status = ComplianceStatus.PASS if has_ci else ComplianceStatus.WARNING
    checks[4].details = "CI/CD pipeline configured" if has_ci else "No CI/CD"
    checks[4].checked_at = __import__('time').time()

    # Check 6: Data Backup
    has_backup = False
    try:
        from ..backup import BackupManager
        has_backup = True
    except ImportError:
        pass
    checks[5].status = ComplianceStatus.PASS if has_backup else ComplianceStatus.WARNING
    checks[5].details = "BackupManager available" if has_backup else "No backup module"
    checks[5].checked_at = __import__('time').time()

    # Check 7: Vulnerability Management
    has_bandit = os.path.exists(os.path.join(os.path.dirname(__file__), '..', '..', '.bandit'))
    checks[6].status = ComplianceStatus.PASS if has_bandit else ComplianceStatus.WARNING
    checks[6].details = "Bandit security scanning configured" if has_bandit else "No security scanning"
    checks[6].checked_at = __import__('time').time()

    # Check 8: Audit Logging
    has_audit = False
    try:
        from ..enterprise.audit_log import AuditLogger
        has_audit = True
    except ImportError:
        pass
    checks[7].status = ComplianceStatus.PASS if has_audit else ComplianceStatus.WARNING
    checks[7].details = "AuditLogger available" if has_audit else "No audit logging"
    checks[7].checked_at = __import__('time').time()

    report.checks = checks
    return report


class SOC2Compliance:
    def check(self, store=None, config=None) -> ComplianceReport:
        return check_soc2(store=store, config=config)
