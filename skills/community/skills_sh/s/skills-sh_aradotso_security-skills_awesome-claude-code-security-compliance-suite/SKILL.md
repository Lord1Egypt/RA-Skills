---
name: awesome-claude-code-security-compliance-suite
description: Security & compliance skill suite providing OWASP scanning, CVE detection, GDPR/SOC2 audits, threat modeling, and incident response workflows for AI coding agents
triggers:
  - scan this code for OWASP vulnerabilities
  - check dependencies for CVEs and security issues
  - audit this application for GDPR compliance
  - generate a threat model for this architecture
  - create a SOC2 readiness assessment
  - detect secrets and credentials in the codebase
  - perform an IAM least privilege audit
  - generate a security incident response playbook
---

# 🔒 Security & Compliance Skills Suite

> Skill by [ara.so](https://ara.so) — Security Skills collection.

A comprehensive security and compliance skill suite derived from hesreallyhim/awesome-claude-code, providing specialized commands and workflows for security audits, vulnerability management, GDPR/SOC2/ISO27001 compliance, and incident response.

## What This Project Does

This skill suite provides **10 specialized security commands** and **5 multi-step compliance workflows** with structured output UI for:

- **Vulnerability Scanning**: OWASP Top-10 analysis, dependency CVE detection
- **Compliance Auditing**: GDPR, SOC2, ISO27001 gap analysis
- **Security Operations**: Threat modeling, penetration testing, IAM audits
- **Incident Response**: Breach response playbooks and investigation workflows
- **Policy Generation**: Privacy policies, security documentation

All commands use consistent structured output with progress tracking, findings tables, and prioritized action plans.

## Installation

### Quick Install (Local Skills Directory)

```bash
# Create Claude skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Clone the skill suite
git clone https://github.com/sparkfinderoven/r01-hesreallyhim-awesome-claude-code-security.git \
  ~/.claude/skills/awesome-claude-code-security

# Activate in Claude Code session
# In your IDE with Claude Code, run:
/read ~/.claude/skills/awesome-claude-code-security/SKILL.md
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/sparkfinderoven/r01-hesreallyhim-awesome-claude-code-security.git

# Navigate to project directory
cd r01-hesreallyhim-awesome-claude-code-security

# Read the skill documentation
cat SKILL.md
```

### Verification

Verify installation by checking available commands:

```bash
# List all security commands
ls -la ~/.claude/skills/awesome-claude-code-security/

# Expected output:
# - SKILL.md (this file)
# - README.md (documentation)
# - commands/ (individual command definitions)
# - workflows/ (multi-step workflow definitions)
```

## Core Commands

### 1. OWASP Top-10 Security Scan

Scans code for OWASP Top-10 vulnerabilities with CVSS scores and remediation guidance.

```bash
/owasp-scan <target_directory>

# Options
/owasp-scan src/ --format json
/owasp-scan . --severity critical,high
/owasp-scan api/ --output report.md
```

**Example Output Structure:**

```
╔══════════════════════════════════════════════════╗
║  OWASP Security Scan — ./src/api                 ║
╠══════════════════════════════════════════════════╣
║  Files scanned       ✓   47                      ║
║  OWASP checks        ✓   14                      ║
║  Findings            ✗   8 issues                ║
╚══════════════════════════════════════════════════╝

FINDINGS (severity: desc)
┌──────┬──────────────────────────────┬──────────┬──────────────┐
│ Sev  │ Vulnerability                │ CVSS     │ File         │
├──────┼──────────────────────────────┼──────────┼──────────────┤
│  🔴  │ SQL Injection                │  9.8     │ users.js:42  │
│  🔴  │ JWT None Algorithm           │  9.1     │ auth.js:18   │
│  🟠  │ CORS Misconfiguration        │  6.5     │ server.js:12 │
└──────┴──────────────────────────────┴──────────┴──────────────┘

REMEDIATION
• SQL Injection: Use parameterized queries or ORM
• JWT None: Validate algorithm in token verification
• CORS: Restrict origins to known domains
```

### 2. Dependency CVE Scanner

Scans project dependencies for known CVEs with exploitability scores.

```bash
/dep-cve

# Options
/dep-cve --scope production
/dep-cve --output json > cve-report.json
/dep-cve --min-cvss 7.0
/dep-cve --show-paths
```

**Example for Node.js project:**

```bash
# Scans package.json and package-lock.json
/dep-cve --scope full

# Output includes:
# - CVE IDs with CVSS scores
# - Affected package versions
# - Upgrade paths
# - Exploitability assessment
```

**Expected Output:**

```
╔══════════════════════════════════════════════════╗
║  CVE Dependency Scan                             ║
╠══════════════════════════════════════════════════╣
║  Dependencies checked    ✓   234                 ║
║  CVEs found              ✗   12                  ║
║  Critical                ✗   3                   ║
║  High                    ⚠   5                   ║
║  Medium                  ⚠   4                   ║
╚══════════════════════════════════════════════════╝

┌─────────────┬──────────┬─────────────┬──────────────┬─────────────┐
│ Package     │ CVE      │ CVSS        │ Installed    │ Fixed In    │
├─────────────┼──────────┼─────────────┼──────────────┼─────────────┤
│ lodash      │ CVE-2021 │ 9.8 🔴      │ 4.17.15      │ 4.17.21     │
│ axios       │ CVE-2022 │ 8.1 🔴      │ 0.21.0       │ 0.21.4      │
│ express     │ CVE-2022 │ 7.5 🟠      │ 4.17.1       │ 4.18.2      │
└─────────────┴──────────┴─────────────┴──────────────┴─────────────┘

UPGRADE COMMANDS
npm install lodash@4.17.21
npm install axios@0.21.4
npm install express@4.18.2
```

### 3. GDPR Compliance Audit

Maps data flows, identifies consent gaps, and generates DPA checklist.

```bash
/gdpr-audit <application_path>

# Options
/gdpr-audit . --data-map
/gdpr-audit src/ --consent-analysis
/gdpr-audit . --full-report --output gdpr-audit.pdf
```

**Example Analysis:**

```
╔══════════════════════════════════════════════════╗
║  GDPR Compliance Audit                           ║
╠══════════════════════════════════════════════════╣
║  Data flows mapped       ✓   24                  ║
║  Personal data types     ✓   8                   ║
║  Consent gaps            ✗   5                   ║
║  DPA requirements        ⚠   12/15 met           ║
╚══════════════════════════════════════════════════╝

DATA FLOW MAP
User Registration → Database (PII: email, name, phone)
  ↳ Consent: ✗ Missing explicit opt-in
  ↳ Retention: ⚠ No deletion policy defined
  ↳ Encryption: ✓ AES-256 at rest

Analytics Pipeline → Third-party (IP address, user agent)
  ↳ Consent: ✗ No cookie banner
  ✳ DPA: ⚠ No Data Processing Agreement on file

COMPLIANCE GAPS
🔴 Critical:
  • No cookie consent mechanism implemented
  • Missing data retention policies in privacy policy
  • No user data deletion endpoint

🟠 High:
  • DPA missing for analytics provider
  • DSAR (data subject access request) workflow undefined
```

### 4. SOC2 Readiness Assessment

Performs gap analysis across all 5 Trust Service Criteria.

```bash
/soc2-readiness

# Options
/soc2-readiness --criteria security,availability
/soc2-readiness --type type2
/soc2-readiness --output xlsx
```

**Example Output:**

```
╔══════════════════════════════════════════════════╗
║  SOC 2 Type II Readiness Assessment              ║
╠══════════════════════════════════════════════════╣
║  Security                ⚠   65% ready           ║
║  Availability            ✓   90% ready           ║
║  Confidentiality         ✗   45% ready           ║
║  Processing Integrity    ⚠   70% ready           ║
║  Privacy                 ✗   50% ready           ║
╚══════════════════════════════════════════════════╝

SECURITY GAPS
✗ CC6.1: No background checks policy
✗ CC6.6: Missing logical access reviews (quarterly)
⚠ CC7.2: Incomplete system monitoring

AVAILABILITY GAPS
⚠ A1.2: RTO/RPO not documented in DR plan

REMEDIATION TIMELINE
Quick Wins (1-2 weeks):
  • Document RTO/RPO targets
  • Implement access review schedule

Medium-term (1-3 months):
  • Establish background check policy
  • Deploy SIEM for continuous monitoring

Strategic (3-6 months):
  • Conduct third-party penetration test
  • Implement data classification framework
```

### 5. Threat Modeling (STRIDE)

Generates STRIDE threat model for architecture diagrams.

```bash
/threat-model <architecture_file>

# Options
/threat-model architecture.png --framework stride
/threat-model system-design.md --risk-matrix
/threat-model . --auto-discover
```

**Example for Web Application:**

```
╔══════════════════════════════════════════════════╗
║  STRIDE Threat Model                             ║
╠══════════════════════════════════════════════════╣
║  Components analyzed     ✓   8                   ║
║  Data flows              ✓   12                  ║
║  Threats identified      ✗   18                  ║
╚══════════════════════════════════════════════════╝

ARCHITECTURE COMPONENTS
• Web Application (React SPA)
• API Gateway (nginx)
• Backend API (Node.js/Express)
• Database (PostgreSQL)
• Auth Service (OAuth2)
• External Payment Gateway

THREAT ANALYSIS (STRIDE)

[S]poofing
  🔴 API Gateway: No mutual TLS for backend communication
     Impact: High | Likelihood: Medium
     Mitigation: Implement mTLS between gateway and API

[T]ampering
  🟠 Database: SQL injection possible via user input
     Impact: Critical | Likelihood: Low
     Mitigation: Use parameterized queries

[R]epudiation
  🟡 API: Insufficient audit logging for sensitive operations
     Impact: Medium | Likelihood: Medium
     Mitigation: Implement comprehensive audit trail

[I]nformation Disclosure
  🔴 Payment Flow: PCI data logged in application logs
     Impact: Critical | Likelihood: Medium
     Mitigation: Implement PCI-compliant logging filters

[D]enial of Service
  🟠 API: No rate limiting on public endpoints
     Impact: High | Likelihood: High
     Mitigation: Implement rate limiting middleware

[E]levation of Privilege
  🔴 Auth: JWT lacks role claims validation
     Impact: Critical | Likelihood: Medium
     Mitigation: Add RBAC middleware with role enforcement

RISK MATRIX
        Impact →
Likelihood  │  Low    Medium   High    Critical
───────────┼───────────────────────────────────
High        │                   DoS
Medium      │          Repud.   Spoof   InfoDisc, EoP
Low         │                   Tamper
```

### 6. Penetration Test Report Generator

Structures penetration test findings with executive summary and remediation.

```bash
/pentest-report <findings_file>

# Options
/pentest-report findings.json --template executive
/pentest-report scan-results/ --format pdf
/pentest-report . --cvss-threshold 7.0
```

**Example Report Structure:**

```
╔══════════════════════════════════════════════════╗
║  Penetration Test Report                         ║
║  Target: api.example.com                         ║
║  Date: 2024-01-15                                ║
╠══════════════════════════════════════════════════╣
║  Critical findings       ✗   4                   ║
║  High findings           ✗   7                   ║
║  Medium findings         ⚠   12                  ║
║  Low/Info                ✓   8                   ║
╚══════════════════════════════════════════════════╝

EXECUTIVE SUMMARY
The penetration test identified 31 findings across the web application
and API infrastructure. 4 critical vulnerabilities require immediate
remediation, including SQL injection and authentication bypass issues.

CRITICAL FINDINGS

1. SQL Injection in User Search (CVSS 9.8)
   Location: /api/v1/users/search?q=
   
   Description:
   User-supplied input in the 'q' parameter is directly concatenated
   into SQL query without sanitization.
   
   Proof of Concept:
   GET /api/v1/users/search?q=' OR '1'='1
   
   Remediation:
   • Implement parameterized queries
   • Add input validation and sanitization
   • Deploy WAF rules to detect SQL injection patterns
   
   Timeline: Immediate (< 48 hours)

2. Authentication Bypass via JWT None Algorithm (CVSS 9.1)
   Location: /api/v1/auth/verify
   
   Description:
   JWT library accepts 'none' algorithm, allowing unsigned tokens.
   
   Proof of Concept:
   eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4ifQ.
   
   Remediation:
   • Explicitly reject 'none' algorithm in JWT verification
   • Implement algorithm whitelist
   • Add token signature validation tests
   
   Timeline: Immediate (< 48 hours)

REMEDIATION ROADMAP

Immediate (< 48 hours):
  ✗ Fix SQL injection vulnerabilities
  ✗ Patch JWT authentication bypass
  ✗ Disable debug endpoints in production

Short-term (1-2 weeks):
  ⚠ Implement rate limiting
  ⚠ Add CSRF protection
  ⚠ Deploy Web Application Firewall

Medium-term (1 month):
  ⚠ Conduct security code review
  ⚠ Implement security headers (CSP, HSTS)
  ⚠ Add automated security scanning to CI/CD
```

### 7. Secret Detection (Pre-commit Hook)

Configures pre-commit hooks for secret and credential detection.

```bash
/secret-detect init

# Options
/secret-detect scan <directory>
/secret-detect --entropy-threshold 4.5
/secret-detect --add-patterns custom-patterns.json
```

**Example Configuration:**

```bash
# Initialize secret detection
/secret-detect init

# Creates .pre-commit-config.yaml
```

**Generated `.pre-commit-config.yaml`:**

```yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args:
          - '--baseline'
          - '.secrets.baseline'
          - '--exclude-files'
          - 'package-lock.json|.*\.min\.js'
        
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
        args:
          - '--verbose'
          - '--redact'

# Custom entropy scanning
  - repo: local
    hooks:
      - id: high-entropy-strings
        name: Detect high-entropy strings
        entry: python scripts/entropy-scan.py
        language: python
        args: ['--threshold', '4.5']
```

**Scan Example:**

```bash
/secret-detect scan src/

# Output:
╔══════════════════════════════════════════════════╗
║  Secret Detection Scan                           ║
╠══════════════════════════════════════════════════╣
║  Files scanned           ✓   156                 ║
║  Secrets detected        ✗   8                   ║
║  High entropy strings    ⚠   3                   ║
╚══════════════════════════════════════════════════╝

DETECTED SECRETS
┌─────────────────────┬──────────────────┬─────────────────┐
│ Type                │ File             │ Line            │
├─────────────────────┼──────────────────┼─────────────────┤
│ AWS Access Key      │ config.js        │ 12              │
│ Private Key         │ certs/dev.key    │ 1               │
│ API Key (Generic)   │ api-client.js    │ 45              │
│ High Entropy String │ utils.js         │ 89              │
└─────────────────────┴──────────────────┴─────────────────┘

REMEDIATION
• Move secrets to environment variables
• Add affected files to .gitignore
• Rotate exposed credentials immediately
• Review git history with: git log -p <file>
```

### 8. IAM Least Privilege Audit

Audits IAM roles for over-permissions, stale access, and MFA gaps.

```bash
/iam-audit

# Options
/iam-audit --provider aws
/iam-audit --check-mfa
/iam-audit --stale-days 90
/iam-audit --output csv
```

**Example AWS IAM Audit:**

```
╔══════════════════════════════════════════════════╗
║  IAM Least Privilege Audit (AWS)                 ║
╠══════════════════════════════════════════════════╣
║  Users analyzed          ✓   24                  ║
║  Roles analyzed          ✓   18                  ║
║  Over-permissioned       ✗   7                   ║
║  Stale access (90d)      ✗   5                   ║
║  Missing MFA             ✗   3                   ║
╚══════════════════════════════════════════════════╝

OVER-PERMISSIONED ROLES
┌──────────────────┬─────────────────┬──────────────────┐
│ Role/User        │ Issue           │ Last Used        │
├──────────────────┼─────────────────┼──────────────────┤
│ DevOps-Role      │ Admin policy    │ 2 days ago       │
│ DataScience-Role │ S3 Full Access  │ 15 days ago      │
│ CI-Pipeline      │ IAM permissions │ 1 day ago        │
└──────────────────┴─────────────────┴──────────────────┘

RECOMMENDATIONS

DevOps-Role:
  Current: AdministratorAccess
  Recommended: Custom policy with specific permissions
  Unused services: RDS, Lambda, DynamoDB
  
  Suggested Policy:
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "ec2:*",
          "s3:GetObject",
          "s3:PutObject",
          "cloudwatch:PutMetricData"
        ],
        "Resource": "*"
      }
    ]
  }

STALE ACCESS (>90 days)
• jenkins-user (145 days) - Consider deactivating
• legacy-integration (234 days) - Remove
• contractor-temp (98 days) - Review and remove

MISSING MFA
🔴 admin-user (console access)
🔴 ops-team-lead (console access)
⚠ backup-operator (API only)

ACTION PLAN
Immediate:
  ✗ Enable MFA for admin-user and ops-team-lead
  ✗ Deactivate access for legacy-integration

Short-term:
  ⚠ Replace AdministratorAccess with scoped policies
  ⚠ Implement 90-day access review process
  ⚠ Add MFA enforcement policy
```

### 9. Security Incident Playbook

Generates security incident response playbook following NIST framework.

```bash
/incident-playbook <incident_type>

# Options
/incident-playbook data-breach
/incident-playbook ransomware
/incident-playbook ddos-attack
/incident-playbook --format pdf
```

**Example Playbook:**

```
╔══════════════════════════════════════════════════╗
║  Security Incident Playbook: Data Breach         ║
╠══════════════════════════════════════════════════╣
║  Framework: NIST SP 800-61                       ║
║  Phases: 5                                       ║
╚══════════════════════════════════════════════════╝

PHASE 1: DETECTION & TRIAGE (0-1 hour)

Immediate Actions:
  ☐ Confirm incident severity and scope
  ☐ Notify Security Team Lead
  ☐ Activate incident response team
  ☐ Begin incident log (time, actions, findings)
  
Detection Checklist:
  ☐ Review SIEM alerts and logs
  ☐ Check data exfiltration indicators
  ☐ Identify compromised systems/accounts
  ☐ Determine data types affected

Key Questions:
  • What data was accessed/exfiltrated?
  • How many records affected?
  • When did the breach occur?
  • Is the breach ongoing?

PHASE 2: CONTAINMENT (1-4 hours)

Short-term Containment:
  ☐ Isolate affected systems from network
  ☐ Disable compromised user accounts
  ☐ Block malicious IP addresses at firewall
  ☐ Reset credentials for affected systems
  ☐ Enable enhanced monitoring

Long-term Containment:
  ☐ Apply security patches
  ☐ Implement additional access controls
  ☐ Deploy IDS/IPS rules
  ☐ Segment network if not already done

Evidence Preservation:
  ☐ Take disk/memory snapshots
  ☐ Preserve logs (application, system, network)
  ☐ Document all containment actions
  ☐ Chain of custody for forensic evidence

PHASE 3: ERADICATION (4-24 hours)

  ☐ Remove malware/backdoors from affected systems
  ☐ Close vulnerability that enabled breach
  ☐ Verify no persistence mechanisms remain
  ☐ Conduct full system security scan
  ☐ Review and update security configurations

Root Cause Analysis:
  • Entry point identification
  • Attack vector analysis
  • Timeline reconstruction
  • Identify control failures

PHASE 4: RECOVERY (1-7 days)

  ☐ Restore systems from clean backups
  ☐ Verify system integrity before reconnection
  ☐ Gradually restore services (least critical first)
  ☐ Enhanced monitoring for 30 days
  ☐ User access verification

Validation:
  ☐ Penetration testing of restored systems
  ☐ Vulnerability scanning
  ☐ Security control verification

PHASE 5: POST-INCIDENT (7-30 days)

Lessons Learned Meeting (within 48 hours):
  • What happened?
  • What was done well?
  • What could be improved?
  • What will we do differently?

Deliverables:
  ☐ Incident report (technical)
  ☐ Executive summary
  ☐ Timeline of events
  ☐ Financial impact assessment
  ☐ Regulatory notification (if required)

Regulatory Obligations:
  • GDPR: 72-hour notification to supervisory authority
  • CCPA: Notification without unreasonable delay
  • HIPAA: 60-day notification to affected individuals
  • State breach notification laws (check jurisdictions)

Security Improvements:
  ☐ Update incident response plan
  ☐ Implement identified security controls
  ☐ Conduct security awareness training
  ☐ Schedule follow-up security assessment

CONTACTS

Security Team:
  • Security Lead: ENV:SECURITY_LEAD_CONTACT
  • On-Call SIEM: ENV:SIEM_ONCALL
  • Forensics Team: ENV:FORENSICS_CONTACT

External:
  • Legal Counsel: ENV:LEGAL_CONTACT
  • PR/Communications: ENV:PR_CONTACT
  • Cyber Insurance: ENV:INSURANCE_CONTACT
  • Law Enforcement (FBI IC3): https://www.ic3.gov

Regulatory:
  • GDPR DPA: ENV:DPA_CONTACT
  • State Attorney General: ENV:STATE_AG_CONTACT
```

### 10. Privacy Policy Generator

Generates GDPR/CCPA-compliant privacy policy from data inventory.

```bash
/privacy-policy <data_inventory_file>

# Options
/privacy-policy inventory.json --jurisdiction eu,us,uk
/privacy-policy . --auto-discover
/privacy-policy data-map.yaml --format html
```

**Example Data Inventory:**

```json
{
  "personal_data": [
    {
      "type": "contact",
      "fields": ["email", "name", "phone"],
      "purpose": "user_account",
      "retention": "account_lifetime",
      "third_parties": []
    },
    {
      "type": "analytics",
      "fields": ["ip_address", "user_agent", "session_id"],
      "purpose": "service_improvement",
      "retention": "90_days",
      "third_parties": ["Google Analytics"]
    }
  ]
}
```

**Generated Policy Excerpt:**

```markdown
# Privacy Policy

Last Updated: 2024-01-15

## 1. Information We Collect

### Contact Information
We collect your email address, name, and phone number when you:
- Create an account
- Contact customer support
- Subscribe to our newsletter

**Legal Basis (GDPR):** Contract performance, legitimate interest
**Retention:** Duration of account plus 30 days

### Analytics Data
We automatically collect:
- IP address
- Browser type and version
- Device information
- Pages visited and time spent

**Legal Basis (GDPR):** Legitimate interest (service improvement)
**Retention:** 90 days

## 2. How We Use Your Information

We use your information to:
- Provide and maintain our services
- Send account-related notifications
- Improve our products and services
- Comply with legal obligations

## 3. Third-Party Service Providers

We share your information with:

**Google Analytics**
- Purpose: Website analytics and usage patterns
- Data shared: IP address, user agent, page views
- Location: United States
- Privacy Policy: https://policies.google.com/privacy
- Data Processing Agreement: In place

## 4. Your Rights (GDPR)

You have the right to:
- **Access:** Request a copy of your personal data
- **Rectification:** Correct inaccurate data
- **Erasure:** Request deletion of your data
- **Restriction:** Limit processing of your data
- **Portability:** Receive your data in machine-readable format
- **Objection:** Object to processing based on legitimate interest
- **Withdraw Consent:** Where processing is based on consent

To exercise these rights, contact: ENV:PRIVACY_CONTACT_EMAIL

## 5. Your Rights (CCPA)

California residents have the right to:
- Know what personal information is collected
- Know whether personal information is sold or disclosed
- Say no to the sale of personal information
- Access your personal information
- Request deletion of personal information
- Equal service and price, even if you exercise your privacy rights

## 6. Data Security

We implement appropriate technical and organizational measures:
- Encryption in transit (TLS 1.3)
- Encryption at rest (AES-256)
- Access controls and authentication
- Regular security assessments
- Employee security training

## 7. International Data Transfers

Your data may be transferred to and processed in:
- United States (Standard Contractual Clauses)
- European Union (GDPR compliant)

We ensure appropriate safeguards are in place for all transfers.

## 8. Children's Privacy

Our services are not directed to individuals under 16. We do not
knowingly collect personal information from children.

## 9. Contact Information

Data Controller: [Company Name]
Email: ENV:PRIVACY_CONTACT_EMAIL
Address: [Company Address]

EU Representative: ENV:EU_REP_CONTACT
UK Representative: ENV:UK_REP_CONTACT

Supervisory Authority: [Relevant DPA]
```

## Multi-Step Workflows

### Workflow 1: Secure SDLC (Shift-Left Security)

End-to-end secure development lifecycle implementation.

```bash
/workflow:secure-sdlc <project_path>

# Options
/workflow:secure-sdlc . --phase all
/workflow:secure-sdlc src/ --skip-dast
```

**Workflow Steps:**

```
╔══════════════════════════════════════════════════╗
║  Secure SDLC Workflow                            ║
╠══════════════════════════════════════════════════╣
║  1. Threat Model        ⟳   In Progress          ║
║  2. SAST Scan           ░   Pending              ║
║  3. Dependency Check    ░   Pending              ║
║  4. DAST Scan           ░   Pending              ║
║  5. Penetration Test    ░   Pending              ║
║  6. Security Sign-off   ░   Pending              ║
╚══════════════════════════════════════════════════╝

PHASE 1: THREAT MODELING
  Running: /threat-model architecture.md
  [Output from threat model command...]

PHASE 2: STATIC ANALYSIS
  Running: /owasp-scan src/
  [Output from OWASP scan...]

PHASE 3: DEPENDENCY CHECK
  Running: /dep-cve --scope full
  [Output from CVE scan...]

PHASE 4: DYNAMIC TESTING
  Running DAST against staging environment...
  [DAST results...]

PHASE 5: PENETRATION TEST
  Generating penetration test checklist...
  [Pentest scope and requirements...]

PHASE 6: SECURITY SIGN-OFF
  Generating security release checklist...
  
  RELEASE CRITERIA
  ☐ All critical vulnerabilities resolved
