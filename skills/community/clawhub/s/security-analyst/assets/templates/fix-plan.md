# Fix Plan Template

This template is used by the fix-planner agent to produce an implementation plan from the security analysis report. Output to `{REPORTS_DIR}/fix-plan.md`.

---

    # Security Fix Implementation Plan

    **Source Report:** {REPORT_PATH}
    **Generated:** {ISO_TIMESTAMP}
    **Total Findings:** {TOTAL_COUNT} ({CRITICAL_COUNT} Critical, {HIGH_COUNT} High, {MEDIUM_COUNT} Medium, {LOW_COUNT} Low)
    **Estimated Total Effort:** {TOTAL_EFFORT}

    ---

    ## Quick Wins (do first)

    Findings with Remediation ROI >= 4 AND Exploitability >= 4. These are high-value, low-effort fixes.

    ### Task 1: [FINDING-ID] — [Title]

    **Priority:** Quick Win (ROI: [score], Exploitability: [score])
    **Severity:** [severity] | **CVSS:** [score] | **ATT&CK:** [technique]
    **Files to modify:**
    - `[file:line]` — [what to change]

    **Fix:**
    ```[language]
    // concrete fix code from the report
    ```

    **Regression test:**
    ```[language]
    // test code from the report
    ```

    **Estimated effort:** [hours]
    **Commit message:** `fix(security): [FINDING-ID] — [one-line description]`

    ---

    ## Immediate (fix before next deploy)

    ### Task N: [FINDING-ID] — [Title]
    (same structure as Quick Wins tasks)

    ---

    ## Short-term (within 1 week)

    ### Task N: [FINDING-ID] — [Title]
    (same structure)

    ---

    ## Medium-term (within 1 month)

    ### Task N: [FINDING-ID] — [Title]
    (same structure)

    ---

    ## Backlog (track and plan)

    ### Task N: [FINDING-ID] — [Title]
    (same structure, may omit regression test for Low/Info)

    ---

    ## Root Cause Fixes

    These systemic fixes address multiple findings at once. Implementing these may resolve several individual tasks above.

    ### RC-1: [Root Cause Name]

    **Addresses findings:** [FINDING-A], [FINDING-B], [FINDING-C]
    **From Root Cause Analysis:** [description of the systemic issue]

    **Systemic fix:**
    ```[language]
    // concrete fix code
    ```

    **Files to modify:**
    - `[file:line]` — [what to change]

    **Estimated effort:** [days]
    **Commit message:** `fix(security): address [root cause] — resolves [FINDING-A], [FINDING-B], [FINDING-C]`

    ---

    ## Implementation Notes

    - Fix tasks are numbered sequentially across all priority tiers for easy reference
    - If a root cause fix resolves individual tasks, mark those tasks as "Resolved by RC-N" and skip them
    - Run the project's test suite after each fix to catch regressions: `npm test`
    - Follow project code style from CLAUDE.md (no eslint-disable comments, double quotes, 2-space indentation)
