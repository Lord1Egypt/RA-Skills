## Description: <br>
（司库系统）API 全生命周期管理智能 Skill <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infochen-sub](https://clawhub.ai/user/infochen-sub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API integrators use this skill to inspect PSBC treasury API definitions, validate request and response payloads, generate curl or Python examples, and mock banking workflow responses for test scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers high-impact banking and treasury operations, including payment, payroll, balance, transaction, and token-related API workflows. <br>
Mitigation: Use it only in sandbox or approved test environments unless explicit approval gates, redaction, and environment separation are in place. <br>
Risk: Production credentials, certificates, signatures, passwordless token URLs, account identifiers, payroll files, or live payment payloads could expose sensitive financial operations or data. <br>
Mitigation: Do not provide production secrets or live financial payloads; use synthetic data and keep credentials outside prompts and artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/infochen-sub/psbc-treasury-api) <br>
- [Skill README](artifact/README.md) <br>
- [API definitions](artifact/apis.json) <br>
- [Response code dictionary](artifact/response-codes.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and curl or Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local JSON API definitions and example scripts; live API calls require user-supplied credentials and cryptographic integration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact SKILL.md lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
