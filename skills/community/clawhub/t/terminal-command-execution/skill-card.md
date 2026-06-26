## Description: <br>
Execute terminal commands safely and reliably with clear pre-checks, output validation, and recovery steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[big-fox](https://clawhub.ai/user/big-fox) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to have an agent inspect terminal state, run shell commands incrementally, diagnose failures, and verify results while minimizing risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terminal commands can change files, install software, or affect services. <br>
Mitigation: Review proposed commands before execution and prefer scoped, incremental commands with explicit outcome verification. <br>
Risk: Privileged, destructive, or broad filesystem commands can cause unintended changes. <br>
Mitigation: Require explicit user approval for deletion, force flags, chmod/chown, sudo, package installation, service changes, networking, or broad filesystem changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/big-fox/terminal-command-execution) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command summaries, validation steps, and recovery instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
