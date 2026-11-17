## Description:

Xiaohongshu viral content data insight tool for querying viral posts, analyzing category trends, and exporting example engagement data for content creation and creative research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and content analysts use this skill to explore Xiaohongshu viral-post patterns, compare engagement signals, generate trend reports, and export reference datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Report and export scripts can write to user-selected output paths without overwrite confirmation.

Mitigation: Choose output paths deliberately, use a scratch directory for generated files, and avoid paths containing important existing files.

Risk: The included scripts use mock/demo data, so generated insights may not reflect current Xiaohongshu activity.

Mitigation: Treat script output as example analysis unless the skill is connected to a trusted, current data source.

## Reference(s):

- [Xiaohongshu Insight ClawHub release](https://clawhub.ai/openlark/skills/xiaohongshu-insight)
- [OpenLark publisher profile](https://clawhub.ai/user/openlark)
- [Data Schema](references/data_schema.md)
- [Viral Criteria](references/viral_criteria.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, terminal tables, JSON, CSV, and XLSX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces mock/demo trend reports and exports through local scripts; output files may overwrite existing paths if reused.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
