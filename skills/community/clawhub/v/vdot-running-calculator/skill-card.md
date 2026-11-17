## Description:

Calculates a runner's VDOT score and Daniels training paces from a recent race result using the Daniels-Gilbert VO2 and race-duration equations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbazex](https://clawhub.ai/user/arbazex)

### License/Terms of Use:

MIT-0

## Use Case:

External runners, coaches, and agent users use this skill to convert a recent race result into a VDOT estimate and Daniels Easy, Marathon, Threshold, Interval, and Repetition training paces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Training paces may be misleading if the input race was not an honest recent effort or was affected by terrain, heat, altitude, fatigue, or injury.

Mitigation: Ask for a recent race result and state that unusual conditions can distort the estimate.

Risk: Users may treat calculated training paces as medical advice or follow intensity guidance when injured, new to structured training, or managing cardiovascular concerns.

Mitigation: Present the output as training-planning guidance and advise appropriate medical consultation for higher-risk users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arbazex/skills/vdot-running-calculator)
- [Server-resolved GitHub repository](https://github.com/arbazex/vdot-running-calculator)
- [agentskills.io specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with calculated pace values, labeled training zones, assumptions, and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires one race distance and finish time; outputs training-planning estimates, not medical advice.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
