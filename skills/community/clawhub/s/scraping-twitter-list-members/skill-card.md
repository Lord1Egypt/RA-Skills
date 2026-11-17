## Description:

Scrapes members and profile metadata from public Twitter/X lists using apidojo's Twitter List scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and intelligence or outreach teams use this skill to export public Twitter/X list members and profile fields for list-based research, curation, and audience workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify API tokens may appear in URLs, command history, logs, or shared transcripts when token-in-URL examples are used.

Mitigation: Prefer MCP or header-based authentication, use a narrowly scoped Apify token, and rotate the token if exposure is possible.

Risk: List URLs and scraped public profile data are processed by Apify/apidojo as a third-party service.

Mitigation: Use the skill only for public Twitter/X lists the user is authorized to process, and apply applicable privacy, retention, and third-party data handling policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-twitter-list-members)
- [ClawHub publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify actor: apidojo/twitter-list-scraper](https://apify.com/apidojo/twitter-list-scraper)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, API Calls, Files]

**Output Format:** [Markdown table with inline shell commands and optional CSV or JSON dataset files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Apify token and returns public list member profile fields such as username, bio, follower count, location, and verification status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
