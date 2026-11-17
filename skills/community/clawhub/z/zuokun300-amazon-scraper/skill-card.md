## Description:

Scrapes Amazon product search data through Apify and generates structured Excel and Markdown reports with product details, brand summaries, and clickable links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuokun300](https://clawhub.ai/user/zuokun300)

### License/Terms of Use:

MIT

## Use Case:

E-commerce researchers, sellers, and analysts use this skill to collect Amazon product search results, compare competing products, and produce spreadsheet and Markdown summaries for market, pricing, and brand analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Amazon search terms and scraping activity are sent to Apify as part of the scraping workflow.

Mitigation: Use the skill only when that third-party processing is acceptable, and review the target site's terms and applicable scraping policies before running collection jobs.

Risk: The skill requires an Apify API key, and the artifact includes setup paths that could lead users to place the token directly in code.

Mitigation: Store the Apify token in an environment variable or secret manager, run the skill in an isolated virtual environment, and avoid hardcoding credentials.

Risk: Scheduled scraping can create unexpected third-party activity or costs.

Mitigation: Use the cron example only for intentional monitoring workflows, keep product limits modest, and monitor Apify account usage.

Risk: Generated spreadsheet and Markdown reports contain externally sourced product links and image links.

Mitigation: Treat generated reports as untrusted external-content files and review links before redistribution or automated processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zuokun300/skills/zuokun300-amazon-scraper)
- [zuokun300 publisher profile](https://clawhub.ai/user/zuokun300)
- [Apify account integrations](https://console.apify.com/account/integrations)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, plus generated Excel and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may include Amazon product titles, ASINs, inferred brands, product links, image links, and brand distribution summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
