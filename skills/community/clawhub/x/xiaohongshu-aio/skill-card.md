## Description:

A Xiaohongshu MCP client skill for managing accounts, login state, content publishing, feed retrieval, comments, replies, user profiles, and local MCP service operations through CLI and REST API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-p5](https://clawhub.ai/user/cn-p5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill to automate Xiaohongshu account workflows, login checks, content publishing, feed search and detail retrieval, comments, replies, profile lookup, and MCP service management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download, start, and restart unverified third-party native MCP binaries.

Mitigation: Review carefully before installing, run only in a dedicated directory, avoid elevated privileges, and treat MCP download/start/restart as execution of unverified third-party native code.

Risk: The skill can store account cookies in plaintext JSON files.

Mitigation: Use a test account where possible, do not casually store or share cookie JSON files, and restrict access to the working directory.

Risk: The skill can perform real account and platform actions such as publishing content, commenting, logging out, and switching accounts.

Mitigation: Confirm the target account and content before any publish, comment, logout, or account-switch action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cn-p5/skills/xiaohongshu-aio)
- [README.md](artifact/README.md)
- [README.zh-CN.md](artifact/README.zh-CN.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands, environment variable names, local file paths, and account or content workflow guidance.]

## Skill Version(s):

0.1.6 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
