## Description: <br>
Web Notepad helps agents guide teams through enterprise form-management workflows, including batch operations, webhook setup, RBAC assignments, reusable templates, encrypted storage, exports, and audit-log review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business teams use this skill to draft and review form-service API workflows for approvals, data collection, webhook delivery, permissions, exports, and audit operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live API examples may create forms, change RBAC assignments, export submissions, or enable webhooks. <br>
Mitigation: Verify the API host and credential scope, use a sandbox first, and require explicit approval before executing curl commands. <br>
Risk: Security evidence marks this release suspicious because administrative examples and mixed security-review claims require human review. <br>
Mitigation: Complete a human security review before installation and operate with least-privilege credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/web-notepad) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with curl examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes examples for live form, webhook, export, and RBAC operations that require review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
