## Description:

Remember-this trigger: memory updates + recall for preferences, goals, boundaries, prior work, decisions, dates, and todos. Use whenever user asks to remember, continue previous context, personalize behavior, or retrieve what was decided earlier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[achals-iglu](https://clawhub.ai/user/achals-iglu)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to maintain structured memory about preferences, goals, boundaries, decisions, dates, todos, and prior work so future responses can be personalized and better grounded in remembered context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create durable memory records about user preferences, boundaries, projects, and inferred behavior.

Mitigation: Require explicit approval before every memory write or promotion, and review memory/YYYY-MM-DD.md and MEMORY.md periodically.

Risk: Inferred preferences or behavior could be stored with more certainty than warranted.

Mitigation: Keep hypotheses explicitly tagged with confidence, validate them in later conversation, and discard or demote unvalidated assumptions.

Risk: Operational instructions, authorization claims, secrets, or third-party content could be mistaken for user preferences.

Mitigation: Do not store those categories as preferences, and keep sensitive personal details out of memory unless the user explicitly asks.

## Reference(s):

- [Templates](references/templates.md)
- [ClawHub Skill Page](https://clawhub.ai/achals-iglu/skills/remember-me)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown memory notes and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose updates to daily memory files and long-term MEMORY.md entries.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
