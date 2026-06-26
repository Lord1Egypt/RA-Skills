## Description: <br>
Manage TickTick tasks and projects from the command line with OAuth2 auth, batch operations, and rate limit handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ManuelHettich](https://clawhub.ai/user/ManuelHettich) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to authenticate with TickTick and manage tasks and projects from shell commands. It supports creating, listing, updating, completing, and abandoning tasks, including JSON output for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change TickTick tasks and projects. <br>
Mitigation: Require explicit user approval before mutations such as complete, abandon, batch-abandon, task updates, or project updates. <br>
Risk: OAuth client secrets and tokens are stored in a local plaintext config file. <br>
Mitigation: Protect the config file, keep local filesystem permissions restrictive, and avoid sharing the credentials directory. <br>
Risk: Task and project text may contain sensitive personal or work information. <br>
Mitigation: Avoid storing secrets in TickTick task text and prefer project filters or task IDs to reduce unintended access. <br>


## Reference(s): <br>
- [TickTick Developer Center](https://developer.ticktick.com/manage) <br>
- [TickTick Open API v1](https://developer.ticktick.com/api) <br>
- [TickTick Batch Task API](https://api.ticktick.com/open/v1/batch/task) <br>
- [ClawHub Skill Page](https://clawhub.ai/ManuelHettich/ticktick) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TickTick OAuth credentials stored locally and supports machine-readable output with --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
