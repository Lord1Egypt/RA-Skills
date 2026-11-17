## Description:

Provides agent-guided access to Google Search Console, PageSpeed Insights, CrUX, Indexing API, GA4, YouTube, Natural Language, Keyword Planner, Knowledge Graph, and Web Risk data for SEO analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers, SEO practitioners, and site operators use this skill to collect Google-sourced SEO, performance, indexation, traffic, and content signals and turn them into analysis reports or follow-up commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured Google credentials can grant access to Search Console, GA4, Indexing API, and other Google APIs for specific properties.

Mitigation: Use a dedicated Google Cloud project and service account, restrict API keys, avoid Owner access unless Indexing API operations require it, and set credential files to owner-only permissions.

Risk: Optional paid or broader Google APIs may increase account exposure or cost when enabled.

Mitigation: Enable only the APIs needed for the task, review quotas before use, and confirm credential tiers before running commands.

## Reference(s):

- [Google API Authentication Setup](artifact/references/auth-setup.md)
- [PageSpeed Insights v5 + CrUX API Reference](artifact/references/pagespeed-crux-api.md)
- [Google Search Console API Reference](artifact/references/search-console-api.md)
- [Google Indexing API v3 Reference](artifact/references/indexing-api.md)
- [GA4 Data API v1beta Reference](artifact/references/ga4-data-api.md)
- [Google API Rate Limits & Quotas](artifact/references/rate-limits-quotas.md)
- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/seo-google)
- [ClawHub publisher profile](https://clawhub.ai/user/asale-ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Google SEO report files and JSON-backed analyses when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version is 2.2.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
