## Description:

Continuously monitor Reddit for new posts and comments mentioning a topic, brand, or competitor, deduped across polls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veezee-build](https://clawhub.ai/user/veezee-build)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and brand or community teams use this skill to configure recurring Reddit polling for keyword mentions and watched subreddits, then report only newly observed posts or comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitored keywords, brand terms, subreddit names, and usage metadata are sent to Veezee for polling.

Mitigation: Install and use the skill only when those watch terms are acceptable to share with Veezee.

Risk: Unattended polling can consume credits quickly, especially with broad queries, short cadences, realtime freshness, or many watched subreddits.

Mitigation: Set a clear polling cadence and max_credits before starting a loop, check usage first, and stop on budget or trial-cap errors.

Risk: SDK or CLI setup uses a third-party dependency path, including examples that run npx.

Mitigation: Prefer the MCP path or use a pinned and verified SDK or CLI version.

Risk: Optional X escalation broadens monitoring beyond Reddit.

Mitigation: Enable X or all-platform monitoring only when cross-platform coverage is explicitly intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veezee-build/skills/veezee-reddit-monitoring)
- [Veezee Reddit MCP server](https://mcp.veezee.io/reddit)
- [Veezee key mint endpoint](https://api.veezee.io/v1/keys/mint)
- [Veezee upgrade page](https://veezee.io/upgrade)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code, API call patterns, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a running list of new Reddit mentions with source, subreddit, author, excerpt, created_at, permalink, grouping, and credits spent.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
