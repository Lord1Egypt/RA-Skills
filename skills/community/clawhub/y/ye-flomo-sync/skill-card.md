## Description:

快速同步内容到flomo笔记，支持自动标签识别、内容格式化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ranhuang](https://clawhub.ai/user/ranhuang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send plain text, links, and tagged content to a configured flomo webhook so the content is saved as a flomo note.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected note text is sent to the webhook URL configured in ~/.flomo_token.

Mitigation: Use the skill only with notes appropriate for that flomo destination, and verify the webhook URL before sending private or business-sensitive content.

Risk: The ~/.flomo_token file contains a webhook credential.

Mitigation: Protect the file like a password and restrict local file permissions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Plain text status messages with shell command invocation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a flomo webhook URL stored in ~/.flomo_token and jq/curl availability for script execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
