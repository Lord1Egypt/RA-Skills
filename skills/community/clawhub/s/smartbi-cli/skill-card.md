## Description: <br>
Helps agents discover Smartbi OpenAPI operations, inspect contracts, construct request bodies, execute calls, and handle scheduled tasks or outbound messages through @smartbi/cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wahsonleung](https://clawhub.ai/user/wahsonleung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data teams, and Smartbi administrators use this skill to turn natural-language BI requests into Smartbi API discovery, contract review, API calls, scheduled jobs, and notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad Smartbi API authority and persist local tokens. <br>
Mitigation: Use least-privileged, revocable tokens; restrict permissions on ~/.smartbi/config.yaml; rotate tokens if exposed; and review each operationKey and request body before execution. <br>
Risk: Scheduled jobs and outbound messages can create recurring actions or send content to external channels. <br>
Mitigation: Require explicit user approval for schedules, recipients, webhook URLs, outbound content, and activation of recurring jobs. <br>
Risk: Documentation loading and parameter construction can influence API calls. <br>
Mitigation: Use Smartbi-provided documentation and schemas as the source of truth, ask for missing values, and avoid arbitrary external documentation links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wahsonleung/smartbi-cli) <br>
- [Publisher profile](https://clawhub.ai/user/wahsonleung) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Scheduled task scenario](scenarios/schedule-task.md) <br>
- [Message push scenario](scenarios/push-message.md) <br>
- [Smartbi document index](references/doc-index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Smartbi CLI commands, JSON request-body files, and result summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary JSON or JavaScript files for request bodies and scheduled task scripts; expected responses include operation keys, final commands, key results, and repair suggestions.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
