## Description: <br>
Workspace boundary enforcement and file operation safety checks. Use before ANY file operation (read, write, edit, exec, delete) to: (1) Validate paths are within ~/openclaw workspace, (2) Confirm user permission for sensitive operations, (3) Check file operation safety, (4) Prevent unauthorized access outside workspace boundaries, or (5) Audit file access patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dougchambes](https://clawhub.ai/user/dougchambes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to check workspace boundaries before file operations, classify risky operations, request permission for sensitive actions, and handle blocked access attempts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reference guidance includes an unsafe path-expansion example. <br>
Mitigation: Replace eval-based path expansion with safe path handling before relying on the pattern. <br>
Risk: Audit-log storage guidance is inconsistent with the intended workspace boundary. <br>
Mitigation: Configure audit logs inside the intended workspace and define retention controls before deployment. <br>
Risk: The skill can block or request approval for legitimate file operations if the workspace root is not configured for the target machine. <br>
Mitigation: Review and set the workspace root explicitly for each environment before installation. <br>


## Reference(s): <br>
- [Workspace Boundaries Reference](artifact/references/boundaries.md) <br>
- [ClawHub skill page](https://clawhub.ai/dougchambes/workspace-guard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include path checks, operation classifications, permission prompts, and violation-handling messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
