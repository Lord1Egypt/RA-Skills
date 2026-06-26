---
name: security-compliance-skills-suite-claude
description: Security audits, vulnerability management, GDPR/SOC2/ISO27001 compliance and incident response skill suite for AI coding agents
triggers:
  - "scan this code for OWASP vulnerabilities"
  - "run a GDPR compliance audit"
  - "check dependencies for CVEs"
  - "generate a threat model for this architecture"
  - "create a SOC 2 readiness report"
  - "detect secrets in the codebase"
  - "audit IAM permissions"
  - "help me respond to a security incident"
---

# 🔒 Security & Compliance Skills Suite

> Skill by [ara.so](https://ara.so) — Security Skills collection.

A comprehensive skill suite for security audits, vulnerability management, compliance frameworks (GDPR, SOC2, ISO27001), and incident response. Derived from `hesreallyhim/awesome-claude-code` with specialized commands and workflows for security professionals.

## What This Project Does

This skill suite provides AI coding agents with 10 specialized security commands and 5 multi-step workflows to:

- Perform OWASP Top-10 vulnerability scans
- Audit dependencies for known CVEs
- Generate GDPR/SOC2/ISO27001 compliance reports
- Create STRIDE threat models
- Detect secrets and credentials in code
- Audit IAM permissions for least-privilege violations
- Orchestrate security incident response
- Design zero-trust architectures

All commands use structured output with progress tracking, severity-sorted findings, and actionable remediation steps.

## Installation

### Method 1: Direct Clone

```bash
# Clone to Claude Code skills directory
mkdir -p ~/.claude/skills
git clone https://github.com/sparkfinderoven/r01-hesreallyhim-awesome-claude-code-security.git \
  ~/.claude/skills/security-compliance-suite

# Register in Claude Code session
/read ~/.claude/skills/security-compliance-suite/SKILL.md
```

### Method 2: Manual Setup

```bash
# Create skill directory
mkdir -p ~/.claude/skills/security-compliance-suite

# Copy skill files
cp -r ./commands ~/.claude/skills/security-compliance-suite/
cp -r ./workflows ~/.claude/skills/security-compliance-suite/
cp ./SKILL.md ~/.claude/skills/security-compliance-suite/
```

### Verification

In a Claude Code session:

```bash
/skills list
# Should show: security-compliance-suite
```

## Core Commands

### `/owasp-scan` - OWASP Top-10 Vulnerability Scan

Scans code for OWASP Top-10 vulnerabilities with CVSS scores and remediation guidance.

**Usage:**

```bash
/owasp-scan <target_path> [--format=json|md|html] [--severity=critical|high|medium|low]
```

**Example:**

```bash
# Scan web API directory
/owasp-scan ./src/api --format=md --severity=high

# Scan specific file
/owasp-scan ./auth/login.py
```

**Output Structure:**

```
╔══════════════════════════════════════════════════╗
║  OWASP Top-10 Scan — ./src/api                   ║
╠══════════════════════════════════════════════════╣
║  Files scanned:     47                           ║
║  Vulnerabilities:   12                           ║
║  Critical:          3                            ║
║  High:              5                            ║
╚══════════════════════════════════════════════════╝

FINDINGS (sorted by CVSS score)
┌─────┬────────────────────────────┬──────┬──────────┬─────────────┐
│ Sev │ Vulnerability              │ CVSS │ Location │ CWE         │
├─────┼────────────────────────────┼──────┼──────────┼─────────────┤
│ 🔴  │ SQL Injection              │ 9.8  │ api.py:45│ CWE-89      │
│ 🔴  │ Path Traversal             │ 9.1  │ file.py:12│ CWE-22     │
│ 🔴  │ Command Injection          │ 8.8  │ exec.py:89│ CWE-78     │
└─────┴────────────────────────────┴──────┴──────────┴─────────────┘

REMEDIATION (Priority: Critical)
1. [SQL Injection] Use parameterized queries
   Code: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
   
2. [Path Traversal] Validate and sanitize file paths
   Code: safe_path = os.path.realpath(os.path.join(base_dir, user_input))
```

### `/dep-cve` - Dependency CVE Scanner

Scans project dependencies for known CVEs with exploitability scores.

**Usage:**

```bash
/dep-cve [--scope=prod|dev|all] [--output=json|md] [--min-cvss=7.0]
```

**Example:**

```bash
# Scan production dependencies
/dep-cve --scope=prod --min-cvss=7.0

# Full dependency audit
/dep-cve --scope=all --output=json
```

**Supported Ecosystems:**

- Python: `requirements.txt`, `Pipfile`, `pyproject.toml`
- JavaScript: `package.json`, `package-lock.json`, `yarn.lock`
- Ruby: `Gemfile.lock`
- Java: `pom.xml`, `build.gradle`
- Go: `go.mod`, `go.sum`
- Rust: `Cargo.lock`

**Output Example:**

```
CVE REPORT — 234 dependencies scanned
┌──────────────────┬─────────┬──────┬───────────────┬──────────────┐
│ Package          │ Current │ CVSS │ CVE           │ Fixed In     │
├──────────────────┼─────────┼──────┼───────────────┼──────────────┤
│ urllib3          │ 1.26.5  │ 9.8  │ CVE-2023-4567 │ 1.26.18      │
│ django           │ 3.2.0   │ 8.1  │ CVE-2023-1234 │ 3.2.19       │
│ requests         │ 2.25.0  │ 7.5  │ CVE-2023-7890 │ 2.31.0       │
└──────────────────┴─────────┴──────┴───────────────┴──────────────┘

UPGRADE PATH
pip install urllib3==1.26.18 django==3.2.19 requests==2.31.0

EXPLOITABILITY
• urllib3 CVE-2023-4567: Public exploit available, CVSS:3.1/AV:N/AC:L
• django CVE-2023-1234: PoC available, requires authentication
```

### `/gdpr-audit` - GDPR Compliance Audit

Maps data flows, identifies consent gaps, and generates DPA checklist.

**Usage:**

```bash
/gdpr-audit <codebase_path> [--output=report|checklist|map]
```

**Example:**

```bash
# Full GDPR audit with data flow map
/gdpr-audit ./src --output=report

# Generate Article 30 checklist
/gdpr-audit ./src --output=checklist
```

**Analysis Coverage:**

- Personal data collection points
- Lawful basis for processing (Article 6)
- Consent mechanisms (Article 7)
- Data subject rights implementation (Articles 15-22)
- Data retention policies (Article 5)
- Third-party data processors (Article 28)
- Data breach notification (Articles 33-34)

**Output Example:**

```
╔══════════════════════════════════════════════════╗
║  GDPR Compliance Audit — ./src                   ║
╠══════════════════════════════════════════════════╣
║  Personal data fields:     23                    ║
║  Processing activities:    8                     ║
║  Consent mechanisms:       3                     ║
║  Compliance gaps:          5 🔴                  ║
╚══════════════════════════════════════════════════╝

DATA FLOW MAP
User Registration → [email, name, dob] → PostgreSQL
├─ Lawful basis: Consent (Art. 6.1.a)
├─ Retention: 2 years after last login
└─ ⚠️  Missing: explicit consent checkbox

Email Marketing → [email, preferences] → Mailchimp (processor)
├─ Lawful basis: Legitimate interest (Art. 6.1.f)
├─ DPA status: ✓ Agreement signed
└─ 🔴 Missing: opt-out mechanism

COMPLIANCE GAPS
1. 🔴 No data breach notification procedure (Art. 33)
2. 🔴 Data portability not implemented (Art. 20)
3. 🟠 Privacy policy outdated (last updated 2021)
4. 🟡 Cookie consent banner missing GDPR language
5. 🟡 Data retention policy not documented

RECOMMENDED ACTIONS
□ Implement breach detection and 72h notification workflow
□ Add /api/data-export endpoint for data portability
□ Update privacy policy with current processing activities
□ Review and update cookie consent implementation
```

### `/soc2-readiness` - SOC 2 Type II Readiness Assessment

Gap analysis across all 5 Trust Service Criteria.

**Usage:**

```bash
/soc2-readiness [--criteria=CC|A|C|P|PI] [--type=1|2]
```

**Example:**

```bash
# Full SOC 2 Type II assessment
/soc2-readiness --type=2

# Focus on specific criteria
/soc2-readiness --criteria=CC,A --type=2
```

**Trust Service Criteria:**

- **CC**: Common Criteria (governance, risk assessment, monitoring)
- **A**: Availability (uptime, incident management)
- **C**: Confidentiality (data protection, encryption)
- **P**: Processing Integrity (data accuracy, completeness)
- **PI**: Privacy (notice, choice, access)

**Output Example:**

```
SOC 2 TYPE II READINESS — 64 controls assessed
┌──────────┬─────────┬────────┬─────────┬──────────┐
│ Criteria │ Total   │ Pass   │ Fail    │ Score    │
├──────────┼─────────┼────────┼─────────┼──────────┤
│ CC       │ 17      │ 12     │ 5       │ 71%      │
│ A        │ 9       │ 8      │ 1       │ 89%      │
│ C        │ 14      │ 9      │ 5       │ 64%      │
│ P        │ 12      │ 11     │ 1       │ 92%      │
│ PI       │ 12      │ 7      │ 5       │ 58%      │
└──────────┴─────────┴────────┴─────────┴──────────┘

CRITICAL GAPS (Type II POC blockers)
🔴 CC6.1: No formal risk assessment process documented
🔴 C1.2: Encryption at rest not enabled for all databases
🔴 PI1.2: Privacy notice not provided at data collection

EVIDENCE REQUIREMENTS
CC2.1: Organizational chart → ✓ Available
CC3.1: Security policies → ⚠️  Outdated (2022)
A1.2: Incident response plan → ✓ Available
C1.1: Data classification policy → 🔴 Missing
```

### `/threat-model` - STRIDE Threat Modeling

Generates STRIDE threat models from architecture diagrams with risk matrices.

**Usage:**

```bash
/threat-model <architecture_file> [--framework=STRIDE|PASTA|OCTAVE] [--output=md|drawio]
```

**Example:**

```bash
# Generate STRIDE threat model from diagram
/threat-model ./docs/architecture.png --framework=STRIDE

# From text description
/threat-model ./docs/system-design.md
```

**STRIDE Categories:**

- **S**poofing: Authentication threats
- **T**ampering: Integrity threats
- **R**epudiation: Non-repudiation threats
- **I**nformation Disclosure: Confidentiality threats
- **D**enial of Service: Availability threats
- **E**levation of Privilege: Authorization threats

**Output Example:**

```
THREAT MODEL — E-Commerce Platform
Architecture: Web App → API Gateway → Microservices → Database

TRUST BOUNDARIES IDENTIFIED
1. Internet ↔ API Gateway (TLS termination)
2. API Gateway ↔ Internal Services (VPC)
3. Services ↔ Database (Encryption in transit)

THREATS (sorted by risk score)
┌──────┬─────────────────────────────┬──────────┬────────┬──────┐
│ Cat  │ Threat                      │ Asset    │ Impact │ Risk │
├──────┼─────────────────────────────┼──────────┼────────┼──────┤
│ S    │ JWT signature not validated │ API      │ High   │ 9.0  │
│ E    │ IDOR in /api/orders/:id     │ Orders   │ High   │ 8.5  │
│ I    │ PII in server logs          │ Database │ Medium │ 7.0  │
│ T    │ No integrity checks on S3   │ Files    │ Medium │ 6.5  │
│ D    │ No rate limiting on /login  │ Auth     │ Low    │ 5.0  │
└──────┴─────────────────────────────┴──────────┴────────┴──────┘

MITIGATIONS
1. [S] Validate JWT signature with public key in middleware
2. [E] Implement authorization check: user owns order
3. [I] Sanitize PII from logs or use structured logging
4. [T] Enable S3 object versioning and integrity checks
5. [D] Add rate limiting: 5 attempts per 15 minutes
```

### `/secret-detect` - Secret Detection

Pre-commit hook configuration with entropy scanning.

**Usage:**

```bash
/secret-detect [--setup] [--scan-history] [--config]
```

**Example:**

```bash
# Setup pre-commit hook
/secret-detect --setup

# Scan Git history
/secret-detect --scan-history

# Generate configuration
/secret-detect --config
```

**Detection Patterns:**

- AWS keys (AKIA*, ASIA*)
- API keys (high-entropy strings)
- Private keys (BEGIN PRIVATE KEY)
- OAuth tokens
- Database credentials
- JWT secrets
- Slack/Discord webhooks

**Setup Output:**

```bash
# Creates .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

# Creates .gitleaks.toml
[extend]
useDefault = true

[[rules]]
id = "generic-api-key"
description = "Generic API Key"
regex = '''(?i)(api[_-]?key|apikey)['\"]?\s*[:=]\s*['\"]?([a-z0-9]{32,})'''
entropy = 3.5

# Install hook
pre-commit install
```

**History Scan Example:**

```
SCANNING GIT HISTORY — 1,247 commits
⣾ Analyzing commit 892/1247 (71%)

SECRETS FOUND
┌─────────────┬──────────────────┬──────────────────┬─────────┐
│ Type        │ File             │ Commit           │ Branch  │
├─────────────┼──────────────────┼──────────────────┼─────────┤
│ AWS Key     │ config.py        │ a4f3c21 (2023)   │ main    │
│ Private Key │ deploy_key.pem   │ 7b8e912 (2022)   │ prod    │
│ API Token   │ .env.example     │ c2d4f98 (2024)   │ develop │
└─────────────┴──────────────────┴──────────────────┴─────────┘

REMEDIATION
1. Rotate compromised credentials immediately
2. Remove secrets from history:
   git filter-repo --path config.py --invert-paths
3. Add to .gitignore: .env, *.pem, secrets/
```

### `/iam-audit` - IAM Least-Privilege Audit

Audits IAM roles for over-permissioned access, stale credentials, and MFA gaps.

**Usage:**

```bash
/iam-audit [--provider=aws|azure|gcp] [--scope=users|roles|policies]
```

**Example:**

```bash
# Full AWS IAM audit
/iam-audit --provider=aws

# Audit specific scope
/iam-audit --provider=aws --scope=roles
```

**Configuration:**

```bash
# AWS credentials (use environment variables)
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}"
export AWS_REGION="us-east-1"
```

**Output Example:**

```
IAM AUDIT — AWS Account (123456789012)
Users: 47 | Roles: 23 | Policies: 156

OVER-PERMISSIONED ROLES
┌──────────────────────┬─────────────┬──────────────────────┐
│ Role                 │ Risk Score  │ Excessive Permission │
├──────────────────────┼─────────────┼──────────────────────┤
│ DevOps-Engineer      │ 8.5 🔴      │ iam:* (admin)        │
│ Lambda-Execution     │ 7.2 🟠      │ s3:* (all buckets)   │
│ Analytics-Reader     │ 6.1 🟠      │ dynamodb:DeleteTable │
└──────────────────────┴─────────────┴──────────────────────┘

STALE ACCESS
• User: john.doe@company.com — Last activity: 347 days ago
• Access key AKIA...XYZ — Created: 2021-03-15 (unused)

MFA GAPS
• 12 users without MFA (26% of workforce)
• Root account MFA: ✓ Enabled

RECOMMENDATIONS
1. Replace DevOps-Engineer wildcard with specific actions
2. Scope Lambda-Execution to specific S3 buckets
3. Deactivate stale access keys older than 90 days
4. Enforce MFA policy with conditional IAM deny
```

### `/incident-playbook` - Security Incident Response

Orchestrates incident response: triage → contain → eradicate → recover → lessons.

**Usage:**

```bash
/incident-playbook [--type=breach|ransomware|ddos|insider] [--severity=p0|p1|p2]
```

**Example:**

```bash
# Start data breach playbook
/incident-playbook --type=breach --severity=p0

# DDoS incident response
/incident-playbook --type=ddos --severity=p1
```

**Incident Types:**

- **breach**: Data breach / unauthorized access
- **ransomware**: Ransomware infection
- **ddos**: Distributed denial of service
- **insider**: Insider threat / privilege abuse

**Playbook Flow:**

```
╔══════════════════════════════════════════════════╗
║  INCIDENT RESPONSE — Data Breach (P0)            ║
╠══════════════════════════════════════════════════╣
║  Phase: CONTAINMENT                              ║
║  Elapsed: 00:37:12                               ║
║  Next deadline: GDPR notification (71h 22m)      ║
╚══════════════════════════════════════════════════╝

PHASE 1: TRIAGE ✓ Complete (00:15:00)
✓ Incident confirmed: Unauthorized database access
✓ Severity: P0 (>10,000 PII records exposed)
✓ Incident commander: Alice Chen
✓ War room: Slack #incident-2024-05-11

PHASE 2: CONTAINMENT (In Progress)
⟳ [00:37] Isolating affected database server
✓ [00:20] Disabled compromised credentials
✓ [00:10] Enabled detailed audit logging
□ Pending: Block external database access
□ Pending: Snapshot affected systems

NEXT ACTIONS
1. Execute: aws ec2 create-snapshot --volume-id vol-abc123
2. Execute: aws rds modify-db-instance --publicly-accessible false
3. Notify: Legal team (GDPR 72h clock started)
4. Document: Initial breach assessment in incident tracker

STAKEHOLDERS NOTIFIED
✓ Security team
✓ Engineering lead
✓ CTO
⚠️  Legal team (notification pending)
□ Data Protection Officer
```

### `/privacy-policy` - Privacy Policy Generator

Generates GDPR/CCPA-compliant privacy policies from data inventory.

**Usage:**

```bash
/privacy-policy [--framework=gdpr|ccpa|pipeda] [--language=en|de|fr]
```

**Example:**

```bash
# Generate GDPR-compliant policy
/privacy-policy --framework=gdpr --language=en

# Multi-jurisdiction policy
/privacy-policy --framework=gdpr,ccpa
```

**Input (Data Inventory):**

```yaml
# data-inventory.yaml
company:
  name: "Acme Corp"
  dpo_email: "dpo@acme.com"
  
personal_data:
  - type: "email"
    purpose: "Account authentication"
    lawful_basis: "Contract (Art. 6.1.b)"
    retention: "Account lifetime + 30 days"
    
  - type: "name, address"
    purpose: "Order fulfillment"
    lawful_basis: "Contract (Art. 6.1.b)"
    retention: "7 years (tax law)"
    
processors:
  - name: "AWS"
    service: "Database hosting"
    dpa_status: "Signed"
```

**Generated Policy Sections:**

```markdown
# Privacy Policy

**Effective Date:** May 11, 2024  
**Data Protection Officer:** dpo@acme.com

## 1. Data Controller
Acme Corp is the data controller for personal data processed through this service.

## 2. Personal Data We Collect

### Account Authentication
- **Data:** Email address
- **Legal Basis:** Performance of contract (GDPR Art. 6.1.b)
- **Retention:** Account lifetime + 30 days after deletion
- **Your Rights:** Access, rectification, deletion, portability

### Order Fulfillment
- **Data:** Name, postal address
- **Legal Basis:** Performance of contract (GDPR Art. 6.1.b)
- **Retention:** 7 years (legal obligation - tax records)
- **Your Rights:** Access, rectification (deletion limited by law)

## 3. Data Processors
We use third-party processors who have access to your data:
- **AWS** — Database hosting (Data Processing Agreement signed)

## 4. Your Rights (GDPR)
You have the right to:
- Access your personal data (Art. 15)
- Rectify inaccurate data (Art. 16)
- Request deletion (Art. 17)
- Restrict processing (Art. 18)
- Data portability (Art. 20)
- Object to processing (Art. 21)
- Lodge a complaint with supervisory authority

## 5. Data Breach Notification
We will notify you within 72 hours of discovering a breach that affects your rights.

## 6. Contact
For privacy inquiries: dpo@acme.com
```

## Multi-Step Workflows

### `secure-sdlc` - Secure Software Development Lifecycle

Shift-left security workflow: threat model → SAST → DAST → pen test → sign-off.

**Usage:**

```bash
/workflows:secure-sdlc <project_path> [--stage=all|threat|sast|dast|pentest]
```

**Workflow Stages:**

```
1. THREAT MODELING
   ├─ /threat-model ./docs/architecture.md
   └─ Output: Risk matrix with mitigations

2. STATIC ANALYSIS (SAST)
   ├─ /owasp-scan ./src
   ├─ /secret-detect --scan-history
   └─ Output: Vulnerability report

3. DEPENDENCY AUDIT
   ├─ /dep-cve --scope=all
   └─ Output: CVE report with upgrade path

4. DYNAMIC ANALYSIS (DAST)
   ├─ Run web app security scanner
   └─ Output: Runtime vulnerability findings

5. PENETRATION TEST
   ├─ /pentest-report ./results
   └─ Output: Executive summary + findings

6. SECURITY SIGN-OFF
   └─ Risk acceptance form
```

### `breach-response` - Data Breach Response

Orchestrates breach response: detect → assess → notify → remediate → post-mortem.

**Usage:**

```bash
/workflows:breach-response [--type=confirmed|suspected]
```

**Workflow:**

```
PHASE 1: DETECTION (0-1 hour)
□ Confirm breach indicator
□ Assign incident commander
□ Start incident log

PHASE 2: ASSESSMENT (1-4 hours)
□ Identify affected systems
□ Estimate data exposure scope
□ Classify data sensitivity

PHASE 3: NOTIFICATION (Within 72h for GDPR)
□ Notify Data Protection Officer
□ Notify supervisory authority (if Art. 33 threshold met)
□ Notify affected individuals (if Art. 34 threshold met)
□ Document notification timeline

PHASE 4: REMEDIATION
□ Close security gap
□ Revoke compromised credentials
□ Deploy security patches

PHASE 5: POST-MORTEM
□ Root cause analysis
□ Timeline reconstruction
□ Preventive measures
```

### `compliance-audit` - Full Compliance Audit

End-to-end audit: scope → gap analysis → evidence collection → remediation plan.

**Usage:**

```bash
/workflows:compliance-audit [--framework=soc2|iso27001|gdpr]
```

### `zero-trust-design` - Zero Trust Architecture

Design workflow: identity → network → workload → data layer security.

**Usage:**

```bash
/workflows:zero-trust-design <architecture_file>
```

**Design Layers:**

```
1. IDENTITY LAYER
   ├─ Multi-factor authentication
   ├─ Identity federation (SSO)
   └─ /iam-audit for least privilege

2. NETWORK LAYER
   ├─ Micro-segmentation
   ├─ Software-defined perimeter
   └─ Zero-trust network access (ZTNA)

3. WORKLOAD LAYER
   ├─ Container security
   ├─ Runtime protection
   └─ /owasp-scan for vulnerabilities

4. DATA LAYER
   ├─ Encryption at rest and in transit
   ├─ Data classification
   └─ /gdpr-audit for data governance
```

### `vendor-security` - Third-Party Vendor Assessment

Vendor risk assessment: questionnaire → risk scoring → decision framework.

**Usage:**

```bash
/workflows:vendor-security <vendor_name>
```

**Assessment Domains:**

- Security certifications (SOC 2, ISO 27001)
- Data processing agreements
- Incident response capabilities
- Business continuity plans
- Subprocessor disclosure

## Configuration

### Global Settings

Create `~/.security-skills/config.yaml`:

```yaml
# Output preferences
output:
  format: "markdown"  # markdown | json | html
  severity_colors: true
  progress_bars: true

# CVSS scoring
cvss:
  min_reportable: 4.0
  critical_threshold: 9.0
  high_threshold: 7.0

# Compliance frameworks
compliance:
  primary: "gdpr"  # gdpr | soc2 | iso27001
  data_residency: "eu"
  
# Notifications
notifications:
  slack_webhook: "${SLACK_WEBHOOK_URL}"
  email: "security@company.com"
  
# Cloud providers
cloud:
  aws:
    profile: "default"
    regions: ["us-east-1", "eu-west-1"]
  azure:
    subscription_id: "${AZURE_SUBSCRIPTION_ID}"
  gcp:
    project_id: "${GCP_PROJECT_ID}"
```

### Environment Variables

```bash
# Cloud provider credentials
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}"
export AZURE_SUBSCRIPTION_ID="${AZURE_SUBSCRIPTION_ID}"
export GCP_PROJECT_ID="${GCP_PROJECT_ID}"

# Notifications
export SLACK_WEBHOOK_URL="${SLACK_WEBHOOK_URL}"

# CVE databases
export NVD_API_KEY="${NVD_API_KEY}"  # Optional: faster CVE lookups

# Scanning tools
export GITLEAKS_CONFIG="~/.security-skills/gitleaks.toml"
```

## Common Patterns

### Pattern 1: Pre-Deployment Security Gate

```bash
# Run before each deployment
/owasp-scan ./src --severity=high
/dep-cve --scope=prod --min-cvss=7.0
/secret-detect

# If any critical findings, block deployment
if [ $? -ne 0 ]; then
  echo "❌ Security gate failed - deployment blocked"
  exit 1
fi
```

### Pattern 2: Continuous Compliance Monitoring

```bash
# Weekly compliance check
/gdpr-audit ./src --output=report
/soc2-readiness --type=2
/iam-audit --provider=aws

# Generate compliance dashboard
# Send to stakeholders
```

### Pattern 3: Incident Response Automation

```bash
# Triggered by security alert
/incident-playbook --type=breach --severity=p0

# Automatic containment actions
aws ec2 modify-instance-attribute \
  --instance-id i-1234567890abcdef0 \
  --no-source-dest-check

# Notify stakeholders
curl -X POST "${SLACK_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{"text": "🚨 P0 Security Incident - War room #incident-active"}'
```

### Pattern 4: Shift-Left Security in CI/CD

```yaml
# .github/workflows/security.yml
name: Security Checks
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: OWASP Scan
        run: /owasp-scan ./src --format=json --output=owasp.json
        
      - name: Dependency CVE Check
        run: /dep-cve --scope=all --output=json --output=cve.json
        
      - name: Secret Detection
        run: /secret-detect
        
