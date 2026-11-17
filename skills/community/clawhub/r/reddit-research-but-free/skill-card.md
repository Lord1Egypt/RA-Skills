## Description:

Reddit Research But Free helps agents search Reddit posts and comments, read threads, monitor subreddits, analyze users, track cross-posts, and use Reddit, PullPush, or Arctic Shift data from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minilozio](https://clawhub.ai/user/minilozio)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to gather community evidence from Reddit, including search results, thread summaries, subreddit activity, user activity, cross-posts, and watchlist updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The normal run path uses npx to resolve tsx at execution time, which may fetch or run unpinned tooling despite the zero-dependencies claim.

Mitigation: Review the skill before installation and pin or install the runner dependency in a controlled environment before use.

Risk: Reddit and archive-provider content returned by the skill is untrusted and may contain prompt-injection or misleading claims.

Mitigation: Treat returned content as evidence for human or agent analysis, not as instructions to execute or follow.

## Reference(s):

- [Reddit JSON API Reference](artifact/references/reddit-json-api.md)
- [ClawHub Skill Page](https://clawhub.ai/minilozio/skills/reddit-research-but-free)
- [Old Reddit JSON Endpoint Base](https://old.reddit.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Terminal text, JSON, or Markdown with Reddit links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save result files and uses a local file cache for repeated Reddit or archive-provider requests.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
