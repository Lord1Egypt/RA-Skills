## Description:

A Chinese-language multi-agent personal life operations system that routes natural-language user needs across 12 specialized roles for health, emotions, relationships, productivity, learning, finances, leisure, career growth, hobbies, aesthetics, reflection, and crisis response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zabr1314](https://clawhub.ai/user/zabr1314)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a personal life-management assistant that creates a YOU-INC workspace, routes natural-language requests to domain-specific agent personas, and maintains context for recurring life operations. It is intended for self-management tasks such as planning, learning support, emotional reflection, health routines, finance tracking, relationship maintenance, leisure planning, career development, and crisis escalation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store sensitive personal, health, financial, relationship, and emotional context in persistent files.

Mitigation: Require explicit user consent before writing memory, keep only minimal summaries, and let users review or delete the YOU-INC context files.

Risk: The skill may invoke external integrations with access to health, calendar, email, and notes data.

Mitigation: Disable automatic external tool calls by default and require confirmation before any integration reads or modifies user data.

Risk: Crisis and mental-health guidance can be inappropriate if it is not location-aware or treated as professional support.

Mitigation: Present crisis responses as immediate safety guidance, provide location-appropriate emergency resources, and encourage contacting trusted people or qualified professionals.

Risk: Pinned paths or unscoped workspace writes can expose unrelated personal files.

Mitigation: Use user-selected, scoped storage locations and remove hard-coded paths before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zabr1314/skills/you-inc-life-ops)
- [Skill Definition](artifact/SKILL.md)
- [Orchestrator Routing Rules](artifact/references/ORCHESTRATOR.md)
- [Conflict Arbitration Protocol](artifact/references/PROTOCOLS/冲突仲裁规则.md)
- [Crisis Escalation Protocol](artifact/references/PROTOCOLS/危机升级流程.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file and command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update a persistent YOU-INC workspace containing personal context files.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
