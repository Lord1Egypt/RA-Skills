## Description:

Schedules Chinese plain-text summaries of recent technology and AI news from a configurable company whitelist and sends them to a configured delivery channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuewuya20180928](https://clawhub.ai/user/yuewuya20180928)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to schedule recurring Chinese news digests about selected AI and technology companies, with configurable search, article count, length, delivery channel, recipient, and timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring delivery can send messages to an unintended recipient or schedule if defaults are accepted without review.

Mitigation: Require an explicit recipient, delivery account, channel, and schedule before installation, and remove the concrete WeChat recipient fallback.

Risk: Diagnostic commands can expose local API keys or bearer tokens if copied into logs or chat.

Mitigation: Run credential diagnostics only by an administrator, redact tokens and API keys, and avoid printing secrets during normal operation.

Risk: Manual reset steps can delete local bot account state.

Mitigation: Keep bot reset commands out of routine agent instructions and require administrator approval plus a backup before account-state deletion.

Risk: Delivery can silently fail when a bot token expires or a sandboxed channel stops accepting messages.

Mitigation: Monitor cron run history and delivery receipts, rotate expired tokens, and update the cron job's delivery account after re-pairing.

## Reference(s):

- [Skill page](https://clawhub.ai/yuewuya20180928/skills/redian-jiansuo-baochuwen)
- [Configuration variables](references/variables.md)
- [Prompt template](references/prompt.md)
- [Cron job configuration](references/cron-config.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with plain-text message output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scheduled news message content and operator setup guidance; default article count, length, whitelist, model, search provider, channel, recipient, and cron timing are configurable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
