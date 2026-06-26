## Description: <br>
Integrate with Squad Control kanban for AI agent task orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wgan](https://clawhub.ai/user/wgan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to poll Squad Control for assigned work, dispatch worker or reviewer sessions, update task state, create GitHub pull requests, and recover stuck tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can handle GitHub tokens and Squad Control API keys while cloning repositories, pushing branches, creating pull requests, and updating task state. <br>
Mitigation: Install only on a dedicated, monitored OpenClaw instance; use workspace-scoped Squad Control keys where possible and fine-grained GitHub tokens from a bot account. <br>
Risk: The skill can spawn workers and merge code, so incorrect task routing or excessive permissions could affect protected repositories. <br>
Mitigation: Use protected branches, required CI and reviews, conservative agent concurrency, and repository-scoped credentials. <br>
Risk: The optional wake-listener flow depends on runtime support and is identified by the security guidance as a feature to avoid until reviewed. <br>
Mitigation: Prefer the polling flow unless the wake-listener script and local runtime path have been reviewed in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wgan/squad-control) <br>
- [Squad Control](https://squadcontrol.ai) <br>
- [Setup Guide](references/setup.md) <br>
- [Squad Control API Reference](references/api-reference.md) <br>
- [Advanced Flows Reference](references/advanced-flows.md) <br>
- [Workspace Config Reference](references/workspace-config.md) <br>
- [Poll Result Schema](references/poll-result.schema.json) <br>
- [Review Checklist](references/review-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown instructions with inline shell commands, JSON examples, and API request templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces task orchestration guidance and command/API call patterns for an agent; poll scripts can emit HEARTBEAT_OK or a POLL_RESULT JSON envelope.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
