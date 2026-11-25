## Description:

Audits live webpages against a 12-point SEO checklist and creates a visual HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tutorgpt-io](https://clawhub.ai/user/tutorgpt-io)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams and website developers use the skill to audit live production or test pages before publishing and review a visual report of SEO issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional keyword-difficulty validation may send a page-derived keyword to an external service.

Mitigation: Review the data transfer before enabling keyword validation; skip it for private or staging pages, or use a non-sensitive keyword.

Risk: The security scan was partial because one local reference could not be resolved.

Mitigation: Review the unresolved reference and reassess the skill before installing or using it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/tutorgpt-io/skills/seo-checker)
- [Server-resolved source repository](https://github.com/tutorgpt-io/tutorgpt-skills/tree/main/skills/seo/page-seo-checker)
- [SEO checklist](references/seo-checklist.md)
- [HTML report template](references/report-template.html)

## Skill Output:

**Output Type(s):** [Analysis, Files, Guidance]

**Output Format:** [SEO audit findings and a standalone HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a live page URL and brand name; keyword-difficulty validation is optional.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
