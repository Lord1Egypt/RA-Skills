## Description:

Skill Analytics monitors ClawHub skill performance, fetches public skill metrics, tracks recommendations, and avoids repeating prior suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tommot2](https://clawhub.ai/user/tommot2)

### License/Terms of Use:

MIT-0

## Use Case:

External skill publishers and developers use this skill to review public ClawHub performance metrics, track adoption recommendations, and rotate analysis focus across growth topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains local analytics state and may update files after a run.

Mitigation: Review the files under memory/skill-analytics/ before and after use, especially recommendations.md, ideas-tried.md, and state.json.

Risk: Analytics and recommendations are based on public ClawHub metrics and may be incomplete or stale.

Mitigation: Treat recommendations as planning guidance and verify important adoption or growth decisions against current ClawHub pages.

## Reference(s):

- [Skill Analytics on ClawHub](https://clawhub.ai/tommot2/skills/skill-analytics)
- [Skill Analytics homepage](https://clawhub.ai/skills/skill-analytics)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown analytics report with tables and concise recommendations; local JSON and Markdown state files may be updated.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps local state under memory/skill-analytics/ and limits reports to 40 lines.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
