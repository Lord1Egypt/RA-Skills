## Description:

Yeeth Claw adds Claude Code PreToolUse hooks that inspect npm, pip, yarn, pnpm, and cargo install commands for supply-chain risk signals before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bkojusner](https://clawhub.ai/user/bkojusner)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add package-install guardrails to Claude Code sessions, warning on suspicious dependency installs and blocking higher-risk installs before Bash execution proceeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can persistently change Claude Code hook configuration and affect future Bash package install commands.

Mitigation: Review the hook and settings snippet before installation, back up ~/.claude/settings.json, and confirm the configured PreToolUse hook is expected.

Risk: The hook performs outbound package registry lookups and can optionally submit blocked package metadata to Argus.

Mitigation: Install only where outbound registry checks are acceptable, and configure Argus only with a fixed HTTPS endpoint and a narrowly scoped API key.

Risk: BLOCK-tier decisions can stop package installation during Claude Code Bash tool use.

Mitigation: Treat blocked installs as review prompts and verify package identity, age, and typosquat signals before proceeding manually or changing hook policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bkojusner/skills/yeeth-claw)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal hook messages with shell and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hook output uses allow, warn, and block exit codes for Claude Code Bash tool calls.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
