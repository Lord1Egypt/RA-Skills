## Description:

Session Scribe summarizes new OpenClaw session transcript entries with OpenAI or Anthropic and appends bullet-point notes to daily memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kitsune](https://clawhub.ai/user/kitsune)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to preserve OpenClaw session context by periodically summarizing selected session transcripts into reusable daily memory notes. It is intended for automated or manual runs where transcript processing by an external LLM provider is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private session transcripts may be sent to external LLM providers during summarization.

Mitigation: Use a dedicated low-privilege API key with spending limits, run --dry-run first, and avoid processing sessions containing secrets, PII, or regulated data.

Risk: Recurring or all-session operation can broaden transcript processing beyond the intended conversation.

Mitigation: Prefer a single explicit session unless broad coverage is required, and review the selected sessions before enabling a cron schedule.

Risk: Generated memory notes may be incomplete, inaccurate, or misleading.

Mitigation: Treat generated memory as untrusted notes and review important entries before relying on them.

## Reference(s):

- [OpenClaw Transcript Format](references/transcript-format.md)
- [ClawHub Skill Page](https://clawhub.ai/kitsune/skills/session-scribe-openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown memory notes and console text, with setup examples as shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can append daily memory files, print dry-run summaries, and persist per-session progress state.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
