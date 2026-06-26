## Description: <br>
Post tweets, replies, and quotes to X/Twitter using the official API v2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xmythril](https://clawhub.ai/user/0xmythril) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and operators use Tweet Cli to publish, reply to, quote, and delete X/Twitter posts through the official API when the user explicitly requests posting or an approved schedule triggers it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can post, reply, quote, or delete content from a real X/Twitter account. <br>
Mitigation: Use a dedicated X app token with minimum permissions and require user confirmation or an approved schedule before posting actions. <br>
Risk: X API credentials are stored in a local ~/.config/tweet-cli/.env file. <br>
Mitigation: Restrict file permissions with chmod 600, protect the host account, and rotate credentials if exposure is suspected. <br>
Risk: Posting actions consume X API credits and may exhaust the monthly quota. <br>
Mitigation: Run posting commands only when explicitly requested or scheduled, and report credit exhaustion errors to the user. <br>


## Reference(s): <br>
- [ClawHub Tweet Cli release page](https://clawhub.ai/0xmythril/tweet-cli) <br>
- [0xmythril ClawHub publisher profile](https://clawhub.ai/user/0xmythril) <br>
- [tweet-cli project homepage](https://github.com/0xmythril/tweet-cli) <br>
- [X Developer Portal](https://developer.x.com/en/portal/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may lead the agent to run tweet-cli commands that call the X API only when explicitly directed by the user or an approved schedule.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
