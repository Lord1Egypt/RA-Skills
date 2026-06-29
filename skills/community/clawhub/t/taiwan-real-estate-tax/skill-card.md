## Description: <br>
Calculates and helps plan Taiwan real estate taxes for property sales, purchases, gifts, inheritance, and ongoing ownership. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsaitepiao-alt](https://clawhub.ai/user/tsaitepiao-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, real estate professionals, and agents use this skill to estimate Taiwan real estate tax liability, compare self-use, rental, business, sale, gift, and inheritance scenarios, and generate tax estimate reports. <br>

### Deployment Geography for Use: <br>
Taiwan <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to run a usage analytics command without clear consent or data-handling details. <br>
Mitigation: Run the tax calculator locally, and do not run analytics commands unless the publisher explains what is recorded and the user explicitly consents. <br>
Risk: Tax calculations are estimates and may not match official determinations. <br>
Mitigation: Verify outputs against official Taiwan tax guidance or a qualified tax professional before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tsaitepiao-alt/taiwan-real-estate-tax) <br>
- [Tax types and formulas](references/tax-types.md) <br>
- [Tax rates](references/rates.md) <br>
- [Scenario examples](references/scenarios.md) <br>
- [Tax-saving guidance](references/tax-saving.md) <br>
- [Tax report template](assets/tax-report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated Markdown tax reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; tax results are estimates and should be checked against official guidance or a qualified professional.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
