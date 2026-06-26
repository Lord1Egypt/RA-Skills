## Description: <br>
个税汇算清缴助手。支持年终奖与期权双重单独/合并计税决策优化，智能分析多雇主重复起征点与税率跳档，生成个税 APP 申报实操指南。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afeicn](https://clawhub.ai/user/afeicn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External taxpayers and tax advisors use this skill to compare Chinese annual tax settlement strategies for salary, labor income, annual bonuses, options, deductions, prepaid tax, and duplicated exemptions. The agent runs a local calculator and produces a filing recommendation, comparison table, diagnostics, and individual income tax app filing steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive tax data and screenshots from the individual income tax app. <br>
Mitigation: Enter only the minimum required numbers manually where possible, and redact names, ID numbers, employer identifiers, addresses, QR codes, account details, and unrelated records before sharing screenshots. <br>
Risk: Tax filing guidance can affect refund or payment decisions. <br>
Mitigation: Review the calculator inputs and generated filing recommendation before submission, and confirm the final figures in the official tax app or with a qualified tax professional when the case is material or ambiguous. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/afeicn/tax-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with JSON-backed calculations and inline shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a best filing strategy, four-scenario tax comparison, diagnostics, deduction effect analysis, and app filing steps.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
