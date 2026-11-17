## Description:

TaskMaster breaks down complex work, assigns model tiers by task complexity, spawns sub-agents for parallel execution, tracks progress, and manages token budgets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlwrow](https://clawhub.ai/user/jlwrow)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use TaskMaster to coordinate multi-step research, development, analysis, and documentation work while selecting lower-cost model tiers for simpler tasks and reserving higher-cost models for complex work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task descriptions and cost history can be written to a local plaintext cost log.

Mitigation: Do not include credentials, customer data, proprietary code, or confidential incident details in delegated task descriptions unless local logging has been reviewed and accepted.

Risk: Budget controls are advisory and may not prevent duplicate or parallel spending overruns.

Mitigation: Use external spending limits or manual review for high-cost workflows, and treat TaskMaster budget checks as planning guidance rather than an enforced control.

Risk: Delegated work may be sent to isolated sub-agents for execution.

Mitigation: Review task prompts before delegation and avoid sending sensitive material to sub-agents unless that routing is approved for the data involved.

## Reference(s):

- [TaskMaster ClawHub release](https://clawhub.ai/jlwrow/skills/taskmaster)
- [Model Selection Rules](references/model-selection-rules.md)
- [Task Templates](references/task-templates.md)
- [Token Tracking Guide](TOKEN_TRACKING_README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON spawn-command payloads, Python code examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local taskmaster-costs.json cost log when token tracking is used.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
