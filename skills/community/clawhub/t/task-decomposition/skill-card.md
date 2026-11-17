## Description:

Breaks a user goal or requirement into a hierarchical work breakdown structure with phases, tasks, steps, dependencies, effort estimates, and a suggested execution order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and project planners use this skill to turn broad goals into actionable WBS-style plans before implementation, delegation, scheduling, or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The learning module can persist notes, errors, recent operations, and preferences.

Mitigation: Avoid entering secrets or confidential details into learner notes or preferences, and review the local learning log before sharing artifacts.

Risk: The learning module can write to a skill directory supplied by the caller.

Mitigation: Run learner.py only against this skill's own directory unless intentionally updating another skill's learned_patterns.json.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/task-decomposition)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or JSON work breakdown structure with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes phases, tasks, steps, dependencies, S/M/L effort estimates, execution order, and optional local learning records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
