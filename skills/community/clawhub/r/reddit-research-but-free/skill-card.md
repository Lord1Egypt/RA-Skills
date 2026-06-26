## Description: <br>
Reddit Research But Free lets agents search Reddit, read threads and comments, monitor subreddits, analyze users, track cross-posts, and use Reddit, PullPush, or Arctic Shift data without API authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minilozio](https://clawhub.ai/user/minilozio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to gather Reddit-sourced community signals, read relevant discussions, monitor subreddits, inspect user activity, and synthesize findings for product, security, trend, scam, or troubleshooting research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reddit search terms, subreddit names, usernames, and thread URLs may be sent to Reddit or the selected archive provider. <br>
Mitigation: Avoid sensitive investigations with external providers unless that exposure is acceptable, and prefer the default Reddit provider when archive search is not needed. <br>
Risk: Cached responses, saved search results, and watchlist entries may persist locally. <br>
Mitigation: Use --save and watchlist commands only when local persistence is intended, and run the cache clear command after sensitive work. <br>
Risk: Archive-provider results can include historical or deleted Reddit content whose context may be incomplete. <br>
Mitigation: Cross-check important findings against live threads or multiple sources before acting on them. <br>


## Reference(s): <br>
- [Reddit JSON API Reference](artifact/references/reddit-json-api.md) <br>
- [Reddit JSON API Base](https://old.reddit.com) <br>
- [PullPush API](https://api.pullpush.io) <br>
- [Arctic Shift API](https://arctic-shift.photon-reddit.com/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/minilozio/reddit-research-but-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance] <br>
**Output Format:** [Terminal text, Markdown, or JSON; optional saved Markdown files for search results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use network requests to Reddit, PullPush, or Arctic Shift and may persist local cache, watchlist, or saved result files when those features are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
