## Description: <br>
Provides role-based access checks, input and output content review, sensitive-operation confirmation signals, and audit logging for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add permission checks, content-safety review, and audit logs around file, web, execution, and memory operations. It is best treated as a helper library that supports application-level security controls rather than as a complete enforcement boundary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan warns that the skill should not be relied on as a complete security boundary without review. <br>
Mitigation: Use it as a helper library, review role configuration in code, and pair it with independent enforcement controls before production use. <br>
Risk: High-risk operations can return requiresConfirmation and need application code to handle that state correctly. <br>
Mitigation: Handle confirmation fail-closed so operations do not proceed unless an explicit confirmation path approves them. <br>
Risk: Wildcard administrator roles and broad custom permissions can bypass fine-grained restrictions. <br>
Mitigation: Avoid wildcard admin roles in production and verify role policies before assigning them to users or agents. <br>
Risk: Audit logs may contain sensitive operational metadata and are written to a configurable local directory. <br>
Mitigation: Set a protected audit log directory and define retention so sensitive metadata is not kept longer than intended. <br>


## Reference(s): <br>
- [Security Guard on ClawHub](https://clawhub.ai/yuyonghao-123/yuyonghao-security-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces security-check results, audit report data, and implementation guidance for integrating the helper modules.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
