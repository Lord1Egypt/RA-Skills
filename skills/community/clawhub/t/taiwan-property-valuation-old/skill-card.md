## Description:

Provides Taiwan real estate valuation using market comparison and floor-area pricing with adjustments for location, floor level, building age, parking, property type, and comparable transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsaitepiao-alt](https://clawhub.ai/user/tsaitepiao-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and real estate practitioners use this skill to estimate Taiwan residential property value, compare listing or transaction reasonableness, and produce client-facing valuation reports in Traditional Chinese.

### Deployment Geography for Use:

Taiwan

## Known Risks and Mitigations:

Risk: Valuation reports may be mistaken for definitive appraisal advice in high-stakes property decisions.

Mitigation: Treat generated valuations as estimates and consult a licensed appraiser before relying on them for financing, legal, or major transaction decisions.

Risk: The skill includes a disclosed but under-described usage analytics command.

Mitigation: Run analytics logging only when comfortable with local usage logging; it is not required for the valuation workflow.

Risk: Incorrect input or output paths could cause failed runs or misplaced reports.

Mitigation: Use only intended local JSON input files and user-controlled report output paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tsaitepiao-alt/skills/taiwan-property-valuation-old)
- [Valuation report template](assets/valuation-report.md)
- [價格調整因子](references/adjustment-factors.md)
- [車位拆算方法](references/parking-deduction.md)
- [各縣市行情基準與區域調整](references/regional-multipliers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown valuation report and terminal status text generated from JSON property inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; report output is written to a user-specified local path.]

## Skill Version(s):

2026.6.26 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
