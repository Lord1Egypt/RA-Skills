## Description:

Helps an agent proactively report task progress, raise blockers immediately, respond quickly to user requests, and maintain continuity through memory notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdt328606](https://clawhub.ai/user/sdt328606)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to shape an assistant's communication behavior so it reports completed work, surfaces blockers promptly, records useful memory, and avoids unnecessary check-ins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent memory about user preferences, active tasks, and lessons learned, which can expose sensitive context if used without boundaries.

Mitigation: Use it only where persistent memory is acceptable, and add consent, redaction, retention, and deletion controls before deployment.

Risk: The skill uses broad priority language around proactive responses and cross-skill coordination.

Mitigation: Keep platform and user instructions higher priority than this skill, and review proactive messages before they affect important workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdt328606/skills/stitch-proactive-agent)
- [Proactive Agent Memory System](assets/MEMORY-SYSTEM.md)
- [Proactive Agent Guidelines](assets/PROACTIVE-GUIDELINES.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance for agent communication and memory practices]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No explicit runtime parameters; behavior depends on the agent applying the guidance and any available memory files.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
