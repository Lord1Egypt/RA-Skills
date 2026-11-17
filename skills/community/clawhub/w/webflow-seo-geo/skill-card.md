## Description:

End-to-end workflow for SEO/GEO content updates in Webflow: prioritize via GSC, draft/refresh content, create patch JSONs, update Webflow CMS via API, set images/alt/SEO, publish, and handle technical SEO fixes (canonical domain, redirects).

This skill is ready for commercial/non-commercial use.

## Publisher:

[jchopard69](https://clawhub.ai/user/jchopard69)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and site operators use this skill to plan SEO and location-page updates, draft Webflow CMS payloads, and coordinate API-based content publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to prepare and publish Webflow CMS changes through an API, which can alter public site content.

Mitigation: Require manual review before any publish call, prefer a staging or draft workflow first, and use a least-privilege Webflow token.

Risk: Generated patch files may contain incorrect content, metadata, image fields, or item identifiers.

Mitigation: Keep generated /out/ patch files under review and validate JSON payloads before POST or PATCH requests.

## Reference(s):

- [Webflow API v2 quick reference](references/webflow_api.md)
- [SEO/GEO copy patterns](references/seo_copy_patterns.md)
- [Patch templates](references/patch_templates.md)
- [Webflow API v2](https://api.webflow.com/v2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload examples and inline API command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local patch JSON files for review before Webflow CMS updates or publish calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
