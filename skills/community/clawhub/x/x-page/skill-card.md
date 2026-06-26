## Description: <br>
X/Twitter manager: post, reply, search, like, retweet, get analytics, and construct signed X API calls using local OAuth credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seph1709](https://clawhub.ai/user/seph1709) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and account operators use this skill to manage an X/Twitter account through X API calls, including posting, replying, timeline lookup, engagement actions, media upload, and basic analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a user's X/Twitter account, including posting, deleting, following, unfollowing, bookmarking, list changes, and media upload. <br>
Mitigation: Require explicit review before account-changing actions and grant only the least-privilege X app permissions needed. <br>
Risk: The credential file contains sensitive X API keys and account tokens. <br>
Mitigation: Protect the credential file, avoid committing it, and rotate tokens if they are exposed or the host is compromised. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seph1709/x-page) <br>
- [X Developer Portal](https://developer.twitter.com/en/portal/dashboard) <br>
- [X API v2 base URL](https://api.twitter.com/2) <br>
- [X media upload endpoint](https://upload.twitter.com/1.1/media/upload.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline PowerShell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Constructs X API requests from user intent and uses locally stored OAuth 1.0a credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
