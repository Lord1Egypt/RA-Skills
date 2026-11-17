## Description:

Weather Character Skill generates daily weather-themed character images from a user's mood, real-time weather, and selected city, with interactive selection and character consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waffle105](https://clawhub.ai/user/waffle105)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate weather-themed character images based on mood, local weather, and one of 27 Chinese cities. It also supports daily scheduling and custom character replacement when the referenced implementation files are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release artifact only includes SKILL.md and references implementation files that were not included for review.

Mitigation: Review weather_character.py and scheduler.py before running or scheduling the skill.

Risk: The quick start installs unpinned dependencies and can run a daily scheduled task.

Mitigation: Use a virtual environment, pin dependency versions where possible, and confirm the scheduled task behavior before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/waffle105/skills/weather-character-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell command snippets; generated image files when the referenced implementation is present]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run as an interactive dialog or as a daily scheduled task at 7:30 AM.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
