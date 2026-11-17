## Description:

Tracks Google search rankings and SERP features for any keyword using apidojo's Google Search scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

SEO managers, content strategists, and digital marketing teams use this skill to check keyword rankings, compare competitors, and identify Google SERP features such as featured snippets, People Also Ask, local packs, and ads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose an Apify token through the documented token-in-URL curl fallback.

Mitigation: Use MCP or a helper that sends the token in an Authorization header, and avoid logging URLs that contain credentials.

Risk: Search terms and ranking targets are sent to Apify when the actor runs.

Mitigation: Use the skill only for queries that are acceptable to share with Apify and avoid sensitive campaign or customer data unless approved.

Risk: The optional customMapFunction runs user-provided JavaScript transformations.

Mitigation: Do not pass customMapFunction code unless it has been reviewed and is fully trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/tracking-google-serp-rankings)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Files, Analysis]

**Output Format:** [Markdown ranking report with tables, optional CSV or JSON files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can summarize ranking positions, URLs, titles, snippets, SERP feature types, and competitor dominance metrics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
