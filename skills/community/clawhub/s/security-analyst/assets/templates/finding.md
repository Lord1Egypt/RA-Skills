# Finding Report Format — Level of Detail (LOD)

Findings are written as **atomic files** to `{FINDINGS_DIR}/`. Each file contains the full LOD-2 finding. Agents return LOD-0 summaries to the orchestrator. The orchestrator builds an index with LOD-0 and LOD-1 views.

## LOD-0: One-Line Summary (returned to orchestrator)

Format: `| [FINDING-ID] | [Severity] | [One-sentence description] |`

Example: `| HTTP-001 | High | Unauthenticated webhook endpoint allows attacker to enqueue arbitrary processing tasks |`

## LOD-1: Finding Brief (for index file)

    ### [FINDING-ID]: [Title]
    **Severity:** [S] | **CVSS:** [Score] | **CWE:** [ID] | **ATT&CK:** [TID] | **File:** [path:line]
    [One-paragraph description of the vulnerability and its impact]

## LOD-2: Full Finding (atomic file on disk)

Every Medium+ finding MUST use this format. Low and Informational findings can use an abbreviated version (skip PoC and Regression Test sections).

---

## Individual Finding

    ### [FINDING-ID]: [Title]

    **Severity:** Critical / High / Medium / Low / Informational
    **CVSS 3.1:** [Score] ([Vector String])
    **CWE:** [CWE-ID] — [CWE Name]
    **ATT&CK:** [Technique ID] — [Technique Name] (e.g., T1190 — Exploit Public-Facing Application)
    **Confidence:** Confirmed / Likely / Possible / Informational

    **Affected Component:** [File:Line or module name]
    **Attacker Profile:** [Which attacker from `step-05-crown-jewels.md`'s Attacker Profiles table]
    **Preconditions:** [What must be true for this attack to work]

    #### Exploit Scoring

    | Dimension | Score (1-5) | Rationale |
    |-----------|-------------|-----------|
    | Exploitability | | 1=theoretical chain, 5=single curl command |
    | Blast Radius | | 1=single user with specific config, 5=all users |
    | Detectability | | 1=leaves obvious audit trail, 5=invisible to monitoring |
    | Remediation ROI | | 1=massive refactor for marginal gain, 5=one-line fix eliminates critical risk |

    #### Attack Steps
    1. [Exact step with specific file:line references from the recon step files]
    2. [...]
    3. [...]

    #### Proof of Concept
    ```[language]
    // Concrete exploit code, curl command, or crafted payload
    // Must be specific enough to reproduce
    ```

    #### Impact
    - **What the attacker gains:** [...]
    - **Blast radius:** [How many users/resources affected]
    - **Data compromised:** [Specific data types]

    #### Remediation
    ```[language]
    // Concrete fix code — not a description, actual code
    ```

    #### Regression Test
    ```[language]
    // Test that prevents reintroduction of this vulnerability
    ```

    #### References
    - [Relevant CWE page]
    - [Related findings in this report]

---

## Exploit Chain

When multiple findings combine into a more severe attack:

    ### CHAIN-[ID]: [Chain Title]

    **Combined Severity:** [Higher than individual findings]
    **CVSS 3.1:** [Combined score]
    **ATT&CK Chain:** [T1190] → [T1078] → [T1530]
    **Findings Combined:** [FINDING-A] + [FINDING-B] + [FINDING-C]

    #### Chain Description
    1. [FINDING-A] allows attacker to [...]
    2. This enables [FINDING-B] because [...]
    3. Combined with [FINDING-C], the attacker can [...]

    #### Combined Impact
    [Why the chain is worse than individual findings]

    #### Combined Remediation
    [Which fix breaks the chain most effectively]

---

## Confidence Levels

| Level | Definition | Required Evidence |
|-------|-----------|------------------|
| **Confirmed** | Verified with working PoC | Reproducible exploit code or payload |
| **Likely** | Strong evidence, high probability | Code path analysis showing exploitable flow |
| **Possible** | Theoretical, needs specific conditions | Identified pattern but unverified exploitability |
| **Informational** | Best practice improvement | No direct exploit, defense-in-depth recommendation |

---

## Finding ID Convention

Use the format: `[CATEGORY]-[NUMBER]`

Examples:
- `HTTP-001` — HTTP entry point, finding 1
- `INJ-003` — Injection variant, finding 3
- `RACE-001` — Race condition, finding 1
- `CFG-002` — Configuration, finding 2
