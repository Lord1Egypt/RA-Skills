## Description:

Extracts structured data from web pages with CSS selectors or XPath, supports batch scraping and automatic pagination, and exports results as CSV, JSON, or Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[careytian-ai](https://clawhub.ai/user/careytian-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to collect public web data for market research, competitor analysis, content aggregation, data analysis, sentiment monitoring, and SEO analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports undocumented local command-execution authority beyond the documented scraping and export workflow.

Mitigation: Review requested permissions before installation and prefer a version that removes exec unless command execution is explicitly needed.

Risk: Bulk scraping and automatic pagination can create unwanted site load or collect data outside the intended scope.

Mitigation: Limit collection to public data, respect robots.txt, use conservative concurrency and delays, and confirm target URLs before running.

Risk: Exported CSV, JSON, or Markdown files may contain sensitive or unwanted scraped content.

Mitigation: Review extracted fields before sharing and write outputs only to expected user-approved locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/careytian-ai/skills/web-data-extractor)
- [Publisher profile](https://clawhub.ai/user/careytian-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration]

**Output Format:** [CSV, JSON, Markdown tables, and concise extraction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write exported datasets to user-approved paths; batch fetching should respect robots.txt and conservative rate limits.]

## Skill Version(s):

1.0.0 (source: CHANGELOG.md, config.json, metadata.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
