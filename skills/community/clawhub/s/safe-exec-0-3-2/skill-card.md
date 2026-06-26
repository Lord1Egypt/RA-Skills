## Description: <br>
Safe Exec provides command execution oversight for OpenClaw agents by detecting dangerous shell-command patterns, assigning risk levels, requesting user approval for risky operations, and writing audit logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lucky-2968](https://clawhub.ai/user/Lucky-2968) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to add a local approval workflow around shell commands that may delete data, modify system state, or otherwise require human oversight. It is intended for OpenClaw agent sessions where command risk assessment, pending-request management, and audit logging are useful safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approval controls can be bypassed or weakened through context-based risk downgrades, non-interactive approval skipping, auto-confirm environment variables, or the global disable behavior. <br>
Mitigation: Do not rely on the skill as a strong safety boundary until those bypass paths are removed or restricted; install only where the prompts, environment variables, and approval flow are controlled. <br>
Risk: Bundled monitoring and publishing documents or tools are outside the core safety-wrapper behavior. <br>
Mitigation: Review and scope those files separately before deployment, and deploy only the components required for the intended command-approval workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lucky-2968/safe-exec-0-3-2) <br>
- [Safe Exec documentation listed in artifact](https://github.com/OTTTTTO/safe-exec/blob/master/README.md) <br>
- [Issue tracker listed in artifact](https://github.com/OTTTTTO/safe-exec/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local pending-request files, audit-log entries, and command approval or rejection instructions during use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact documentation identifies Safe Exec 0.3.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
