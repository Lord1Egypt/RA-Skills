## Description: <br>
Tasktrove helps agents manage todos through a Tasktrove API, including listing, creating, completing, updating, and searching tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willwebberley](https://clawhub.ai/user/willwebberley) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users of a self-hosted Tasktrove instance use this skill to inspect, create, search, and update task lists through API-backed commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a user-selected Tasktrove host and may send an API token. <br>
Mitigation: Set TASKTROVE_HOST only to a trusted server, prefer HTTPS or a trusted local network, and protect TASKTROVE_TOKEN. <br>
Risk: State-changing actions can complete, update, create, or delete tasks. <br>
Mitigation: Require explicit confirmation before completing, updating, creating, or deleting tasks. <br>


## Reference(s): <br>
- [ClawHub Tasktrove Skill](https://clawhub.ai/willwebberley/tasktrove) <br>
- [Tasktrove](https://tasktrove.io) <br>
- [Tasktrove GitHub Repository](https://github.com/dohsimpson/tasktrove) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TASKTROVE_HOST and optional TASKTROVE_TOKEN to connect to a selected Tasktrove instance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
