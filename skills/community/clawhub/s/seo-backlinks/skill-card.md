## Description:

Backlink profile analysis: referring domains, anchor text distribution, toxic link detection, competitor gap analysis. Works with free APIs (Moz, Bing Webmaster, Common Crawl) and DataForSEO extension. Use when user says backlinks, link profile, referring domains, anchor text, toxic links, link gap, link building, disavow, or backlink audit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and SEO practitioners use this skill to audit backlink profiles, identify toxic links, compare competitor link gaps, verify known backlinks, and produce source-labeled backlink recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured SEO providers may receive target domains, backlink lists, or related site data.

Mitigation: Use approved providers, avoid sensitive internal targets, and review provider terms before sharing backlink data.

Risk: Optional setup or extension install commands may change the agent environment.

Mitigation: Review setup commands before execution and install only trusted extensions or API integrations.

Risk: Free or partial data sources can produce incomplete backlink coverage and misleading health scores.

Mitigation: Preserve source labels and insufficient-data notices, and require enough supported factors before reporting numeric scores.

Risk: The skill suggests an automatic PDF report after analysis, which may be promotional rather than necessary for the task.

Mitigation: Treat report generation as optional and confirm user intent before invoking related commands.

## Reference(s):

- [Bing Webmaster Tools](https://www.bing.com/webmasters)
- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/seo-backlinks)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, findings, recommendations, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source confidence labels, insufficient-data notices, setup guidance, and optional PDF-report guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
