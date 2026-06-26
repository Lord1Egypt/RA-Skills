## Description: <br>
Runs Twitter/X reads, likes, follows, replies, and OAuth-gated posting through AIsa for approved account and campaign workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect known Twitter/X accounts or tweets, then perform approved posting, replies, likes, follows, unfollows, and media uploads through AIsa. It is intended for workflows where the target account, tweet, or campaign is already known and the user reviews the action before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive AISA_API_KEY and security evidence reports that the key can appear in normal command output. <br>
Mitigation: Treat AISA_API_KEY as a secret, avoid shared or logged terminals, and rotate the key if it may have been exposed. <br>
Risk: The skill can make live Twitter/X account changes, including posts, replies, likes, follows, unfollows, and media uploads. <br>
Mitigation: Review exact tweet text, media files, tweet IDs, and target accounts before approving an action, and rely on API confirmation before treating the action as complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/twitter-post-aisa) <br>
- [AIsa homepage](https://aisa.one) <br>
- [AIsa Twitter Engagement](references/engage_twitter.md) <br>
- [AIsa Twitter OAuth](references/post_twitter.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; approved actions can send requests and media to AIsa and Twitter/X.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
