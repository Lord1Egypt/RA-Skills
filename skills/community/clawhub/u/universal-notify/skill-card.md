## Description:

Universal Notify sends alert and event notifications through ntfy.sh, Gotify, generic webhooks, SMTP email, Telegram Bot API, and Pushover with a unified priority interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josunlp](https://clawhub.ai/user/josunlp)

### License/Terms of Use:


## Use Case:

Developers, operators, and support engineers use this skill to route alerts, monitoring notices, deployment updates, and other human-facing events to the recipient's preferred notification channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notification text may be sent to external or self-hosted notification providers.

Mitigation: Send only content appropriate for the configured destination; avoid secrets, personal data, or sensitive incident details unless the destination is trusted.

Risk: Channel credentials can be exposed through shell history or command arguments.

Mitigation: Prefer disposable or limited-scope notification tokens and avoid placing real tokens directly in shell history.

Risk: The generic webhook channel can forward untrusted text to an arbitrary endpoint.

Mitigation: Review the webhook destination and be cautious when forwarding untrusted message content.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and option examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and channel-specific credentials except for ntfy.sh.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-02-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
