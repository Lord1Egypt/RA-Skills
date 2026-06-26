---
name: security-auditor
description: >
  Perform comprehensive security audits on codebases, infrastructure configs, API designs,
  and architecture documents. Use this skill whenever the user wants to review code or
  config for vulnerabilities, assess security posture, identify attack surface, produce
  a findings report, or get remediation recommendations. Trigger on phrases like "security
  review", "audit this", "find vulnerabilities", "is this secure", "pen test", "threat
  model", "OWASP", "check for CVEs", "security assessment", or any request to assess
  risk in code, infra, or system design — even if the word "audit" isn't used. Covers
  web apps, APIs, cloud configs, IAM policies, secrets management, auth flows, and more.
---

# Security Auditor

A skill for performing structured security audits across code, infrastructure, APIs,
and architecture. Produces prioritised findings with severity ratings and actionable
remediation steps.

---

## Scope & Trigger Contexts

Use this skill for any of the following:

- **Code review** — source files in any language (Python, JS/TS, Go, PHP, Java, etc.)
- **Infrastructure-as-code** — Terraform, CloudFormation, Kubernetes manifests, Docker files
- **API design** — OpenAPI/Swagger specs, REST or GraphQL schemas
- **Cloud configs** — IAM policies, S3 bucket policies, security group rules, GCP/Azure equivalents
- **Architecture diagrams or descriptions** — threat modelling, attack surface analysis
- **Dependency audit** — package.json, requirements.txt, pom.xml, go.mod

---

## Audit Process

### Step 1 — Clarify Scope (if needed)

If the user hasn't specified, quickly confirm:
- What is being audited? (code, config, architecture description)
- What is the deployment context? (web app, internal tool, public API, mobile backend)
- Any compliance requirements in scope? (SOC 2, ISO 27001, GDPR, PCI-DSS, HIPAA)
- Desired output format? (inline annotations, structured report, executive summary)

If context is obvious from what's been shared, skip straight to the audit — don't ask
unnecessary questions.

### Step 2 — Reconnaissance

Before diving into findings, briefly characterise what you're looking at:
- Tech stack / languages / frameworks identified
- Entry points (endpoints, event handlers, CLI args, file inputs)
- Trust boundaries (what's user-controlled vs internal)
- Data sensitivity (PII, financial, credentials, health data)

### Step 3 — Findings

For each issue found, produce a finding block (see format below). Organise findings
by severity: Critical → High → Medium → Low → Informational.

**Don't pad the report.** Only include genuine issues. A clean section is fine if
nothing material was found.

### Step 4 — Remediation Summary

After all findings, include a prioritised remediation plan — what to fix first and why.
If relevant, note any quick wins (easy fixes with high impact).

### Step 5 — Positive Observations (optional)

If the code/config shows good security practices, briefly acknowledge them. This adds
credibility and context to the report.

---

## Finding Format

```
### [SEV-###] Finding Title

**Severity**: Critical | High | Medium | Low | Informational
**Category**: [OWASP category or CWE if applicable]
**Location**: file.py:42 (or "Architecture — auth flow")

**Description**
Clear explanation of the vulnerability and why it matters.

**Evidence**
Relevant code snippet or config extract (keep it brief — just enough to illustrate).

**Impact**
What an attacker could achieve if this is exploited.

**Remediation**
Concrete steps to fix it, with a code example where helpful.

**References** (optional)
- OWASP: https://owasp.org/...
- CWE-###
```

---

## Severity Definitions

| Severity | Criteria |
|---|---|
| **Critical** | Direct path to full compromise, data breach, RCE, or auth bypass with no mitigations |
| **High** | Significant risk requiring exploitation of one step; privilege escalation, SQLi, SSRF |
| **Medium** | Requires chaining with other issues or specific conditions; CSRF, insecure defaults |
| **Low** | Defence-in-depth issues, info leakage, weak configs with limited direct impact |
| **Informational** | Best practice gaps, code hygiene, no direct security impact |

---

## Common Vulnerability Categories to Check

### Web Applications
- Injection (SQL, NoSQL, command, LDAP, XPath)
- Broken authentication & session management
- Insecure direct object references (IDOR)
- XSS (reflected, stored, DOM-based)
- CSRF
- Security misconfigurations (debug mode, verbose errors, default creds)
- Sensitive data exposure (logging PII, weak encryption, HTTP instead of HTTPS)
- Using components with known vulnerabilities
- Insufficient logging & monitoring

### APIs
- Broken object-level authorisation (BOLA/IDOR)
- Broken function-level authorisation
- Excessive data exposure
- Lack of rate limiting / resource exhaustion
- Mass assignment vulnerabilities
- Improper input validation
- JWT issues (alg:none, weak secrets, no expiry)

### Infrastructure & Cloud
- Overly permissive IAM roles / wildcard policies
- Public S3 buckets or blob storage
- Unrestricted security group ingress (0.0.0.0/0)
- Secrets hardcoded in configs or environment variables committed to source control
- Missing encryption at rest / in transit
- No MFA on privileged accounts
- Outdated AMIs / base images
- Missing audit logging (CloudTrail, GCP Audit Logs)

### Authentication & Authorisation
- Weak password policies
- Missing brute-force protection
- Insecure password reset flows
- Privilege escalation paths
- Missing authorisation checks on sensitive routes
- Token leakage in URLs or logs

---

## Output Formats

### Full Audit Report
Use for detailed code or config reviews. Includes all sections: scope, recon summary,
findings (with evidence), remediation plan, positive observations.

### Quick Assessment
Use when the user wants a fast pass or the input is small. Bullet-point findings with
severity tags, brief descriptions, and one-line remediations. No full report structure.

### Executive Summary
Use when explicitly requested. Plain English, no code snippets, business risk framing.
Suitable for sharing with non-technical stakeholders.

Default to **Full Audit Report** unless the user indicates otherwise or the input is
under ~50 lines of code/config.

---

## Tone & Style

- Be direct and precise — don't soften genuine risks
- Avoid false positives; if you're uncertain, flag it as "Potential issue — verify"
- Don't be alarmist about low-severity findings
- Remediation advice should be practical, not just "validate your inputs"
- Where relevant, link to authoritative references (OWASP, CWE, NIST, vendor docs)

---

## Compliance Mapping (optional)

If the user mentions a compliance framework, map critical/high findings to relevant
controls where appropriate:

| Framework | Notes |
|---|---|
| **SOC 2** | Map to Trust Service Criteria (CC6, CC7, CC8, CC9) |
| **ISO 27001** | Map to Annex A controls |
| **OWASP Top 10** | Always reference where applicable |
| **GDPR** | Flag PII handling, data retention, breach notification gaps |
| **PCI-DSS** | Flag cardholder data exposure, network segmentation issues |

Only include compliance mapping if explicitly requested or if a specific framework
was mentioned in scope.
