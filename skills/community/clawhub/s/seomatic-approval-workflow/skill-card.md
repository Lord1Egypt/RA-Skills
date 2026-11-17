## Description:

Operate SEOmatic's human-gated execution loop from chat - inspect staged proposals with full evidence, record the user's approve/dismiss decisions, watch execution, and undo with rollback if needed. Use when the user wants to review pending SEO work, approve tasks, check what the agent did, or revert a change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minh42](https://clawhub.ai/user/minh42)

### License/Terms of Use:

MIT-0

## Use Case:

SEO professionals and site owners use the skill to review proposed site changes against search performance evidence, record their approval or dismissal, monitor execution, and roll back a change when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Noindex and redirect changes can remove pages from search results or reroute ranking value, and may take weeks to reverse.

Mitigation: Show the exact URL and consequence, then require the user's explicit confirmation before applying a destructive change.

Risk: Executing approved changes and recording decisions require a paid plan and may incur execution credits.

Mitigation: Explain the stated cost and plan requirement before recording a decision or executing a change.

## Reference(s):

- [SEOmatic](https://app.seomatic.ai)
- [SEOmatic skill release on ClawHub](https://clawhub.ai/minh42/skills/seomatic-approval-workflow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text and Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task evidence, decision and execution status, and before-and-after details when available.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
