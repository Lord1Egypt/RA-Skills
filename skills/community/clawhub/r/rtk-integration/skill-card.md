## Description:

Integrates RTK (Rust Token Killer) so agents can install RTK, check token savings, and use rtk-prefixed shell commands to reduce shell-output tokens before they enter the context window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davydenkovm](https://clawhub.ai/user/davydenkovm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install RTK, configure command filtering, check token savings, and guide agents to use RTK-wrapped shell commands during development workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can run an unverified remote installer and add RTK to the user's PATH.

Mitigation: Review the installer before use, prefer a pinned and checksum-verified release or package-manager installation, and confirm shell profile changes.

Risk: RTK can mediate broad shell activity and optional global hooks can alter how future commands are handled.

Mitigation: Avoid global hooks until their behavior is understood, and initially limit RTK usage to read-only or low-risk commands.

Risk: Compressed command output can omit details needed for debugging or review.

Mitigation: Run commands without RTK when full raw output is required or when investigating unclear failures.

## Reference(s):

- [RTK Command Reference](references/commands.md)
- [RTK Configuration Guide](references/config.md)
- [RTK Releases](https://github.com/rtk-ai/rtk/releases)
- [ClawHub Skill Page](https://clawhub.ai/davydenkovm/skills/rtk-integration)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and TOML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose installing RTK, updating PATH, initializing optional hooks, and prefixing future shell commands with rtk.]

## Skill Version(s):

1.1.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
