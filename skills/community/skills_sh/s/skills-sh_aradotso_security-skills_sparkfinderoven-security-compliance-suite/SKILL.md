---
name: sparkfinderoven-security-compliance-suite
description: Security audit and compliance automation suite with OWASP scanning, CVE detection, GDPR/SOC2 audits, threat modeling, and incident response playbooks
triggers:
  - scan for OWASP vulnerabilities
  - check dependencies for CVEs
  - audit GDPR compliance
  - generate threat model
  - run security audit
  - check SOC2 readiness
  - detect secrets in code
  - create incident response playbook
---

# 🔒 Security & Compliance Skills Suite

> Skill by [ara.so](https://ara.so) — Security Skills collection.

A comprehensive security and compliance automation toolkit derived from awesome-claude-code. Provides 10 specialized commands for vulnerability scanning, compliance auditing, threat modeling, and incident response with structured output and multi-step workflows.

## What This Project Does

This skill suite enables AI coding agents to perform:

- **Vulnerability Scanning**: OWASP Top-10 checks, CVE dependency analysis
- **Compliance Auditing**: GDPR, SOC2 Type II, ISO27001 gap analysis
- **Threat Modeling**: STRIDE-based architecture security assessment
- **IAM Security**: Least-privilege audits, over-permission detection
- **Incident Response**: Structured playbooks for breach handling
- **Secret Detection**: Pre-commit hooks with entropy scanning

All commands follow a consistent 5-step interaction pattern with visual progress tracking and prioritized action plans.

## Installation

### Quick Install

```bash
# Clone to Claude skills directory
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/sparkfinderoven/r01-hesreallyhim-awesome-claude-code-security.git security-compliance-suite

# Register in Claude Code session
# In Claude Code:
/read ~/.claude/skills/security-compliance-suite/SKILL.md
```

### Manual Setup

```bash
# Copy skill files to your project
cp -r ~/.claude/skills/security-compliance-suite/.claude-skills ./

# Or reference directly in your .claude/config.json
{
  "skills": [
    "~/.claude/skills/security-compliance-suite"
  ]
}
```

## Core Commands

### OWASP Security Scan

Performs OWASP Top-10 vulnerability analysis with CVSS scoring.

```bash
# Scan entire codebase
/owasp-scan .

# Scan specific directory
/owasp-scan ./src/api

# With custom configuration
/owasp-scan . --exclude node_modules --severity high
```

**Output Structure**:
- SQL Injection checks (A03:2021)
- Broken Authentication (A07:2021)
- XSS vulnerabilities (A03:2021)
- CSRF protection gaps
- Security misconfiguration (A05:2021)
- CVSS scores with exploit descriptions

### Dependency CVE Scanning

```bash
# Full dependency tree scan
/dep-cve --scope full

# Production dependencies only
/dep-cve --scope prod --output json

# With upgrade path suggestions
/dep-cve --fix-suggestions
```

**Checks**:
- NPM/PyPI/Maven/NuGet packages
- Direct and transitive dependencies
- Exploitability scores (EPSS)
- Available patches and upgrade paths

### GDPR Compliance Audit

```bash
# Full GDPR audit
/gdpr-audit

# Specific data flow analysis
/gdpr-audit --focus data-flow

# Generate DPA checklist
/gdpr-audit --output dpa-checklist
```

**Analyzes**:
- Personal data collection points
- Consent mechanisms and gaps
- Right to erasure implementation
- Data processor agreements (DPA)
- Cross-border transfer safeguards
- Breach notification procedures

### SOC2 Readiness Assessment

```bash
# Full SOC2 Type II assessment
/soc2-readiness

# Specific Trust Service Criteria
/soc2-readiness --criteria security,availability

# Gap analysis with timeline
/soc2-readiness --timeline 6-months
```

**Evaluates**:
- Security (CC6.x controls)
- Availability (A1.x controls)
- Processing Integrity
- Confidentiality
- Privacy
- Evidence collection readiness

### Threat Modeling

```bash
# STRIDE threat model from architecture
/threat-model ./docs/architecture.md

# With risk matrix output
/threat-model ./design.yaml --risk-matrix

# Focus on specific components
/threat-model --components api,database,auth
```

**Generates**:
- Spoofing threats
- Tampering vectors
- Repudiation risks
- Information disclosure
- Denial of service scenarios
- Elevation of privilege paths

### Penetration Test Report

```bash
# Generate structured pentest report
/pentest-report --target https://api.example.com

# From vulnerability scan results
/pentest-report --import ./scan-results.json

# With executive summary
/pentest-report --format executive
```

### Secret Detection

```bash
# Setup pre-commit hook
/secret-detect --setup

# Scan codebase for secrets
/secret-detect --scan .

# Check specific files
/secret-detect ./config/production.yml
```

**Detects**:
- API keys (AWS, GitHub, Stripe)
- Private keys and certificates
- Database credentials
- OAuth tokens
- High-entropy strings

### IAM Audit

```bash
# Full IAM privilege audit
/iam-audit

# Specific cloud provider
/iam-audit --provider aws

# Focus on over-permissions
/iam-audit --focus over-privileged
```

**Identifies**:
- Over-permissioned roles
- Stale access (unused >90 days)
- MFA gaps
- Service account issues
- Cross-account access risks

### Incident Response Playbook

```bash
# Generate incident playbook
/incident-playbook --type data-breach

# For specific scenario
/incident-playbook --scenario "SQL injection exploit"

# With team assignments
/incident-playbook --assign-roles
```

**Phases**:
1. Triage & Detection
2. Containment
3. Eradication
4. Recovery
5. Lessons Learned

### Privacy Policy Generator

```bash
# Generate GDPR/CCPA policy
/privacy-policy --regions eu,us

# From data inventory
/privacy-policy --inventory ./data-map.json

# With specific clauses
/privacy-policy --include cookies,analytics,marketing
```

## Workflows

### Secure SDLC Workflow

End-to-end security integration in development lifecycle.

```bash
# Full secure SDLC workflow
/workflows:secure-sdlc --target ./src

# Specific phases
/workflows:secure-sdlc --phases threat-model,code-scan,dast
```

**Steps**:
1. Threat model design review
2. Static code analysis (SAST)
3. Dynamic testing (DAST)
4. Penetration testing
5. Security sign-off

### Breach Response Workflow

```bash
# Data breach response workflow
/workflows:breach-response --incident "Customer data exposure"

# With specific scope
/workflows:breach-response --scope "database_users table" --severity high
```

**Process**:
1. Detection & initial assessment
2. Impact analysis & legal review
3. Notification (GDPR 72h requirement)
4. Remediation & containment
5. Post-mortem & improvements

### Compliance Audit Workflow

```bash
# Full compliance audit
/workflows:compliance-audit --standards gdpr,soc2,iso27001

# Gap analysis only
/workflows:compliance-audit --mode gap-analysis --output report.pdf
```

### Zero Trust Design Workflow

```bash
# Zero trust architecture design
/workflows:zero-trust-design --scope "API infrastructure"

# Specific layers
/workflows:zero-trust-design --layers identity,network,workload
```

**Layers**:
1. Identity (authentication, authorization)
2. Network (segmentation, encryption)
3. Workload (container security, least privilege)
4. Data (encryption, DLP)

### Vendor Security Assessment

```bash
# Third-party vendor assessment
/workflows:vendor-security --vendor "Acme SaaS Provider"

# With questionnaire
/workflows:vendor-security --questionnaire vsaq --risk-threshold medium
```

## Configuration

### Command Options

All commands support these common flags:

```bash
--output <format>    # json, md, html, pdf
--severity <level>   # critical, high, medium, low
--exclude <paths>    # Comma-separated exclusion patterns
--verbose           # Detailed logging
--quiet             # Minimal output
```

### Custom Configuration File

Create `.security-suite.yaml` in project root:

```yaml
# .security-suite.yaml
scan:
  exclude_paths:
    - node_modules/
    - vendor/
    - test/fixtures/
  severity_threshold: medium
  
owasp:
  enabled_checks:
    - sql_injection
    - xss
    - csrf
    - auth
  custom_rules: ./security-rules.yaml

cve:
  sources:
    - nvd
    - github-advisory
    - snyk
  ignore_dev_dependencies: true

gdpr:
  data_residency: eu-west-1
  dpo_contact: ${DPO_EMAIL}
  representative_contact: ${EU_REP_EMAIL}

soc2:
  target_readiness: 6-months
  auditor: ${AUDITOR_FIRM}
  
notifications:
  slack_webhook: ${SLACK_WEBHOOK_URL}
  email: ${SECURITY_EMAIL}
  pagerduty_key: ${PAGERDUTY_KEY}
```

### Environment Variables

```bash
# Required for external integrations
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
export SECURITY_EMAIL="security@company.com"
export DPO_EMAIL="dpo@company.com"

# Cloud provider credentials for IAM audit
export AWS_PROFILE="security-audit"
export AZURE_SUBSCRIPTION_ID="..."
export GCP_PROJECT_ID="..."

# Optional: CVE database API keys
export NVD_API_KEY="..."
export SNYK_TOKEN="..."
```

## Code Examples

### Integrating OWASP Scan in CI/CD

```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Security Suite
        run: |
          git clone https://github.com/sparkfinderoven/r01-hesreallyhim-awesome-claude-code-security.git
          echo "SUITE_PATH=$(pwd)/r01-hesreallyhim-awesome-claude-code-security" >> $GITHUB_ENV
      
      - name: Run OWASP Scan
        run: |
          ${SUITE_PATH}/bin/owasp-scan . --output json --severity high > scan-results.json
      
      - name: Check for Critical Issues
        run: |
          CRITICAL=$(jq '[.findings[] | select(.severity=="critical")] | length' scan-results.json)
          if [ "$CRITICAL" -gt 0 ]; then
            echo "Found $CRITICAL critical vulnerabilities"
            exit 1
          fi
      
      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: security-scan
          path: scan-results.json
```

### Pre-commit Hook for Secret Detection

```bash
#!/bin/bash
# .git/hooks/pre-commit

SUITE_PATH="$HOME/.claude/skills/security-compliance-suite"

echo "🔍 Scanning for secrets..."
if ! ${SUITE_PATH}/bin/secret-detect --scan --staged; then
  echo "❌ Secret detected! Commit blocked."
  echo "Run: /secret-detect --help for remediation"
  exit 1
fi

echo "✓ No secrets detected"
exit 0
```

### Automated Compliance Reporting

```python
# compliance_report.py
import subprocess
import json
from datetime import datetime

def run_compliance_audit(standards=["gdpr", "soc2"]):
    """Run compliance audit and generate report"""
    
    results = {}
    for standard in standards:
        cmd = [
            f"~/.claude/skills/security-compliance-suite/bin/compliance-audit",
            f"--standard={standard}",
            "--output=json"
        ]
        
        output = subprocess.check_output(cmd, text=True)
        results[standard] = json.loads(output)
    
    # Generate consolidated report
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "standards": results,
        "overall_score": calculate_compliance_score(results)
    }
    
    with open("compliance-report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    return report

def calculate_compliance_score(results):
    """Calculate overall compliance percentage"""
    total_controls = 0
    passed_controls = 0
    
    for standard, data in results.items():
        total_controls += data["total_controls"]
        passed_controls += data["passed_controls"]
    
    return (passed_controls / total_controls * 100) if total_controls > 0 else 0

if __name__ == "__main__":
    report = run_compliance_audit()
    print(f"Overall Compliance: {report['overall_score']:.1f}%")
```

### Threat Modeling from Architecture

```javascript
// threat-model-integration.js
const { execSync } = require('child_process');
const fs = require('fs');

async function generateThreatModel(architectureFile) {
  const command = `~/.claude/skills/security-compliance-suite/bin/threat-model ${architectureFile} --output json`;
  
  try {
    const output = execSync(command, { encoding: 'utf-8' });
    const threatModel = JSON.parse(output);
    
    // Filter high-risk threats
    const highRisk = threatModel.threats.filter(t => 
      t.risk_score >= 7.0
    );
    
    // Generate Jira tickets for high-risk threats
    for (const threat of highRisk) {
      await createSecurityTicket({
        title: `[SECURITY] ${threat.category}: ${threat.title}`,
        description: threat.description,
        severity: threat.severity,
        mitigation: threat.recommended_mitigations
      });
    }
    
    return threatModel;
  } catch (error) {
    console.error('Threat modeling failed:', error.message);
    throw error;
  }
}

async function createSecurityTicket(threat) {
  // Integration with issue tracker
  console.log(`Creating ticket for: ${threat.title}`);
  // Implementation depends on your issue tracker
}

module.exports = { generateThreatModel };
```

## Common Patterns

### Daily Security Dashboard

```bash
#!/bin/bash
# daily-security-check.sh

echo "🔒 Daily Security Dashboard - $(date)"
echo "========================================"

# 1. Quick vulnerability scan
echo "\n📊 Vulnerability Scan"
/owasp-scan . --quick --severity high | grep -E "(🔴|🟠)"

# 2. Check for new CVEs
echo "\n🚨 New CVEs in Dependencies"
/dep-cve --new-only --output table

# 3. IAM changes
echo "\n👤 IAM Changes (last 24h)"
/iam-audit --since 24h --changes-only

# 4. Secret detection on recent commits
echo "\n🔑 Secret Scan (recent commits)"
git diff HEAD~5..HEAD | /secret-detect --stdin

echo "\n✓ Daily check complete"
```

### Compliance Evidence Collection

```bash
# collect-compliance-evidence.sh
#!/bin/bash

EVIDENCE_DIR="./compliance-evidence/$(date +%Y-%m-%d)"
mkdir -p "$EVIDENCE_DIR"

# Collect SOC2 evidence
/soc2-readiness --output json > "$EVIDENCE_DIR/soc2-assessment.json"

# GDPR data flows
/gdpr-audit --focus data-flow --output pdf > "$EVIDENCE_DIR/gdpr-data-flows.pdf"

# Access logs audit
/iam-audit --export-logs > "$EVIDENCE_DIR/iam-audit-logs.json"

# System configurations
/security-config-export > "$EVIDENCE_DIR/security-configs.yaml"

echo "Evidence collected in: $EVIDENCE_DIR"
```

### Incident Response Automation

```python
# incident_response.py
import os
import subprocess
from datetime import datetime

def initiate_incident_response(incident_type, severity, description):
    """Automated incident response workflow"""
    
    timestamp = datetime.utcnow().isoformat()
    incident_id = f"INC-{timestamp.replace(':', '').replace('-', '')}"
    
    # 1. Generate playbook
    subprocess.run([
        "~/.claude/skills/security-compliance-suite/bin/incident-playbook",
        f"--type={incident_type}",
        f"--id={incident_id}",
        f"--severity={severity}"
    ])
    
    # 2. Notify team
    notify_security_team(incident_id, severity, description)
    
    # 3. Trigger containment if critical
    if severity == "critical":
        trigger_containment_measures(incident_id)
    
    # 4. Start evidence collection
    collect_forensic_evidence(incident_id)
    
    return incident_id

def notify_security_team(incident_id, severity, description):
    """Send notifications via configured channels"""
    webhook = os.getenv("SLACK_WEBHOOK_URL")
    if webhook:
        # Send Slack notification
        pass

def trigger_containment_measures(incident_id):
    """Automated containment for critical incidents"""
    # Rotate credentials, block IPs, etc.
    pass

def collect_forensic_evidence(incident_id):
    """Collect logs and system state"""
    subprocess.run([
        "~/.claude/skills/security-compliance-suite/bin/forensic-collect",
        f"--incident={incident_id}"
    ])
```

## Troubleshooting

### Command Not Found

```bash
# Ensure binary is executable
chmod +x ~/.claude/skills/security-compliance-suite/bin/*

# Add to PATH
export PATH="$PATH:$HOME/.claude/skills/security-compliance-suite/bin"
```

### Permission Denied on IAM Audit

```bash
# Verify cloud provider credentials
aws sts get-caller-identity  # For AWS
az account show             # For Azure
gcloud auth list            # For GCP

# Grant required permissions (AWS example)
# Attach SecurityAudit managed policy to your role
```

### CVE Scan Timeouts

```bash
# Reduce scope to production dependencies only
/dep-cve --scope prod

# Or scan in batches
/dep-cve --scope prod --batch-size 50

# Cache CVE database locally
export CVE_CACHE_DIR="$HOME/.cache/cve-db"
/dep-cve --use-cache
```

### GDPR Audit Missing Data Sources

```yaml
# .security-suite.yaml
gdpr:
  data_sources:
    - type: database
      connection: ${DATABASE_URL}
    - type: api
      endpoint: https://api.example.com
      auth: ${API_KEY}
    - type: file
      path: ./user-data/
```

### False Positives in Secret Detection

```yaml
# .secret-detect.yaml
ignore_patterns:
  - "test/fixtures/*"
  - "docs/examples/*"

false_positive_hashes:
  - "abc123..."  # Example API key hash

custom_entropy_threshold: 4.5  # Increase to reduce false positives
```

### Report Generation Fails

```bash
# Install report dependencies
pip install jinja2 weasyprint  # For PDF reports
npm install -g marked          # For Markdown processing

# Or use JSON output and convert separately
/owasp-scan . --output json | jq '.' > report.json
```

### Workflow Timeout

```bash
# Increase timeout for long-running workflows
/workflows:secure-sdlc --timeout 3600  # 1 hour

# Or run phases separately
/workflows:secure-sdlc --phase threat-model
/workflows:secure-sdlc --phase code-scan --resume
```

## Integration Examples

### Slack Notifications

```bash
# Send scan results to Slack
/owasp-scan . --output json | \
  jq '.summary' | \
  curl -X POST ${SLACK_WEBHOOK_URL} \
    -H 'Content-Type: application/json' \
    -d @-
```

### Jira Ticket Creation

```bash
# Create Jira tickets for high-severity findings
/owasp-scan . --output json | \
  jq -r '.findings[] | select(.severity=="high") | 
    "curl -X POST ${JIRA_API_URL}/issue -H \"Authorization: Bearer ${JIRA_TOKEN}\" -d '"'"'{\"fields\":{\"project\":{\"key\":\"SEC\"},\"summary\":\"\(.title)\",\"description\":\"\(.description)\",\"issuetype\":{\"name\":\"Security\"}}}'"'"'"' | \
  bash
```

### Continuous Monitoring

```bash
# Cron job for daily scans
# /etc/cron.d/security-scan
0 2 * * * /home/user/.claude/skills/security-compliance-suite/bin/daily-security-check.sh >> /var/log/security-scan.log 2>&1
```

## Best Practices

1. **Run scans in CI/CD**: Fail builds on critical/high severity issues
2. **Schedule regular audits**: Weekly OWASP, monthly compliance checks
3. **Automate evidence collection**: For SOC2/ISO27001 audits
4. **Version control playbooks**: Track incident response improvements
5. **Use environment variables**: Never commit credentials
6. **Test workflows in staging**: Before production deployment
7. **Review false positives**: Tune detection rules regularly
8. **Document exceptions**: Maintain risk acceptance log

---

## Related Skills

- [OWASP Dependency Check](https://ara.so/skills/owasp-dependency-check)
- [Trivy Security Scanner](https://ara.so/skills/trivy-scanner)
- [HashiCorp Vault](https://ara.so/skills/hashicorp-vault)
- [AWS Security Hub](https://ara.so/skills/aws-security-hub)

---

**License**: MIT  
**Source**: https://github.com/sparkfinderoven/r01-hesreallyhim-awesome-claude-code-security
