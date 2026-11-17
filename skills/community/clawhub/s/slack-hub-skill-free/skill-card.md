## Description: <br>
Slack消息中枢LITE helps agents send Slack channel messages and list public Slack channels through the Slack Web API with a bot token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team operators use this skill to publish basic Slack notifications and discover public channel IDs from an agent workflow. It is suited to simple team collaboration tasks that need channel messaging or public channel listing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends content to Slack channels using a bot token, so an agent could post to the wrong channel or send unintended message text. <br>
Mitigation: Review the target channel and message text before sending, invite the bot only to intended channels, and keep the Slack bot token in an environment variable. <br>
Risk: The Slack bot token requires workspace permissions and could expose Slack access if copied into chat or stored in files. <br>
Mitigation: Grant only needed scopes such as chat:write and channels:read, never paste or echo the token, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [Slack App Configuration](https://api.slack.com/apps) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SLACK_BOT_TOKEN from the environment and returns Slack API success or error responses for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
