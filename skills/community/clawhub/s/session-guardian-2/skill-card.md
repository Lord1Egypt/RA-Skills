## Description:

Detect natural session boundaries, minimize unnecessary context carryover, and produce concise handoff summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zd200572](https://clawhub.ai/user/zd200572)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and agent users use Session Guardian to decide when a conversation has reached a natural boundary and to create a concise handoff for a new session. It is useful when completed work, an unrelated follow-up, or reliable context pressure makes carrying the full prior conversation unnecessary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A handoff may include secrets, private paths, customer names, or sensitive commands from the prior conversation.

Mitigation: Review and redact the generated handoff before copying it into a new session.

Risk: Global installation can make the skill available outside the intended project context.

Mitigation: Use a per-project install when the skill should only apply to one workspace or project.

Risk: A premature boundary recommendation can interrupt tightly coupled active work.

Mitigation: Apply the skill only at meaningful checkpoints and continue silently when prior context is still needed.

## Reference(s):

- [Server-resolved GitHub repository](https://github.com/zd200572/session-guardian)
- [ClawHub skill page](https://clawhub.ai/zd200572/skills/session-guardian-2)
- [Topic boundary guide](references/topic-boundaries.md)
- [Session handoff template](templates/handoff.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown handoff summary and short natural-language recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No automatic session switching; users review and carry handoff text manually.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
