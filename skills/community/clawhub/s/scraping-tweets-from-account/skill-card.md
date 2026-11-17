## Description:

Scrapes tweets, replies, and media from public Twitter/X accounts using apidojo's Tweet scraper on Apify and returns tweet text, engagement counts, media URLs, and timestamps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, journalists, researchers, competitive analysts, and data engineers use this skill to collect and export public Twitter/X account timelines for analysis, reporting, or downstream datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents REST examples that place the Apify token in query strings.

Mitigation: Prefer header-based authentication or the official Apify client, and use a limited, rotatable Apify token.

Risk: Requested handles, search filters, and scraped results are sent to Apify.

Mitigation: Confirm that third-party processing is acceptable for the use case and avoid submitting sensitive or unnecessary query data.

Risk: The documented scraping scope is broader than account-only collection.

Mitigation: Review selected filters and collection scope before each run, and ensure use complies with applicable platform, privacy, and organizational policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-tweets-from-account)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with bash examples and optional JSON or CSV dataset outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return tweet timeline summaries and saved JSON or CSV datasets when an Apify token and actor runner are available.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata.version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
