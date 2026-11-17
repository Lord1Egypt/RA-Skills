## Description:

Improve reusable agent workflows with reflective experiments, value checks, and local pattern memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to improve recurring agent workflows through local experiment logs, value-gated promotion of proven patterns, and bounded local memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save durable behavior preferences and activation rules with unclear scope.

Mitigation: Keep saved rules inside ~/self-evolving/ unless the user explicitly confirms another memory write.

Risk: Stored activation cues or always/never rules may persist after they stop matching the user's intent.

Mitigation: Periodically inspect or delete saved activation cues and always/never rules.

Risk: Workflow changes could be promoted before they have enough supporting evidence.

Mitigation: Promote only after three comparable wins and discard changes that add churn or weaken reliability.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/self-evolving)
- [Skill homepage](https://clawic.com/skills/self-evolving)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance and local markdown memory templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update concise local notes under ~/self-evolving/ when the user has been told about persistent storage.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
