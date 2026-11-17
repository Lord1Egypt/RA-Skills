## Description:

Use this skill when the user needs public business emails, phone numbers, social profiles, source URLs, and crawl diagnostics from website domains or URLs through the Website Email Scraper & Phone Finder Apify actor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hundevmode](https://clawhub.ai/user/hundevmode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and lead-enrichment teams use this skill to run website-domain contact extraction through Apify, control crawl and spend settings, and return structured contact rows for CRM, spreadsheet, database, BI, or agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target website domains, scrape settings, and collected public contact data are sent to Apify.

Mitigation: Use the skill only for lawful, user-approved contact extraction and confirm that Apify data handling is acceptable for the intended workflow.

Risk: The skill defaults to collecting personal contact data.

Mitigation: Set includePersonalData=false unless collecting person-like emails or personal profile URLs is explicitly needed and approved.

Risk: Apify token handling can expose credentials when tokens are passed on the command line.

Mitigation: Provide APIFY_TOKEN through a protected environment variable and avoid --apify-token in command history or logs.

Risk: Runs may incur Apify usage charges.

Mitigation: Set a budget limit with --budget-usd or maxTotalChargeUsd before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hundevmode/skills/website-email-scraper-apify)
- [Project homepage](https://github.com/hundevmode/apify-website-email-scraper-agent-skill)
- [Apify actor store page](https://apify.com/x_guru/website-email-phone-finder)
- [Apify actor console source](https://console.apify.com/actors/kWfD7C0WpHtIt8VAh/source)
- [Input and output contract](references/input-output-contract.md)
- [Sample input](references/sample_input.json)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and structured JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns website contact rows, crawl diagnostics, input settings used, item counts, actor ID, and fetch timestamp.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
