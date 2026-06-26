## Description: <br>
Post tweets, threads, and media to X/Twitter via API v2 with OAuth 1.0a signing and minimal dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abdelkrim](https://clawhub.ai/user/Abdelkrim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent verify X/Twitter credentials and publish tweets, replies, threads, and media from a configured account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish content from the configured X/Twitter account. <br>
Mitigation: Review the exact tweet text, thread content, media path, and reply target before allowing posting commands to run. <br>
Risk: OAuth tokens grant account-level posting capability if exposed or misused. <br>
Mitigation: Store X/Twitter OAuth credentials securely, avoid sharing logs or environment files, and rotate tokens if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Abdelkrim/x-twitter-by-altf1be) <br>
- [X Developer Platform](https://developer.x.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text CLI output with status messages, account details, tweet IDs, and posted tweet URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires X_CONSUMER_KEY, X_CONSUMER_SECRET, X_ACCESS_TOKEN, and X_ACCESS_TOKEN_SECRET environment variables.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
