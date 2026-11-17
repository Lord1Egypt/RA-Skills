## Description:

Track smoking and nicotine use, reduce consumption, or quit with neutral logs, trigger mapping, and adaptive plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this agent skill to log smoking or nicotine use, identify trigger patterns, and follow user-selected logger, reduction, or quit plans without judgment. It supports local tracking, structured check-ins, craving responses, and escalation to licensed care for safety-sensitive situations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Smoking, nicotine-use, trigger, and plan notes may be retained in local files under ~/smoking/.

Mitigation: Present planned writes for user confirmation, store only behavior-change-relevant data, and review or delete local notes when history is no longer wanted.

Risk: Health-related coaching can be mistaken for medical diagnosis, prescribing, or emergency support.

Mitigation: Keep recommendations within tracking and coaching scope, avoid medication dosing, and direct urgent symptoms, pregnancy concerns, severe withdrawal, medication questions, or self-harm thoughts to licensed professional or emergency care.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/smoking)
- [Skill homepage](https://clawic.com/skills/smoking)
- [Setup - Smoking](artifact/setup.md)
- [Goal Modes - Smoking](artifact/goal-modes.md)
- [Logging Template and Metrics](artifact/log-template.md)
- [Reduction Methods](artifact/reduction-methods.md)
- [Quit Playbook](artifact/quit-playbook.md)
- [Craving Playbook](artifact/craving-playbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with structured local note templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose user-approved local notes under ~/smoking/; no credentials, external services, or network endpoints are required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
