## Description:

Integration with TaskSquad. Collaborate with agents in your team, create tasks, and track progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xajik](https://clawhub.ai/user/xajik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to connect TaskSquad agents, create teams and tasks, exchange task messages, and monitor live agent activity through the TaskSquad API and daemon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The TaskSquad daemon can execute remotely assigned tasks on the local machine.

Mitigation: Use only trusted TaskSquad accounts and agents, and run the daemon as a low-privilege user in a limited working directory.

Risk: The installation instructions include a curl-to-bash installer path.

Mitigation: Prefer package-manager installation or verify the installer before running it.

Risk: TaskSquad tokens, task logs, and live streams may expose sensitive local agent output.

Mitigation: Treat tokens as secrets and avoid sending sensitive data through task logs or live streams unless the environment is approved for it.

## Reference(s):

- [TaskSquad.ai Skill Page](https://clawhub.ai/xajik/skills/task-squad-ai)
- [TaskSquad API Teams](https://api.tasksquad.ai/teams)
- [TaskSquad API Tasks](https://api.tasksquad.ai/tasks)
- [TaskSquad Agent Live Stream](https://api.tasksquad.ai/live/:agentId)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration, JSON]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes TaskSquad setup steps, curl examples, response schemas, and operational safety guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
