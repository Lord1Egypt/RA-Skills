## Description:

Monitors configured Reddit communities for technology and culture headlines, curates relevant items, and helps an agent produce Chinese-language commentary with a sarcastic tone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianyushi](https://clawhub.ai/user/qianyushi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch and curate Reddit RSS headlines from configured communities, then prompt an agent to produce concise Chinese-language hot-topic commentary with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill executes local Python and shell scripts.

Mitigation: Review the packaged scripts before installation or execution and run them only in an environment where local cache writes are acceptable.

Risk: The skill contacts Reddit RSS feeds for every configured subreddit.

Mitigation: Review config.json before use and remove communities that are unnecessary for the intended workflow.

Risk: The local headline cache may contain stale, irrelevant, or third-party user-generated content.

Mitigation: Have the agent verify source links and treat curated headlines as prompts for review, not authoritative facts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qianyushi/skills/witpulse-redditnews)
- [Reddit RSS source pattern](https://www.reddit.com/r/technology/.rss)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown source links and text commentary; optional shell commands and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Refreshes a local prepared_quotes.md cache from configured public Reddit RSS feeds.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
