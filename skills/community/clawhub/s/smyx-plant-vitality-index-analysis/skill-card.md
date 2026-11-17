## Description:

Analyzes plant images, environmental data, and growth metrics to produce a 0–100 vitality score and a rising, stable, or declining trend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Home gardeners and plant-monitoring teams use the skill to review plant vitality from images and optional environmental or growth data. It summarizes condition as a score and trend for care tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious, citing account and credential handling, local persistence, selected media uploads without clear disclosure, and possible mismatch with the advertised task; scan coverage is partial.

Mitigation: Review the skill and its dependencies before installing, and use it only if its account handling, local persistence, and external media processing are acceptable. Avoid sending sensitive images or credentials.

## Reference(s):

- [Plant vitality API reference](artifact/references/api_doc.md)
- [Skill overview and demo](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-plant-vitality-index-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Structured vitality report with a score, grade, trend, and optional sub-scores or alert hint; JSON or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plant-care reference only. Single-image scores may vary with camera angle and lighting; consistent image sequences support trend assessment.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
