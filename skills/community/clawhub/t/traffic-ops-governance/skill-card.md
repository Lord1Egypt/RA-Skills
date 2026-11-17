## Description:

Governa como agentes de trafego operam Meta Ads com seguranca, padrao de aprovacao, auditoria de mudancas e limites claros para o MCP brijr/meta-mcp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moskoweb](https://clawhub.ai/user/moskoweb)

### License/Terms of Use:

MIT-0

## Use Case:

Traffic operations teams and agent developers use this skill to govern Meta Ads work through brijr/meta-mcp with approval gates, change limits, and audit-ready response structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: No-approval budget changes and pause or resume actions can affect live ad delivery and spend.

Mitigation: Review the autonomous action limits before use, especially the 10% budget increase cap, 24-hour window, and conditions for stable assets.

Risk: Incorrect tracking or incomplete account context can reduce confidence in operational recommendations.

Mitigation: Confirm ad account, business objective, analysis window, tracking reliability, and review deadline before execution.

Risk: Structural Meta Ads changes can combine multiple variables and make results hard to interpret.

Mitigation: Require explicit approval for objective, tracking, audience, architecture, activation, and budget changes above the documented limits.

## Reference(s):

- [Operating Principles](artifact/references/operating-principles.md)
- [Approval Matrix](artifact/references/approval-matrix.md)
- [Change Policy](artifact/references/change-policy.md)
- [Naming Conventions](artifact/references/naming-conventions.md)
- [Safety Checklists](artifact/references/safety-checklists.md)
- [brijr/meta-mcp Tool Policy](artifact/references/brijr-meta-mcp-tool-policy.md)
- [ClawHub Skill Page](https://clawhub.ai/moskoweb/skills/traffic-ops-governance)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with structured sections and optional tool-use or command recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses separate context, observed facts, hypotheses, recommended action, approval status, and post-change audit details when execution occurs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
