## Description:

Research subreddits, draft Reddit-native posts, and publish or schedule Reddit posts via Late API, with ScrapeCreators-powered reading tools and an anti-AI-slop drafting pass.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nirusan](https://clawhub.ai/user/nirusan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research Reddit communities, draft posts that fit subreddit norms, validate posting details, and publish or schedule Reddit content through connected ScrapeCreators and Late accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public Reddit posts through a connected Late account.

Mitigation: Require the agent to show the final subreddit, title, body, flair, scheduling choice, and publish mode, then obtain explicit user approval before running create-post or using --publish-now.

Risk: Stored API keys grant access to ScrapeCreators and Late workflows.

Mitigation: Use environment variables or a secret manager where possible, keep file-based keys chmod 600, and restrict the connected Reddit account to the minimum authority needed.

Risk: Posts can fail or be removed because subreddit rules, flair requirements, and account limits vary.

Mitigation: Check subreddit details, validate the subreddit, list available flairs, and review subreddit-specific rules before posting.

## Reference(s):

- [Reddit Publisher ClawHub skill page](https://clawhub.ai/skills/reddit-publisher)
- [Reddit Publisher release page](https://clawhub.ai/nirusan/skills/reddit-publisher)
- [ScrapeCreators](https://scrapecreators.com)
- [Late](https://getlate.dev)
- [Phrases to Remove](references/stop-slop/phrases.md)
- [Structures to Avoid](references/stop-slop/structures.md)
- [Before/After Examples](references/stop-slop/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCRAPECREATORS_API_KEY for Reddit research and LATE_API_KEY for Reddit posting workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
