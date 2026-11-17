## Description:

Generates verifiable business metrics, charts, and reports from CSV or XLSX data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and analysts use this skill to inspect CSV or XLSX files, calculate checked metrics and charts, and generate or export business reports with clearly identified limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected CSV or XLSX business files are uploaded to a remote reporting service.

Mitigation: Upload only files you are comfortable sharing with that service.

Risk: Exposing an API key or overriding the service URL may compromise credentials or send data to an unintended endpoint.

Mitigation: Configure keys through OpenClaw environment settings, do not paste full keys into chat, and verify any custom service URL; use a product-scoped key for tighter separation.

Risk: Partial results may be mistaken for a complete interpreted report.

Mitigation: Clearly label partial results and report only verified metrics and available deterministic content.

## Reference(s):

- [Report Generation on ClawHub](https://clawhub.ai/youteacher/skills/report-generation)
- [AI Skills platform](https://ai-skills.open-idea.net)
- [API key configuration](https://ai-skills.open-idea.net/skill-docs/report-generation/API-KEY.md)
- [HTTP requests and uploads](https://ai-skills.open-idea.net/skill-docs/report-generation/HTTP-REQUESTS.md)
- [Report operations and exports](https://ai-skills.open-idea.net/skill-docs/report-generation/OPERATIONS.md)
- [Validation and interpretation boundaries](https://ai-skills.open-idea.net/skill-docs/report-generation/BEHAVIOR-RULES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Report text and optional Markdown, XLSX, PNG, or PDF exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes checked metrics and charts; partial results identify missing narrative interpretation.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
