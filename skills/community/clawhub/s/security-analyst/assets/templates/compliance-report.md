# Compliance Mapping Report Template

The orchestrator produces this report by mapping existing security findings to a specified compliance framework. Output to `{REPORTS_DIR}/compliance.md`.

---

    # Compliance Mapping Report

    **Date:** {ISO_TIMESTAMP}
    **Security Run:** {RUN_DIR}
    **Framework:** [SOC 2 / ISO 27001 / PCI DSS / HIPAA / GDPR / NIST CSF / custom]
    **Total Findings Mapped:** [count] of [total findings]
    **Controls Assessed:** [count]
    **Controls with Findings:** [count]

    ---

    ## Executive Summary

    [2-3 paragraphs covering:]
    - Compliance posture overview against the selected framework
    - Critical control gaps that require immediate remediation
    - Controls that are well-addressed by current implementation
    - Recommended priority actions for compliance readiness

    ---

    ## Control Mapping Matrix

    ### SOC 2 Trust Service Criteria (use this section if framework is SOC 2)

    | Control ID | Category | Control Description | Related Findings | Status | Gap Description |
    |-----------|----------|-------------------|-----------------|--------|-----------------|
    | CC1.1 | Security | COSO Principle 1 — Integrity and ethical values | | Pass / Fail / Partial / N/A | |
    | CC5.1 | Security | Risk identification and assessment | | | |
    | CC6.1 | Security | Logical and physical access controls | | | |
    | CC6.2 | Security | User authentication | | | |
    | CC6.3 | Security | Authorization enforcement | | | |
    | CC6.6 | Security | Security events monitoring | | | |
    | CC6.7 | Security | Change management | | | |
    | CC6.8 | Security | Unauthorized/malicious software prevention | | | |
    | CC7.1 | Security | Infrastructure and software monitoring | | | |
    | CC7.2 | Security | Security incident detection | | | |
    | CC8.1 | Security | Change management process | | | |

    ### ISO 27001 Annex A Controls (use this section if framework is ISO 27001)

    | Control | Domain | Description | Related Findings | Status | Gap |
    |---------|--------|-------------|-----------------|--------|-----|
    | A.5 | Information Security Policies | Policy documentation | | | |
    | A.6 | Organization of IS | Roles, mobile, teleworking | | | |
    | A.8 | Asset Management | Classification, handling | | | |
    | A.9 | Access Control | Business requirements, user access | | | |
    | A.10 | Cryptography | Policy, key management | | | |
    | A.12 | Operations Security | Procedures, malware, backup, logging | | | |
    | A.13 | Communications Security | Network, information transfer | | | |
    | A.14 | System Acquisition/Dev | Security requirements, development, test data | | | |
    | A.16 | Incident Management | Reporting, response, lessons learned | | | |
    | A.18 | Compliance | Legal, policy, technical compliance | | | |

    ### PCI DSS Requirements (use this section if framework is PCI DSS)

    | Requirement | Description | Related Findings | Status | Gap |
    |------------|-------------|-----------------|--------|-----|
    | 1 | Install and maintain network security controls | | | |
    | 2 | Apply secure configurations | | | |
    | 3 | Protect stored account data | | | |
    | 4 | Protect cardholder data with strong cryptography during transmission | | | |
    | 5 | Protect all systems against malware | | | |
    | 6 | Develop and maintain secure systems | | | |
    | 7 | Restrict access by business need-to-know | | | |
    | 8 | Identify users and authenticate access | | | |
    | 9 | Restrict physical access to cardholder data | | | |
    | 10 | Log and monitor all access | | | |
    | 11 | Test security regularly | | | |
    | 12 | Support IS with organizational policies | | | |

    ### HIPAA Security Rule (use this section if framework is HIPAA)

    | Standard | Safeguard | Description | Related Findings | Status | Gap |
    |----------|-----------|-------------|-----------------|--------|-----|
    | 164.312(a) | Technical | Access control | | | |
    | 164.312(b) | Technical | Audit controls | | | |
    | 164.312(c) | Technical | Integrity controls | | | |
    | 164.312(d) | Technical | Person or entity authentication | | | |
    | 164.312(e) | Technical | Transmission security | | | |
    | 164.308(a)(1) | Administrative | Security management process | | | |
    | 164.308(a)(3) | Administrative | Workforce security | | | |
    | 164.308(a)(4) | Administrative | Information access management | | | |
    | 164.308(a)(5) | Administrative | Security awareness and training | | | |

    ### GDPR Articles (use this section if framework is GDPR)

    | Article | Topic | Description | Related Findings | Status | Gap |
    |---------|-------|-------------|-----------------|--------|-----|
    | Art. 5 | Principles | Lawfulness, purpose limitation, data minimization | | | |
    | Art. 6 | Lawful Basis | Processing legality | | | |
    | Art. 25 | DPbD | Data protection by design and default | | | |
    | Art. 30 | Records | Records of processing activities | | | |
    | Art. 32 | Security | Security of processing | | | |
    | Art. 33 | Breach Notification | To supervisory authority (72h) | | | |
    | Art. 34 | Breach Notification | To data subjects | | | |
    | Art. 35 | DPIA | Data protection impact assessment | | | |
    | Art. 44-49 | Transfers | International data transfers | | | |

    Only include the framework section requested by the user. Omit the others.

    ---

    ## Detailed Gap Analysis

    For each control with Status = Fail or Partial:

    ### [Control ID]: [Control Description]

    **Status:** Fail / Partial
    **Related Findings:** [Finding IDs with severity]
    **Current State:** [What the project does now]
    **Required State:** [What the control requires]
    **Gap:** [Specific delta between current and required]
    **Remediation:**
    - [Specific action 1 — reference fix-plan task if available]
    - [Specific action 2]
    **Effort:** [hours/days]
    **Priority:** [Critical / High / Medium / Low]

    ---

    ## Compliance Score Summary

    | Category | Total Controls | Pass | Partial | Fail | N/A | Score |
    |----------|---------------|------|---------|------|-----|-------|
    | [category 1] | | | | | | [%] |
    | [category 2] | | | | | | [%] |
    | **Overall** | | | | | | **[%]** |

    ---

    ## Recommendations

    ### Immediate Actions (blocking compliance)
    1. [Action] — addresses [Control IDs] — Effort: [estimate]

    ### Short-Term Improvements
    1. [Action] — addresses [Control IDs] — Effort: [estimate]

    ### Documentation Gaps
    1. [Missing documentation] — required by [Control IDs]

    ---

    ## Data Sources

    | Source | Path | Used For |
    |--------|------|---------|
    | Security Analysis Report | {FINAL_REPORT} | Finding-to-control mapping |
    | Fix Plan | {REPORTS_DIR}/fix-plan.md | Remediation effort estimates |
    | Recon Index | {RECON_DIR}/index.md | Current implementation state |
    | SBOM | {REPORTS_DIR}/sbom.md | Dependency and license inventory |
