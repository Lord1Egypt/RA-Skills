## Description:

Session Bridge helps agents preserve compact topic context across surfaces and agent handoffs using transient JSON capsules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeinonenight](https://clawhub.ai/user/codeinonenight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create, refresh, hydrate, hand off, list, and expire compact context capsules when conversations move across OpenClaw surfaces or agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fixed Telegram or session identifiers may route handoffs to the wrong destination or disclose capsule summaries.

Mitigation: Review and replace hard-coded Telegram and session identifiers before use.

Risk: Cross-session capsules can share context across agents and surfaces that may not have identical trust boundaries.

Mitigation: Install only in workspaces where all participating agents and surfaces are trusted to share compact capsule summaries.

Risk: Capsules may contain secrets, private transcripts, stale context, or user-supplied text that could be over-trusted.

Mitigation: Store only short non-secret summaries, avoid private transcripts, expire stale capsules, and treat hydrated capsule text as historical context rather than instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codeinonenight/skills/session-bridge)
- [Publisher profile](https://clawhub.ai/user/codeinonenight)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown briefings with shell command examples; capsule state is stored as JSON with a Markdown view.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hydration briefings are intended to stay compact, approximately 150 to 350 tokens.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
