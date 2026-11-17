## Description:

Sends local image files to Feishu group or individual chats using a configured Feishu app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ye1358215818](https://clawhub.ai/user/ye1358215818)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to send screenshots, design images, or other local image files to a Feishu group or individual recipient from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app credentials may be exposed if passed on the command line or hardcoded.

Mitigation: Use environment variables or a secret manager for FEISHU_APP_ID and FEISHU_APP_SECRET.

Risk: Sensitive local images may be sent to an unintended chat or user.

Mitigation: Review image contents and confirm the destination chat or user ID before sending.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn/)
- [ClawHub skill page](https://clawhub.ai/ye1358215818/skills/zoe-feishu-media)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local image path, Feishu recipient ID, and Feishu app credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
