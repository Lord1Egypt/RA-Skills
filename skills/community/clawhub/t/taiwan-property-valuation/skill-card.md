## Description: <br>
Professional property valuation for Taiwan real estate using market comparison and floor area pricing, with adjustments for location, floor level, building age, parking space deduction, and property type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsaitepiao-alt](https://clawhub.ai/user/tsaitepiao-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and real estate practitioners use this skill to estimate Taiwan residential property value before buying or selling, compare similar transactions, prepare client valuation reports, and check whether a listing price is reasonable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires property details in a local JSON input file and writes a valuation report to a chosen path. <br>
Mitigation: Use only property details you are comfortable processing locally, review the input JSON before execution, and choose an output path that is appropriate for the report contents. <br>
Risk: The artifact includes an optional usage analytics command. <br>
Mitigation: Do not let an agent run analytics automatically; execute it only when the user intentionally wants usage recorded by the external ClawHub/OpenClaw analytics mechanism. <br>
Risk: The valuation is an estimate and can be misleading if comparable transactions, special property risks, or local market conditions are incomplete. <br>
Mitigation: Treat generated prices as decision support, compare against multiple recent transactions, and seek a qualified property valuation professional for precise valuation decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tsaitepiao-alt/skills/taiwan-property-valuation) <br>
- [Valuation Report Template](assets/valuation-report.md) <br>
- [價格調整因子](references/adjustment-factors.md) <br>
- [車位拆算方法](references/parking-deduction.md) <br>
- [各縣市行情基準與區域調整](references/regional-multipliers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Shell commands, Guidance] <br>
**Output Format:** [Markdown valuation report with command-line execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a local JSON property input file; writes the valuation report to the user-selected output path.] <br>

## Skill Version(s): <br>
2026.6.26 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
