## Description:

Researches public Threads (Meta) profiles, posts, replies, and search results via the Crawlora API, returning clean JSON. Use when the user wants a Threads profile's stats, a post's content/replies, a profile's recent posts, or a keyword search on Threads — instead of scraping the app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and social-listening teams use this skill to research public Threads profiles, posts, replies, and search results through Crawlora without scraping the app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Threads usernames, post identifiers, cursors, topic IDs, and search queries are sent to Crawlora for public lookups.

Mitigation: Use only if you are comfortable with Crawlora handling those inputs; avoid sensitive searches unless intended, and keep CRAWLORA_API_KEY in the environment rather than hardcoding or committing it.

## Reference(s):

- [Endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)
- [ClawHub release](https://clawhub.ai/crawlora-org/skills/threads-research)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Normalized JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Threads lookup results; paginated endpoints may provide an opaque cursor for subsequent pages.]

## Skill Version(s):

1.0.18 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
