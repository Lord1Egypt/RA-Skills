## Description: <br>
Ravi gives AI agents real email inboxes, phone numbers, and an encrypted secret store for identity, email, phone, and credential workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raunaksingwi](https://clawhub.ai/user/raunaksingwi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use Ravi to provision and use an agent identity, read email or SMS, handle login and 2FA workflows, send messages, manage contacts, and store passwords or API secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ravi workflows can expose sensitive identity, inbox, phone, password, and secret data to delegated agent actions. <br>
Mitigation: Use the skill only when that delegated access is intended, keep user approval in the loop for sensitive operations, and avoid using it for unrelated tasks. <br>
Risk: The artifact tells agents to email feedback after every Ravi workflow, which can disclose sensitive workflow details. <br>
Mitigation: Do not send automatic feedback emails; require explicit user approval and omit OTPs, passwords, API keys, secret names or values, account identifiers, inbox contents, phone numbers, contacts, and login details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raunaksingwi/ravi) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational cautions for identity, inbox, phone, password, and secret workflows.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
