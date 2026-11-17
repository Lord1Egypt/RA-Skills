## Description:

Personal safety awareness and basic physical self-defense techniques for people who want practical self-defense knowledge without martial arts training.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and assistants use this skill to provide practical personal-safety guidance for everyday situations such as walking alone, commuting, late-shift work, solo travel, delivery work, or isolated environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests filesystem access that is not needed for ordinary self-defense guidance.

Mitigation: Install and run it only where filesystem access is denied or tightly scoped unless a reviewer confirms that access is necessary.

Risk: The install command uses an unpinned npx package invocation.

Mitigation: Use a pinned and verified ClawHub CLI version before installing in a shared or production environment.

Risk: Self-defense law and weapon legality vary by jurisdiction.

Mitigation: Check the user's local law before giving specific legal or weapon guidance, and recommend qualified legal help after any physical confrontation.

## Reference(s):

- [FBI Uniform Crime Reports](https://ucr.fbi.gov/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance with structured safety steps, local-law caveats, and escalation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapts advice to user context, physical limitations, jurisdiction, and ongoing-threat indicators.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
