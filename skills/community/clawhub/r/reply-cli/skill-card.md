## Description: <br>
Manage sequences, contacts, email accounts, and schedules in Reply.io directly from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grizzlyzp1](https://clawhub.ai/user/grizzlyzp1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and sales operations teams use this skill to let an agent inspect Reply.io campaign data, manage contacts, and run Reply.io CLI commands for sequences, accounts, and schedules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live Reply.io campaign and contact-changing authority, including creating contacts, enrolling or removing contacts, and starting or pausing sequences. <br>
Mitigation: Use the narrowest available Reply.io API key, avoid exposing it broadly in default agent environments, and require explicit confirmation before contact, enrollment, or sequence state changes. <br>
Risk: The skill depends on REPLY_API_KEY credentials that could expose Reply.io account access if logged or hardcoded. <br>
Mitigation: Store the API key in a protected environment variable, OpenClaw environment configuration, or Docker secret, and do not print or persist the key in agent logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/grizzlyzp1/reply-cli) <br>
- [Reply.io](https://reply.io) <br>
- [Reply.io API settings](https://run.reply.io/Dashboard/Material#/settings/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, curl, and REPLY_API_KEY; CLI commands commonly use --json or --pretty for machine-readable output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
