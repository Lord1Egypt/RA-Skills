---
name: sparkfinderoven-security-compliance-skills
description: Security & compliance skill suite with OWASP scanning, CVE detection, GDPR audits, SOC2 readiness, threat modeling, and incident response workflows
triggers:
  - scan my code for OWASP vulnerabilities
  - check for CVEs in my dependencies
  - audit GDPR compliance in this application
  - run a SOC2 readiness assessment
  - create a threat model for this architecture
  - generate a security incident playbook
  - detect secrets in my codebase
  - audit IAM permissions and roles
---

# 🔒 Security & Compliance Skills Suite

> Skill by [ara.so](https://ara.so) — Security Skills collection.

This skill suite provides specialized commands and workflows for security audits, vulnerability management, compliance (GDPR/SOC2/ISO27001), and incident response. Derived from hesreallyhim/awesome-claude-code, it offers 10 security-focused commands and 5 multi-step workflows with structured output.

## Installation

### Local Installation

```bash
# Clone the repository
git clone https://github.com/sparkfinderoven/r01-hesreallyhim-awesome-claude-code-security.git

# Copy to Claude skills directory
mkdir -p ~/.claude/skills
cp -r r01-hesreallyhim-awesome-claude-code-security ~/.claude/skills/security-compliance

# Or create symlink for auto-updates
ln -s $(pwd)/r01-hesreallyhim-awesome-claude-code-security ~/.claude/skills/security-compliance
```

### Register with Claude Code

In a Claude Code session:

```bash
/read ~/.claude/skills/security-compliance/SKILL.md
```

## Core Commands

### `/owasp-scan` - OWASP Top 10 Security Scan

Scans code for OWASP Top 10 vulnerabilities with exploit descriptions, CVSS scores, and remediation steps.

**Usage:**

```bash
/owasp-scan <target_directory>
/owasp-scan src/ --output json
/owasp-scan . --exclude node_modules,dist
```

**Output Structure:**

```
╔══════════════════════════════════════════════════╗
║  OWASP Top 10 Scan  —  src/                     ║
╠══════════════════════════════════════════════════╣
║  A01 Broken Access Control     ✓   3 checks     ║
║  A02 Cryptographic Failures    ✓   2 checks     ║
║  A03 Injection                 ✓   5 checks     ║
║  A04 Insecure Design          ✓   1 check       ║
║  A05 Security Misconfiguration ✓   4 checks     ║
╚══════════════════════════════════════════════════╝

FINDINGS (17 files scanned)
┌──────┬────────────────────────────────┬──────────┬─────────────┐
│ Sev  │ Vulnerability                  │ CVSS     │ File:Line   │
├──────┼────────────────────────────────┼──────────┼─────────────┤
│  🔴  │ SQL Injection                  │  9.8     │ api.js:45   │
│  🔴  │ Hardcoded JWT Secret           │  9.1     │ auth.js:12  │
│  🟠  │ Insecure Deserialization       │  8.1     │ parser.js:8 │
│  🟡  │ Missing CSRF Protection        │  6.5     │ routes.js:3 │
└──────┴────────────────────────────────┴──────────┴─────────────┘
```

**Example Remediation:**

```javascript
// ❌ VULNERABLE: SQL Injection
const query = `SELECT * FROM users WHERE id = ${req.params.id}`;

// ✅ FIXED: Parameterized Query
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [req.params.id]);

// ❌ VULNERABLE: Hardcoded Secret
const secret = 'my-secret-key-123';

// ✅ FIXED: Environment Variable
const secret = process.env.JWT_SECRET;
```

### `/dep-cve` - Dependency CVE Scanner

Analyzes project dependencies for known CVEs with exploitability scores and upgrade paths.

**Usage:**

```bash
/dep-cve
/dep-cve --scope full --output md
/dep-cve --severity high,critical
```

**Example Output:**

```
CVE SCAN RESULTS (234 dependencies checked)

Critical Vulnerabilities: 2
High: 5
Medium: 12
Low: 8

┌────────────┬─────────────────┬──────────┬────────────┬──────────────┐
│ Package    │ CVE ID          │ CVSS     │ Current    │ Fix Version  │
├────────────┼─────────────────┼──────────┼────────────┼──────────────┤
│ lodash     │ CVE-2021-23337  │  9.8     │ 4.17.15    │ 4.17.21      │
│ express    │ CVE-2022-24999  │  7.5     │ 4.17.1     │ 4.18.0       │
└────────────┴─────────────────┴──────────┴────────────┴──────────────┘

UPGRADE PATH:
npm update lodash@4.17.21 express@4.18.0
```

**Checking in CI/CD:**

```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]

jobs:
  cve-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: CVE Scan
        run: |
          /dep-cve --severity critical,high --output json > cve-report.json
          if [ $(jq '.critical + .high' cve-report.json) -gt 0 ]; then
            exit 1
          fi
```

### `/gdpr-audit` - GDPR Compliance Audit

Maps data flows, identifies consent gaps, and generates DPA (Data Processing Agreement) checklists.

**Usage:**

```bash
/gdpr-audit
/gdpr-audit --scope full --output pdf
/gdpr-audit --focus consent,data-flow
```

**Example Analysis:**

```
╔══════════════════════════════════════════════════╗
║  GDPR Compliance Audit                           ║
╠══════════════════════════════════════════════════╣
║  Data Inventory         ✓   Complete             ║
║  Consent Mechanisms     ⚠   3 gaps found         ║
║  Data Flow Mapping      ✓   Complete             ║
║  DPA Requirements       ✗   5 missing            ║
╚══════════════════════════════════════════════════╝

DATA FLOWS IDENTIFIED:
User Registration → Database (EU) → Analytics (US) → Email Provider (US)

CONSENT GAPS:
🔴 Analytics tracking: No explicit consent banner
🔴 Email marketing: Opt-out only (requires opt-in)
🟡 Cookie policy: Missing granular control

ACTION ITEMS:
□ Implement consent management platform (est: 2 weeks)
□ Add cookie consent banner with granular controls (est: 3 days)
□ Update privacy policy with Article 13/14 requirements (est: 1 week)
□ Establish Data Processing Agreements with US vendors (est: 2 weeks)
```

**Implementation Example:**

```javascript
// GDPR-compliant consent implementation
class ConsentManager {
  constructor() {
    this.consent = this.loadConsent();
  }
  
  requestConsent(purposes = ['necessary', 'analytics', 'marketing']) {
    return {
      necessary: true, // Always granted
      analytics: this.consent.analytics || false,
      marketing: this.consent.marketing || false,
      timestamp: new Date().toISOString()
    };
  }
  
  grantConsent(purpose) {
    this.consent[purpose] = true;
    this.consent.timestamp = new Date().toISOString();
    this.saveConsent();
  }
  
  revokeConsent(purpose) {
    this.consent[purpose] = false;
    this.saveConsent();
    this.deleteData(purpose); // Article 17: Right to erasure
  }
  
  saveConsent() {
    // Store in cookie with 13-month expiry (ePrivacy Directive)
    document.cookie = `gdpr_consent=${JSON.stringify(this.consent)}; max-age=${60*60*24*395}; secure; samesite=strict`;
  }
}
```

### `/soc2-readiness` - SOC 2 Type II Readiness Assessment

Gap analysis across all 5 Trust Service Criteria (TSC): Security, Availability, Processing Integrity, Confidentiality, Privacy.

**Usage:**

```bash
/soc2-readiness
/soc2-readiness --tsc security,availability
/soc2-readiness --generate-evidence-list
```

**Example Report:**

```
SOC 2 TYPE II READINESS ASSESSMENT

Overall Readiness: 68% (Medium Risk)

┌────────────────────────────┬──────────┬──────────┬─────────────┐
│ Trust Service Criteria     │ Score    │ Gaps     │ Risk Level  │
├────────────────────────────┼──────────┼──────────┼─────────────┤
│ CC1: Control Environment   │  75%     │  3       │  🟡 Medium  │
│ CC2: Communication         │  80%     │  2       │  🟢 Low     │
│ CC3: Risk Assessment       │  60%     │  5       │  🟠 High    │
│ CC4: Monitoring            │  70%     │  4       │  🟡 Medium  │
│ CC5: Control Activities    │  65%     │  6       │  🟠 High    │
│ CC6: Logical Access        │  55%     │  8       │  🔴 Critical│
│ CC7: System Operations     │  72%     │  3       │  🟡 Medium  │
└────────────────────────────┴──────────┴──────────┴─────────────┘

CRITICAL GAPS (CC6: Logical Access):
🔴 No MFA enforcement for administrative accounts
🔴 Password policy does not meet complexity requirements
🔴 No formal access review process (90-day requirement)
🔴 Service accounts share credentials

REMEDIATION ROADMAP (12 weeks):
Week 1-2:   Implement MFA (Okta/Auth0)
Week 3-4:   Deploy password manager + rotate service accounts
Week 5-6:   Establish quarterly access review process
Week 7-8:   Implement SIEM for security monitoring
Week 9-10:  Conduct tabletop exercise for incident response
Week 11-12: Evidence collection + documentation
```

### `/threat-model` - STRIDE Threat Modeling

Generates STRIDE threat models for architecture diagrams with risk matrices.

**Usage:**

```bash
/threat-model <architecture_file>
/threat-model design.drawio --output md
/threat-model --interactive
```

**Example Analysis:**

```
STRIDE THREAT MODEL: E-Commerce API

ARCHITECTURE COMPONENTS:
- Web App (React) → API Gateway → Microservices → Database
- Auth Service (JWT) → Redis Cache
- Payment Service → Stripe API

┌──────────────┬─────────────────────────────────────┬──────────┬────────┐
│ Threat Type  │ Threat                              │ Impact   │ Risk   │
├──────────────┼─────────────────────────────────────┼──────────┼────────┤
│ Spoofing     │ JWT token forgery                   │  High    │  8.5   │
│ Tampering    │ API request parameter manipulation  │  High    │  7.2   │
│ Repudiation  │ Missing audit logs for payment ops  │  Medium  │  6.0   │
│ Info Disc.   │ PII exposed in API error messages   │  High    │  7.8   │
│ DoS          │ No rate limiting on /api/search     │  Medium  │  5.5   │
│ Elevation    │ Admin endpoints accessible w/o authz│  Critical│  9.2   │
└──────────────┴─────────────────────────────────────┴──────────┴────────┘

MITIGATIONS:
✓ Use asymmetric JWT with RS256 (not HS256)
✓ Implement request signature validation
✓ Add structured logging with correlation IDs
✓ Sanitize error messages (remove stack traces)
✓ Deploy rate limiting (Redis-backed)
✓ Implement RBAC with least-privilege principle
```

**Code Example:**

```javascript
// Implementing RBAC for elevation of privilege mitigation
const permissions = {
  user: ['read:profile', 'write:profile'],
  admin: ['read:*', 'write:*', 'delete:*'],
  auditor: ['read:*']
};

function authorize(role, action, resource) {
  const userPerms = permissions[role] || [];
  
  // Check exact match
  if (userPerms.includes(`${action}:${resource}`)) return true;
  
  // Check wildcard
  if (userPerms.includes(`${action}:*`)) return true;
  
  return false;
}

// Middleware usage
app.delete('/api/users/:id', (req, res, next) => {
  if (!authorize(req.user.role, 'delete', 'users')) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  next();
});
```

### `/secret-detect` - Pre-commit Secret Detection

Configures pre-commit hooks for secret detection with entropy scanning.

**Usage:**

```bash
/secret-detect --init
/secret-detect --scan .
/secret-detect --generate-config
```

**Generated Configuration:**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: package-lock.json

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.16.1
    hooks:
      - id: gitleaks
```

**Custom Rules:**

```python
# .detect-secrets/custom-rules.py
import re

class CustomSecretDetector:
    """Detect organization-specific secrets"""
    
    secret_type = 'Custom API Key'
    
    def analyze_string(self, string):
        # Matches: ACME_KEY_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        pattern = r'ACME_KEY_[A-Za-z0-9]{32}'
        return bool(re.search(pattern, string))
```

**Git Hook Installation:**

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run secret detection
detect-secrets-hook --baseline .secrets.baseline $(git diff --cached --name-only)

if [ $? -ne 0 ]; then
  echo "❌ Secret detected! Commit blocked."
  echo "To allow, update baseline: detect-secrets scan > .secrets.baseline"
  exit 1
fi

# Run gitleaks
gitleaks protect --staged --verbose

exit $?
```

### `/iam-audit` - IAM Least-Privilege Audit

Audits IAM roles for over-permissioned access, stale accounts, and MFA gaps.

**Usage:**

```bash
/iam-audit
/iam-audit --provider aws
/iam-audit --focus mfa,stale-access
```

**Example Report:**

```
IAM AUDIT RESULTS

Users Scanned: 47
Roles Scanned: 23
Policies Scanned: 156

┌─────────────────────────────┬────────┬──────────────────────────┐
│ Finding                     │ Count  │ Risk                     │
├─────────────────────────────┼────────┼──────────────────────────┤
│ Users without MFA           │  12    │  🔴 Critical             │
│ Over-permissioned roles     │  8     │  🟠 High                 │
│ Unused access keys (>90d)   │  15    │  🟡 Medium               │
│ Policies with wildcard (*)  │  5     │  🟠 High                 │
│ Inactive users (>180d)      │  7     │  🟡 Medium               │
└─────────────────────────────┴────────┴──────────────────────────┘

OVER-PERMISSIONED ROLES:
Role: developers-full-access
  Granted: s3:*, ec2:*, rds:*
  Required: s3:GetObject, s3:PutObject, ec2:DescribeInstances
  Recommendation: Scope down to least-privilege

REMEDIATION SCRIPT:
```

```bash
#!/bin/bash
# iam-remediation.sh

# Enforce MFA for all users
aws iam list-users --query 'Users[*].UserName' --output text | while read user; do
  mfa=$(aws iam list-mfa-devices --user-name $user --query 'MFADevices' --output text)
  if [ -z "$mfa" ]; then
    echo "❌ $user: No MFA configured"
    # Attach policy requiring MFA
    aws iam attach-user-policy --user-name $user --policy-arn arn:aws:iam::aws:policy/RequireMFA
  fi
done

# Delete unused access keys
aws iam list-users --query 'Users[*].UserName' --output text | while read user; do
  aws iam list-access-keys --user-name $user --query 'AccessKeyMetadata[*].[AccessKeyId,CreateDate]' --output text | while read key_id create_date; do
    age=$(($(date +%s) - $(date -d $create_date +%s)))
    if [ $age -gt $((90 * 86400)) ]; then
      echo "🗑️  Deleting stale key: $key_id for $user"
      aws iam delete-access-key --user-name $user --access-key-id $key_id
    fi
  done
done
```

### `/incident-playbook` - Security Incident Response

Generates structured incident response playbooks: triage → contain → eradicate → recover → lessons learned.

**Usage:**

```bash
/incident-playbook --type data-breach
/incident-playbook --type ransomware
/incident-playbook --custom
```

**Generated Playbook:**

```markdown
# INCIDENT RESPONSE PLAYBOOK: Data Breach

## Phase 1: DETECTION & TRIAGE (0-1 hour)

### Initial Response Checklist
□ Activate incident response team
□ Document incident start time: ___________
□ Assign incident commander: ___________
□ Create war room channel: #incident-YYYY-MM-DD
□ Preserve evidence (disk images, logs, network captures)

### Classification
- [ ] Confirmed incident
- [ ] False positive
- [ ] Severity: P1 (Critical) / P2 (High) / P3 (Medium) / P4 (Low)

### Scope Assessment
- Affected systems: ___________
- Data exposed: ___________
- Attack vector: ___________
- Number of records: ___________

## Phase 2: CONTAINMENT (1-4 hours)

### Short-term Containment
□ Isolate affected systems (network segmentation)
□ Disable compromised accounts
□ Block malicious IPs at firewall
□ Enable enhanced logging

### Long-term Containment
□ Patch vulnerable systems
□ Rotate all credentials
□ Deploy intrusion detection rules
□ Apply compensating controls

## Phase 3: ERADICATION (4-24 hours)

□ Remove malware/backdoors
□ Close attack vectors
□ Rebuild compromised systems from clean backups
□ Verify integrity of restored systems

## Phase 4: RECOVERY (24-72 hours)

□ Restore systems to production
□ Monitor for reinfection (72-hour watch)
□ Validate business operations
□ Communicate restoration to stakeholders

## Phase 5: POST-INCIDENT REVIEW (Within 7 days)

### Lessons Learned Template
1. What happened? (timeline)
2. What was the root cause?
3. What worked well in our response?
4. What should we improve?
5. Action items with owners and due dates

### Notification Requirements
□ GDPR: Notify DPA within 72 hours (Art. 33)
□ Affected individuals: Notify without undue delay (Art. 34)
□ Law enforcement: ___________
□ Cyber insurance: ___________

## Communication Templates

### Internal Notification
Subject: [P1] Security Incident - Data Breach

Team,

We are responding to a confirmed security incident involving [brief description].

Status: CONTAINED
Impact: [X] systems, [Y] records potentially exposed
Next Update: [time]

Do NOT:
- Discuss externally
- Delete logs or evidence

Incident Commander: [name] - [contact]

### External Notification (GDPR Art. 34)
Subject: Important Security Notice

Dear [Customer],

We are writing to inform you of a security incident that may have affected your personal data.

What happened: [brief description]
When: [date range]
Data affected: [specific categories]
What we're doing: [response actions]
What you should do: [recommendations]

For questions: security@company.com | 1-800-XXX-XXXX
```

### `/privacy-policy` - Privacy Policy Generator

Generates GDPR/CCPA-compliant privacy policies from data inventory.

**Usage:**

```bash
/privacy-policy --region eu,us
/privacy-policy --format html,pdf
/privacy-policy --from-inventory data-inventory.json
```

**Data Inventory Format:**

```json
{
  "data_categories": [
    {
      "category": "account_info",
      "fields": ["email", "name", "phone"],
      "purpose": "Account management",
      "legal_basis": "Contract (GDPR Art. 6.1.b)",
      "retention": "Account lifetime + 2 years",
      "shared_with": ["Email provider (AWS SES)", "CRM (Salesforce)"]
    },
    {
      "category": "analytics",
      "fields": ["ip_address", "user_agent", "page_views"],
      "purpose": "Service improvement",
      "legal_basis": "Legitimate interest (GDPR Art. 6.1.f)",
      "retention": "13 months",
      "shared_with": ["Google Analytics (US - Privacy Shield)"]
    }
  ]
}
```

**Generated Policy Excerpt:**

```html
<h2>1. Information We Collect</h2>

<h3>Account Information</h3>
<p>We collect your email, name, and phone number when you create an account.</p>
<ul>
  <li><strong>Purpose:</strong> Account management</li>
  <li><strong>Legal Basis (GDPR):</strong> Performance of contract (Art. 6.1.b)</li>
  <li><strong>Retention:</strong> Account lifetime + 2 years</li>
</ul>

<h3>Analytics Data</h3>
<p>We automatically collect IP address, user agent, and page views.</p>
<ul>
  <li><strong>Purpose:</strong> Service improvement</li>
  <li><strong>Legal Basis (GDPR):</strong> Legitimate interest (Art. 6.1.f)</li>
  <li><strong>Retention:</strong> 13 months</li>
</ul>

<h2>2. How We Share Your Data</h2>
<p>We share your information with:</p>
<ul>
  <li>Email provider (AWS SES, US) - for transactional emails</li>
  <li>CRM (Salesforce, US) - for customer support</li>
  <li>Google Analytics (US, Privacy Shield certified) - for usage analytics</li>
</ul>

<h2>3. Your Rights (GDPR)</h2>
<ul>
  <li>Right of access (Art. 15)</li>
  <li>Right to rectification (Art. 16)</li>
  <li>Right to erasure ("right to be forgotten") (Art. 17)</li>
  <li>Right to data portability (Art. 20)</li>
  <li>Right to object (Art. 21)</li>
</ul>

<p>To exercise your rights, contact: dpo@company.com</p>

<h2>4. International Transfers</h2>
<p>Your data may be transferred to the United States. We ensure adequate protection through:</p>
<ul>
  <li>Standard Contractual Clauses (SCCs) approved by the European Commission</li>
  <li>Privacy Shield certification (where applicable)</li>
</ul>
```

## Multi-Step Workflows

### `secure-sdlc` - Secure Software Development Lifecycle

End-to-end security workflow: threat model → SAST → DAST → pen test → sign-off.

**Usage:**

```bash
/workflows:secure-sdlc <project_directory>
/workflows:secure-sdlc . --skip-pentest
```

**Workflow Steps:**

```
╔══════════════════════════════════════════════════╗
║  Secure SDLC Pipeline                            ║
╠══════════════════════════════════════════════════╣
║  1. Threat Model           ✓   Complete          ║
║  2. SAST (Code Scan)       ✓   14 findings       ║
║  3. SCA (Dependencies)     ✓   3 CVEs            ║
║  4. DAST (Running App)     ⟳   In progress…      ║
║  5. Penetration Test       ░   Pending           ║
║  6. Security Sign-off      ░   Pending           ║
╚══════════════════════════════════════════════════╝

Step 4: DAST Running...
  Testing: Authentication endpoints
  Testing: API authorization
  Testing: Input validation
```

**CI/CD Integration:**

```yaml
# .github/workflows/secure-sdlc.yml
name: Secure SDLC
on: [pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Threat Model (cached)
        run: |
          if [ ! -f .threat-model.json ]; then
            /threat-model --output json > .threat-model.json
          fi
      
      - name: SAST
        run: /owasp-scan . --output sarif > sast-results.sarif
      
      - name: SCA
        run: /dep-cve --output json > sca-results.json
      
      - name: Upload Results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: sast-results.sarif
      
      - name: Block on Critical
        run: |
          critical=$(jq '.runs[0].results | map(select(.level=="error")) | length' sast-results.sarif)
          if [ $critical -gt 0 ]; then
            echo "❌ $critical critical vulnerabilities found"
            exit 1
          fi
```

### `breach-response` - Data Breach Response

Full breach response workflow: detect → assess → notify → remediate → post-mortem.

**Usage:**

```bash
/workflows:breach-response --type suspected
/workflows:breach-response --confirmed --severity high
```

### `compliance-audit` - Full Compliance Audit

End-to-end compliance audit: scope → gap analysis → evidence collection → remediation plan.

**Usage:**

```bash
/workflows:compliance-audit --framework soc2
/workflows:compliance-audit --framework gdpr,iso27001
```

### `zero-trust-design` - Zero Trust Architecture

Design zero-trust architecture across identity, network, workload, and data layers.

**Usage:**

```bash
/workflows:zero-trust-design --current-arch architecture.yml
/workflows:zero-trust-design --interactive
```

### `vendor-security` - Third-Party Vendor Assessment

Security assessment for third-party vendors: questionnaire → risk scoring → decision.

**Usage:**

```bash
/workflows:vendor-security <vendor_name>
/workflows:vendor-security --generate-questionnaire
```

## Configuration

### Global Configuration

Create `~/.claude/skills/security-compliance/config.yml`:

```yaml
# Global settings
severity_threshold: high  # Block on: critical, high, medium, low
output_format: markdown   # json, markdown, html, pdf

# OWASP Scan
owasp:
  exclude_dirs:
    - node_modules
    - dist
    - vendor
  custom_rules: .owasp-rules.yml

# CVE Scan
cve:
  sources:
    - nvd
    - github-advisories
    - snyk
  auto_update: true

# IAM Audit
iam:
  providers:
    - aws
    - gcp
    - azure
  mfa_required: true
  max_key_age_days: 90

# Notifications
notifications:
  slack_webhook: ${SLACK_WEBHOOK_URL}
  email: security@company.com
  pagerduty_key: ${PAGERDUTY_KEY}
```

### Environment Variables

```bash
# Required for cloud provider access
export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
export GCP_SERVICE_ACCOUNT_KEY=${GCP_SERVICE_ACCOUNT_KEY}

# Optional: Notifications
export SLACK_WEBHOOK_URL=${SLACK_WEBHOOK_URL}
export PAGERDUTY_KEY=${PAGERDUTY_KEY}

# Optional: CVE Database API Keys
export NVD_API_KEY=${NVD_API_KEY}
export SNYK_TOKEN=${SNYK_TOKEN}
```

## Common Patterns

### Daily Security Scan

```bash
#!/bin/bash
# daily-security-scan.sh

echo "🔒 Running daily security scan..."

# Quick OWASP scan
/owasp-scan src/ --severity critical,high --output json > daily-owasp.json

# CVE check
/dep-cve --severity critical,high --output json > daily-cve.json

# Check for secrets
/secret-detect --scan .

# Summary
critical_owasp=$(jq '[.findings[] | select(.severity=="critical")] | length' daily-owasp.json)
critical_cve=$(jq '.critical' daily-cve.json)

if [ $critical_owasp -gt 0 ] || [ $critical_cve -gt 0 ]; then
  echo "❌ Critical vulnerabilities found!"
  echo "OWASP: $critical_owasp | CVE: $critical_cve"
  # Send notification
  curl
