## Description:

Use when the user wants to create, inspect, update, or run scheduled remote agents in the cloud rather than local cron jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create, inspect, update, or run scheduled remote agent jobs in isolated cloud environments while keeping repo source, environment, connectors, cron schedule, and prompt payload explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled remote agent runs may continue operating after setup and can act on configured repositories, environments, connectors, schedules, and prompt payloads.

Mitigation: Before installing or running the skill, confirm the intended remote-agent schedule and review the repo, environment, connectors, cron schedule, and prompt payload.

Risk: Missing authentication, environment access, or repository access can block trigger creation or updates.

Mitigation: Confirm authentication, environment, connector, and repository-access assumptions before returning trigger details or next management steps.

## Reference(s):

- [Remote Agent Scheduler on ClawHub](https://clawhub.ai/wimi321/skills/remote-agent-scheduler)
- [Publisher profile](https://clawhub.ai/user/wimi321)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with trigger details, confirmations, and operational notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include scheduled trigger definitions, run or update confirmations, setup blockers, and next management steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
