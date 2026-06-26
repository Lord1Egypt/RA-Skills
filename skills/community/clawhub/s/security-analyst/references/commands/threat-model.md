---
description: "Generate a threat model document — maps trust boundaries, crown jewels, attacker profiles, and attack surface."
model: opus
---

# Security Analyst — Threat Model

Generate a threat model document from the codebase reconnaissance. This is equivalent to `/security-analyst:recon` but with additional threat modeling analysis.

**Read `references/constants.md` for all directory paths, filenames, and placeholder variables.**

## What This Produces

Beyond the standard recon, the threat model adds:

1. **STRIDE Analysis**: For each trust boundary, analyze:
   - **S**poofing — Can an attacker impersonate a legitimate entity?
   - **T**ampering — Can data be modified in transit or at rest?
   - **R**epudiation — Can actions be performed without audit trail?
   - **I**nformation Disclosure — Can sensitive data leak?
   - **D**enial of Service — Can availability be impacted?
   - **E**levation of Privilege — Can access controls be bypassed?

2. **Attack Trees**: For each crown jewel, construct attack trees:
   - Root: "Compromise [crown jewel]"
   - Branches: different attack paths
   - Leaves: specific techniques
   - Annotations: difficulty, detectability, prerequisites

3. **Risk Matrix**: Map each threat to likelihood x impact

## Execution

1. Run the recon agent (same as `/security-analyst:recon`)
2. Read the recon index
3. Spawn the threat model agent via Task tool:
   - Read `references/prompts/threat-model-agent.md` for the agent prompt
   - Read `assets/templates/finding.md` for the finding format
   - Read `assets/templates/agent-common.md` for shared output instructions
   - Replace `{RECON_INDEX_PATH}` with the recon index path
   - Replace `{RECON_DIR}` with the recon directory path
   - Replace `{OUTPUT_PATH}` with `{REPORTS_DIR}/threat-model.md`
   - Replace `{FINDINGS_DIR}` with `{RUN_DIR}/findings`
   - Replace `{FINDING_TEMPLATE_PATH}`, `{PRIOR_FINDINGS_SUMMARY}`, `{INCIDENTAL_FINDINGS_SECTION}` per standard orchestrator pattern
   - Append agent-common.md output instructions to the prompt
4. Collect the agent's LOD-0 summary and any findings written to `{FINDINGS_DIR}/`

## Output

- `{RUN_DIR}/recon/` — Recon index + atomic step files
- `{REPORTS_DIR}/threat-model.md` — Full threat model document

**STOP after presenting the threat model summary. Do not continue to vulnerability analysis phases or take any further actions. Wait for the user to ask a follow-up question.**

## Use Cases

- Starting point for a security program
- Input for security architecture review
- Compliance documentation (SOC 2, ISO 27001)
- Planning a full penetration test
- Onboarding new security team members
