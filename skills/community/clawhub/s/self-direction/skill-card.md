## Description:

Your agent learns to think like you. Captures your direction system, makes decisions as you would, guides all processes toward your goals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to help an agent build, validate, and apply a local model of the user's goals, values, boundaries, and decision patterns. It supports more consistent autonomous decisions and direction frames for sub-agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently builds a behavioral profile of user preferences, values, boundaries, reasoning, and decision patterns.

Mitigation: Define what may be stored, review and delete local records regularly, and keep sensitive or off-limit topics out of the profile.

Risk: The skill may encourage agents or sub-agents to act from an underspecified profile without enough scoping or user control.

Mitigation: Require explicit approval for high-stakes actions, low-confidence inferences, conflicts, and decisions outside the current direction frame.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/self-direction)
- [Skill Homepage](https://clawic.com/skills/self-direction)
- [Setup Guide](setup.md)
- [Memory Template](memory-template.md)
- [Evidence Logging Guide](evidence.md)
- [Direction Transmission Guide](transmission.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance and local profile templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local files under ~/self-direction/ to maintain direction, evidence, confidence, conflict, and transmission records.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
