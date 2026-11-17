## Description:

Provides structured AI programming workflows for local coding agents, including test-driven development, code review, refactoring, documentation, debugging, and acceptance testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yantianlong-01](https://clawhub.ai/user/yantianlong-01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to orient local AI coding tools around Superpowers workflows for TDD, code review, refactoring, documentation, debugging, and acceptance testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a mutable third-party agent plugin without pinning or verification can expose users to unreviewed upstream changes.

Mitigation: Review the upstream project before installing and prefer a pinned release or commit from a trusted source.

Risk: Symlinking a mutable working directory can cause the installed skill behavior to change unexpectedly.

Mitigation: Avoid symlinking mutable directories unless you control them and can review changes before use.

Risk: The skill can guide agents toward commands or project-file changes in local development environments.

Mitigation: Confirm the coding agent requires user approval before running commands or modifying project files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yantianlong-01/skills/yantianlong-superpowers)
- [Superpowers GitHub repository](https://github.com/obra/superpowers)
- [Superpowers quick start](https://lzw.me/docs/opencodedocs/zh/obra/superpowers/start/quick-start/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tables, links, and inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local coding-agent workflows and installation steps; it does not execute installation steps by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
