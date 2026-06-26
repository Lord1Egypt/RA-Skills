# Delta Report Template

The orchestrator produces this report by comparing two security analysis runs to highlight what changed. Output to `{RUN_DIR_B}/reports/delta.md`.

---

    # Security Analysis Delta Report

    **Date:** {ISO_TIMESTAMP}
    **Baseline Run (A):** {RUN_DIR_A} ([date of run A])
    **Current Run (B):** {RUN_DIR_B} ([date of run B])
    **Days Between Runs:** [count]

    ---

    ## Summary

    | Metric | Run A | Run B | Delta |
    |--------|-------|-------|-------|
    | Total Findings | | | +N / -N |
    | Critical | | | |
    | High | | | |
    | Medium | | | |
    | Low | | | |
    | Informational | | | |
    | Exploit Chains | | | |
    | Dependencies | | | |
    | Known CVEs | | | |

    **Overall Trend:** [Improving / Stable / Degrading]

    ---

    ## New Findings (in B but not in A)

    Findings that appear in the current run but were not present in the baseline.

    | Finding ID | Severity | CVSS | Title | File:Line | Likely Cause |
    |-----------|----------|------|-------|-----------|-------------|

    **Analysis:** [Are new findings from new code, new dependencies, deeper analysis, or methodology changes?]

    ---

    ## Resolved Findings (in A but not in B)

    Findings from the baseline that no longer appear in the current run.

    | Finding ID (A) | Severity | Title | Resolution |
    |---------------|----------|-------|-----------|

    Resolution categories: Fixed (code change), Mitigated (compensating control), Removed (feature deleted), False Positive (critic caught), Methodology Change (analysis scope changed).

    ---

    ## Persistent Findings (in both A and B)

    Findings present in both runs. Note severity changes.

    | Finding ID | Severity A → B | CVSS A → B | Title | Change Notes |
    |-----------|---------------|-----------|-------|-------------|

    **Stale Findings:** List findings that persisted across runs despite being in the fix plan. These represent remediation failures or deprioritized items.

    ---

    ## Severity Changes

    Findings where severity changed between runs.

    | Finding ID | A Severity | B Severity | Reason |
    |-----------|-----------|-----------|--------|

    ---

    ## Dependency Changes

    | Change Type | Package | A Version | B Version | Security Impact |
    |------------|---------|-----------|-----------|-----------------|
    | Added | | — | | |
    | Removed | | | — | |
    | Upgraded | | | | [CVEs fixed / new CVEs introduced] |
    | Downgraded | | | | [Risk assessment] |

    **New CVEs Since Run A:** [count] — list any new CVEs affecting current dependencies

    ---

    ## Attack Surface Changes

    | Change | Details |
    |--------|---------|
    | New endpoints | [endpoints added since Run A] |
    | Removed endpoints | [endpoints removed since Run A] |
    | New integrations | [external services added] |
    | New file upload points | [upload handlers added] |
    | Auth changes | [auth mechanism changes] |

    ---

    ## Fix Plan Progress

    Cross-reference Run A's fix plan with Run B's findings:

    | Fix Plan Task (A) | Status | Finding Resolved? | Notes |
    |------------------|--------|-------------------|-------|

    **Fix Plan Completion Rate:** [X of Y tasks completed] ([%])

    ---

    ## Recommendations

    ### Regressions to Address Immediately
    1. [New Critical/High findings that appeared since Run A]

    ### Stale Items to Escalate
    1. [Findings that were in Run A's fix plan but remain unresolved]

    ### Positive Trends to Continue
    1. [Categories where security improved]

    ---

    ## Matching Methodology

    Findings are matched between runs using:
    1. **Finding ID** — exact ID match (same vulnerability, same location)
    2. **CWE + File** — same weakness type in the same file (vulnerability may have moved lines)
    3. **CWE + Component** — same weakness type in the same component (file may have been renamed/refactored)

    Unmatched findings in Run A = Resolved. Unmatched findings in Run B = New.
