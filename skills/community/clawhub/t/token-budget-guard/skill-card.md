## Description:

Automatically manages and compresses agent context to optimize token usage through summarization, selective loading, progressive disclosure, and token budgeting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep long-running AI agent sessions within context and cost budgets by compressing history, loading only relevant file sections, and escalating tool schema detail only when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Aggressive context compression may remove exact details needed for accuracy, reproducibility, or auditability during long sessions.

Mitigation: Ask the agent to preserve verbatim requirements, citations, identifiers, and final decisions before summarizing or dropping earlier context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aptratcn/skills/token-budget-guard)
- [README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)
- [Cost Tracking Template](artifact/COST_TRACKING_TEMPLATE.md)
- [codeburn](https://github.com/getagentseal/codeburn)
- [token-dashboard](https://github.com/nateherkai/token-dashboard)
- [OpenClaw](https://openclaw.ai)
- [Context Optimizer](https://github.com/aptratcn/openclaw-context-optimizer)
- [Error Recovery](https://github.com/aptratcn/skill-error-recovery)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code, shell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown-only skill with no runtime dependencies; includes a cost tracking template.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
