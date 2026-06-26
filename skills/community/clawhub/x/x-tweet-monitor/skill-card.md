## Description: <br>
Monitor X/Twitter accounts for new tweets and send notifications to Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mmmuffin](https://clawhub.ai/user/mmmuffin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor a selected X/Twitter account and receive Telegram notifications when new tweets appear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive X/Twitter session cookies and a Telegram bot token. <br>
Mitigation: Store AUTH_TOKEN, CT0, and Telegram credentials outside source control and logs, rotate them if exposed, and prefer a dedicated or low-risk X/Twitter account. <br>
Risk: Tweet retrieval depends on an undeclared local `xreach` command that receives the X/Twitter credentials. <br>
Mitigation: Install and run the skill only after verifying that the local `xreach` binary is trusted and expected. <br>
Risk: The monitor runs continuously and sends outbound Telegram messages. <br>
Mitigation: Run it in an environment where the process can be monitored and stopped, and limit Telegram bot and chat access to the intended destination. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mmmuffin/x-tweet-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Notifications, Guidance] <br>
**Output Format:** [Markdown with environment variable setup and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires X/Twitter session cookies, a Telegram bot token, a Telegram chat ID, and a local xreach command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
