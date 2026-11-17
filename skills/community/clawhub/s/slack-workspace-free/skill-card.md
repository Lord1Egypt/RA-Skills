## Description: <br>
Slack Workspace Free helps agents send basic Slack channel messages and list Slack channels or users through a ClawLink-managed OAuth connection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team operators use this skill to automate basic Slack workspace tasks: checking the Slack connection, finding channel IDs, sending channel notifications, and listing workspace channels or users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post live Slack messages. <br>
Mitigation: Use it only for explicit Slack tasks and confirm every message before posting. <br>
Risk: Channel or user listings can expose workspace data. <br>
Mitigation: Avoid sending sensitive channel or user data to callback URLs or unnecessary outputs. <br>
Risk: OAuth permissions may exceed the free skill's basic message sending and listing needs. <br>
Mitigation: Use a Slack OAuth connection with the minimum scopes needed for message sending and listing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/slack-workspace-free) <br>
- [Slack Web API endpoint pattern](https://slack.com/api/*) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Slack API calls that send live messages or list workspace channels and users.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
