## Description:

Search Reddit posts and comments, read threads, monitor subreddits, analyze users, and run watchlists from a zero-auth TypeScript CLI using Reddit JSON, PullPush, and Arctic Shift data providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minilozio](https://clawhub.ai/user/minilozio)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to research Reddit discussions, monitor subreddit activity, inspect user and thread context, and synthesize community opinions from terminal-accessible sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal use may download and run an unpinned npm helper through npx when invoking tsx.

Mitigation: Review before installing, or pin and install tsx with a lockfile before running the skill.

Risk: The skill makes outbound requests to Reddit, PullPush, and Arctic Shift, and writes local cache and watchlist files under the skill directory.

Mitigation: Run it only in environments where those network calls and local writes are expected, and clear local cache or watchlist data when needed.

Risk: Historical providers and unauthenticated Reddit endpoints may be rate-limited, unavailable, or incomplete.

Mitigation: Treat results as research leads, retry or switch providers when data is missing, and corroborate important claims before relying on them.

## Reference(s):

- [Reddit JSON API Reference](references/reddit-json-api.md)
- [ClawHub Skill Page](https://clawhub.ai/minilozio/skills/reddit-search-but-free)
- [Reddit JSON Endpoint Base](https://old.reddit.com)
- [PullPush API](https://api.pullpush.io)
- [Arctic Shift API](https://arctic-shift.photon-reddit.com/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Terminal text, Markdown, or pretty-printed JSON, with optional saved Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports command-specific limits, a 15-minute local cache by default, and an optional quick mode with a longer cache TTL.]

## Skill Version(s):

1.0.0 (source: package.json and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
