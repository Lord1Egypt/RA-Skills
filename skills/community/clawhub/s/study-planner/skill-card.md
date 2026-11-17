## Description:

Create personalized study plans with time allocation, phased learning schedules, and review strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Learners, educators, and agents use this skill to turn a subject, current level, available time, and deadline into a phased study plan with review cadence and practical daily or weekly structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated plan may include inappropriate workload assumptions or weak deadline pacing if the learner provides incomplete context.

Mitigation: Ask brief clarifying questions about level, available time, deadline, priorities, and preferences before finalizing the plan.

Risk: The skill may produce Chinese phase names or templates when the user expects another language.

Mitigation: Adapt the final plan to the learner's requested language and translate phase labels when needed.

## Reference(s):

- [Study Planner skill page](https://clawhub.ai/smallkeyboy/skills/study-planner)
- [learning-methods.md](references/learning-methods.md)
- [templates.md](references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown study plans with optional inline shell command usage and interpreted schedule data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bilingual Chinese and English phase names, review intervals, time blocks, and adjustment guidance.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
