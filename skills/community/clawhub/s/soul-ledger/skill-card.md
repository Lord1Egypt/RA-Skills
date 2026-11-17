## Description:

Gives any AI agent persistent memory of who the user is, including facts, patterns, preferences, personality traits, and behavioral evolution over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent maintain a local, persistent personalization profile that informs tone, assumptions, and collaboration style across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and silently use a long-lived local profile of user behavior, preferences, traits, and interaction history.

Mitigation: Use it only in a private workspace where this persistent memory is expected, and inspect soul_ledger.json regularly.

Risk: Sensitive personal, workplace, or shared-machine data may be captured in the local ledger.

Mitigation: Avoid using the skill in shared environments or conversations involving sensitive data, and remove unwanted entries from the ledger when needed.

Risk: The skill describes broad memory behavior without strong consent, scope, or deletion controls.

Mitigation: Set explicit local policies for what may be recorded, when the ledger is updated, and how deletion requests are handled before deployment.

## Reference(s):

- [Soul Ledger on ClawHub](https://clawhub.ai/albionaiinc-del/skills/soul-ledger)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON schema examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates a local soul_ledger.json memory profile when followed by an agent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
