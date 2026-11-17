## Description:

Professional property valuation for Taiwan real estate using market comparison, floor area pricing, location, floor level, building age, parking deduction, and property type adjustments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsaitepiao-alt](https://clawhub.ai/user/tsaitepiao-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and property professionals can use this skill to estimate Taiwan residential property values before buying, selling, or preparing client valuation reports. It supports comparison against recent transaction data and applies adjustments for parking, building age, floor level, property type, and local market factors.

### Deployment Geography for Use:

Taiwan

## Known Risks and Mitigations:

Risk: The security review flagged a recommendation to run an unbundled local analytics script with unclear privacy and execution boundaries.

Mitigation: Do not automatically run analytics commands unless the platform-provided script, collected data, and storage destination are known and trusted.

Risk: Generated Markdown reports may contain property data supplied by another party.

Mitigation: Treat generated reports as untrusted content and review them before sharing, storing, or using them for decisions.

## Reference(s):

- [Adjustment Factors](references/adjustment-factors.md)
- [Parking Deduction](references/parking-deduction.md)
- [Regional Multipliers](references/regional-multipliers.md)
- [ClawHub Skill Page](https://clawhub.ai/tsaitepiao-alt/skills/tw-property-valuation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown valuation report with supporting shell commands and JSON input guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces estimated total price, unit price, adjustment factors, comparable transaction analysis, and valuation range guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
