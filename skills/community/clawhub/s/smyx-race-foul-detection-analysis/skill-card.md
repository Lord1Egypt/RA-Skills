## Description:

Analyzes pet race videos to identify start times, finish order, lane assignments, and possible false starts or lane crossings for referee review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Race stewards and event operators use this skill to review start or finish video for false starts and lane crossings, and to look up historical analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags account, identity, and credential handling beyond the stated race-video task, as well as unclear privacy and control practices.

Mitigation: Clarify which service receives video and what is stored locally, and resolve the account and credential behavior before installation.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured JSON analysis results and Markdown report lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes race-foul judgments and report links when available.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
