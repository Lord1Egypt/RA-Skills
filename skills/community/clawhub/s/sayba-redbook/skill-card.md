## Description:

Search, read, analyze, and automate Xiaohongshu (小红书) content via CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saybanet](https://clawhub.ai/user/saybanet)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, marketers, and developers use this skill to direct agents through Xiaohongshu topic research, creator analysis, comment operations, content planning, card rendering, and optional account actions through the redbook CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool uses an active Xiaohongshu browser session and can perform account actions such as posting, commenting, collecting, and batch replies.

Mitigation: Install only for accounts where this access is acceptable, avoid pasting cookies into chats or shell history, and manually review posting and reply commands before execution.

Risk: Batch replies and other automation can trigger platform risk controls or create unwanted public interactions.

Mitigation: Run dry-run previews first, keep human approval in the loop, use the documented delay and batch limits, and stop on captcha or verification prompts.

Risk: Installation can modify local agent skill state by creating or replacing the redbook Claude skill path.

Mitigation: Review the existing local skill path before installation and install in an environment where changing that path is acceptable.

Risk: The release evidence reports a suspicious security verdict due to cookie handling, install-time behavior, and anti-detection automation guidance.

Mitigation: Treat deployment as requiring review, scan the package before use, and start with read-only commands such as whoami, search, and read before enabling write actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saybanet/skills/sayba-redbook)
- [Publisher profile](https://clawhub.ai/user/saybanet)
- [Project homepage from ClawHub metadata](https://github.com/lucasygu/redbook)
- [Research task notes](docs/research-task-1789.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Use --json when parsing CLI output programmatically; render workflows can produce Xiaohongshu-ready PNG card files.]

## Skill Version(s):

0.5.0 (source: server release and SKILL.md frontmatter; package.json reports 0.5.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
