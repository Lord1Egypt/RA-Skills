# Final Report Structure

The report writer agent produces the final security analysis report following this structure. Output to `{REPORTS_DIR}/final.md`.

---

    # Security Analysis Report
    **Date:** [YYYY-MM-DD]
    **Analyst:** Claude Security Analyst (Opus)
    **Scope:** [Full / Focused on X / Variant hunt for Y / Threat model]
    **Methodology:** Offensive penetration testing — multi-phase analysis with team-based orchestration
    **Project:** [From recon index's Project Metadata]

    ---

    ## Executive Summary

    [2-3 paragraphs covering:]
    - Overall security posture assessment (strong/adequate/concerning/critical)
    - Most critical findings and their business impact
    - Key systemic issues (root causes that produce multiple findings)
    - Top 3 recommended immediate actions

    ---

    ## Risk Dashboard

    | Severity | Count | Confirmed | Likely | Possible | Informational |
    |----------|-------|-----------|--------|----------|---------------|
    | Critical |       |           |        |          |               |
    | High     |       |           |        |          |               |
    | Medium   |       |           |        |          |               |
    | Low      |       |           |        |          |               |
    | Info     |       |           |        |          |               |
    | **Total** |     |           |        |          |               |

    **Exploit Chains Identified:** [count]

    ---

    ## Critical & High Findings

    [Full exploit scenarios from Phase 7, ordered by CVSS score descending]
    [Use the finding format from assets/templates/finding.md]

    ---

    ## Medium Findings

    [Full exploit scenarios, CVSS ordered]

    ---

    ## Low & Informational Findings

    [Brief descriptions with file references — no full PoC required]

    | ID | Title | Severity | CWE | File:Line | Description |
    |----|-------|----------|-----|-----------|-------------|

    ---

    ## Exploit Chains

    [Full chain descriptions from Phase 7]
    [Use the chain format from assets/templates/finding.md]

    ---

    ## Root Cause Analysis

    Group findings by underlying root cause. A single root cause may explain multiple findings.

    | Root Cause | Affected Findings | Systemic Fix |
    |-----------|-------------------|-------------|

    [For each root cause, explain:]
    1. What the systemic issue is
    2. Which findings it produces
    3. A single fix that addresses all of them

    ---

    ## ATT&CK Tactic Coverage

    Map all findings to MITRE ATT&CK Enterprise tactics to visualize kill chain exposure and identify blind spots. Only include tactics relevant to the project's architecture (e.g., skip Lateral Movement for a single-service app).

    | Tactic | ID | Findings | Coverage |
    |--------|----|----------|----------|
    | Initial Access | TA0001 | [finding IDs or "—"] | [Covered / Gap / N/A] |
    | Execution | TA0002 | | |
    | Persistence | TA0003 | | |
    | Privilege Escalation | TA0004 | | |
    | Defense Evasion | TA0005 | | |
    | Credential Access | TA0006 | | |
    | Discovery | TA0007 | | |
    | Collection | TA0009 | | |
    | Exfiltration | TA0010 | | |
    | Impact | TA0040 | | |

    **Coverage Gaps:** List tactics that are architecturally relevant but produced no findings — these are either well-defended (note why) or blind spots that warrant follow-up analysis.

    **Kill Chain Patterns:** Note if findings cluster in a particular phase (e.g., many Initial Access findings but no Credential Access findings may indicate testing didn't reach deeper attack stages).

    ---

    ## Remediation Roadmap

    ### Quick Wins (ROI 4-5, Exploitability 4-5)

    Findings where a small fix eliminates a highly exploitable risk. Do these first regardless of severity tier.

    | Finding | Fix | Effort | ROI | Exploitability |
    |---------|-----|--------|-----|----------------|

    ### Immediate (fix before next deploy)
    - [ ] [Finding ID] — [One-line fix description] — Effort: [hours] — ROI: [1-5] — Exploitability: [1-5]

    ### Short-term (fix within 1 week)
    - [ ] [Finding ID] — [One-line fix description] — Effort: [hours/days] — ROI: [1-5] — Exploitability: [1-5]

    ### Medium-term (fix within 1 month)
    - [ ] [Finding ID] — [One-line fix description] — Effort: [days] — ROI: [1-5] — Exploitability: [1-5]

    ### Backlog (track and plan)
    - [ ] [Finding ID] — [One-line fix description] — Effort: [days/weeks] — ROI: [1-5] — Exploitability: [1-5]

    ---

    ## Comparison with Previous Security Work

    [Cross-reference with findings from recon step-10-security-work.md]

    | Previous Fix | Status | Variants Found | Notes |
    |-------------|--------|---------------|-------|

    - What was already fixed and remains secure
    - What was fixed but has remaining variants
    - What is entirely new

    ---

    ## Positive Security Observations

    [Acknowledge security measures that are well-implemented]

    | Security Measure | Implementation | Assessment |
    |-----------------|---------------|-----------|

    ---

    ## Methodology Notes

    | Phase | Agents | Duration | Findings |
    |-------|--------|----------|----------|
    | Phase 0: Recon | 1 | | |
    | Phase 1: Attack Surface | up to 4 | | |
    | Phase 2: Git History | up to 4 | | |
    | Phase 3: Business Logic | up to 4 | | |
    | Phase 4: Data Flow | variable | | |
    | Phase 5: Dependencies | up to 2 | | |
    | Phase 6: Configuration | up to 4 | | |
    | Phase 7: Exploit Dev | 1 | | |
    | Phase 8: Report | 1 | | |
    | Phase 9: Fix Plan | 1 | | |

    **ATT&CK Coverage:** See the ATT&CK Tactic Coverage section above for full kill chain mapping.

    **Limitations:**
    - [Areas not covered and why]
    - [Scope exclusions]
    - [Tool limitations]

    **Recon Index:** `{RUN_DIR}/recon/index.md`

    ---

    ## Finding Validation (Critic Review)

    | Original Findings | Confirmed | Downgraded | Removed | Upgraded |
    |-------------------|-----------|------------|---------|----------|
    | [count] | [count] | [count] | [count] | [count] |

    **Key Critic Observations:**
    - [Notable false positive caught]
    - [Notable upgrade with reasoning]
