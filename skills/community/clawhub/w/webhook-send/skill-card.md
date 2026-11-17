## Description:

Sends text or Markdown messages to a configured webhook URL read from WEBHOOK_SEND_URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaowenchen](https://clawhub.ai/user/shaowenchen)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to prepare and send notification messages to a configured webhook endpoint in text or Markdown format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages may be posted accidentally or sent to an unintended external webhook endpoint, including shared group or business channels.

Mitigation: Install only when WEBHOOK_SEND_URL is trusted and controlled, tighten triggers to explicit webhook-send requests, and require clear user confirmation before any POST.

## Reference(s):

- [Webhook message body reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON request bodies and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Messages are sent to WEBHOOK_SEND_URL; only text and markdown payloads are described, with a 20 requests/minute and 5000-character message limit.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
