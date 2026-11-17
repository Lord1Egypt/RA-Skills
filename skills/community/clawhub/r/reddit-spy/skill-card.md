## Description:

Reddit Spy browses, reads, searches, and analyzes Reddit communities using OAuth, Tor, stealth HTTP/browser fetching, and PullPush fallback layers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hioliver933](https://clawhub.ai/user/hioliver933)

### License/Terms of Use:


## Use Case:

Developers, analysts, and external users can use this skill to gather read-only subreddit intelligence, inspect posts and comments, compare communities, extract content strategy patterns, and analyze public Reddit user posting behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses stealth scraping, Tor rotation, optional proxies, third-party archives, and user profiling, which can create policy, privacy, and operational risk.

Mitigation: Install only for authorized Reddit research, run in a dedicated low-privilege environment, keep collection limits low, and disable Tor, proxy, or PullPush fallback layers unless they are explicitly approved for the task.

Risk: Optional Reddit OAuth setup requires Reddit credentials and the skill can persist cookies under a local cache directory.

Mitigation: Use a dedicated low-privilege Reddit account instead of a primary account, provide secrets through controlled environment variables, and regularly clear the .reddit-spy cache when session persistence is not needed.

Risk: PullPush archive data may be stale and subreddit or user analysis can be misleading if treated as complete real-time evidence.

Mitigation: Treat archive-backed results as historical, check the reported data source, and verify important conclusions against current Reddit data before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hioliver933/skills/reddit-spy)
- [Publisher profile](https://clawhub.ai/user/hioliver933)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON to stdout with diagnostic logs on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command outputs may include subreddit metrics, post and comment records, search results, user posting summaries, strategy analysis, recommendations, and fetch-layer health checks.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
