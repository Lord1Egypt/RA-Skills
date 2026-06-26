## Description: <br>
Income Lab 收入实验室 helps users systematically test legal earning methods, record experiment data, analyze results, and refine income strategies over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and external users use this skill to plan income experiments, compare possible earning methods, track time and income, and produce periodic retrospectives that guide what to continue, adjust, or stop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports external SkillPay billing behavior that can attempt a 0.01 USDT charge for the environment-selected user when the payment path runs. <br>
Mitigation: Review before installing, confirm the intended SKILLPAY_USER_ID, and require explicit user consent before any billing path is executed. <br>
Risk: The security guidance flags a hardcoded billing API key and recommends separating balance checks from charge execution. <br>
Mitigation: Remove hardcoded credentials, rely on environment-scoped secrets, and keep balance checks separate from charge requests. <br>
Risk: Income notes and experiment records may contain sensitive personal financial details stored locally under ~/.income-lab. <br>
Mitigation: Avoid recording sensitive financial notes unless local storage is acceptable, and protect or delete the local data directory according to the user's privacy needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenmeng/shenmeng-income-lab) <br>
- [income-methods.md](references/income-methods.md) <br>
- [retrospective-framework.md](references/retrospective-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON/CSV files produced by helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts store experiment and report data locally under ~/.income-lab and can export CSV reports.] <br>

## Skill Version(s): <br>
2025.4.15 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
