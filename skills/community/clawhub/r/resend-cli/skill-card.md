## Description: <br>
Send and manage emails via the Resend CLI, including emails, domains, contacts, segments, broadcasts, templates, topics, webhooks, and API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maciejlis](https://clawhub.ai/user/maciejlis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to operate the Resend CLI for email sending, account resource management, webhook setup, and automation with structured JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send emails and change Resend account resources when credentials are available. <br>
Mitigation: Use the least-privileged Resend API key available and require explicit confirmation before sending, broadcasting, deleting, changing API keys, changing webhooks, or modifying scheduled emails. <br>
Risk: Automation may send messages to unintended recipients or audiences. <br>
Mitigation: Verify recipients, segments, broadcasts, and scheduled-send parameters before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/maciejlis/resend-cli) <br>
- [Resend CLI repository](https://github.com/resend/resend-cli) <br>
- [Resend](https://resend.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends --json or --quiet for non-interactive agent usage.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
