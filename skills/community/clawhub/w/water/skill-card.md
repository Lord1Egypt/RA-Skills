## Description:

Tracks daily water intake from casual mentions and sets hydration targets from weight, exercise, heat, and health context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to log water and other non-alcoholic fluid intake, estimate hydration status, and receive context-aware hydration guidance for exercise, heat, illness, travel, and declared medical constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist hydration, routine, exercise, weight, and health-related context in local files.

Mitigation: Install only if local retention of that journal is acceptable; review or delete ~/Clawic/data/water/ when that history should not be retained.

Risk: Hydration guidance may be unsafe for serious symptoms or for users with fluid restrictions.

Mitigation: Do not rely on the skill as a substitute for medical care; follow the documented red flags and defer fluid targets to a clinician when restrictions or serious symptoms apply.

Risk: Overdrinking during endurance events can worsen suspected exercise-associated hyponatremia.

Mitigation: Use the skill's red-flag checks before recommending more fluid, and avoid additional water when the documented hyponatremia signals are present.

## Reference(s):

- [ClawHub Water Tracker Skill Page](https://clawhub.ai/ivangdavila/skills/water)
- [Clawic Water Tracker Skill Page](https://clawic.com/skills/water)
- [Setup Guide](artifact/setup.md)
- [Memory Template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or concise plain text with local log and configuration file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local files under ~/Clawic/data/water/ for logs, memory, and configuration.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
