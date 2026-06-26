---
description: "Privacy and data protection assessment — PII flows, consent, data subject rights, retention."
model: opus
---

# Security Analyst — Privacy Assessment

Conduct a privacy and data protection assessment covering PII flows, consent mechanisms, data subject rights, and cross-border transfers.

**Read `references/constants.md` for all directory paths, filenames, and placeholder variables.**

**Settings:**
- Scope: the recon stage + targeted privacy analysis
- Output: Files to `docs/security/runs/{YYYY-MM-DD-HHMMSS}/`
- Can be run standalone or as a post-analysis on an existing run

**Execution:** Follow `security-analyst.md` with these modifications:
1. Steps 1-2: Create run directory, run the full recon stage — all 14 steps
2. Step 3: Analyze recon report with privacy focus:
   - Identify PII collection points from `step-03-http.md` and `step-05-crown-jewels.md`
   - Map PII flows from `step-09-data-flows.md`
   - Identify third-party sharing from `step-07-integrations.md`
   - Review encryption and storage from `step-08-secrets.md`
3. Read the privacy report template: `{TEMPLATES_DIR}/privacy-report.md`
4. Spawn a single privacy assessment agent to:
   - Trace all PII data flows end-to-end
   - Identify consent collection mechanisms
   - Check data subject rights implementation (access, erasure, portability)
   - Review data retention policies and deletion mechanisms
   - Assess cross-border data transfers
   - Evaluate privacy-by-design principles
5. Write the privacy report to `{REPORTS_DIR}/privacy.md`
6. Skip all vulnerability analysis groups (1-5) and fix plan

**If run against an existing security run:** Read the existing recon data and findings instead of re-running recon. Enrich the privacy assessment with security findings.

**Output files:**
- `{RUN_DIR}/recon/` (if running standalone)
- `{REPORTS_DIR}/privacy.md` (Privacy assessment report)

**STOP after presenting the privacy assessment summary. Wait for the user to ask a follow-up question.**
