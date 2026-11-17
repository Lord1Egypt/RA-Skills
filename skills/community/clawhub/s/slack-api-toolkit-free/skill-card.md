## Description: <br>
Slack API Toolkit Free helps agents use a hosted OAuth gateway to send, reply to, update, delete, and read Slack messages, channels, and users through CLI and Python examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to connect an agent to Slack, create a hosted OAuth connection, send notifications, manage message threads, and look up channel or user information. It is suited for personal Slack automation, team notification bots, and fast validation of Slack integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform real Slack write operations, including sending, updating, and deleting messages. <br>
Mitigation: Review workspace connection, channel IDs, timestamps, message content, and user intent before approving write commands. <br>
Risk: The skill depends on a third-party Slack gateway and OAuth scopes for workspace access. <br>
Mitigation: Confirm the gateway provider is trusted and grant only the Slack OAuth scopes needed for the intended workspace. <br>
Risk: Stored API keys or Slack tokens could expose workspace access if copied into source files or logs. <br>
Mitigation: Use SGW_API_KEY or hosted login storage and avoid hardcoding API keys or Slack tokens in code, scripts, or shared transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/slack-api-toolkit-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with CLI commands, Python examples, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SGW_API_KEY or hosted login state and Slack connection identifiers; outputs may include structured Slack API responses, status codes, results, and execution logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
