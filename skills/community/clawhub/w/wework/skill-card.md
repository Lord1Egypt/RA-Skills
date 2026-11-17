## Description:

Wework helps agents send WeCom group robot notifications as text, markdown, images, or files and provides guidance for WeCom server-side API work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to send deployment, monitoring, reporting, and incident notifications to WeCom groups, including images or files. They can also use it for guidance on WeCom server APIs when group robots are not enough.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The WeCom webhook key can authorize messages to the configured group if exposed.

Mitigation: Store the key as a secret, avoid logging it, and rotate it if disclosure is suspected.

Risk: The file and image commands can send selected local files to a WeCom group.

Mitigation: Confirm the destination group and file sensitivity before sending files or screenshots.

Risk: Using @all can create broad notifications in the target group.

Mitigation: Require explicit user confirmation before using @all or other wide-audience mentions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangifonly/skills/wework)
- [WeCom webhook endpoint used by the CLI](https://qyapi.weixin.qq.com/cgi-bin/webhook)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and a Python CLI script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI sends selected messages or files to the configured WeCom group robot endpoint.]

## Skill Version(s):

2.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
