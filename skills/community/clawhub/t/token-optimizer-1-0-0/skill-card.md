## Description: <br>
Token Optimizer is a workflow-control skill that guides agents through pre-checks, path validation, progress checkpoints, and error triage to reduce repeated work and token waste. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smxtx](https://clawhub.ai/user/smxtx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to structure troubleshooting and implementation work with pre-flight checks, checkpointing, log review, and fast error localization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes process stop, kill, restart, and cleanup guidance that could disrupt unrelated local services. <br>
Mitigation: Require explicit approval before any process-control command and verify the exact process ID, executable path, and ownership before terminating anything. <br>
Risk: The skill may inspect local ports, processes, files, and logs during troubleshooting. <br>
Mitigation: Limit diagnostics to the intended system and avoid exposing secrets or unrelated personal data from files and logs. <br>
Risk: Shell-interpolated diagnostic examples can be unsafe if untrusted names, ports, or paths are inserted directly. <br>
Mitigation: Validate and quote command inputs, prefer read-only inspection first, and review generated commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smxtx/token-optimizer-1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/smxtx) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists, code examples, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local diagnostic commands and process-management steps that require user review before execution.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
