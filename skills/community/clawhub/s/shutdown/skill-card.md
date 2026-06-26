## Description: <br>
Safe shutdown and reboot workflow for local or remote machines that helps an agent power off, restart, schedule, cancel, and run pre-shutdown checks with explicit confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to prepare, confirm, and issue local or remote shutdown, reboot, scheduling, or cancellation commands while checking session and process impact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shutdown or reboot commands can disconnect sessions and terminate running processes if confirmed for the wrong target or timing. <br>
Mitigation: Verify the target machine, timing, exact command, session and process impact, and cancellation path before confirming execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jvy/shutdown) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown with platform-specific command examples and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers macOS, Linux, and Windows; requires explicit user confirmation before disruptive commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
