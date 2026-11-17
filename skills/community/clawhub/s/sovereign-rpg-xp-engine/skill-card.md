## Description:

Tracks and updates RPG-style XP, stats, levels, streaks, and achievements based on real-life task completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryudi84](https://clawhub.ai/user/ryudi84)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to turn completed real-life tasks into RPG-style progress updates, including XP awards, stat progression, streaks, and achievements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain personal progress data locally, including name, progress, streaks, achievements, and completed-task history.

Mitigation: Review, delete, or reset data/character.json when that local history should no longer be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryudi84/skills/sovereign-rpg-xp-engine)
- [Publisher profile](https://clawhub.ai/user/ryudi84)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown-style progress update with XP breakdowns, stat progress, streak status, and achievement notices]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local character state in data/character.json when used by an agent with filesystem access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
