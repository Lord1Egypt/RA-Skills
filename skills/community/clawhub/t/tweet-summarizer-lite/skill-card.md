## Description:

Fetch and summarize single tweets from Twitter/X. Basic search and single tweet fetching. Lightweight version perfect for quick tweet lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franciscobuiltdat](https://clawhub.ai/user/franciscobuiltdat)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to fetch, save, summarize, and search individual Twitter/X posts through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Twitter/X session cookies that can grant account access.

Mitigation: Use a dedicated low-risk account, store cookies only in environment variables, rotate them periodically, and remove them from the environment when not needed.

Risk: The unpinned third-party bird CLI receives the Twitter/X cookies and the process environment.

Mitigation: Verify and pin the bird CLI version before use, and run the skill in an environment without unrelated secrets or API keys.

Risk: Fetched tweets and metadata are stored locally.

Mitigation: Periodically delete stored tweet data from the local OpenClaw data directory, especially when it may include private or protected account content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/franciscobuiltdat/skills/tweet-summarizer-lite)
- [bird CLI](https://github.com/steipete/bird)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tweet excerpts, short summaries, search results, troubleshooting guidance, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save fetched tweet text and metadata to local JSON storage; requires Twitter/X session cookies and the bird CLI.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
