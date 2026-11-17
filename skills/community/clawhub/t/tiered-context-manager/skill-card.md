## Description:

Tiered Context Manager helps OpenClaw agents manage long multi-agent conversations with L1/L2/L3 context compression, memory tiering, cross-agent knowledge sharing, real-time monitoring, statistics, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scorpioxyb](https://clawhub.ai/user/scorpioxyb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to compress long agent sessions, organize retained memories by lifecycle, share selected context across agents, and generate monitoring or compression reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live operation can rewrite session content and create backups.

Mitigation: Start with dry-run operation and restrict filesystem permissions to approved OpenClaw session and backup directories.

Risk: Conversation content may be summarized, persisted, or copied into shared agent memory and inbox files.

Mitigation: Use only on non-sensitive sessions unless users have consented and content has been reviewed or redacted.

Risk: Cross-agent handoffs and weak path scoping can expose integrity and data-sharing risks.

Mitigation: Keep cross-agent handoffs disabled until consent, redaction, path validation, and session rewrite issues are addressed.

## Reference(s):

- [Tiered Context Manager Architecture](references/architecture.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and generated text or Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write compressed session content, backups, statistics, reports, memory files, and inbox tasks when run in live mode.]

## Skill Version(s):

1.0.0 (source: server release evidence, scripts/package.json, and architecture version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
