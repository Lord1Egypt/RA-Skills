## Description:

Provides Taiwan real estate valuation support using market comparison, floor-area pricing, and adjustments for location, floor level, building age, parking, property type, and special risk factors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsaitepiao-alt](https://clawhub.ai/user/tsaitepiao-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, real estate professionals, and property analysts use this skill to estimate Taiwan residential property values, compare similar transactions, and prepare valuation reports for buying, selling, or client review.

### Deployment Geography for Use:

Taiwan

## Known Risks and Mitigations:

Risk: The skill asks agents to run an unbundled analytics command from a relative path after use.

Mitigation: Do not allow the analytics command unless skills/analytics.py has been verified as a trusted platform script and the recorded data is understood.

Risk: Automated property valuations may be inaccurate or misleading if inputs, market comparables, or local adjustment assumptions are incomplete.

Mitigation: Review outputs against current transaction data and obtain qualified professional valuation support for decisions that require precision.

## Reference(s):

- [Valuation Report Template](assets/valuation-report.md)
- [Price Adjustment Factors](references/adjustment-factors.md)
- [Parking Deduction Method](references/parking-deduction.md)
- [Regional Multipliers](references/regional-multipliers.md)
- [ClawHub Skill Page](https://clawhub.ai/tsaitepiao-alt/skills/tw-property-valuation-by-william)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown valuation report with terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and writes the valuation report to the output path supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
