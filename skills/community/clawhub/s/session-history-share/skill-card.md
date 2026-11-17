## Description:

Automatically injects compressed summaries of previous OpenClaw session histories into new sessions for context continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ouhaitao](https://clawhub.ai/user/ouhaitao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to carry concise session summaries across daily session resets by storing summaries on disk and injecting the latest archive into bootstrap context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill retains conversation summaries on disk and injects them into future agent context, which can expose secrets, private business data, or regulated data.

Mitigation: Use only with explicit opt-in and add redaction, retention limits, and review of stored summaries before enabling it in sensitive environments.

Risk: Persistent automation reads active transcripts and writes session archives without strong controls.

Mitigation: Harden archive paths, restrict filesystem permissions, and verify that install and uninstall flows reliably register, remove, and clean up hooks and cron jobs.

Risk: Automatically injected history can carry stale, irrelevant, or unintended context into new sessions.

Mitigation: Keep summaries concise, limit retention, and provide a user-visible way to disable injection or clear prior history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ouhaitao/skills/session-history-share)
- [ClawHub publisher profile](https://clawhub.ai/user/ouhaitao)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and configuration-oriented guidance, with shell commands for installation and removal]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs an OpenClaw bootstrap hook and cron task that persist and inject session summaries.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
