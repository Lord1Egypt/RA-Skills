## Description:

Provides Taiwan real estate valuation guidance and a Python calculator using market comparison, floor-area pricing, 實價登錄 comparisons, and adjustments for location, floor level, building age, parking, and property type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsaitepiao-alt](https://clawhub.ai/user/tsaitepiao-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External property professionals, buyers, sellers, and agents use this skill to prepare rough Taiwan residential valuation reports, compare nearby transaction data, and check listing price reasonableness.

### Deployment Geography for Use:

Taiwan

## Known Risks and Mitigations:

Risk: Generated valuation figures may be mistaken for a certified appraisal.

Mitigation: Treat outputs as rough guidance, compare against multiple recent local transactions, and use a licensed appraiser when a formal valuation is required.

Risk: Client or property details could be exposed through feedback channels or usage analytics workflows.

Mitigation: Avoid including sensitive client or property details in feedback, comments, surveys, or other non-essential channels.

Risk: The local report generator reads an input JSON path and writes to a user-specified output path.

Mitigation: Use explicit input and output paths and review the generated Markdown before sharing it externally.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tsaitepiao-alt/skills/taiwan-property-valuation-v2)
- [價格調整因子](references/adjustment-factors.md)
- [車位拆算方法](references/parking-deduction.md)
- [各縣市行情基準與區域調整](references/regional-multipliers.md)
- [不動產估值分析報告](assets/valuation-report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown report with valuation figures, comparison notes, and Python command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and writes the valuation report to a user-specified output path.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
