## Description: <br>
Helps an agent manage Slack messages, reactions, pins, member lookups, and custom emoji using a Slack Bot Token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and Slack workspace users use this skill to have an agent send, edit, delete, read, react to, and pin individual Slack messages. It also supports member lookup and custom emoji listing for routine Slack workspace management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, edit, delete, and pin Slack messages with a Bot Token, so overbroad scopes can expose or alter sensitive workspace content. <br>
Mitigation: Grant only the Slack scopes needed for the intended workflow, avoid history and delete scopes unless necessary, and require explicit confirmation before reading, editing, exporting, or deleting sensitive messages. <br>
Risk: The trigger wording mentions email and SMS even though the skill evidence describes Slack-only behavior. <br>
Mitigation: Treat email and SMS requests as out of scope and use the skill only for Slack message, reaction, pin, member, and emoji workflows. <br>


## Reference(s): <br>
- [Slack Toolkit Free on ClawHub](https://clawhub.ai/thcjp/skills/slack-toolkit-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Slack Web API endpoint](https://slack.com/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return operation status, result data, and Slack API error guidance; the free version is limited to single-message operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
