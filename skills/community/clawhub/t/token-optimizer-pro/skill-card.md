## Description:

Agent token usage optimizer. Input usage logs, transcript excerpts, model bills, or runtime traces; output token/cost breakdown, waste patterns, context compaction opportunities, caching suggestions, and before/after optimization actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and operations teams use this skill to analyze token usage, model costs, runtime logs, transcripts, and prompt templates, then identify practical ways to reduce waste while preserving task quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Usage logs, transcripts, runtime traces, and billing artifacts may contain secrets, personal data, or customer data.

Mitigation: Redact API keys, credentials, private customer data, and personal identifiers before using the skill.

Risk: External service use could disclose sensitive logs or transcripts if selected without review.

Mitigation: Use external service routes only after an explicit user choice and after sensitive data has been removed.

Risk: Cost estimates can be misleading when based on partial logs or unofficial billing summaries.

Mitigation: Treat estimates as approximate unless official billing exports are provided, and review recommendations before changing production routing or budgets.

## Reference(s):

- [Token Optimizer Pro on ClawHub](https://clawhub.ai/harrylabsj/skills/token-optimizer-pro)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown with cost and token breakdowns, waste patterns, optimization checklists, and before/after estimates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cost estimates are approximate unless official billing exports are provided; users should redact secrets, customer data, and personal identifiers before analysis.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
