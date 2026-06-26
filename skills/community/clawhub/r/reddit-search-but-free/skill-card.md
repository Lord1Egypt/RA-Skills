## Description: <br>
A Reddit research CLI that searches posts and comments, reads threads, monitors subreddits, analyzes users, tracks cross-posts, and uses Reddit JSON, PullPush, or Arctic Shift without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minilozio](https://clawhub.ai/user/minilozio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, agents, and research users use this skill to gather Reddit community signals, compare user opinions, monitor subreddit activity, and investigate posts, comments, users, and cross-posts from the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reddit search terms, usernames, subreddit names, and research topics are sent to the selected public provider. <br>
Mitigation: Avoid sensitive personal investigations and choose search terms, usernames, and provider settings intentionally. <br>
Risk: Research topics and watched subreddits can be stored in local cache and watchlist files. <br>
Mitigation: Clear the cache after sensitive work and keep watchlist entries limited to intentional monitoring targets. <br>
Risk: Commands shown by the skill use npx tsx, which can resolve tooling at execution time if tsx is not already pinned or installed. <br>
Mitigation: Preinstall or pin tsx in the operating environment before running the CLI. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Reddit JSON API Reference](references/reddit-json-api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/minilozio/reddit-search-but-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Terminal text, JSON, Markdown, and saved Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can cache responses locally and save result files when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
