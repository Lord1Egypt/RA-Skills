---
description: "Complete 9-phase offensive security analysis. No prompts — runs everything."
model: opus
---

# Security Analyst — Full Analysis

Run the complete analysis with no interactive prompts.

**Settings:**
- Scope: Full — all phases, all attack surfaces
- Output: Files to `docs/security/runs/{YYYY-MM-DD-HHMMSS}/`
- Agent skipping: Only if recon determines irrelevance (e.g., no frontend)

**Execution:** Follow the orchestration flow in `references/commands/security-analyst.md` with these settings.

**Output files:** See `references/commands/security-analyst.md` Step 9 for the full file list.

**Expected duration:** 23+ agents across 6 execution groups. Significant processing time.
