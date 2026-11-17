## Description:

Scrapes YouTube channel statistics and video catalogs for channel URLs or handles using Apidojo's YouTube scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, analysts, and creator-research teams use this skill to collect YouTube channel metadata, subscriber and view counts, and recent video data for benchmarking, competitor analysis, and audience research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify tokens can be exposed by URL-based curl examples.

Mitigation: Use a dedicated least-privilege Apify token from a secret store or environment variable and avoid placing tokens in URLs, shell history, or logs.

Risk: YouTube identifiers and scrape results are sent to Apify.

Mitigation: Run the skill only with data you are permitted to process, minimize submitted channel inputs, and review the selected Apify actor before execution.

Risk: Actor names are inconsistent between the artifact metadata and usage examples.

Mitigation: Confirm the intended Apify actor before running commands or MCP calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-youtube-channel-data)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON input examples, and optional tabular channel dataset output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to produce JSON or CSV files when an output path and format are requested; requires an Apify token for live actor runs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
