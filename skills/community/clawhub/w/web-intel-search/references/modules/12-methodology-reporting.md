# M12 - Methodology, Scoping, Reporting & Remediation

**Purpose:** Find authoritative testing methodologies, scoping/RoE templates, risk-rating schemes,
report structures, and remediation guidance. Use this module to keep every engagement defensible,
reproducible, and useful to the client.

**Triggers:** methodology, PTES, OWASP WSTG, OSSTMM, NIST 800-115, scoping, rules of engagement,
RoE, statement of work, SOW, penetration test report, risk rating, CVSS, remediation, retest,
quality assurance, peer review.

**Process contract:** Always run the Universal Search Loop (Section 1) and the Process Compliance
Gate (Section 0.5). This module supplies sources and queries only.

---

## Primary sources

### Methodologies and standards
| Source | Use |
|---|---|
| **PTES** (`pentest-standard.org`) | End-to-end penetration testing process |
| **OWASP WSTG** | Web test cases |
| **OSSTMM** (`isecom.org`) | Open-source security testing methodology |
| **NIST SP 800-115** | Technical security testing guide |
| **MITRE ATT&CK** | Adversary technique mapping |
| **TIBER-EU / CBEST** | Threat-led testing |
| **CREST** | Professional standards and reporting |
| **PCI DSS** | Penetration testing requirements |
| **ISO/IEC 27001/27035** | ISMS and incident management |
| **ISACA** | Audit and assurance guidance |

### Risk rating and reporting
- **CVSS v3.1 / v4.0** (`first.org/cvss`).
- **EPSS** and **CISA KEV** for prioritization.
- **OWASP Risk Rating Methodology**.
- **DREAD** (legacy; use with caution).
- **STRIDE** for threat classification.
- **MITRE ATT&CK** for technique mapping.

### Templates and checklists
- Scoping questionnaire and RoE templates (CREST, SANS, OWASP).
- Penetration test report templates (SANS, OffSec, vendor examples).
- Remediation and retest checklists.
- Evidence handling and chain-of-custody guidance.
- Quality assurance / peer review checklists.

---

## Query recipes

```text
# Methodologies
site:pentest-standard.org "PTES" "intelligence gathering"
site:owasp.org "WSTG" "testing checklist"
site:isecom.org "OSSTMM"
site:nist.gov "800-115" "security testing"
"threat-led penetration testing" TIBER-EU

# Scoping and RoE
"rules of engagement" penetration test template
"scoping questionnaire" pentest
"statement of work" "penetration testing"
"scope" "in scope" "out of scope" pentest template
"test window" "emergency contact" pentest

# Reporting
"penetration test report" template
"security assessment report" template
"executive summary" pentest report
"risk rating" "CVSS" "likelihood" "impact"
"remediation" "retest" checklist
"evidence" "screenshot" "reproduction steps" report

# Quality and ethics
"peer review" pentest report
"quality assurance" security assessment
"code of ethics" penetration tester
"data handling" pentest engagement
```

---

## Workflow

1. **Scope.** Define assets, exclusions, test windows, accounts, data handling, and success
   criteria. Put it in writing.
2. **Rules of engagement.** Authorization, contacts, escalation, prohibited techniques, emergency
   stop, legal boundaries.
3. **Methodology selection.** PTES + OWASP WSTG + ATT&CK as appropriate; document deviations.
4. **Test plan.** Map test cases to risks and effort; define evidence requirements.
5. **Execution and evidence.** Log every action, timestamp, request/response, screenshot, and
   command. Preserve chain of custody.
6. **Risk rating.** Use CVSS + business impact; calibrate with EPSS/KEV for exploitation likelihood.
7. **Report.** Executive summary, scope, methodology, findings, evidence, impact, remediation,
   appendices.
8. **Quality review.** Peer review for accuracy, reproducibility, and consistency.
9. **Debrief.** Walk through findings with the client; prioritize fixes.
10. **Retest.** Verify remediation; issue a closure letter.

---

## What to extract

| Field | Example |
|---|---|
| Framework | PTES + OWASP WSTG |
| Scope | 12 domains, 2 APIs, 1 mobile app; no DoS |
| Test window | 2026-11-01 to 2026-11-10 |
| Finding | Broken access control |
| Evidence | request/response + screenshot + timestamp |
| CVSS | 8.1 (AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N) |
| Business impact | cross-tenant data exposure |
| Remediation | server-side authorization check |
| Retest | verify 403 for cross-tenant request |

---

## Pitfalls

- **Checklist-only testing.** Frameworks are scaffolds, not a substitute for judgment.
- **Scope creep.** Testing beyond the agreed assets creates legal and operational risk.
- **Inconsistent severity.** Calibrate across findings and explain business impact.
- **Missing reproduction steps.** A finding without evidence is not actionable.
- **No retest.** Remediation is unverified until retested.
- **Poor data handling.** Reports contain sensitive data; encrypt and limit distribution.
- **Template bloat.** Keep reports concise and decision-oriented.

---

## Ethics

- Written authorization and RoE are mandatory before testing.
- Respect confidentiality, data minimization, and retention limits.
- Do not test prohibited techniques or out-of-scope assets.
- Disclose findings responsibly and coordinate publication.
- Protect evidence and client data throughout and after the engagement.

---

## Output contract

```
module:        M12 Methodology
objective:     plan/report <engagement> using <framework>
authorization: signed scope + RoE
sources_used:  PTES/WSTG/NIST/CREST + templates, mapped to the claim it supports
sources_read:  URLs opened but excluded, with reason (off-scope, stale, duplicate, low confidence, inaccessible, discovery only)
findings:      scope, methodology, findings, ratings, remediation, retest
pivots:        M1-M11 as needed
caveats:       scope limits, assumptions, unverified remediation
```
