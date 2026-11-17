## Description:

Batch-distill completed and live OpenClaw session transcripts, meeting notes, and daily log entries into structured daily memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pjmorr](https://clawhub.ai/user/pjmorr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to preserve useful context from completed sessions, approved live sessions, meeting notes, and daily logs as markdown memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private session transcripts, meeting notes, and memory content may be copied into long-term memory or sent through model and Telegram channels.

Mitigation: Install only where that data flow is acceptable, treat the LiteLLM endpoint as a sensitive data processor, and avoid Telegram alerts or redact session identifiers in sensitive environments.

Risk: context-gate.py may process live session content beyond the live-session allowlist used by distill.py.

Mitigation: Disable or patch context-gate.py unless it enforces the same live-session allowlist before automatic distillation.

Risk: Durable memory entries may preserve user preferences, instructions, or edited and deleted group-chat content.

Mitigation: Review generated memory entries before relying on them and require review before durable user preferences or instructions are written to memory.

Risk: Shared or hardcoded credentials can weaken deployment isolation.

Mitigation: Replace shared credentials before use and configure alerting tokens through environment-specific secrets.

## Reference(s):

- [ROADMAP.md](references/ROADMAP.md)
- [trash CLI](https://github.com/ali-rantakari/trash)
- [ClawHub skill page](https://clawhub.ai/pjmorr/skills/session-distiller)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown memory entries with shell command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes daily memory files and may emit Telegram alerts when context-gate monitoring is enabled.]

## Skill Version(s):

0.5.1 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
