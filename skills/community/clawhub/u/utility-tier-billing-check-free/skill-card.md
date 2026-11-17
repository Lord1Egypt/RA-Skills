## Description:

Checks utility time-of-use billing worksheets by recalculating line items, totals, duplicate items, and required fields, with every finding tied to source line numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and finance operators use this skill to check Chinese-language commercial utility billing tables for arithmetic mismatches before relying on a bill. It helps review supplied worksheet fields, not official tariff schedules, meter readings, or legal billing correctness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The arithmetic result could be mistaken for verification of official tariffs, meter readings, or legal billing correctness.

Mitigation: Treat outputs as arithmetic checks over the supplied worksheet fields and confirm tariffs, meter data, and billing obligations with authoritative sources.

Risk: Incomplete or poorly structured worksheet material can prevent meaningful checking.

Mitigation: Provide the full billing table with headers and review any missing-input messages before drawing conclusions.

Risk: The free release omits several checks that are listed as not included.

Mitigation: Review the executed-check and checks-not-run lists in the output before relying on coverage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/utility-tier-billing-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable text or JSON containing findings, source line numbers, summary totals, missing-input messages, executed checks, and checks not run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided worksheet text or JSON; material must include recognizable billing-table headers.]

## Skill Version(s):

1.0.30 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
