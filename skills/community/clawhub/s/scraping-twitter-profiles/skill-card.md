## Description:

Scrapes Twitter/X profile data for lists of usernames using API Dojo's Twitter User scraper on Apify, returning account metadata such as display name, bio, follower counts, verification status, profile URL, and join date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, data analysts, and market researchers use this skill to collect and export Twitter/X profile metadata for account lists, enrichment workflows, and profile checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: REST examples place the Apify token in request URLs, which can expose credentials through shell history, logs, or shared command transcripts.

Mitigation: Use an official Apify client, MCP server, or Authorization header; prefer a limited Apify token and avoid sharing logs that contain commands.

Risk: Follower, following, and retweeter collection can broaden the amount of account graph data processed by Apify.

Mitigation: Review collection options before use and enable graph extraction only when it is necessary for the approved workflow.

Risk: Submitted handles, profile URLs, and scraped results are processed by Apify and may include sensitive or regulated account lists.

Mitigation: Avoid submitting sensitive account lists unless approved, and handle exported datasets according to the user's data governance requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-twitter-profiles)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables, JSON examples, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide CSV or JSON export of scraped profile datasets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
