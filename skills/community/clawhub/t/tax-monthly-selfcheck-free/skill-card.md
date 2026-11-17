## Description:

A local deterministic self-check skill for segmented Chinese tax reconciliation materials, covering VAT input/output and tax burden checks, VAT surtax checks, and corporate income tax prepayment checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting staff use this skill during monthly or quarterly close to check user-provided Chinese tax reconciliation tables for arithmetic consistency, totals, duplicates, blanks, and missing required material. It is intended as a reproducible reconciliation aid, not tax, audit, filing, or attestation advice.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Inputs may contain sensitive accounting or tax data.

Mitigation: Review and minimize input files before running the skill, handle outputs under the same internal controls as source accounting records, and use the local execution path described by the artifact.

Risk: Reconciliation output could be mistaken for tax, audit, filing, or attestation advice.

Mitigation: Treat the output as deterministic arithmetic and consistency checks only, and have qualified finance or tax reviewers verify conclusions before filing or external reliance.

Risk: The free version omits some checks and may return no conclusion when required material is missing.

Mitigation: Confirm the executed and omitted checks in the output, provide all required table sections and headers, and avoid treating missing findings as proof that the tax position is correct.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/tax-monthly-selfcheck-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON reports with findings, per-check status, summaries, missing-input guidance, and local execution notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with bundled Node.js standard-library checks; no network use or persistence is reported in the security evidence.]

## Skill Version(s):

1.0.47 (source: evidence.json release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
