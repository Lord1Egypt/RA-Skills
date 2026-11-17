## Description:

Automated context health management for OpenClaw. Monitors token usage, snapshots memory, and resets sessions to maintain performance. Authored by Sophie.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zayresz](https://clawhub.ai/user/zayresz)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to archive session state, update long-term memory, and reset the main OpenClaw session when context health needs maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete main OpenClaw session files and restart the OpenClaw gateway service.

Mitigation: Require explicit operator confirmation before reset actions and restrict deletion to the intended session directory.

Risk: The skill can rewrite persistent OpenClaw memory with provided summaries.

Mitigation: Review and sanitize summaries before writing them to MEMORY.md.

Risk: The documented token threshold is a safety control, but the executable behavior should be checked before unattended use.

Mitigation: Enforce the documented threshold before archiving or resetting, and avoid cron or heartbeat scheduling until that control is confirmed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Terminal status text, JSON archive files, Markdown memory updates, and shell-driven reset actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run manually or from a scheduler and can optionally trigger a hard session reset.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
