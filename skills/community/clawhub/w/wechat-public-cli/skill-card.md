## Description:

Publish and download WeChat Public Platform content and Baijiahao articles via a local CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-chen2050](https://clawhub.ai/user/ai-chen2050)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to prepare, publish, download, and inspect WeChat Public Platform and Baijiahao article content through a local command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow installs mutable third-party CLI code before running account-impacting commands.

Mitigation: Review the package and repository before installation and prefer a pinned local version over global npm or unpinned npx.

Risk: The workflow uses sensitive WeChat and Baijiahao credentials.

Mitigation: Keep credentials out of source control, use restricted file permissions, and prefer environment or local configuration controls appropriate for the deployment.

Risk: Publish and send-all commands can change external account state or distribute content broadly.

Mitigation: Require explicit human review before executing publishing or send-all commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-chen2050/skills/wechat-public-cli)
- [Publisher profile](https://clawhub.ai/user/ai-chen2050)
- [Skill homepage](https://github.com/ai-chen2050/obsidian-wechat-public-platform)
- [OpenClaw install repository](https://github.com/ai-chen2050/obsidian-wechat-public-platform.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and article frontmatter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include publishing commands that affect external WeChat or Baijiahao accounts.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
