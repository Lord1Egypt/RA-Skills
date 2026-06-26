## Description: <br>
Sends text or Markdown messages to a configured webhook URL using HTTP POST. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaowenchen](https://clawhub.ai/user/shaowenchen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to prepare text or Markdown webhook notifications for group messages, bot alerts, and message-push integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook URLs and message contents can be sensitive because messages are sent outside the local chat. <br>
Mitigation: Store WEBHOOK_SEND_URL like a secret and avoid sending passwords, tokens, personal data, or confidential business content unless the webhook is approved for that use. <br>
Risk: An incorrect or untrusted webhook destination can send notifications to the wrong external service. <br>
Mitigation: Confirm the webhook destination before use and send only to webhooks the user controls or trusts. <br>


## Reference(s): <br>
- [Webhook message body reference](reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with JSON request-body examples and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports text and Markdown webhook payloads; messages are limited to 20 requests per minute and 5000 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
