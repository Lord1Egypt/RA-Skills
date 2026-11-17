## Description:

Provides a persona and memory framework for agents to adopt a consistent, opinionated voice and use SOUL.md, USER.md, and MEMORY.md for continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhrisfu](https://clawhub.ai/user/xhrisfu)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to guide an agent toward persona continuity, user-specific memory practices, and a more opinionated conversational style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to persist sensitive psychological and relationship inferences about a user over time.

Mitigation: Require explicit consent before writing user or relationship memory, keep memory files reviewable, and provide a clear path to edit or delete stored assumptions.

Risk: Persona and memory guidance may change agent behavior in ways that conflict with user expectations or instruction precedence.

Mitigation: Keep system, developer, safety, privacy, and current user instructions above persona guidance, and review persona files before deployment.

## Reference(s):

- [Soul Framework ClawHub release page](https://clawhub.ai/xhrisfu/skills/soul-framework)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Markdown guidance for persona, user, and memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create or update SOUL.md, USER.md, and MEMORY.md files when adopted.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
