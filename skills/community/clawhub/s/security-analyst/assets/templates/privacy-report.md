# Privacy & Data Protection Assessment Template

The privacy assessment agent produces this report by tracing PII flows, data retention, and consent mechanisms. Output to `{REPORTS_DIR}/privacy.md`.

---

    # Privacy & Data Protection Assessment

    **Date:** {ISO_TIMESTAMP}
    **Security Run:** {RUN_DIR}
    **Applicable Regulations:** [GDPR / CCPA / HIPAA / PIPEDA / LGPD / custom]
    **Project:** [From recon index]

    ---

    ## Executive Summary

    [2-3 paragraphs covering:]
    - Types and volume of personal data processed
    - Data flow risk assessment (high-risk flows)
    - Compliance posture for applicable regulations
    - Top 3 privacy risks requiring immediate attention

    ---

    ## Personal Data Inventory

    ### Data Categories Collected

    | Category | Data Elements | Collection Point | Storage Location | Lawful Basis | Retention Period |
    |----------|-------------|-----------------|-----------------|-------------|-----------------|
    | Identity | name, email | | | | |
    | Contact | phone, address | | | | |
    | Financial | payment info, billing | | | | |
    | Behavioral | usage logs, analytics | | | | |
    | Technical | IP, device info, cookies | | | | |
    | Sensitive | health, biometric, race | | | | |
    | Auth | passwords, tokens, sessions | | | | |

    ### Data Subject Categories

    | Subject Type | Data Collected | Volume Estimate | Special Protections |
    |-------------|---------------|-----------------|-------------------|
    | End Users | | | |
    | Employees | | | |
    | Minors (if applicable) | | | COPPA / GDPR Art. 8 |
    | Third-Party Contacts | | | |

    ---

    ## PII Data Flow Map

    For each critical PII flow, trace the complete lifecycle:

    ### Flow: [Name] (e.g., "User Registration")

    | Step | Component | File:Line | Data Elements | Operation | Protection | Risk |
    |------|-----------|-----------|--------------|-----------|-----------|------|
    | 1 | [entry point] | | [fields] | Collect | [TLS, validation] | |
    | 2 | [handler] | | [fields] | Process | [sanitization] | |
    | 3 | [database] | | [fields] | Store | [encryption] | |
    | 4 | [service] | | [fields] | Share | [consent check] | |
    | 5 | [output] | | [fields] | Display/Export | [redaction] | |

    Repeat for each PII flow (typically 4-8 flows: registration, authentication, profile management, data export, payment processing, communication, analytics, third-party sharing).

    ---

    ## Data Storage & Encryption

    | Data Element | Storage | Encrypted at Rest | Encrypted in Transit | Key Management | Retention | Deletion Method |
    |-------------|---------|-------------------|---------------------|----------------|-----------|-----------------|

    ---

    ## Third-Party Data Sharing

    | Third Party | Data Shared | Purpose | Legal Basis | DPA in Place? | Transfer Mechanism | Risk |
    |------------|------------|---------|-------------|---------------|-------------------|------|

    Transfer mechanisms: Standard Contractual Clauses, Adequacy Decision, Binding Corporate Rules, Consent, Derogation.

    ---

    ## Consent Management

    | Consent Type | Collection Method | File:Line | Granularity | Withdrawal Method | Record Keeping |
    |-------------|------------------|-----------|-------------|------------------|----------------|

    ### Consent Issues

    - Is consent obtained BEFORE data collection? (not retroactive)
    - Is consent granular? (separate consent per purpose, not bundled)
    - Is consent freely given? (not a condition of service where not necessary)
    - Can consent be withdrawn as easily as it was given?
    - Is consent recorded with timestamp and version?

    ---

    ## Data Subject Rights Implementation

    | Right | Implemented? | Mechanism | File:Line | Response Time | Automated? |
    |-------|-------------|-----------|-----------|--------------|-----------|
    | Access (GDPR Art. 15) | | | | | |
    | Rectification (Art. 16) | | | | | |
    | Erasure / Right to be Forgotten (Art. 17) | | | | | |
    | Restriction of Processing (Art. 18) | | | | | |
    | Data Portability (Art. 20) | | | | | |
    | Object to Processing (Art. 21) | | | | | |
    | Automated Decision-Making (Art. 22) | | | | | |
    | Opt-Out of Sale (CCPA) | | | | | |

    ### Implementation Gaps

    For each unimplemented or partially implemented right:
    - What is missing?
    - What effort is required?
    - What is the regulatory risk of non-compliance?

    ---

    ## Data Retention & Deletion

    | Data Category | Defined Retention Period | Actual Implementation | Deletion Method | Verification |
    |-------------|------------------------|---------------------|-----------------|-------------|

    ### Retention Issues

    - Is there a data retention policy documented?
    - Are retention periods enforced automatically? (scheduled deletion jobs)
    - Is data in backups subject to the same retention policy?
    - After deletion: is data purged from all locations (caches, logs, backups, search indexes)?

    ---

    ## Privacy by Design Assessment

    | Principle | Implementation | Assessment |
    |-----------|---------------|-----------|
    | Data Minimization | Do we collect only what's needed? | |
    | Purpose Limitation | Is data used only for stated purposes? | |
    | Storage Limitation | Is data deleted when no longer needed? | |
    | Accuracy | Can data subjects correct their data? | |
    | Integrity & Confidentiality | Is data protected against unauthorized access? | |
    | Accountability | Are processing activities documented? | |

    ---

    ## Cross-Border Data Transfers

    | Data | Source Jurisdiction | Destination | Transfer Mechanism | Adequacy Decision? | Risk |
    |------|-------------------|------------|-------------------|-------------------|------|

    ---

    ## Privacy Risk Register

    | Risk ID | Risk Description | Data Elements | Likelihood | Impact | Risk Level | Mitigation |
    |---------|-----------------|--------------|-----------|--------|-----------|-----------|

    Likelihood: Rare / Unlikely / Possible / Likely / Almost Certain
    Impact: Negligible / Minor / Moderate / Major / Severe

    ---

    ## Findings

    Privacy-specific findings that may not appear in the main security report:

    | ID | Severity | Description | Regulation | Remediation |
    |----|----------|-------------|-----------|-------------|

    Finding IDs use prefix `PRV-XXX`.

    ---

    ## Recommendations

    ### Immediate (regulatory risk)
    1. [Action] — addresses [risk/gap] — Effort: [estimate]

    ### Short-Term (privacy improvement)
    1. [Action] — Effort: [estimate]

    ### Documentation Needed
    1. [Document] — required by [regulation]

    ---

    ## Data Sources

    | Data | Source File | Collected By |
    |------|-----------|-------------|
    | PII locations | recon/step-05-crown-jewels.md | Recon agent |
    | Data flows | recon/step-09-data-flows.md | Recon agent |
    | Auth mechanisms | recon/step-06-auth.md | Recon agent |
    | External integrations | recon/step-07-integrations.md | Recon agent |
    | Encryption | recon/step-08-secrets.md | Recon agent |
    | Security findings | findings/index.md | All analysis agents |
