## Description:

Analyzes feedback logs to identify patterns and suggest improvements to review skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and review-skill maintainers use this skill to analyze structured review feedback logs, identify high-rejection rules, and draft evidence-bound improvements to review guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated recommendations could introduce incorrect or misleading review guidance if applied without review.

Mitigation: Review generated recommendations before applying them to review skills, especially proposed skill text changes.

Risk: Future automation concepts such as PR generation, long-term tracking, or experiments could affect review workflows if adopted without oversight.

Mitigation: Treat automation-oriented recommendations as proposals and scan or review any resulting skill changes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/review-skill-improver)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown report with tables, evidence pointers, and proposed skill text changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are gated by schema checks, aggregation, and evidence-bound rationale requirements.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
