---
description: "Quick security reconnaissance — maps attack surface without vulnerability analysis."
model: opus
---

# Security Analyst — Reconnaissance Only

Run Phase 0 only. Produces a structured security map without vulnerability analysis.

**Execution:** Follow `security-analyst.md` Steps 1-2 (create run dir, spawn recon agent). Stop after recon completes.

**Output:** `docs/security/runs/{YYYY-MM-DD-HHMMSS}/recon/` (index.md + 14 atomic step files)

**Next steps:** `/security-analyst:full` for complete analysis, `/security-analyst:focused [component]` to target a specific area.

**STOP after presenting the recon index. Do not continue to vulnerability analysis phases. Wait for the user to ask a follow-up question.**
