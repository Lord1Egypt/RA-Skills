## Description:

Analyzes plant images, optional environmental readings, and growth metrics to produce a 0–100 vitality score and a recent trend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Gardeners and plant-monitoring operators use the skill to assess plant vitality from images and optional environmental or growth data, and to review historical reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious with high confidence, citing account, credential, and media-handling behavior that does not clearly match its plant-analysis purpose; scan coverage was partial because a referenced local path could not be resolved.

Mitigation: Review the account registration, credential handling, remote media upload, and export-only behavior, and resolve the missing scan path before installation; defer use until these concerns are clarified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-plant-vitality-index-analysis)
- [Plant vitality API documentation](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [JSON, Markdown]

**Output Format:** [Structured JSON analysis reports and Markdown report lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include an overall score, grade, trend, sub-scores, alerts, and report links. A single image may not support a trend.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata; artifact SKILL.md frontmatter lists 1.0.23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
