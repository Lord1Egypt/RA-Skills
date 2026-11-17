## Description:

Supports Korean startup and business-registration guidance by routing questions across nine intents for startup checklists, business registration, permits, funding programs, tax setup, entity comparison, costs, and beginner guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sw326](https://clawhub.ai/user/sw326)

### License/Terms of Use:


## Use Case:

External users and agents supporting Korean founders use this skill to produce informational startup, registration, permit, funding, tax, entity-selection, and startup-cost guidance. The skill is intended for Korean business contexts and directs users to verify legal, tax, funding, and permit details with official agencies or qualified professionals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented shell commands may pass user-provided industry names, law names, or business registration numbers without validation.

Mitigation: Use typed tools or sanitized argument arrays instead of shell interpolation, and validate user-provided inputs before invoking supporting scripts.

Risk: Legal, tax, funding, and permit guidance can become outdated or may not match a user's specific jurisdiction, business model, or filing status.

Mitigation: Treat outputs as informational and require confirmation with official Korean agencies or qualified legal, tax, and business professionals before acting.

## Reference(s):

- [Intent Router](artifact/references/intent_router.md)
- [Output Templates](artifact/references/output_templates.md)
- [Source Tiers](artifact/references/source_tiers.md)
- [K-Startup](https://www.k-startup.go.kr)
- [Bizinfo](https://www.bizinfo.go.kr)
- [SME Support Program Integrated Management System](https://www.smes.go.kr)
- [Korean Law Information Center](https://www.law.go.kr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with checklists, tables, short reports, delegation notices, and occasional shell command examples for agent-side data collection.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flash output is always produced and capped at 40 lines; deep-dive output is available on request or for selected intents; every response includes an informational legal and tax disclaimer.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
