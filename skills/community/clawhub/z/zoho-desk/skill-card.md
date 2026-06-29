## Description: <br>
Zoho Desk API integration with managed OAuth. Manage support tickets, track conversations, list departments and agents, handle contacts and organizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support teams and operators use this skill to work with Zoho Desk from an agent chat workflow, including listing tickets, reading conversations, creating support tickets, and checking contacts, departments, agents, organizations, roles, and tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects an agent to Zoho Desk through managed OAuth and can access sensitive customer support data. <br>
Mitigation: Install only for intended Zoho Desk accounts, review the OAuth permissions granted through ClawLink, and revoke access when no longer needed. <br>
Risk: Write-capable tools can create tickets, upload department logos, or update multiple tasks. <br>
Mitigation: Require confirmation before write actions and review ticket, department, and task identifiers before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hith3sh/zoho-desk) <br>
- [Zoho Desk API documentation](https://www.zoho.com/desk/developer-help/api/) <br>
- [ClawLink OpenClaw documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=zoho-desk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include setup instructions, connection checks, Zoho Desk records, ticket URLs, and confirmation-gated write actions.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
