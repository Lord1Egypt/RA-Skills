## Description:

Provides Taiwan real estate valuation support using market comparison and floor area pricing, with adjustments for location, floor level, building age, parking, and property type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsaitepiao-alt](https://clawhub.ai/user/tsaitepiao-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and property professionals use this skill to estimate Taiwan residential property values before buying, selling, comparing listings, or preparing client-facing valuation reports.

### Deployment Geography for Use:

Taiwan

## Known Risks and Mitigations:

Risk: Property addresses and transaction details may be sensitive when included in local input or report files.

Mitigation: Only provide details suitable for local storage and review generated reports before sharing them.

Risk: The generated valuation is an estimate and may not match a professional appraisal or final transaction price.

Mitigation: Treat results as decision support, compare against recent local transactions, and consult a qualified appraiser for formal valuation needs.

Risk: Optional analytics and feedback commands can record usage statistics.

Mitigation: Review those commands before running them and skip them when usage reporting is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tsaitepiao-alt/skills/taiwan-property-valuation-v1)
- [價格調整因子](references/adjustment-factors.md)
- [車位拆算方法](references/parking-deduction.md)
- [各縣市行情基準與區域調整](references/regional-multipliers.md)
- [不動產估值分析報告](assets/valuation-report.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown report with valuation tables and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local JSON property inputs and writes a local valuation report file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
