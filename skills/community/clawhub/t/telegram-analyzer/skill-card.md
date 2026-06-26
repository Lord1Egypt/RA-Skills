## Description: <br>
Telegram Analyzer helps agents search SaaS contacts, view recent incoming Telegram messages, and update contact details such as stages, tags, or notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samuewalton](https://clawhub.ai/user/samuewalton) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Customer-facing and operations teams can use this skill through an agent to look up Telegram-linked SaaS contacts, review recent incoming messages, and maintain contact notes, tags, or stages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a hardcoded backend token. <br>
Mitigation: Move the token to a secret store or runtime configuration, rotate any exposed token, and scope credentials to the minimum backend actions required. <br>
Risk: The skill depends on a localhost backend service that must be trusted. <br>
Mitigation: Install only with a verified backend, document backend setup and authentication scopes, and restrict access to authorized users. <br>
Risk: Advertised contact actions can change stages, tags, or notes. <br>
Mitigation: Require explicit user confirmation before mutating contact records and show the target contact, action, and new value before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text] <br>
**Output Format:** [JSON responses from a local backend service, typically summarized or acted on by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return contact records, recent message data, or contact update results depending on the selected tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
