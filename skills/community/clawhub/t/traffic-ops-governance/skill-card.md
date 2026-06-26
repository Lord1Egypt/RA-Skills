## Description: <br>
Governs how traffic agents operate Meta Ads with safety, approval standards, change auditability, and clear limits for the brijr/meta-mcp server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moskoweb](https://clawhub.ai/user/moskoweb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and operations teams use this skill to govern Meta Ads account work through brijr/meta-mcp. It helps agents classify actions, request approval when needed, preserve audit records, and avoid unsafe campaign, tracking, billing, permission, or deletion changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent could make Meta Ads changes that affect spend, delivery, tracking, or campaign structure. <br>
Mitigation: Apply the approval matrix: keep new campaigns paused, cap autonomous budget increases at 10% per 24 hours, require approval for structural or tracking changes, and record an audit entry after execution. <br>
Risk: An agent could exceed the intended operational scope or attempt sensitive account administration. <br>
Mitigation: Use only explicitly listed brijr/meta-mcp tools, keep deletion, billing, permissions, and business settings out of scope, and configure least-privileged Meta Ads credentials. <br>
Risk: Weak or suspect tracking could lead to overconfident recommendations. <br>
Mitigation: Check account setup and tracking before execution, lower diagnostic confidence when signals conflict, and prefer controlled experiments with a defined review window. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/moskoweb/traffic-ops-governance) <br>
- [Operating Principles](references/operating-principles.md) <br>
- [Approval Matrix](references/approval-matrix.md) <br>
- [Change Policy](references/change-policy.md) <br>
- [Naming Conventions](references/naming-conventions.md) <br>
- [Safety Checklists](references/safety-checklists.md) <br>
- [brijr/meta-mcp Tool Policy](references/brijr-meta-mcp-tool-policy.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown response sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured operational guidance with context, observed facts, hypotheses, recommended action, approval status, and post-change audit notes when execution occurs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
