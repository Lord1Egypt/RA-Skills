## Description:

Publishes Markdown articles to a WeChat Official Account draft box through a remote wenyan-mcp service, with credential separation and dependency checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp33333333333](https://clawhub.ai/user/cp33333333333)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developers use this skill to prepare and publish Markdown content to WeChat Official Account drafts through local agent workflows or shell scripts connected to a trusted remote MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote publishing can expose unpublished articles and WeChat AppID/AppSecret to the remote MCP service.

Mitigation: Use only an MCP server you control or fully trust, require HTTPS, and test with a low-risk account or draft workflow before using production credentials.

Risk: Credential files and legacy shell-based setup can expose secrets if permissions or file contents are loose.

Mitigation: Protect wechat.env with restrictive permissions, avoid legacy TOOLS.md credential loading, and do not put shell commands in credential files.

Risk: Unpinned CLI execution can change behavior between publishing runs.

Mitigation: Prefer a pinned or preinstalled publishing CLI and verify the remote wenyan-cli version before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp33333333333/skills/wechat-mp-publisher1)
- [wenyan-mcp](https://github.com/caol64/wenyan-mcp)
- [wenyan-cli](https://github.com/caol64/wenyan-cli)
- [wenyan-cli themes](https://github.com/caol64/wenyan-core/tree/main/src/assets/themes)
- [Theme reference](references/themes.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce publishing command invocations and status guidance for Markdown articles; successful publishing returns a WeChat draft media ID.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and _meta.json report 2.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
