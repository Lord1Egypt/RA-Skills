## Description:

Automated transcript trimming, LLM memory extraction, and session hygiene for OpenClaw gateways.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfdeadcat](https://clawhub.ai/user/halfdeadcat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Session Janitor to keep OpenClaw gateway transcripts manageable by offloading large tool results, trimming oversized JSONL sessions, extracting memories from archived content, and pruning stale or orphaned session records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic transcript rewriting and deletion can remove or alter session history.

Mitigation: Back up sessions first and install only on gateways where automated cleanup is acceptable.

Risk: Persistent cron and watcher jobs can continue changing session files after installation.

Mitigation: Review generated configuration and installed services before enabling them, and disable cron or watcher automation when persistent cleanup is not desired.

Risk: LLM extraction and memory storage can expose private transcript-derived facts, especially if a Git-backed memory directory is configured.

Mitigation: Keep config.json private and user-writable only, disable LLM extraction and memory-related paths unless explicitly needed, and keep memory stores out of public repositories.

Risk: Watchdog Slack alerts and auto-restart settings may disclose operational details or run restart scripts.

Mitigation: Disable Slack alerts and auto-restart unless they are explicitly needed, and validate any restart scripts before use.

## Reference(s):

- [Session Janitor on ClawHub](https://clawhub.ai/halfdeadcat/skills/session-janitor)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Session Janitor Architecture](artifact/ARCHITECTURE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute local cleanup scripts that rewrite or delete OpenClaw session artifacts when installed and run.]

## Skill Version(s):

1.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
