## Description: <br>
Interface with the SanctifAI Human-in-the-Loop API to create tasks, route them to humans, and retrieve structured responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndgates](https://clawhub.ai/user/ndgates) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill when an automated workflow needs human review, data entry, approval, fact verification, or other structured input through SanctifAI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task details, attachments, callback URLs, and invite targets may be shared with SanctifAI and human reviewers. <br>
Mitigation: Avoid secrets, credentials, regulated personal data, and confidential files unless authorized; prefer guild or direct routing for trusted reviewers. <br>
Risk: API keys, generated agent keys, and webhook secrets grant access to SanctifAI account actions. <br>
Mitigation: Protect keys as account credentials, store them securely, rotate compromised keys, and verify webhook signatures. <br>
Risk: Paid tasks and billing invites can spend organization funds or invite the wrong administrator. <br>
Mitigation: Verify billing invite email addresses, spending limits, and task prices before creating paid tasks. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/ndgates/sanctifai) <br>
- [SanctifAI API Quick Start](https://app.sanctifai.com/v1) <br>
- [SanctifAI OpenAPI JSON](https://app.sanctifai.com/v1/openapi.json) <br>
- [SanctifAI OpenAPI YAML](https://app.sanctifai.com/v1/openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON, HTTP, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request bodies, MCP configuration, endpoint references, and webhook verification examples.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
