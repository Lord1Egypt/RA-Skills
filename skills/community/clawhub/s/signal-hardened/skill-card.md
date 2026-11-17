## Description:

Bridges the current Claude Code session to Telegram, Discord, Feishu/Lark, or QQ for setup, daemon lifecycle management, diagnostics, and message forwarding to a phone or team messaging app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure, run, stop, inspect, and diagnose a local bridge daemon that connects an active Claude Code session to supported IM platforms. It is intended for controlled session access from a phone or team messaging app while preserving per-platform credential boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores IM platform tokens and other messaging credentials on disk.

Mitigation: Store credentials only in ~/.claude-to-im/config.env with restrictive file permissions, mask secrets in output, restrict bot or app permissions, and revoke tokens if exposure is suspected.

Risk: The bridge daemon can relay Claude session content to external messaging platforms.

Mitigation: Enable only intended channels and users, keep per-platform access controls separate, stop the daemon when it is not needed, and understand how to revoke platform credentials.

Risk: Daemon and diagnostic operations rely on local scripts that must match the reviewed package.

Mitigation: Verify the installed script directory and package source before running start, stop, status, logs, reconfigure, or doctor commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/skills/signal-hardened)
- [Faberlens Safety Evaluation](https://faberlens.ai/explore/signal)
- [QQ Bot OpenClaw Portal](https://q.qq.com/qqbot/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [User-facing output should mask secrets; setup and reconfiguration flows may create or update local configuration when credentials are provided and confirmed.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
