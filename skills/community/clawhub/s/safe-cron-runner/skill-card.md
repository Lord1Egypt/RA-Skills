## Description: <br>
Executes background tasks safely by dropping privileges and enforcing timeouts, with an ISNAD signed manifest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horn111](https://clawhub.ai/user/horn111) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to run local background tasks with timeouts, privilege dropping, and structured execution logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local commands selected by the caller. <br>
Mitigation: Install it only for agents that need local command execution and use explicit trusted command lists. <br>
Risk: Command output previews are logged under /tmp and could expose sensitive data if a command prints secrets. <br>
Mitigation: Avoid commands that print secrets and treat the log file as sensitive operational data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/horn111/safe-cron-runner) <br>
- [ISNAD manifest](artifact/isnad_manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Logs] <br>
**Output Format:** [JSON execution result with status, duration, command, and stdout/stderr previews] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [stdout_preview and stderr_preview are truncated to 500 characters and appended to /tmp/safe_cron.log when logging succeeds.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
