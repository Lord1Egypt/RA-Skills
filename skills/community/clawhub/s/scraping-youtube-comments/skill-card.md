## Description:

Scrapes comments from YouTube videos using apidojo's YouTube scraper on Apify and returns commenter usernames, comment text, like counts, reply counts, and timestamps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, product teams, content teams, and researchers use this skill to collect YouTube comment text and engagement metadata for audience feedback and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-token handling examples may expose Apify credentials when tokens are placed in URLs.

Mitigation: Prefer Apify MCP or an Authorization header, keep APIFY_TOKEN in environment or secret storage, and use a limited Apify token.

Risk: The security summary reports scope mismatches for a skill intended for YouTube video comment scraping.

Mitigation: Review and narrow the skill before installation when only video comment scraping is needed.

Risk: Exported YouTube comment datasets may include personal data.

Mitigation: Treat exports as potentially personal data and apply appropriate access, retention, and sharing controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-youtube-comments)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and optional CSV or JSON datasets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return comment tables or saved CSV/JSON exports; exported comments may contain personal data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
