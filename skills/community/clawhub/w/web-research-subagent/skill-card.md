## Description:

Web research and synthesis workflow for making an agent or subagent smarter before it acts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nevilpaulo](https://clawhub.ai/user/nevilpaulo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent builders use this skill to plan and synthesize web research before implementation, advice, or delegated subagent work. It is useful when tasks need current web knowledge, source evaluation, citations, or compact research handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts or web queries may expose sensitive private context if delegated without care.

Mitigation: Do not include sensitive private context in delegated research prompts or web queries unless it is necessary for the user's task.

Risk: Web results can be outdated, low quality, or affected by prompt-injection content.

Mitigation: Prefer primary sources, read sources before relying on them, cite claims near their evidence, and treat fetched web pages as untrusted data.

## Reference(s):

- [Source Quality Checklist](references/source-quality.md)
- [Research Patterns](references/research-patterns.md)
- [Web Research Subagent on ClawHub](https://clawhub.ai/nevilpaulo/skills/web-research-subagent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown research briefs, handoffs, recommendations, and inline commands or configuration when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes citations, risks, unknowns, and recommended next actions when research evidence supports them.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
