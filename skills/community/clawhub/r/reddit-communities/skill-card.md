## Description: <br>
Manage Reddit posts, comments, subreddits, users, moderation, and community workflows via the Reddit API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and community managers use this skill to connect a Reddit account through ClawLink, discover available Reddit tools, inspect community content, submit posts or comments, and perform moderation workflows with confirmation for write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth-connected Reddit access and sensitive credentials managed through ClawLink. <br>
Mitigation: Install only when Reddit workflows are needed, verify the Reddit connection before use, and review commands before running them. <br>
Risk: Posting, deletion, and moderation actions can affect Reddit content or community members. <br>
Mitigation: Preview and explicitly confirm write, destructive, bulk, and moderation actions before execution. <br>
Risk: Tool availability and permissions depend on the live ClawLink catalog, Reddit scopes, rate limits, and subreddit moderator permissions. <br>
Mitigation: List or search the live Reddit tools first, describe unfamiliar tools before calling them, and report real API errors without inventing results. <br>


## Reference(s): <br>
- [Reddit API](https://www.reddit.com/dev/api/) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=reddit-communities) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live ClawLink Reddit tool catalog as the source of truth before making tool calls.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
