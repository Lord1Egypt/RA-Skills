## Description: <br>
Browse, search, post, and moderate Reddit. Read-only works without auth; posting/moderation requires OAuth setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theglove44](https://clawhub.ai/user/theglove44) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to browse subreddit content, search Reddit, retrieve comments, and perform authenticated posting, replies, and moderation actions from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated commands can create posts, send replies, and perform moderation actions on live Reddit communities. <br>
Mitigation: Require explicit human approval before submit, reply, or moderation commands, and test with low-impact subreddits before using moderator permissions. <br>
Risk: The OAuth token is persistent and stored at ~/.reddit-token.json. <br>
Mitigation: Use a dedicated low-privilege Reddit account or app, restrict file permissions on the token file, and delete the token file when access is no longer needed. <br>
Risk: The OAuth scope set is broad for posting and moderation workflows. <br>
Mitigation: Grant only the Reddit OAuth scopes needed for the intended workflow and avoid enabling moderation scopes for read-only use. <br>


## Reference(s): <br>
- [ClawHub Reddit Skill](https://clawhub.ai/theglove44/reddit) <br>
- [README.md](README.md) <br>
- [Reddit App Preferences](https://www.reddit.com/prefs/apps) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, API Calls, Configuration] <br>
**Output Format:** [Markdown command examples and CLI output from Reddit API operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node. Read-only commands can run without authentication; posting, replies, and moderation require Reddit OAuth and store a refresh token at ~/.reddit-token.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
