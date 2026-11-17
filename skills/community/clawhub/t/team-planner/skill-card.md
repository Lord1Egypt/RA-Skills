## Description:

Team Planner helps users design multi-agent teams by analyzing task requirements, defining roles and responsibilities, and planning collaboration workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghost0118](https://clawhub.ai/user/ghost0118)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project leads, and agent operators use this skill to decide whether a task needs one agent or a multi-agent team, then produce role assignments, collaboration phases, startup prompts, and success criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Team plans may assign agents to handle sensitive customer or company data without sufficient privacy or access controls.

Mitigation: Review proposed plans before launching agents and add explicit privacy, access-control, and confirmation steps for sensitive data.

Risk: Generated coordination plans may over-scope multi-agent work or introduce unnecessary operational complexity.

Mitigation: Validate the single-agent versus multi-agent recommendation and adjust team size, dependencies, and handoffs before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ghost0118/skills/team-planner)
- [Team Planner examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown team architecture plan with role sections, phase lists, and startup prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a single-agent versus multi-agent recommendation, team roles, collaboration workflow, communication strategy, startup sequence, and success criteria.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
