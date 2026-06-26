---
name: sparkfinderoven-r01-security-compliance-skills
description: Security & compliance skill suite for OWASP scanning, CVE detection, GDPR/SOC2 audits, threat modeling, and incident response workflows
triggers:
  - scan my code for OWASP vulnerabilities
  - check dependencies for CVEs
  - audit our application for GDPR compliance
  - create a threat model for this architecture
  - generate a SOC 2 readiness report
  - detect secrets in the codebase
  - run a security audit on this project
  - help me respond to a security incident
---

# 🔒 Security & Compliance Skills Suite

> Skill by [ara.so](https://ara.so) — Security Skills collection.

This skill suite provides AI coding agents with expertise in security auditing, vulnerability management, compliance frameworks (GDPR/SOC2/ISO27001), and incident response. Derived from hesreallyhim/awesome-claude-code, it offers 10 specialized commands and 5 multi-step workflows with structured output.

## What This Project Does

The r01-security-compliance-skills suite enables:
- **OWASP Top-10 vulnerability scanning** with CVSS scoring and remediation guidance
- **Dependency CVE detection** with exploitability analysis and upgrade paths
- **Compliance auditing** for GDPR, SOC 2, ISO 27001 frameworks
- **Threat modeling** using STRIDE methodology
- **IAM least-privilege auditing** for over-permissioned roles
- **Secret detection** with pre-commit hooks and entropy scanning
- **Incident response playbooks** for breach scenarios

## Installation

### Local Installation

```bash
# Clone to Claude Code skills directory
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/sparkfinderoven/r01-hesreallyhim-awesome-claude-code-security.git

# Or copy into existing skills directory
cp -r /path/to/r01-security-compliance-skills ~/.claude/skills/
```

### Register with Claude Code

```bash
# In a Claude Code session, load the skill:
/read ~/.claude/skills/r01-hesreallyhim-awesome-claude-code-security/SKILL.md
```

### Verify Installation

```bash
# Check available commands
/help security

# Test with a simple scan
/owasp-scan --target ./src --dry-run
```

## Core Commands

### `/owasp-scan` - OWASP Top-10 Code Scanning

Scans code for OWASP Top-10 vulnerabilities with exploit descriptions and CVSS scores.

```bash
# Scan entire project
/owasp-scan .

# Scan specific directory with custom rules
/owasp-scan ./api --rules owasp-top-10-2021 --severity high

# Output JSON report
/owasp-scan ./src --output json > security-report.json
```

**Example Output Structure:**
```
OWASP Scan Results — ./api
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Files scanned: 47
✓ Checks run: 14
⚠ Findings: 3 critical, 5 high, 12 medium

CRITICAL FINDINGS
┌──────┬─────────────────────────────┬──────┬──────────────┐
│ ID   │ Issue                       │ CVSS │ Location     │
├──────┼─────────────────────────────┼──────┼──────────────┤
│ A03  │ SQL Injection               │ 9.8  │ api/search.js│
│ A07  │ JWT None Algorithm Accepted │ 9.1  │ auth/jwt.js  │
└──────┴─────────────────────────────┴──────┴──────────────┘

REMEDIATION (Critical Priority)
• SQL Injection: Use parameterized queries
  - Replace: db.query(`SELECT * FROM users WHERE id=${id}`)
  - With: db.query('SELECT * FROM users WHERE id=?', [id])
```

### `/dep-cve` - Dependency CVE Scanning

Analyzes dependencies for known CVEs with exploitability scores.

```bash
# Scan package.json dependencies
/dep-cve --file package.json

# Full recursive scan with dev dependencies
/dep-cve --scope full --include-dev

# Check specific package
/dep-cve --package express@4.17.1
```

**Example Integration:**
```javascript
// In package.json scripts
{
  "scripts": {
    "security:deps": "claude-code /dep-cve --scope full --output md > SECURITY.md",
    "precommit": "claude-code /dep-cve --severity critical --exit-code"
  }
}
```

### `/gdpr-audit` - GDPR Compliance Auditing

Maps data flows, identifies consent gaps, and generates DPA checklists.

```bash
# Full GDPR audit
/gdpr-audit --scope full

# Audit specific data category
/gdpr-audit --category personal-data --output report

# Check consent mechanisms
/gdpr-audit --focus consent --include-cookies
```

**Configuration File (`.gdpr-config.yml`):**
```yaml
data_inventory:
  - category: personal_identifiable
    fields: [email, name, phone]
    storage: postgresql
    retention_days: 365
    legal_basis: consent
  
  - category: tracking
    fields: [ip_address, user_agent, session_id]
    storage: redis
    retention_days: 90
    legal_basis: legitimate_interest

consent_mechanisms:
  - type: cookie_banner
    granular: true
    documented: true
  
processors:
  - name: AWS
    dpa_signed: true
    location: eu-west-1
```

### `/soc2-readiness` - SOC 2 Compliance Gap Analysis

Evaluates readiness across all 5 Trust Service Criteria (TSC).

```bash
# Full SOC 2 Type II assessment
/soc2-readiness --type type2

# Focus on specific criteria
/soc2-readiness --criteria security,availability

# Generate evidence requirements
/soc2-readiness --output evidence-matrix
```

**Example Report:**
```
SOC 2 Readiness Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Score: 67% (Needs Improvement)

TRUST SERVICE CRITERIA
┌────────────────┬────────┬──────┬────────────────┐
│ Criteria       │ Score  │ Gaps │ Priority       │
├────────────────┼────────┼──────┼────────────────┤
│ Security       │ 78%    │  4   │ Medium         │
│ Availability   │ 45%    │  9   │ 🔴 Critical    │
│ Processing     │ 72%    │  3   │ Low            │
│ Confidentiality│ 89%    │  1   │ Low            │
│ Privacy        │ 54%    │  7   │ High           │
└────────────────┴────────┴──────┴────────────────┘

CRITICAL GAPS (Availability)
• No documented disaster recovery plan
• RTO/RPO not defined for production systems
• Backup restoration not tested in last 90 days
```

### `/threat-model` - STRIDE Threat Modeling

Generates STRIDE-based threat models with risk matrices.

```bash
# Create threat model from architecture diagram
/threat-model --input architecture.png

# Text-based architecture description
/threat-model --architecture "Web app → API Gateway → Lambda → RDS"

# Update existing model
/threat-model --update ./docs/threat-model.md --new-component "Redis Cache"
```

**Example Threat Model:**
```markdown
# Threat Model — Payment Processing System

## Architecture
User → HTTPS → Load Balancer → API Server → PostgreSQL
                                    ↓
                               Payment Gateway (Stripe)

## STRIDE Analysis

### Spoofing
🔴 HIGH | User authentication bypass via JWT manipulation
- Mitigation: Implement RS256 with key rotation
- Status: Open

### Tampering
🟠 MEDIUM | SQL injection in payment history endpoint
- Mitigation: Use parameterized queries + ORM
- Status: In Review

### Repudiation
🟡 LOW | Insufficient audit logging on failed payments
- Mitigation: Log all payment attempts with user context
- Status: Planned

### Information Disclosure
🔴 HIGH | Credit card data in application logs
- Mitigation: PCI-DSS compliant logging, tokenization
- Status: Open

### Denial of Service
🟠 MEDIUM | No rate limiting on payment API
- Mitigation: Implement rate limiting (10 req/min per user)
- Status: In Progress

### Elevation of Privilege
🟡 LOW | Admin role has excessive database permissions
- Mitigation: Principle of least privilege review
- Status: Planned
```

### `/secret-detect` - Secret Detection Configuration

Configures pre-commit hooks for secret scanning with entropy analysis.

```bash
# Initialize secret detection
/secret-detect --init

# Scan existing codebase
/secret-detect --scan-history

# Configure custom patterns
/secret-detect --add-pattern "CUSTOM_API_KEY_[A-Za-z0-9]{32}"
```

**Generated Pre-commit Hook (`.git/hooks/pre-commit`):**
```bash
#!/bin/bash
# Auto-generated by /secret-detect

echo "Running secret detection..."

# High-entropy string detection
git diff --cached --name-only | xargs -I {} sh -c '
  if grep -E "[A-Za-z0-9+/]{40,}" {} > /dev/null 2>&1; then
    echo "⚠️  High-entropy string detected in: {}"
    echo "   This may be a secret. Review before committing."
    exit 1
  fi
'

# Known secret patterns
PATTERNS=(
  "AKIA[0-9A-Z]{16}"                    # AWS Access Key
  "sk_live_[0-9a-zA-Z]{24}"             # Stripe Live Key
  "ghp_[0-9a-zA-Z]{36}"                 # GitHub Personal Access Token
  "xox[baprs]-[0-9a-zA-Z]{10,48}"       # Slack Token
  "-----BEGIN (RSA|OPENSSH) PRIVATE KEY" # Private Keys
)

for pattern in "${PATTERNS[@]}"; do
  if git diff --cached | grep -E "$pattern" > /dev/null 2>&1; then
    echo "🔴 SECRET DETECTED: Pattern '$pattern'"
    echo "   Remove secret and use environment variables instead."
    exit 1
  fi
done

echo "✓ No secrets detected"
```

### `/iam-audit` - IAM Least-Privilege Auditing

Audits IAM roles for over-permissions, stale access, and MFA gaps.

```bash
# Full IAM audit
/iam-audit

# Audit specific AWS account
/iam-audit --provider aws --account-id 123456789012

# Check for unused permissions
/iam-audit --focus unused-permissions --days 90
```

**Example Output:**
```
IAM Audit Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OVER-PERMISSIONED ROLES
┌────────────────┬──────────────┬────────────────┐
│ Role           │ Risk Level   │ Issue          │
├────────────────┼──────────────┼────────────────┤
│ dev-full-access│ 🔴 Critical  │ Admin wildcard │
│ lambda-exec    │ 🟠 High      │ s3:* on all    │
│ ec2-instance   │ 🟡 Medium    │ Unused RDS     │
└────────────────┴──────────────┴────────────────┘

STALE ACCESS (90+ days inactive)
• user@example.com — Last login: 147 days ago
• service-account-old — Last used: 203 days ago

MFA GAPS
• 3 admin users without MFA enabled
• 12 privileged roles without MFA requirement

RECOMMENDATIONS
1. Replace dev-full-access with scoped policies
2. Remove s3:* from lambda-exec, grant specific bucket access
3. Deprovision stale accounts within 7 days
4. Enforce MFA for all admin and privileged access
```

### `/incident-playbook` - Security Incident Response

Generates structured incident response playbooks.

```bash
# Create playbook for incident type
/incident-playbook --type data-breach

# Interactive incident response
/incident-playbook --interactive --severity critical

# Load existing incident
/incident-playbook --load INC-2024-001
```

**Example Playbook:**
```markdown
# Security Incident Playbook — Data Breach

## 1. TRIAGE (0-15 minutes)

### Immediate Actions
- [ ] Activate incident response team
- [ ] Establish secure communication channel
- [ ] Document initial discovery and scope
- [ ] Assign incident commander

### Initial Assessment
- [ ] Identify affected systems
- [ ] Estimate number of records exposed
- [ ] Classify data sensitivity (PII, PCI, PHI, etc.)
- [ ] Determine if breach is ongoing

## 2. CONTAIN (15-60 minutes)

### Stop Active Breach
- [ ] Isolate compromised systems from network
- [ ] Rotate all credentials with access to affected systems
- [ ] Block suspicious IP addresses at firewall
- [ ] Disable compromised user accounts

### Preserve Evidence
- [ ] Take disk snapshots of affected systems
- [ ] Collect network logs and traffic captures
- [ ] Document all actions with timestamps
- [ ] Maintain chain of custody

## 3. ERADICATE (1-4 hours)

### Remove Threat
- [ ] Identify root cause and attack vector
- [ ] Patch exploited vulnerabilities
- [ ] Remove malware/backdoors
- [ ] Rebuild compromised systems from clean images

### Verify Clean State
- [ ] Run full security scans
- [ ] Check for persistence mechanisms
- [ ] Review user accounts for unauthorized access
- [ ] Audit configuration changes

## 4. RECOVER (4-24 hours)

### Restore Operations
- [ ] Bring systems back online in controlled manner
- [ ] Monitor for signs of reinfection
- [ ] Restore data from clean backups if needed
- [ ] Update security controls based on lessons learned

### Communication
- [ ] Notify affected users within 72 hours (GDPR)
- [ ] File breach notification with regulators
- [ ] Coordinate with legal and PR teams
- [ ] Prepare public statement if required

## 5. LESSONS LEARNED (1-2 weeks post-incident)

### Post-Mortem
- [ ] Conduct blameless post-mortem
- [ ] Document timeline and decisions
- [ ] Identify preventive measures
- [ ] Update incident response plan
- [ ] Schedule security training

### Metrics
- Detection time: ___
- Containment time: ___
- Recovery time: ___
- Records affected: ___
- Estimated cost: ___
```

### `/pentest-report` - Penetration Test Reporting

Structures penetration test findings into executive and technical reports.

```bash
# Generate report from findings
/pentest-report --input findings.json

# Create executive summary
/pentest-report --type executive --audience board

# Technical deep-dive
/pentest-report --type technical --include-exploits
```

### `/privacy-policy` - Privacy Policy Generator

Generates GDPR/CCPA-compliant privacy policies from data inventory.

```bash
# Generate from data inventory
/privacy-policy --input data-inventory.yml

# Update existing policy
/privacy-policy --update privacy.md --add-processor "SendGrid"

# Multi-jurisdiction support
/privacy-policy --jurisdictions eu,us-ca,uk
```

## Multi-Step Workflows

### `secure-sdlc` - Secure Software Development Lifecycle

End-to-end security workflow from threat modeling to sign-off.

```bash
# Run full secure SDLC workflow
/workflows:secure-sdlc --target ./my-app

# Run specific stages
/workflows:secure-sdlc --stages "threat-model,code-scan"
```

**Workflow Steps:**
1. Threat modeling (STRIDE analysis)
2. Static code analysis (OWASP scan)
3. Dependency vulnerability scan
4. Dynamic application security testing (DAST)
5. Penetration testing
6. Security sign-off checklist

### `breach-response` - Data Breach Response

Orchestrated breach response workflow.

```bash
# Initiate breach response
/workflows:breach-response --severity critical

# Continue from checkpoint
/workflows:breach-response --resume-from contain
```

### `compliance-audit` - Full Compliance Audit

Multi-framework compliance assessment.

```bash
# Run compliance audit
/workflows:compliance-audit --frameworks gdpr,soc2,iso27001

# Specific scope
/workflows:compliance-audit --scope "user data processing"
```

### `zero-trust-design` - Zero Trust Architecture

Designs zero-trust architecture across identity, network, workload, and data layers.

```bash
# Design zero-trust architecture
/workflows:zero-trust-design --current-architecture aws-vpc.yml
```

### `vendor-security` - Third-Party Security Assessment

Assesses vendor security posture with standardized questionnaire.

```bash
# Assess new vendor
/workflows:vendor-security --vendor "Acme SaaS Inc"

# Automated risk scoring
/workflows:vendor-security --questionnaire responses.json --auto-score
```

## Configuration

### Global Config (`.security-skills-config.yml`)

```yaml
# Place in project root or ~/.config/security-skills/

# Default severity thresholds
severity:
  block_on: critical
  warn_on: high
  report_all: true

# Output preferences
output:
  format: table  # table, json, markdown
  color: true
  verbose: false

# Integration settings
integrations:
  jira:
    enabled: true
    url: ${JIRA_URL}
    api_token: ${JIRA_API_TOKEN}
    project_key: SEC
  
  slack:
    enabled: true
    webhook_url: ${SLACK_WEBHOOK_URL}
    channel: "#security-alerts"
  
  github:
    enabled: true
    token: ${GITHUB_TOKEN}
    create_issues: true

# Custom rules
custom_rules:
  - id: custom-001
    name: "Internal API Key Pattern"
    pattern: "INTERNAL_[A-Z0-9]{24}"
    severity: high
    
# Compliance frameworks
compliance:
  primary: gdpr
  secondary: [soc2, iso27001]
  audit_schedule: quarterly
```

### Environment Variables

```bash
# Required for integrations
export JIRA_URL="https://your-org.atlassian.net"
export JIRA_API_TOKEN="your-token-here"
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/xxx"
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"

# Optional - provider-specific
export AWS_PROFILE="security-audit"
export AZURE_SUBSCRIPTION_ID="xxxxx"
export GCP_PROJECT_ID="your-project"
```

## Common Patterns

### CI/CD Integration

**GitHub Actions (`.github/workflows/security.yml`):**
```yaml
name: Security Checks

on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Security Skills
        run: |
          mkdir -p ~/.claude/skills
          cp -r ./.security-skills ~/.claude/skills/
      
      - name: OWASP Scan
        run: |
          claude-code /owasp-scan . --output json > owasp-report.json
      
      - name: Dependency CVE Scan
        run: |
          claude-code /dep-cve --scope full --severity critical --exit-code
      
      - name: Secret Detection
        run: |
          claude-code /secret-detect --scan-history
      
      - name: Upload Reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            owasp-report.json
            SECURITY.md
```

### Pre-commit Hook Integration

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "🔒 Running security checks..."

# Secret detection
if ! claude-code /secret-detect --staged-only; then
  echo "❌ Secret detection failed"
  exit 1
fi

# Quick OWASP scan on changed files
CHANGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(js|py|java|go)$')
if [ -n "$CHANGED_FILES" ]; then
  if ! claude-code /owasp-scan $CHANGED_FILES --fast; then
    echo "❌ Security scan found critical issues"
    exit 1
  fi
fi

echo "✅ Security checks passed"
```

### Automated Compliance Reporting

```python
# scripts/weekly-compliance-report.py
import subprocess
import json
from datetime import datetime

def run_compliance_scan():
    """Run compliance audit and send report"""
    
    # Run GDPR audit
    gdpr_result = subprocess.run(
        ["claude-code", "/gdpr-audit", "--output", "json"],
        capture_output=True,
        text=True
    )
    
    # Run SOC 2 readiness
    soc2_result = subprocess.run(
        ["claude-code", "/soc2-readiness", "--output", "json"],
        capture_output=True,
        text=True
    )
    
    # Parse results
    gdpr_data = json.loads(gdpr_result.stdout)
    soc2_data = json.loads(soc2_result.stdout)
    
    # Generate summary
    report = f"""
    Compliance Report — {datetime.now().strftime('%Y-%m-%d')}
    
    GDPR Status: {gdpr_data['overall_compliance']}%
    Critical Gaps: {gdpr_data['critical_gaps_count']}
    
    SOC 2 Readiness: {soc2_data['overall_score']}%
    TSC Failures: {soc2_data['tsc_failures']}
    
    Action Required: {gdpr_data['critical_gaps_count'] + soc2_data['critical_gaps_count']} items
    """
    
    # Send to Slack
    subprocess.run([
        "curl", "-X", "POST",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"text": report}),
        os.environ["SLACK_WEBHOOK_URL"]
    ])

if __name__ == "__main__":
    run_compliance_scan()
```

### Incident Response Automation

```bash
#!/bin/bash
# scripts/incident-response.sh

SEVERITY=$1
INCIDENT_TYPE=$2

if [ -z "$SEVERITY" ] || [ -z "$INCIDENT_TYPE" ]; then
  echo "Usage: ./incident-response.sh <critical|high|medium> <data-breach|ransomware|ddos>"
  exit 1
fi

# Create incident directory
INCIDENT_ID="INC-$(date +%Y%m%d-%H%M%S)"
mkdir -p "incidents/$INCIDENT_ID"

# Generate playbook
claude-code /incident-playbook \
  --type "$INCIDENT_TYPE" \
  --severity "$SEVERITY" \
  --output "incidents/$INCIDENT_ID/playbook.md"

# Run IAM audit
claude-code /iam-audit \
  --output json > "incidents/$INCIDENT_ID/iam-audit.json"

# Capture current state
echo "Capturing system state..."
claude-code /threat-model \
  --current-state \
  --output "incidents/$INCIDENT_ID/current-threat-model.md"

# Create Jira ticket
if [ -n "$JIRA_API_TOKEN" ]; then
  ISSUE_KEY=$(claude-code /integrations:jira:create-incident \
    --incident-id "$INCIDENT_ID" \
    --severity "$SEVERITY" \
    --type "$INCIDENT_TYPE")
  echo "Jira Issue Created: $ISSUE_KEY"
fi

# Notify team
echo "🚨 Security Incident: $INCIDENT_ID" | \
  claude-code /integrations:slack:notify \
    --channel security-incidents \
    --attach "incidents/$INCIDENT_ID/playbook.md"

echo "Incident $INCIDENT_ID initialized. Follow playbook at incidents/$INCIDENT_ID/playbook.md"
```

## Troubleshooting

### Command Not Found

```bash
# Verify installation
ls -la ~/.claude/skills/

# Reload skill in Claude Code session
/read ~/.claude/skills/r01-hesreallyhim-awesome-claude-code-security/SKILL.md

# Check Claude Code version (requires 0.8.0+)
claude-code --version
```

### False Positives in Scans

```yaml
# Create .security-ignore.yml in project root
ignore_patterns:
  - pattern: "test/fixtures/**"
    reason: "Test data, not production code"
  
  - pattern: "docs/examples/**"
    reason: "Documentation examples"
  
  - finding_id: "OWASP-A03-SQL-001"
    file: "src/legacy/report-builder.js"
    reason: "Acknowledged risk - scheduled for refactor Q3"
    expires: "2024-09-30"
```

### Integration Issues

```bash
# Test Jira connection
claude-code /integrations:test --service jira

# Verify environment variables
env | grep -E '(JIRA|SLACK|GITHUB)'

# Debug mode
claude-code /owasp-scan . --debug --verbose
```

### Performance Optimization

```bash
# For large codebases, use incremental scanning
claude-code /owasp-scan --incremental --cache-results

# Parallel scanning
claude-code /dep-cve --parallel --workers 4

# Exclude directories
claude-code /owasp-scan . --exclude node_modules,vendor,dist
```

### Custom Rule Not Triggering

```yaml
# Validate custom rule syntax
custom_rules:
  - id: custom-api-key
    name: "Custom API Key Detection"
    pattern: "API_KEY_[A-Z0-9]{32}"  # Must be valid regex
    severity: high
    file_types: [".js", ".py", ".env"]  # Limit to specific extensions
    enabled: true  # Explicitly enable
```

```bash
# Test custom rule
claude-code /secret-detect --test-rule custom-api-key --sample "API_KEY_ABC123XYZ789012345678901234567"
```

### Report Generation Failures

```bash
# Ensure output directory exists
mkdir -p reports/

# Check disk space
df -h

# Use streaming output for large reports
claude-code /owasp-scan . --output json --stream > reports/scan-$(date +%Y%m%d).json

# Compress old reports
find reports/ -name "*.json" -mtime +30 -exec gzip {} \;
```

## Advanced Usage

### Programmatic Access

```python
# Python wrapper for security-skills commands
import subprocess
import json

class SecuritySkills:
    def __init__(self, config_path=None):
        self.config = config_path
    
    def owasp_scan(self, target, severity="high"):
        result = subprocess.run(
            ["claude-code", "/owasp-scan", target, 
             "--severity", severity, "--output", "json"],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout)
    
    def dep_cve(self, scope="full"):
        result = subprocess.run(
            ["claude-code", "/dep-cve", 
             "--scope", scope, "--output", "json"],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout)
    
    def create_incident(self, incident_type, severity):
        result = subprocess.run(
            ["claude-code", "/incident-playbook",
             "--type", incident_type,
             "--severity", severity,
             "--output", "json"],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout)

# Usage
skills = SecuritySkills()
scan_results = skills.owasp_scan("./src", severity="critical")
if scan_results["critical_count"] > 0:
    skills.create_incident("vulnerability-detected", "high")
```

### Custom Workflow Orchestration

```yaml
# workflows/custom-audit.yml
name: Custom Security Audit
description: Organization-specific security workflow

steps:
  - name: Pre-audit Setup
    command: /iam-audit
    store_output: iam_results
  
  - name: Code Security
    parallel:
      - command: /owasp-scan
        args: [--target, ./src]
      - command: /dep-cve
        args: [--scope, full]
      - command: /secret-detect
        args: [--scan-history]
  
  - name: Compliance Check
    command: /gdpr-audit
    condition: ${iam_results.high_risk_count} > 0
  
  - name: Generate Report
    command: /pentest-report
    inputs:
      - ${STEP_1_OUTPUT}
      - ${STEP_2_OUTPUT}
      - ${STEP_3_OUTPUT}
  
  - name: Notify Team
    command: /integrations:slack:notify
    args:
      - --channel
      - security-team
      - --attach
      - ${STEP_4_OUTPUT}
```

```bash
# Run custom workflow
claude-code /workflows:run workflows/custom-audit.yml
```

## Resources

- **Source Project**: [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- **Documentation**: Project README and command help (`/help <command>`)
- **Issue Tracker**: GitHub Issues for bug reports and feature requests
- **Community**: Discussions tab for questions and best practices

## License

MIT License - Free to use, modify, and distribute.
