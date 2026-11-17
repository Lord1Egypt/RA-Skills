## Description:

Retrieves OpenClaw session records, reviews message history, and imports selected prior context into local or target conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linshuikeji](https://clawhub.ai/user/linshuikeji)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to find prior conversations, review work progress, audit session activity, and resume interrupted work by importing selected session history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prior conversation history may contain secrets, personal data, or sensitive business context.

Mitigation: Review transcript content before reuse and redact sensitive details before importing it into another session.

Risk: Including tool-call details can expose operational context that is not needed for ordinary session review.

Mitigation: Use tool-inclusive history only when necessary and prefer narrower history limits for routine context recovery.

Risk: Exported session history files can persist sensitive transcripts outside the conversation environment.

Mitigation: Avoid exports by default; when exports are required, store them securely and delete them after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linshuikeji/skills/session-history-retriever-clean)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw session management concepts](https://docs.openclaw.ai/concepts/session)
- [OpenClaw compaction concepts](https://docs.openclaw.ai/concepts/compaction)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell command examples and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include session keys, transcript excerpts, and suggested session-management commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
