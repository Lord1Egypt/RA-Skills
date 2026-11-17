## Description:

Xuanself guides agents through Russia medical-device market research using multilingual search, patient data, government monitoring, and professional Word report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxuan1992asia-svg](https://clawhub.ai/user/wangxuan1992asia-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Commercial teams, country managers, and market research analysts use this skill to assemble Russia-focused medical-device market reports with current news, patient statistics, government activity, tender data, pricing signals, and a structured Word deliverable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad web, command, and file authority.

Mitigation: Review and run it in an isolated Python environment with only the files and network access required for the report.

Risk: The configuration flow encourages storing API keys in data/data_sources.json.

Mitigation: Use secret management or local-only configuration, avoid committing real keys, and rotate any key that was stored in shared files.

Risk: The report runner can load exporter code from a sibling report-gama directory.

Mitigation: Inspect and trust the installed sibling directory before running exports, or use a pinned reviewed exporter.

Risk: Search queries and source collection may share business-sensitive research topics with third-party services.

Mitigation: Avoid confidential queries, review third-party service terms, and verify generated source citations before distribution.

Risk: Generated report files may be written to paths controlled by local configuration.

Mitigation: Confirm output paths before execution and review generated DOCX files before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxuan1992asia-svg/skills/xuanself)
- [Project homepage from metadata](https://github.com/workbuddy/xuanself)
- [SerpAPI](https://serpapi.com)
- [IDF Diabetes Atlas](https://diabetesatlas.org)
- [IDF Diabetes Atlas: Russian Federation](https://diabetesatlas.org/data-by-location/country/russian-federation/)
- [Russian Ministry of Health](https://minzdrav.gov.ru)
- [National Medical Research Center for Endocrinology](https://www.endocrincentr.ru)
- [Russian National Procurement System](https://zakupki.gov.ru)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance]

**Output Format:** [Structured report guidance, Markdown report content, and DOCX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied API keys for best search coverage and may use external web data sources.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
