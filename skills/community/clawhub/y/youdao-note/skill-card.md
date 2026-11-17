## Description:

Use when the user wants to interact with YoudaoNote (Youdao Cloud Notes) by listing, reading, creating, searching, clipping, or saving Markdown and mindmap notes via the youdaonote CLI tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangcheng](https://clawhub.ai/user/huangcheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and YoudaoNote users use this skill to operate YoudaoNote from an agent-assisted command-line workflow, including note lookup, note creation, web clipping, and JSON-based save operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow pipes a remote installer directly into Bash, so users may execute installer code without reviewing or verifying it.

Mitigation: Download the installer separately, inspect it, and verify an official checksum or signature when available before execution.

Risk: The skill can send note contents, clipped web pages, URLs, searches, and API credentials through YoudaoNote services.

Mitigation: Use a dedicated YoudaoNote API key where possible and avoid uploading secrets, regulated data, or other sensitive content.

## Reference(s):

- [ClawHub YoudaoNote release](https://clawhub.ai/huangcheng/skills/youdao-note)
- [YoudaoNote CLI installer](https://artifact.lx.netease.com/download/youdaonote-cli/install.sh)
- [YoudaoNote Open Platform dashboard](https://mopen.163.com/#/dashboard)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, markdown]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that read, create, search, clip, or save notes through the youdaonote CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
