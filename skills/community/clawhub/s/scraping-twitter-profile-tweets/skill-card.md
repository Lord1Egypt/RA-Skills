## Description:

Extracts tweets, reply threads, and engagement metrics from public Twitter/X profiles using Apify's apidojo/twitter-profile-scraper actor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, social media monitors, journalists, and competitive intelligence teams use this skill to collect tweet timelines, reply threads, engagement metrics, and author details from public Twitter/X profile handles for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Twitter/X profile queries and actor inputs are sent to Apify.

Mitigation: Use the skill only when Apify network execution is intended, use a dedicated Apify token, and avoid sending secrets or private data in inputs or custom mapping code.

Risk: Large or unconstrained profile scraping requests can increase cost and data volume.

Mitigation: Set maxItems, date ranges, or other filters before running the actor.

Risk: Private or suspended accounts may return no tweets or errors.

Mitigation: Check account visibility and handle actor errors before relying on the returned dataset.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-twitter-profile-tweets)
- [Apify actor REST API endpoint](https://api.apify.com/v2/acts/apidojo~twitter-profile-scraper/runs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides CSV or JSON export from Apify actor runs; maxItems and date filters can limit result volume.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
