---
description: "Generate a Software Bill of Materials — recon + dependency audit, no vulnerability exploitation."
model: opus
---

# Security Analyst — Software Bill of Materials

Generate a compliance-ready SBOM listing all languages, frameworks, dependencies, licenses, and supply chain indicators.

**Read `references/constants.md` for all directory paths, filenames, and placeholder variables.**

**Settings:**
- Scope: the recon stage + Dependency Audit (from the surface stage) only
- Output: Files to `docs/security/runs/{YYYY-MM-DD-HHMMSS}/`
- No attack surface analysis, exploit development, or vulnerability exploitation

**Execution:** Follow `security-analyst.md` with these steps:
1. Steps 1-2: Create run directory, run the full recon stage — all 14 steps
2. Step 3: Analyze recon report (determines package managers, lockfiles)
3. Step 3.5: Plugin detection (needed for dependency audit prompt injection)
4. Spawn **only** the dependency audit agent from the surface stage (`deps-audit` — `references/prompts/dependency-audit.md`)
5. Step 4.5: Assemble the SBOM from recon data + dependency audit output
6. Skip all remaining groups (2-5) and fix plan generation

**Output files:**
- `{RUN_DIR}/recon/index.md` (LOD-0 + LOD-1 recon index)
- `{RUN_DIR}/recon/step-*.md` (14 atomic recon section files)
- `{REPORTS_DIR}/sbom.md` (Software Bill of Materials)

**STOP after presenting the SBOM report summary. Do not continue to vulnerability analysis phases. Wait for the user to ask a follow-up question.**
