## Description: <br>
Manage Wrike tasks, projects, folders, and comments via the Wrike REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tallhamn](https://clawhub.ai/user/tallhamn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, operators, and developers use this skill to inspect and manage Wrike accounts, spaces, folders, projects, tasks, comments, contacts, workflows, and custom fields through the `claw-wrike` CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive Wrike data and a locally stored API token. <br>
Mitigation: Use the least-privileged Wrike token available and protect or remove the local config file when no longer needed. <br>
Risk: Creates, updates, comments, deletes, or bulk changes can affect shared Wrike workspaces. <br>
Mitigation: Require explicit confirmation before mutating or bulk operations, and use dry-run support where available. <br>
Risk: Operating on guessed IDs or stale task state can modify the wrong Wrike object. <br>
Mitigation: Look up space, folder, task, workflow, and custom status IDs first, and read current task state before updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tallhamn/wrike) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/tallhamn) <br>
- [claw-wrike npm package](https://www.npmjs.com/package/claw-wrike) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use the `claw-wrike` binary and require `WRIKE_TOKEN`; mutating commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
