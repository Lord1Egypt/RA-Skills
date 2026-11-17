## Description:

Complete Zapier automation with Zaps, Tables, Interfaces, webhooks, REST Hooks API, and 6000+ app integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers use this skill to design, test, and operate Zapier workflows across apps, tables, interfaces, webhooks, and API-driven automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad workflow automation, including enabling, deleting, sending messages, and calling arbitrary webhooks.

Mitigation: Require explicit user confirmation before actions that enable automations, delete resources, send messages, or call arbitrary webhooks.

Risk: Workflow payloads may be forwarded, logged, emailed, or placed in URLs.

Mitigation: Map only necessary fields, avoid raw payload logs or emails, and keep personal or sensitive data out of URLs.

Risk: Persistent account and workflow context may accumulate in local Zapier memory or workspace memory.

Mitigation: Review and prune ~/zapier/memory.md and any workspace memory entries created for this skill.

Risk: Zapier API and Tables tokens can grant access to account resources and connected workflow data.

Mitigation: Keep API keys in environment variables or managed secret fields and avoid printing or storing them in logs.

## Reference(s):

- [ClawHub Zapier Skill](https://clawhub.ai/ivangdavila/skills/zapier)
- [Skill Homepage](https://clawic.com/skills/zapier)
- [Zapier Developer Platform](https://zapier.com/developer/platform)
- [Zapier REST API](https://api.zapier.com/v1/*)
- [Zapier Tables API](https://tables.zapier.com/api/v1/*)
- [Zapier Catch Hook Endpoints](https://hooks.zapier.com/hooks/catch/*)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and Zap configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Zapier API requests, webhook payload examples, Zap configuration steps, and local memory notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
