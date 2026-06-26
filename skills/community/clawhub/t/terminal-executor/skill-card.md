## Description: <br>
Executes local terminal commands, including sudo-prefixed commands, and returns command output and status details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[choasx](https://clawhub.ai/user/choasx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill when they intentionally want an agent to run local shell commands, inspect system state, install software, or perform terminal-based tasks. It is appropriate only where command execution has been reviewed and the environment can tolerate unrestricted local shell access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run unrestricted local terminal commands, including sudo-prefixed commands. <br>
Mitigation: Use only in a sandbox or low-risk environment, review every command before execution, and avoid unattended use on systems with sensitive files, credentials, or important workloads. <br>
Risk: Incorrect or destructive commands could modify or delete local files or disrupt important workloads. <br>
Mitigation: Require confirmation for sensitive operations and restrict use to environments where command side effects are acceptable. <br>


## Reference(s): <br>
- [Terminal Executor on ClawHub](https://clawhub.ai/choasx/terminal-executor) <br>
- [choasx publisher profile](https://clawhub.ai/user/choasx) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [JSON-like command result with success, stdout, stderr, error, and command fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command execution uses the provided working directory, environment overrides, and timeout options when supplied.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact package files show 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
