## Description: <br>
Manage TickTick tasks and projects from the command line with OAuth2 auth, batch operations, and rate limit handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Norickkevorkov](https://clawhub.ai/user/Norickkevorkov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, automation users, and agents use this skill to authenticate with TickTick and manage tasks or projects from the command line. It supports listing, creating, updating, completing, abandoning, and batch-abandoning tasks, with JSON output for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change TickTick tasks and projects through the authorized account. <br>
Mitigation: Review task and project commands before execution, use JSON output to verify targets, and confirm destructive operations such as complete, abandon, batch-abandon, and project updates. <br>
Risk: OAuth client secrets and tokens are stored in a local credential file. <br>
Mitigation: Use the skill only on trusted machines, keep the credential file private, and revoke the TickTick developer app or tokens when access is no longer needed. <br>
Risk: Bulk or repeated operations can hit TickTick API rate limits. <br>
Mitigation: Prefer batch operations where appropriate, avoid unnecessary polling loops, and allow retry/backoff behavior to complete before issuing more requests. <br>


## Reference(s): <br>
- [TickTick Developer Center](https://developer.ticktick.com/manage) <br>
- [TickTick Open API v1](https://developer.ticktick.com/api) <br>
- [ClawHub skill page](https://clawhub.ai/Norickkevorkov/ticktick-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI commands can emit JSON with --json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TickTick developer app and OAuth2 credentials; stores tokens locally for command execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json; package.json reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
