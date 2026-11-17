## Description:

Task Planner helps agents turn vague, multi-step goals into structured plans, identify risks and decision points, and guide users through execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangrb](https://clawhub.ai/user/jiangrb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to decompose complex goals into actionable steps, confirm a plan, and execute it iteratively with checkpoints and summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plans may be incomplete or misleading for complex tasks.

Mitigation: Review the generated plan before confirming execution and revise milestones, dependencies, and decision points as needed.

Risk: Execution guidance for code changes or shell commands could affect files or systems if followed without review.

Mitigation: Inspect proposed changes and commands before running them, then use normal testing and review practices for the affected project.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown plans, checklists, progress updates, summaries, and occasional command or code guidance when the task requires it.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output adapts to the user's language and may include staged plans, risk notes, decision points, and execution summaries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
