## Description:

Search, describe, and execute actions across enterprise SaaS tools such as Jira, Salesforce, Gmail, Slack, Google Calendar, Google Drive, GitHub, Notion, and Box through the Venn tool-router REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neil-bd](https://clawhub.ai/user/neil-bd)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operators, and developers use this skill to discover connected enterprise tools, search business data, create or update SaaS records, and automate multi-step workflows across connected services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reach many enterprise SaaS systems and may expose or modify sensitive business data.

Mitigation: Use a narrowly scoped Venn API key and review the skill before installing it in a business environment.

Risk: Setting VENN_API_URL to an untrusted endpoint could redirect tool requests and credentials away from the intended Venn service.

Mitigation: Keep VENN_API_URL unset unless the endpoint is fully trusted and controlled.

Risk: Embedding VENN_API_KEY in images or shared configuration can leak persistent access credentials.

Mitigation: Store the key in the OpenClaw environment or secrets helper and do not bake it into container images.

Risk: Write or delete operations across connected SaaS systems can change production records.

Mitigation: Require explicit user confirmation before any write or delete action proceeds.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/neil-bd/skills/venn)
- [Venn API Key Setup](https://app.venn.ai/api-keys)
- [Venn ToolIQ API Endpoint](https://app.venn.ai/api/tooliq)
- [Platform Query Syntax](references/query-syntax.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, JSON, code, markdown]

**Output Format:** [Markdown guidance with JSON request examples, bash commands, and workflow code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VENN_API_KEY; VENN_API_URL is optional and defaults to the Venn ToolIQ endpoint.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
