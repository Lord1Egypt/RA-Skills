## Description: <br>
Wavye helps solopreneurs use AI agents for weekly planning, time audits, durable memory, automation routines, and life-pillar balance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Skoppert](https://clawhub.ai/user/Skoppert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External solopreneurs use this skill to connect an AI agent with Wayve planning, knowledge, audit, coaching, and automation workflows. It supports recurring rituals such as daily briefs, weekly planning, wrap-ups, time audits, life scans, and business strategy reviews through the Wayve CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent broad persistent access to sensitive personal, business, scheduling, and audit data in the user's Wayve account. <br>
Mitigation: Install only when the user is comfortable with that storage model, and review or delete saved knowledge regularly. <br>
Risk: The skill depends on secrets such as WAYVE_API_KEY, Telegram bot tokens, and Slack or Discord webhooks. <br>
Mitigation: Treat all tokens and webhook URLs as secrets, prefer dedicated limited channels, and rotate credentials if exposed. <br>
Risk: Automation creation and planning-data changes can affect reminders, routines, or stored planning records. <br>
Mitigation: Require explicit user confirmation before creating automations or deleting planning data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Skoppert/wayve) <br>
- [Wayve homepage](https://www.gowayve.com) <br>
- [Wayve CLI setup documentation](https://www.gowayve.com/docs/cli-setup) <br>
- [Wayve CLI setup guide](references/setup-guide.md) <br>
- [Wayve CLI command reference](references/tool-reference.md) <br>
- [Automations guide](references/automations.md) <br>
- [Knowledge and learning system](references/knowledge-learning.md) <br>
- [Time audit workflow](references/time-audit.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with Wayve CLI commands and JSON-oriented command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the wayve CLI and WAYVE_API_KEY for flows that read or persist Wayve account data.] <br>

## Skill Version(s): <br>
1.0.13 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
