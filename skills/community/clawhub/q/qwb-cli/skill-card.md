## Description:

企微瓣 (Qiweiban) AI platform CLI skill helps agents use qwb commands for authentication, voice synthesis and cloning, digital-human video generation, AI chat, image generation, and petals account management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louiseliu](https://clawhub.ai/user/louiseliu)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to perform Qiweiban CLI workflows, including media generation, voice cloning, digital-human video jobs, AI chat, account updates, and petals balance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global, unpinned CLI installation may install an unexpected qwb-cli package version or publisher.

Mitigation: Verify the qwb-cli npm package publisher and version before installation, and prefer a pinned or isolated install.

Risk: Authenticated operations can send passwords, verification codes, tokens, or private media to Qiweiban services.

Mitigation: Keep authentication interactive where possible and require explicit user confirmation before sending credentials, codes, or private media.

Risk: Some actions can delete resources, update profile details, change the API URL, or consume Qiweiban credits.

Mitigation: Require explicit user confirmation before destructive, account-changing, endpoint-changing, or billable operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/louiseliu/skills/qwb-cli)
- [Publisher profile](https://clawhub.ai/user/louiseliu)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The qwb CLI defaults to JSON output, with table and quiet formats available for human review or scripting.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
