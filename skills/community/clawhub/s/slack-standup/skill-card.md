## Description: <br>
Automates Slack daily standups by prompting team members for updates, compiling responses, and posting summaries to a configured Slack channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allanwei](https://clawhub.ai/user/allanwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Team leads, managers, and remote teams use this skill to run asynchronous daily standups in Slack, reducing the need for live status meetings while keeping updates and blockers visible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A script includes a hardcoded Slack-like bot token, which could expose credentials or encourage unsafe token handling. <br>
Mitigation: Create a new least-privilege Slack bot token, store it outside the skill files, rotate any copied token, and restrict the bot to approved channels. <br>
Risk: Standup updates may contain sensitive team or project information and are posted to Slack channels. <br>
Mitigation: Configure only intended channels, confirm who can read them, and make team members aware of where their updates will be posted. <br>


## Reference(s): <br>
- [Slack Bot Setup](references/SETUP.md) <br>
- [Slack App Configuration](https://api.slack.com/apps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Slack-formatted message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Posts prompts and summaries through the Slack API when configured with a Slack bot token and channel.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
