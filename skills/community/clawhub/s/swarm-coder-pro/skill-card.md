## Description: <br>
Swarm Coder Pro guides AI agents through clustered software development with parallel task scheduling, budget controls, multi-layer review, auto-fix loops, multi-role collaboration, and rollback workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to configure and guide AI-agent-assisted development workflows for larger coding efforts that need task decomposition, parallel execution planning, staged review, cost monitoring, and rollback planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite agent configuration files under .swarm. <br>
Mitigation: Install only in repositories where automatic agent edits are acceptable; commit or back up current work and review existing .swarm files before running setup commands. <br>
Risk: Automatic rollback behavior can change repository state without enough user control. <br>
Mitigation: Disable autoRollback until tested, then review checkpoint and rollback settings before enabling it in active repositories. <br>
Risk: Callback URLs or credential directories may expose data depending on the surrounding agent platform. <br>
Mitigation: Avoid callback URLs and credential directories unless the expected data flow and storage behavior are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/swarm-coder-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .swarm prompts, configuration, reports, logs, checkpoints, and metrics when followed by an agent with write or exec access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
