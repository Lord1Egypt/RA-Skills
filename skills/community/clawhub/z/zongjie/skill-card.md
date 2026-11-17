## Description:

将重要事件和问题解决过程整理成结构化记忆文档，便于后续查阅、复盘和经验沉淀。

This skill is ready for commercial/non-commercial use.

## Publisher:

[marklyk](https://clawhub.ai/user/marklyk)

### License/Terms of Use:


## Use Case:

Agents and users use this skill after troubleshooting, configuration changes, important decisions, or debugging work to decide whether an event is worth saving and to produce a structured memory entry with priority, layer, root cause, steps, key details, result, and lessons learned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory entries may capture sensitive content or prompt-like instructions.

Mitigation: Review and sanitize proposed entries before saving, especially P0/L0 or shared entries; avoid raw logs, tokens, passwords, private URLs, customer data, and untrusted instruction-like text.

Risk: Broad memory-writing guidance may preserve incorrect or misleading operational rules.

Mitigation: Confirm that the proposed priority, memory layer, save location, and summary content are appropriate before writing or sharing the memory entry.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marklyk/skills/zongjie)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown memory entry with optional shell commands and a brief save confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Classifies entries by P0/P1/P2 priority and L0/L1/L2 memory layer.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
