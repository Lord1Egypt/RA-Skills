## Description: <br>
RiskShield 案件审批自动化，使用 Playwright 浏览器自动化完成审批，支持 Pass 和 Refuse 两种操作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haoleizhang](https://clawhub.ai/user/haoleizhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Risk operations staff or authorized automation operators use this skill to run case-specific RiskShield approval workflows from the command line. It searches a case, verifies that it is still pending, applies either a Pass decision with a credit amount or a Refuse decision with a refusal code, submits the form, and checks that the case closes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships reusable credentials and a saved token. <br>
Mitigation: Do not install it as-is; rotate exposed credentials and tokens, remove token.json, and use securely injected per-user least-privilege credentials. <br>
Risk: Debug, extraction, and API scripts can access or modify sensitive case data. <br>
Mitigation: Remove debug and extraction scripts before deployment, restrict execution to explicitly requested cases, and keep approval activity logged. <br>
Risk: Automated approval actions can make business-impacting changes. <br>
Mitigation: Run only in an owned RiskShield environment with authorized operators, auditable approvals, and reversible workflows where possible. <br>
Risk: Security guidance calls out TLS bypasses. <br>
Mitigation: Disable TLS bypasses and require standard certificate validation in production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haoleizhang/riskshield) <br>
- [RiskShield system URL](https://riskshield.dcsuat.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance, Code] <br>
**Output Format:** [Markdown instructions with inline shell commands and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses case number, approval action, optional refusal code, and optional credit amount as command-line inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
