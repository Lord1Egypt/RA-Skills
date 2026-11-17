## Description:

Searches Twitter/X with advanced query syntax, fetches tweet data through twitterapi.io, and helps agents produce data-driven social media analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyfoxci](https://clawhub.ai/user/flyfoxci)

### License/Terms of Use:


## Use Case:

Developers, analysts, and social media teams use this skill to collect Twitter/X search results, summarize engagement metrics, identify themes or influential accounts, and draft markdown reports with data-backed recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Twitter/X search queries and a twitterapi.io API key to a third-party API.

Mitigation: Use the skill only when that data sharing is acceptable, scope queries appropriately, and prefer an exported TWITTER_API_KEY over passing keys directly in command arguments.

Risk: The wrapper can evaluate shell startup file content while loading TWITTER_API_KEY.

Mitigation: Review shell configuration before use or bypass the wrapper by running the Python script with a trusted environment variable.

Risk: The wrapper may install an unpinned Python dependency into the user environment.

Mitigation: Run the skill from a preconfigured virtual environment with reviewed dependencies instead of allowing automatic installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flyfoxci/skills/twitter-search-skill)
- [Twitter API Reference](references/twitter_api.md)
- [twitterapi.io Advanced Search Endpoint](https://docs.twitterapi.io/api-reference/endpoint/tweet_advanced_search)
- [Twitter Advanced Search Syntax](https://github.com/igorbrigadir/twitter-advanced-search)
- [Publisher Profile](https://clawhub.ai/user/flyfoxci)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [JSON search results and markdown analysis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches up to 1000 tweets by default and can output either full tweet JSON or aggregate summaries.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
