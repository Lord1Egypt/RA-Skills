## Description:

Scrapes Instagram profile statistics and recent post metrics for lists of accounts using apidojo's Instagram scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and growth or research teams use this skill to collect Instagram profile statistics and recent post metrics for influencer vetting, brand research, and list enrichment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify tokens can be exposed by token-in-URL REST examples or logs.

Mitigation: Use a dedicated, least-privilege APIFY_TOKEN from the environment, prefer the helper or MCP flow, and avoid token-in-URL curl commands when possible.

Risk: Account and URL lists are sent to Apify for scraping.

Mitigation: Confirm the intended account or URL list before running the actor and avoid submitting unnecessary or sensitive lists.

Risk: Unbounded scraping can increase collection scope, cost, or operational risk.

Mitigation: Set explicit item limits such as maxItems and review requested output fields before execution.

Risk: customMapFunction can execute transformation logic in the actor workflow.

Mitigation: Avoid customMapFunction unless the actor and transformation code are trusted and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-instagram-profile-data)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify actor: apidojo/instagram-scraper](https://apify.com/apidojo/instagram-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and structured table output; exported datasets may be JSON or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses APIFY_TOKEN and can run through a Node helper, Apify MCP, or direct REST API calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
