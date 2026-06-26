## Description: <br>
Authorized SansFiction library manager for adding books, updating reading status, logging progress, viewing reading activity, and scheduling a daily reading check-in with a SansFiction token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fgbytes](https://clawhub.ai/user/fgbytes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Readers who use SansFiction can have an agent manage their library, record reading progress, retrieve current reads and stats, and set up a daily reading check-in. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a SansFiction read/write token, which grants sensitive account access if exposed. <br>
Mitigation: Enter the token through secure OpenClaw configuration or environment settings, avoid pasting it into normal chat, and rotate or revoke it if exposed. <br>
Risk: The optional daily check-in can log reading progress at the wrong time or timezone if configured incorrectly. <br>
Mitigation: Confirm the preferred reminder time and timezone before enabling the scheduled check-in. <br>


## Reference(s): <br>
- [SansFiction](https://sansfiction.com) <br>
- [SansFiction agent token documentation](https://sansfiction.com/docs/agents) <br>
- [ClawHub skill page](https://clawhub.ai/fgbytes/sansfiction-library) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-RPC request examples for the SansFiction MCP endpoint and OpenClaw cron commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
