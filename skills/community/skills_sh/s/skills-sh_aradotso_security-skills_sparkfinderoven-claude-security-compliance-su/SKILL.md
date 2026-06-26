---
name: sparkfinderoven-claude-security-compliance-suite
description: Security & compliance skill suite for OWASP scanning, CVE detection, GDPR/SOC2 auditing, threat modeling, and incident response workflows
triggers:
  - scan this code for OWASP vulnerabilities
  - check dependencies for CVEs
  - run a GDPR compliance audit
  - create a threat model for this architecture
  - generate a security incident playbook
  - audit IAM permissions for least privilege
  - detect secrets in the codebase
  - assess SOC2 readiness
---

# 🔒 Security & Compliance Skills Suite

> Skill by [ara.so](https://ara.so) — Security Skills collection.

This skill suite provides AI coding agents with specialized commands and workflows for security auditing, vulnerability management, compliance (GDPR/SOC2/ISO27001), and incident response. Derived from hesreallyhim/awesome-claude-code, it offers 10 specialized commands and 5 multi-step workflows with structured output.

## What This Project Does

The Security & Compliance Skills Suite equips AI agents with:

- **OWASP Top-10 vulnerability scanning** with CVSS scores
- **Dependency CVE detection** with upgrade paths
- **Compliance auditing** (GDPR, SOC2, ISO27001)
- **Threat modeling** using STRIDE methodology
- **IAM security audits** for least-privilege assessment
- **Secret detection** for pre-commit hooks
- **Incident response playbooks** with structured workflows
- **Penetration test reporting** with executive summaries

All commands follow a consistent 5-step interaction pattern with visual progress tracking and prioritized action plans.

## Installation

### Method 1: Clone to Claude Skills Directory

```bash
# Clone the repository
git clone https://github.com/sparkfinderoven/r01-hesreallyhim-awesome-claude-code-security.git

# Copy to Claude skills directory
mkdir -p ~/.claude/skills
cp -r r01-hesreallyhim-awesome-claude-code-security ~/.claude/skills/security-compliance-suite/
```

### Method 2: Manual Setup

```bash
# Create skill directory
mkdir -p ~/.claude/skills/security-compliance-suite

# Download and extract
cd ~/.claude/skills/security-compliance-suite
# Add skill files manually
```

### Activate in Claude Code

In a Claude Code session:

```bash
/read ~/.claude/skills/security-compliance-suite/SKILL.md
```

Or reference in your project's `.claude/config.json`:

```json
{
  "skills": [
    "~/.claude/skills/security-compliance-suite"
  ]
}
```

## Core Commands

### `/owasp-scan` - OWASP Top-10 Vulnerability Scan

Scans code for OWASP Top-10 vulnerabilities with exploit descriptions, CVSS scores, and remediation steps.

**Usage:**
```bash
/owasp-scan <target_path>
/owasp-scan src/api --verbose
/owasp-scan . --format json
```

**Example Output Structure:**
```
╔══════════════════════════════════════════════════╗
║  OWASP Scan  —  src/api/                        ║
╠══════════════════════════════════════════════════╣
║  Injection checks        ✓   23 files            ║
║  Auth checks             ✓   12 files            ║
║  XSS checks              ✓   45 files            ║
║  CSRF checks             ✓   8 files             ║
╚══════════════════════════════════════════════════╝

FINDINGS  (sort: severity desc)
┌──────┬────────────────────────────────────┬──────┬──────────┐
│ Sev  │ Finding                            │ CVSS │ File     │
├──────┼────────────────────────────────────┼──────┼──────────┤
│  🔴  │ SQL injection via string concat    │ 9.8  │ db.js:45 │
│  🔴  │ JWT algorithm confusion            │ 9.1  │ auth.js  │
│  🟠  │ Missing CSRF token validation      │ 6.5  │ form.js  │
└──────┴────────────────────────────────────┴──────┴──────────┘
```

**Code Pattern for SQL Injection Detection:**
```javascript
// VULNERABLE - String concatenation
const query = "SELECT * FROM users WHERE id = " + userId;

// SECURE - Parameterized query
const query = "SELECT * FROM users WHERE id = ?";
db.execute(query, [userId]);
```

### `/dep-cve` - Dependency CVE Report

Scans project dependencies for known CVEs with exploitability scores and upgrade paths.

**Usage:**
```bash
/dep-cve
/dep-cve --scope full --output md
/dep-cve --severity high,critical
```

**Example Implementation Pattern:**
```javascript
// package.json analysis
const auditDependencies = async (packageJsonPath) => {
  const pkg = require(packageJsonPath);
  const deps = { ...pkg.dependencies, ...pkg.devDependencies };
  
  const vulnerabilities = [];
  for (const [name, version] of Object.entries(deps)) {
    const cves = await queryNVD(name, version);
    vulnerabilities.push(...cves);
  }
  
  return vulnerabilities.sort((a, b) => b.cvss - a.cvss);
};
```

**Expected Output:**
```
CVE REPORT  —  234 dependencies scanned
┌─────────────┬─────────┬──────┬────────────────────────┐
│ Package     │ CVE     │ CVSS │ Fix                    │
├─────────────┼─────────┼──────┼────────────────────────┤
│ express     │ CVE-... │ 9.8  │ Upgrade to 4.18.2+     │
│ lodash      │ CVE-... │ 7.4  │ Upgrade to 4.17.21     │
│ axios       │ CVE-... │ 6.5  │ Upgrade to 1.6.0       │
└─────────────┴─────────┴──────┴────────────────────────┘

ACTION PLAN:
□ Critical: Upgrade express (15 min)
□ High: Upgrade lodash (10 min)
□ Medium: Review axios usage (30 min)
```

### `/gdpr-audit` - GDPR Compliance Audit

Maps data flows, identifies consent gaps, and generates DPA checklists.

**Usage:**
```bash
/gdpr-audit
/gdpr-audit --scope full
/gdpr-audit --output report.md
```

**Code Example - Data Flow Detection:**
```python
# Detect personal data processing
import ast

class GDPRAnalyzer(ast.NodeVisitor):
    PII_FIELDS = ['email', 'phone', 'address', 'ssn', 'name']
    
    def __init__(self):
        self.data_flows = []
    
    def visit_Assign(self, node):
        # Check for PII in assignments
        if isinstance(node.value, ast.Call):
            if any(pii in ast.dump(node) for pii in self.PII_FIELDS):
                self.data_flows.append({
                    'line': node.lineno,
                    'type': 'data_collection',
                    'lawful_basis': 'NEEDS_REVIEW'
                })
        self.generic_visit(node)

# Usage
with open('user_service.py') as f:
    tree = ast.parse(f.read())
    analyzer = GDPRAnalyzer()
    analyzer.visit(tree)
```

**Audit Checklist Output:**
```
GDPR DATA FLOW MAP
┌──────────────────┬────────────────┬──────────────────┐
│ Data Type        │ Lawful Basis   │ Retention        │
├──────────────────┼────────────────┼──────────────────┤
│ Email            │ ✓ Consent      │ ✓ 2 years        │
│ Phone            │ ✗ NEEDS REVIEW │ ✗ Indefinite     │
│ IP Address       │ ⚠ Legitimate   │ ✓ 90 days        │
└──────────────────┴────────────────┴──────────────────┘

GAPS FOUND:
□ Phone number: No consent mechanism
□ IP logging: Review retention policy
□ Cookie banner: Missing granular controls
```

### `/soc2-readiness` - SOC2 Compliance Assessment

Performs gap analysis across all 5 SOC2 Trust Service Criteria.

**Usage:**
```bash
/soc2-readiness
/soc2-readiness --criteria availability,confidentiality
```

**Assessment Framework:**
```yaml
# SOC2 Control Matrix
trust_service_criteria:
  - id: CC6.1
    criterion: Security
    control: Logical access controls
    evidence_required:
      - IAM policies
      - MFA enforcement
      - Access logs
    
  - id: CC7.2
    criterion: Availability
    control: System monitoring
    evidence_required:
      - Uptime metrics
      - Incident response logs
      - Backup verification
```

**Output Format:**
```
SOC2 TYPE II READINESS  —  5 criteria assessed

SECURITY (Common Criteria)
  CC6.1 Logical Access      ⚠  MFA not enforced (gap: 23%)
  CC6.6 Encryption          ✓  TLS 1.3, AES-256
  CC6.7 Key Management      ✗  Manual key rotation

AVAILABILITY
  A1.1 System Monitoring    ✓  24/7 alerting
  A1.2 Backup & Recovery    ⚠  RPO exceeds policy

READINESS SCORE: 67%  (needs 85%+ for audit)

PRIORITY ACTIONS:
1. Enforce MFA org-wide (2 weeks)
2. Automate key rotation (1 week)
3. Improve backup RPO (3 days)
```

### `/threat-model` - STRIDE Threat Modeling

Generates STRIDE threat models for architecture diagrams with risk matrices.

**Usage:**
```bash
/threat-model architecture.png
/threat-model --format mermaid --output threats.md
```

**STRIDE Analysis Pattern:**
```python
# STRIDE threat categories
STRIDE = {
    'Spoofing': ['authentication', 'identity'],
    'Tampering': ['data_integrity', 'code_integrity'],
    'Repudiation': ['logging', 'audit_trail'],
    'Information_Disclosure': ['encryption', 'access_control'],
    'Denial_of_Service': ['rate_limiting', 'resource_exhaustion'],
    'Elevation_of_Privilege': ['authorization', 'input_validation']
}

def analyze_component(component, data_flows):
    threats = []
    for category, indicators in STRIDE.items():
        if not has_controls(component, indicators):
            threats.append({
                'category': category,
                'severity': calculate_severity(component, data_flows),
                'mitigation': suggest_controls(category)
            })
    return threats
```

**Example Output:**
```
THREAT MODEL  —  Web API Architecture

COMPONENTS:
  [Client] → [API Gateway] → [Auth Service] → [Database]

STRIDE THREATS:
┌─────────────────────┬──────────┬──────────────────────────┐
│ Threat              │ Risk     │ Mitigation               │
├─────────────────────┼──────────┼──────────────────────────┤
│ Spoofing: API keys  │ 🔴 High  │ Implement JWT + refresh  │
│ Tampering: API req  │ 🟠 Med   │ Add HMAC signatures      │
│ Info Disclosure     │ 🔴 High  │ Encrypt data at rest     │
│ DoS: Rate limiting  │ 🟡 Low   │ Add WAF rules            │
└─────────────────────┴──────────┴──────────────────────────┘

RISK MATRIX:
         Impact →
    Low    Med    High
L ┌──────┬──────┬──────┐
i │  🟢  │  🟡  │  🟠  │
k ├──────┼──────┼──────┤
e │  🟡  │  🟠  │  🔴  │ ← API Spoofing
l ├──────┼──────┼──────┤
i │  🟠  │  🔴  │  🔴  │
h └──────┴──────┴──────┘
o
o
d
```

### `/secret-detect` - Pre-commit Secret Detection

Configures pre-commit hooks to detect secrets with entropy scanning.

**Usage:**
```bash
/secret-detect --install
/secret-detect --scan .
/secret-detect --config .secrets.yaml
```

**Hook Configuration:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: detect-secrets
        name: Detect secrets
        entry: detect-secrets-hook
        language: system
        files: .*
        exclude: |
          (?x)^(
            package-lock.json|
            \.secrets\.baseline
          )$

# .secrets.yaml
plugins:
  - name: ArtifactoryDetector
  - name: AWSKeyDetector
  - name: Base64HighEntropyString
    limit: 4.5
  - name: PrivateKeyDetector
  
filters:
  - path: tests/fixtures/
  - path: docs/examples/
```

**Entropy Detection Implementation:**
```python
import math
from collections import Counter

def calculate_entropy(string):
    """Calculate Shannon entropy to detect high-entropy secrets"""
    if not string:
        return 0
    
    entropy = 0
    for count in Counter(string).values():
        probability = count / len(string)
        entropy -= probability * math.log2(probability)
    
    return entropy

def scan_for_secrets(content, entropy_threshold=4.5):
    """Scan content for potential secrets"""
    findings = []
    
    # Regex patterns for known secret types
    patterns = {
        'AWS_KEY': r'AKIA[0-9A-Z]{16}',
        'PRIVATE_KEY': r'-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----',
        'JWT': r'eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*',
        'GITHUB_TOKEN': r'gh[ps]_[A-Za-z0-9]{36}'
    }
    
    for secret_type, pattern in patterns.items():
        matches = re.finditer(pattern, content)
        for match in matches:
            findings.append({
                'type': secret_type,
                'value': match.group()[:8] + '...',
                'line': content[:match.start()].count('\n') + 1
            })
    
    # High-entropy string detection
    for word in content.split():
        if len(word) > 20 and calculate_entropy(word) > entropy_threshold:
            findings.append({
                'type': 'HIGH_ENTROPY',
                'entropy': calculate_entropy(word),
                'line': 'N/A'
            })
    
    return findings
```

**Example Scan Output:**
```
SECRET DETECTION  —  Pre-commit hook scan

SECRETS FOUND:
┌────────────────┬──────────────┬──────────────────────┐
│ Type           │ Location     │ Value                │
├────────────────┼──────────────┼──────────────────────┤
│ AWS_KEY        │ config.js:12 │ AKIA4ODZ...          │
│ PRIVATE_KEY    │ auth.py:45   │ -----BEGIN RSA...    │
│ HIGH_ENTROPY   │ utils.js:89  │ entropy: 5.2         │
└────────────────┴──────────────┴──────────────────────┘

REMEDIATION:
□ Move secrets to environment variables
□ Add affected files to .gitignore
□ Rotate exposed credentials
□ Update .secrets.baseline
```

### `/iam-audit` - IAM Least Privilege Audit

Audits IAM roles for over-permissioned access, stale users, and MFA gaps.

**Usage:**
```bash
/iam-audit
/iam-audit --provider aws
/iam-audit --output report.json
```

**Audit Logic Example:**
```python
# AWS IAM audit example
import boto3
from datetime import datetime, timedelta

def audit_iam_users():
    iam = boto3.client('iam')
    findings = []
    
    users = iam.list_users()['Users']
    
    for user in users:
        username = user['UserName']
        
        # Check MFA
        mfa_devices = iam.list_mfa_devices(UserName=username)
        if not mfa_devices['MFADevices']:
            findings.append({
                'user': username,
                'issue': 'NO_MFA',
                'severity': 'HIGH'
            })
        
        # Check last access
        last_used = iam.get_user(UserName=username).get('PasswordLastUsed')
        if last_used:
            days_inactive = (datetime.now(last_used.tzinfo) - last_used).days
            if days_inactive > 90:
                findings.append({
                    'user': username,
                    'issue': 'STALE_ACCESS',
                    'days_inactive': days_inactive,
                    'severity': 'MEDIUM'
                })
        
        # Check attached policies
        policies = iam.list_attached_user_policies(UserName=username)
        for policy in policies['AttachedPolicies']:
            if policy['PolicyName'] in ['AdministratorAccess', 'PowerUserAccess']:
                findings.append({
                    'user': username,
                    'issue': 'OVERPRIVILEGED',
                    'policy': policy['PolicyName'],
                    'severity': 'HIGH'
                })
    
    return findings
```

**Output Format:**
```
IAM AUDIT  —  AWS Account (account-id: 123456789012)

FINDINGS:
┌──────────────────┬─────────────────┬──────────┬──────────────┐
│ User/Role        │ Issue           │ Severity │ Remediation  │
├──────────────────┼─────────────────┼──────────┼──────────────┤
│ admin-user       │ NO_MFA          │ 🔴 High  │ Enable MFA   │
│ deploy-role      │ OVERPRIVILEGED  │ 🔴 High  │ Scope policy │
│ old-contractor   │ STALE (180d)    │ 🟠 Med   │ Deactivate   │
│ dev-service      │ UNUSED_KEY      │ 🟡 Low   │ Rotate key   │
└──────────────────┴─────────────────┴──────────┴──────────────┘

STATISTICS:
  Total users: 47
  Without MFA: 12 (26%)
  Stale (90d+): 8 (17%)
  Admin access: 5 (11%)

PRIORITY ACTIONS:
1. Enforce MFA policy (1 day)
2. Remove stale users (2 hours)
3. Replace admin roles with scoped policies (1 week)
```

### `/incident-playbook` - Security Incident Response

Generates incident response playbooks: triage → contain → eradicate → recover → lessons learned.

**Usage:**
```bash
/incident-playbook --type data-breach
/incident-playbook --type ransomware
/incident-playbook --custom
```

**Playbook Template:**
```yaml
# Data Breach Response Playbook
incident_type: data_breach
severity: HIGH
owner: CISO

phases:
  1_triage:
    duration: 0-2 hours
    steps:
      - id: T1
        action: Confirm breach scope
        checklist:
          - Identify affected systems
          - Estimate data volume
          - Determine data sensitivity
      
      - id: T2
        action: Assemble response team
        roles:
          - Incident Commander (CISO)
          - Technical Lead (SecOps)
          - Legal Counsel
          - Communications Lead
  
  2_containment:
    duration: 2-8 hours
    steps:
      - id: C1
        action: Isolate affected systems
        commands:
          - aws ec2 modify-instance-attribute --instance-id $INSTANCE_ID --no-source-dest-check
          - iptables -A INPUT -j DROP
      
      - id: C2
        action: Preserve forensic evidence
        commands:
          - dd if=/dev/sda of=/mnt/forensics/disk.img bs=4M
          - tar czf logs-$(date +%Y%m%d).tar.gz /var/log/
  
  3_eradication:
    duration: 8-24 hours
    steps:
      - id: E1
        action: Remove threat actor access
        checklist:
          - Rotate all credentials
          - Revoke API keys
          - Patch vulnerabilities
  
  4_recovery:
    duration: 24-72 hours
    steps:
      - id: R1
        action: Restore from clean backups
      - id: R2
        action: Monitor for re-infection
  
  5_lessons_learned:
    duration: 1 week post-incident
    steps:
      - id: L1
        action: Post-mortem report
      - id: L2
        action: Update runbooks

notifications:
  - type: regulatory
    condition: PII affected
    deadline: 72 hours
    recipients:
      - Data Protection Authority
      - Affected individuals
  
  - type: internal
    condition: always
    recipients:
      - Executive team
      - Legal
      - Board of Directors
```

**Interactive Execution:**
```
INCIDENT RESPONSE  —  Data Breach

PHASE 1: TRIAGE  (0-2 hours)
  [T1] Confirm breach scope
    ☐ Identify affected systems
    ☐ Estimate data volume: ___________
    ☐ Determine sensitivity: [PII] [PHI] [PCI] [Other]
  
  [T2] Assemble response team
    ✓ Incident Commander: Jane Doe (CISO)
    ✓ Technical Lead: John Smith (SecOps)
    ⏳ Legal Counsel: Contacting...

PHASE 2: CONTAINMENT  (2-8 hours)
  [C1] Isolate affected systems
    Command: aws ec2 modify-instance-attribute --instance-id i-abc123
    Execute? [y/N]: _

TIMELINE:
  00:00 - Breach detected
  00:15 - Response team assembled
  00:45 - Systems isolated
  [Current: 01:23]

NEXT STEPS:
  → Complete containment checklist
  → Begin forensic analysis
  → Prepare regulatory notification
```

## Multi-Step Workflows

### `secure-sdlc` - Secure Software Development Lifecycle

Implements shift-left security: threat model → static scan → dynamic scan → pen test → sign-off.

**Usage:**
```bash
/workflows:secure-sdlc <project_path> --scope full
/workflows:secure-sdlc . --phase threat-model
```

**Workflow Steps:**
```
SECURE SDLC WORKFLOW

Phase 1: Requirements & Design
  ├─ [W1] Threat modeling (STRIDE)
  ├─ [W2] Security requirements gathering
  └─ [W3] Architecture security review

Phase 2: Development
  ├─ [W4] Pre-commit secret scanning
  ├─ [W5] SAST (static analysis)
  └─ [W6] Dependency CVE scanning

Phase 3: Testing
  ├─ [W7] DAST (dynamic analysis)
  ├─ [W8] API security testing
  └─ [W9] Penetration testing

Phase 4: Deployment
  ├─ [W10] Container security scanning
  ├─ [W11] IaC security review
  └─ [W12] Security sign-off

Phase 5: Operations
  ├─ [W13] Runtime security monitoring
  ├─ [W14] Vulnerability management
  └─ [W15] Incident response drills
```

### `breach-response` - Data Breach Response

Data breach workflow: detect → assess → notify → remediate → post-mortem.

**Usage:**
```bash
/workflows:breach-response --severity high
```

### `compliance-audit` - Full Compliance Audit

Comprehensive audit: scope → gap analysis → evidence collection → remediation plan.

**Usage:**
```bash
/workflows:compliance-audit --framework soc2
/workflows:compliance-audit --framework gdpr,iso27001
```

### `zero-trust-design` - Zero Trust Architecture

Design zero-trust architecture: identity → network → workload → data layers.

**Usage:**
```bash
/workflows:zero-trust-design --output architecture.md
```

### `vendor-security` - Third-Party Security Assessment

Vendor security assessment: questionnaire → risk score → decision matrix.

**Usage:**
```bash
/workflows:vendor-security --vendor "Acme SaaS Provider"
```

## Configuration

### Global Configuration

Create `~/.claude/skills/security-compliance-suite/config.yaml`:

```yaml
# Security & Compliance Suite Configuration

defaults:
  output_format: table  # table | json | markdown
  severity_threshold: medium  # low | medium | high | critical
  
integrations:
  nvd:
    api_key_env: NVD_API_KEY
    cache_ttl: 86400
  
  github:
    token_env: GITHUB_TOKEN
    
  aws:
    profile: default
    region: us-east-1

scanning:
  owasp:
    categories:
      - injection
      - broken_auth
      - sensitive_data
      - xxe
      - broken_access
      - security_misconfig
      - xss
      - insecure_deserialization
      - components_with_vulnerabilities
      - insufficient_logging
  
  dependencies:
    package_managers:
      - npm
      - pip
      - maven
      - go
    severity_threshold: medium

compliance:
  gdpr:
    dpo_contact: ${DPO_EMAIL}
    retention_policy_days: 730
  
  soc2:
    audit_period_months: 12
    required_score: 85

reporting:
  template: standard
  include_remediation: true
  export_formats:
    - markdown
    - json
    - pdf
```

### Project-Level Configuration

Create `.security-config.yaml` in your project root:

```yaml
# Project-specific security configuration

project:
  name: My Application
  criticality: high  # low | medium | high | critical
  
scan_exclusions:
  paths:
    - node_modules/
    - vendor/
    - .git/
    - tests/fixtures/
  
  files:
    - "*.min.js"
    - "*.test.js"

compliance:
  frameworks:
    - soc2
    - gdpr
  
  data_classification:
    pii_fields:
      - email
      - phone_number
      - ssn
    retention_days: 365

threat_model:
  assets:
    - name: User Database
      classification: confidential
      threats:
        - sql_injection
        - unauthorized_access
    
    - name: API Gateway
      classification: internal
      threats:
        - ddos
        - injection

contacts:
  security_team: security@example.com
  dpo: dpo@example.com
  incident_response: incidents@example.com
```

## Environment Variables

Set these environment variables for external integrations:

```bash
# NVD (National Vulnerability Database)
export NVD_API_KEY=your_nvd_api_key_here

# GitHub (for dependency scanning)
export GITHUB_TOKEN=your_github_token_here

# AWS (for IAM audits)
export AWS_PROFILE=your_aws_profile
export AWS_REGION=us-east-1

# Slack (for incident notifications)
export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Email (for compliance notifications)
export SMTP_HOST=smtp.example.com
export SMTP_PORT=587
export SMTP_USER=alerts@example.com
export SMTP_PASSWORD=your_smtp_password
```

## Common Patterns

### Pattern 1: Daily Security Scan

```bash
#!/bin/bash
# daily-security-scan.sh

# Run OWASP scan
/owasp-scan src/ --output reports/owasp-$(date +%Y%m%d).md

# Check dependencies
/dep-cve --severity high,critical --output reports/cve-$(date +%Y%m%d).json

# Secret detection
/secret-detect --scan . --exclude node_modules/

# Send summary
if [ $? -eq 0 ]; then
  echo "✓ Security scan completed successfully"
else
  echo "⚠ Security issues found - review reports/"
  exit 1
fi
```

### Pattern 2: Pre-Deployment Security Gate

```bash
#!/bin/bash
# pre-deploy-checks.sh

set -e

echo "Running pre-deployment security checks..."

# Static analysis
/owasp-scan src/

# Dependency check
/dep-cve --severity critical

# Container scan (if using Docker)
docker scan myapp:latest

# IAM validation
/iam-audit --output iam-report.json

echo "✓ All security gates passed"
```

### Pattern 3: Compliance Evidence Collection

```bash
#!/bin/bash
# collect-compliance-evidence.sh

AUDIT_DATE=$(date +%Y%m%d)
EVIDENCE_DIR="compliance-evidence-${AUDIT_DATE}"

mkdir -p "${EVIDENCE_DIR}"

# SOC2 controls
/soc2-readiness --output "${EVIDENCE_DIR}/soc2-readiness.md"

# GDPR data flows
/gdpr-audit --output "${EVIDENCE_DIR}/gdpr-audit.md"

# IAM policies
/iam-audit --output "${EVIDENCE_DIR}/iam-audit.json"

# Security logs
cp /var/log/security.log "${EVIDENCE_DIR}/"

# Create archive
tar czf "${EVIDENCE_DIR}.tar.gz" "${EVIDENCE_DIR}/"

echo "✓ Evidence collected: ${EVIDENCE_DIR}.tar.gz"
```

### Pattern 4: Automated Incident Detection

```python
# incident_detector.py
import subprocess
import json

def check_security_posture():
    """Run security checks and detect incidents"""
    
    findings = {
        'critical': [],
        'high': [],
        'medium': []
    }
    
    # Run OWASP scan
