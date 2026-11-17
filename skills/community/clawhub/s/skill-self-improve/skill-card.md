## Description:

Injects a self-evolving learning system into WorkBuddy skills so they can record usage outcomes, preferences, errors, and improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to add a reusable learning and reflection layer to WorkBuddy skills, including usage recording, preference capture, insight reporting, and suggested improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can bulk-modify installed WorkBuddy skills.

Mitigation: Install and run it only when this behavior is intended; review the hardcoded target list and keep backups of affected SKILL.md files before execution.

Risk: The learning record can contain user behavior, preferences, errors, and notes.

Mitigation: Treat learned_patterns.json as potentially sensitive and avoid storing secrets, personal data, or confidential details in notes or preferences.

Risk: Automatically suggested improvements could add incorrect or misleading guidance to a skill.

Mitigation: Require human review before applying suggested SKILL.md changes and scan modified skills before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/skill-self-improve)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown guidance with Python command examples and JSON learning records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates learner.py, section.md, and learned_patterns.json in targeted WorkBuddy skill directories.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
