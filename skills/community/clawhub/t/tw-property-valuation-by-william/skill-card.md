## Description: <br>
Professional property valuation for Taiwan real estate using market comparison and floor area pricing, with adjustments for location, floor level, building age, parking space deduction, and property type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsaitepiao-alt](https://clawhub.ai/user/tsaitepiao-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, real estate professionals, and agents use this skill to estimate Taiwan residential property value, compare similar transactions, prepare valuation reports, and check whether a listing price is reasonable. <br>

### Deployment Geography for Use: <br>
Taiwan <br>

## Known Risks and Mitigations: <br>
Risk: The local Python script processes property data and writes a report to a path chosen by the user. <br>
Mitigation: Run it in a controlled workspace, review the input JSON and output path, and avoid pointing the output at important existing files. <br>
Risk: The optional usage analytics command records skill usage through the platform analytics script. <br>
Mitigation: Treat analytics as optional and run it only if usage recording is acceptable. <br>
Risk: Property valuation output can be misleading when comparable transactions, local conditions, or special risks are incomplete. <br>
Mitigation: Review the generated report against current comparable sales and use a qualified real estate professional or appraiser for financial decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tsaitepiao-alt/skills/tw-property-valuation-by-william) <br>
- [Valuation Report Template](assets/valuation-report.md) <br>
- [價格調整因子](references/adjustment-factors.md) <br>
- [車位拆算方法](references/parking-deduction.md) <br>
- [各縣市行情基準與區域調整](references/regional-multipliers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown report generated from JSON property input and supporting guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; writes the valuation report to the user-provided output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
