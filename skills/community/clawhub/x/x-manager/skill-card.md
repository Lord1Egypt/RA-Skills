## Description: <br>
Manage X (Twitter) accounts - post tweets, like, reply, retweet, view timeline, search, auto-interact, analyze data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to manage an X account through scripted posting, engagement, timeline retrieval, user tweet lookup, and recent search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored X/Twitter API credentials can read from and modify an account. <br>
Mitigation: Use a dedicated low-privilege token where possible, restrict credential-file permissions, and rotate or revoke tokens if account access changes. <br>
Risk: Posting, liking, replying, retweeting, and auto-interaction can publish or engage from the wrong account or without clear approval. <br>
Mitigation: Verify the USER_ID and target account before write actions, require human approval for engagement workflows, and enable auto-interaction only with review, rate limits, logs, and a clear disable path. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/patches429/x-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with Python shell commands; scripts return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, X/Twitter API credentials, and network access to X API endpoints.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
