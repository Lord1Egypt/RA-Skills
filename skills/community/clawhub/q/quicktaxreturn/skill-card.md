## Description: <br>
QuickTaxReturn is a conversational federal tax preparation assistant for tax year 2025 that interviews taxpayers, collects document data, performs step-by-step calculations, and routes users to DIY filing, CPA handoff, or advisory support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vajih](https://clawhub.ai/user/vajih) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External taxpayers use this skill to organize and calculate in-scope 2025 U.S. federal tax returns, with conservative escalation for complex situations such as self-employment, investment sales, multi-state filing, rental income, K-1s, or foreign income. It can also prepare a structured CPA intake package when the user's return is outside the skill's scope or the user wants professional filing support. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to discuss highly sensitive tax information in chat, including identity, income, dependent, and filing details. <br>
Mitigation: Avoid entering full SSNs, bank account numbers, IRS IP PINs, or prior-year AGI unless truly necessary, and redact sensitive fields before sharing any generated intake package. <br>
Risk: The artifact claims privacy protections, but the security evidence says privacy and CPA handoff safeguards are under-scoped. <br>
Mitigation: Use the skill only in a chat environment acceptable for tax information and transfer CPA handoff materials through a secure channel outside the chat. <br>
Risk: Incorrect tax calculations or unsupported scenarios could affect filing accuracy. <br>
Mitigation: Review all calculated values against original source documents and escalate complex returns to a licensed CPA or enrolled agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vajih/quicktaxreturn) <br>
- [Publisher profile](https://clawhub.ai/user/vajih) <br>
- [QuickTaxReturn core behavior](artifact/SKILL.md) <br>
- [QuickTaxReturn tax rules](artifact/tax-rules.md) <br>
- [QuickTaxReturn escalation config](artifact/escalation-config.md) <br>
- [QuickTaxReturn CPA intake template](artifact/intake-template.md) <br>
- [IRS Free File](https://www.irs.gov/freefile) <br>
- [IRS Direct File](https://directfile.irs.gov) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Conversational text and structured Markdown summaries or CPA intake packages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handles federal-only tax preparation for tax year 2025 and escalates out-of-scope situations to CPA handoff.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
