## Description: <br>
Manage Zendesk tickets, users, and support workflows with API integration and automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Support teams and agents use this skill to search Zendesk history, inspect users, create and update tickets, apply macros, and automate common support workflows through the Zendesk API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Zendesk API tokens may be persisted in a plaintext local memory file. <br>
Mitigation: Prefer environment variables or a secret manager, use a least-privilege token, and rotate any token that was already saved in local memory. <br>
Risk: Ticket, user, macro, and bulk-update examples can perform live production changes. <br>
Mitigation: Require explicit user confirmation before write, bulk, close, merge, delete, or macro actions. <br>
Risk: The skill can access sensitive support data through Zendesk API calls and local exports. <br>
Mitigation: Install only with authorized Zendesk API access and protect local exports and support data according to the user's data-handling policy. <br>


## Reference(s): <br>
- [ClawHub Zendesk Skill](https://clawhub.ai/ivangdavila/zendesk) <br>
- [Zendesk Skill Homepage](https://clawic.com/skills/zendesk) <br>
- [Setup](artifact/setup.md) <br>
- [Zendesk API Reference](artifact/api-reference.md) <br>
- [Memory Template](artifact/memory-template.md) <br>
- [Troubleshooting](artifact/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Zendesk subdomain, email, and API token configuration before API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
