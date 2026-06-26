## Description: <br>
Post tweets to Twitter/X via the official API v2 using OAuth 1.0a, including single tweets, threads, replies, and quote tweets with character weight validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sit-in](https://clawhub.ai/user/sit-in) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill when a user asks to publish content to Twitter/X, including replies, quote tweets, or multi-post threads. It is suited for users who have configured Twitter/X OAuth credentials and want the agent to post through the official API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can publish content from the configured Twitter/X account. <br>
Mitigation: Use dedicated credentials, review final tweet text before posting, and test with TWITTER_DRY_RUN=1. <br>
Risk: OAuth secrets could be exposed if stored in shared files or logs. <br>
Mitigation: Keep Twitter/X tokens in environment variables or protected instance configuration and avoid hardcoding credentials in skill files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sit-in/twitter-post) <br>
- [Twitter/X Developer Portal](https://developer.x.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with bash commands; tweet script output is JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Twitter/X OAuth credentials in environment variables; supports dry-run validation before posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
