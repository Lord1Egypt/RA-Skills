## Description:

Sends WeChat Work group robot notifications through a configured webhook, supporting text, Markdown, news-card, image, file, and template-card messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kriouerlia](https://clawhub.ai/user/kriouerlia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to send operational alerts, scheduled reports, trading-signal notifications, and workflow messages to WeChat Work groups or users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The WeChat Work webhook URL contains a usable key and can be abused if committed, logged, or shared.

Mitigation: Store the webhook URL in an environment variable or local secret store, rotate it if exposed, and avoid including it in source control or shared logs.

Risk: Selected message content is sent to the configured WeChat Work webhook.

Mitigation: Review notification payloads before enabling automated sends, and avoid sending secrets, personal data, or sensitive business data unless the receiving group is approved.

Risk: The setup script may install the Python requests dependency into the active interpreter environment.

Mitigation: Install and run the skill inside a virtual environment or managed runtime so dependency changes are isolated.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kriouerlia/skills/wechat-notify)

## Skill Output:

**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Python return dictionaries, command-line status text, and Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends caller-provided message content to the configured WeChat Work webhook and returns success or error details from the webhook response.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
