---
description: "Map security findings to a compliance framework (SOC 2, ISO 27001, PCI DSS, HIPAA, GDPR)."
model: opus
---

# Security Analyst — Compliance Mapping

Map findings from an existing security analysis run to a compliance framework.

**Arguments:**
- `[framework]` — one of: `soc2`, `iso27001`, `pci-dss`, `hipaa`, `gdpr`
- `[run-dir]` — optional run directory path (defaults to latest)

**Read `references/constants.md` for all directory paths, filenames, and placeholder variables.**

**Execution:**

1. If no `[run-dir]` is specified, auto-detect the latest run in `docs/security/runs/`
2. Validate the run directory contains `reports/final.md` and `findings/index.md`
3. Read the compliance report template: `{TEMPLATES_DIR}/compliance-report.md`
4. Read the run's findings (LOD-1 from index, selectively LOD-2 for detail):
   - `{RUN_DIR}/findings/index.md`
   - `{REPORTS_DIR}/final.md`
   - `{REPORTS_DIR}/fix-plan.md` (for remediation effort estimates)
   - `{REPORTS_DIR}/sbom.md` (for dependency and license data)
5. Read the recon data for implementation state:
   - `{RECON_DIR}/index.md`
   - Selectively: `step-06-auth.md`, `step-08-secrets.md`, `step-11-config.md`
6. Map each finding to the relevant controls in the selected framework
7. Assess each control as Pass / Partial / Fail / N/A based on findings and implementation
8. Write the compliance report to `{REPORTS_DIR}/compliance.md`

**Output files:**
- `{REPORTS_DIR}/compliance.md` (Compliance mapping report)

**STOP after presenting the compliance summary and score. Wait for the user to ask a follow-up question.**
