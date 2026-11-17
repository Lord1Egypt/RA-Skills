# M6 - AppSec, Secure Code & Threat Modeling

**Purpose:** Find secure-coding guidance, SAST/DAST/SCA rules, code-review checklists, threat
modeling methods, and remediation patterns for an application stack.

**Triggers:** appsec, application security, secure code, secure coding, SAST, DAST, SCA, code
review, secure SDLC, SSDLC, threat model, threat modeling, STRIDE, PASTA, LINDDUN, OWASP Top 10,
ASVS, WSTG, CWE, dependency vulnerability, secret scanning, security testing, LLM, GenAI,
agentic AI, prompt injection, AIBOM, SLSA, supply chain security.

**Process contract:** Always run the Universal Search Loop (Section 1) and the Process Compliance
Gate (Section 0.5). This module supplies sources and queries only.

---

## Primary sources

### Standards and guidance
| Source | Use |
|---|---|
| **OWASP Top 10** | Web risk categories |
| **OWASP ASVS** | Verification requirements |
| **OWASP WSTG** | Test cases |
| **OWASP Cheat Sheet Series** | Secure coding patterns |
| **OWASP SAMM** | Software assurance maturity |
| **OWASP MASVS/MASTG** | Mobile security |
| **OWASP API Security Top 10** | API risks |
| **OWASP GenAI** (`genai.owasp.org`) | LLM Top 10, Agentic Applications Top 10, AIBOM |
| **MITRE ATLAS** (`atlas.mitre.org`) | AI/ML adversary tactics, techniques, case studies |
| **CWE Top 25** | Weakness classes |
| **SLSA** (`slsa.dev`) | Build/supply-chain integrity levels and provenance |
| **OpenSSF Scorecard** (`scorecard.dev`, `github.com/ossf/scorecard`) | Automated supply-chain security checks |
| **NIST AI 600-1** (`nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf`) | Generative AI risk profile (AI RMF) |
| **NIST SSDF (SP 800-218)** | Secure SDLC |
| **Microsoft SDL** | Secure development process |
| **BSIMM** | Software security initiative maturity |

### AI incident and risk sources
- **AI Incident Database** (`incidentdatabase.ai`) - real-world AI harms, failures, and near misses.
- **AVID** (`avidml.org/database`) - open database of failure modes in general-purpose AI systems.
- **MIT AI Risk Repository** (`airisk.mit.edu`) - 1,700+ AI risks extracted from 65 frameworks.
- **AIAAIC Repository** (`aiaaic.org`) - AI incidents, controversies, and harms.
- **OECD AI Incidents Monitor** (`oecd.ai/en/incidents`) - policy-oriented AI incident evidence base.

### Tooling documentation
- **Semgrep** (`semgrep.dev`, rules registry).
- **CodeQL** (`codeql.github.com`, query packs).
- **Snyk**, **SonarQube**, **Checkmarx**, **Veracode** (docs and rule descriptions).
- **Trivy**, **Grype**, **OWASP Dependency-Check**, **Retire.js**, **npm audit**, **pip-audit**,
  **Bundler-audit**, **cargo-audit**, **govulncheck**.
- **Gitleaks**, **TruffleHog**, **detect-secrets**.
- **OpenSSF Malicious Packages** (`github.com/ossf/malicious-packages`) - OSV-format reports of
  malicious packages across ecosystems.
- **Dependabot**, **Renovate**.
- **OWASP Threat Dragon**, **Microsoft Threat Modeling Tool**, **IriusRisk**.

### Secure-coding references by stack
- Framework security docs: Django, Rails, Spring Security, Express/Helmet, ASP.NET Core, Laravel,
  FastAPI, Next.js, React, Angular.
- Language docs: memory safety, deserialization, crypto APIs.
- Database docs: parameterized queries, least privilege.
- Cloud docs: IAM, secrets management, metadata service.

---

## Query recipes

```text
# Standards and controls
site:owasp.org "ASVS" "authentication"
site:cheatsheetseries.owasp.org "SQL injection" "prevention"
site:owasp.org "WSTG" "authorization"
site:cwe.mitre.org "CWE-79"
site:owasp.org "Top 10" 2025
site:nist.gov "SSDF" "800-218"

# Secure coding by stack
site:docs.djangoproject.com "security" "CSRF"
site:docs.spring.io "security" "authorization"
site:expressjs.com "security best practices"
site:learn.microsoft.com "ASP.NET Core" "security"
"secure coding" "Java" checklist
"secure code review" checklist "Python"

# SAST/DAST/SCA rules
site:semgrep.dev "rule" "java" "sql injection"
site:codeql.github.com "query" "command injection"
"Semgrep rule" "SSRF"
"CodeQL" "path traversal" query
"dependency check" "SBOM" "CI"

# Threat modeling
"threat model" "STRIDE" example
"threat modeling" "data flow diagram"
"PASTA" threat modeling
"LINDDUN" privacy threat model
"OWASP Threat Dragon" tutorial

# AI/LLM and agentic security
site:genai.owasp.org "LLM Top 10"
site:genai.owasp.org "Agentic" "Top 10"
site:genai.owasp.org "AIBOM"
site:atlas.mitre.org "prompt injection"
site:incidentdatabase.ai "harm"
site:avidml.org "LLM"
site:airisk.mit.edu "risk"
site:aiaaic.org "LLM"
site:oecd.ai "AI incident"
site:nist.gov "AI 600-1" "generative AI"
"prompt injection" "LLM" mitigation
"agentic AI" security checklist

# Secrets and supply chain
"secret scanning" "pre-commit"
"SBOM" "CycloneDX" "SPDX"
site:slsa.dev "provenance"
site:scorecard.dev "dependency update"
"SLSA" "supply chain" "provenance"
"OpenSSF Scorecard" "branch protection"
site:github.com/ossf/malicious-packages "npm"
```

---

## Workflow

1. **Identify the stack and data flows.** Language, framework, dependencies, auth, data stores,
   external services, trust boundaries.
2. **Select the standard.** OWASP Top 10 for breadth, ASVS for verification, WSTG for testing,
   CWE for weakness mapping, SSDF for process.
3. **Threat model.** Draw data-flow diagrams, identify assets/actors/trust boundaries, enumerate
   threats (STRIDE), rate risk, choose mitigations.
4. **Map controls to code.** For each threat, find the secure pattern and the vulnerable
   anti-pattern in the framework docs.
5. **Configure tooling.** Semgrep/CodeQL rules, SCA, secret scanning, IaC scanning, DAST.
6. **Review.** Combine automated findings with manual review of auth, input handling, crypto,
   session management, file upload, deserialization, and business logic.
7. **Verify.** Write a test that fails on the vulnerable pattern and passes on the fix.
8. **Report.** Include CWE, evidence, severity, remediation, and references (M12).

---

## What to extract

| Field | Example |
|---|---|
| Risk class | Broken access control (OWASP A01) |
| CWE | CWE-639 |
| Vulnerable pattern | object ID trusted from request |
| Secure pattern | server-side ownership check |
| Tool rule | Semgrep rule ID / CodeQL query |
| Test | unit/integration test for cross-tenant access |
| Severity | High (CVSS 8.1) |
| Confidence | A (code + test + framework docs) |

---

## Pitfalls

- **False positives.** SAST rules lack context; triage every finding.
- **Framework magic.** ORMs, middleware, and annotations may enforce controls implicitly.
- **Transitive dependencies.** SCA must include the full lockfile and container image.
- **Secrets in history.** Removing a secret from HEAD is not enough; rotate and purge history.
- **Config vs code.** Many issues live in deployment config, not source.
- **Checklist compliance.** Passing ASVS does not prove security; test behavior.
- **Threat model drift.** Update it when architecture changes.

---

## Ethics

- Review only code you are authorized to access.
- Do not exfiltrate source code, secrets, or customer data.
- Redact secrets and PII in reports.
- Prefer responsible disclosure for third-party software.
- Recommend fixes, not just findings.

---

## Output contract

```
module:        M6 AppSec
objective:     assess <app/stack> against <standard>
authorization: code owner / authorized review
sources_used:  OWASP/ASVS/WSTG/CWE, framework docs, tool rules, mapped to the claim it supports
sources_read:  URLs opened but excluded, with reason (off-scope, stale, duplicate, low confidence, inaccessible, discovery only)
findings:      threat model, control gaps, CWE, evidence, remediation
pivots:        M7 architecture, M12 report, M9 labs
caveats:       false positives, scope of review, unverified runtime behavior
```
