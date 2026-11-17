## Description:

Research trending topics, tweets, user profiles, and conversations on X (Twitter) using twitterapi.io for insights and trend reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xartex](https://clawhub.ai/user/0xartex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to query X/Twitter data through twitterapi.io and compile Markdown trend reports, especially for Solana ecosystem monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a twitterapi.io API key and sends search terms and account lookups to that provider.

Mitigation: Install only if that data flow is acceptable, keep TWITTERAPI_KEY in local secrets, and avoid submitting sensitive queries.

Risk: API calls may incur usage costs.

Mitigation: Review the query cadence and provider pricing before running recurring reports.

Risk: The helper script writes reports to a local output directory.

Mitigation: Choose or review the output directory before execution when report location or filenames matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xartex/skills/x-research-skill)
- [twitterapi.io API](https://api.twitterapi.io)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and API JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a twitterapi.io API key; the helper script writes timestamped local Markdown reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
