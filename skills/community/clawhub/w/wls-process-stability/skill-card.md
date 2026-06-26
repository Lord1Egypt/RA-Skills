## Description: <br>
WLS runtime engineer skill for worker lifecycle, reload versus restart decisions, process cleanup, and runtime stability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiweline](https://clawhub.ai/user/aiweline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose WLS worker lifecycle issues, dispatcher behavior, reload-versus-restart decisions, process cleanup, and runtime-sensitive stability problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Process start, reload, restart, and stop commands can affect running WLS instances or the wrong port. <br>
Mitigation: Review process-control commands before running them, use a dedicated test instance on port 9502 or higher, avoid port 9501, use a unique instance name, and stop the instance after validation. <br>
Risk: Blocking calls or abrupt termination in runtime-sensitive code can destabilize workers. <br>
Mitigation: Avoid sleep, die, and exit inside WLS runtime-sensitive code, and validate worker behavior, cleanup, and stability after changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiweline/wls-process-stability) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown guidance with code or shell command examples when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes lifecycle impact, validation steps, and cleanup confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
