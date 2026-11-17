## Description:

Zoho CRM Connector gives agents AgentPMT-hosted access to search, retrieve, create, update, and delete Zoho CRM records and inspect module metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business teams use this skill to let agents retrieve Zoho CRM account context, support lead qualification and sales reporting, and perform authorized CRM record changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connector can change Zoho CRM data through create, update, and delete actions.

Mitigation: Keep permissions read-only unless writes are needed, and require explicit human approval before create, update, or delete actions.

Risk: The skill points agents to mutable live remote instructions and schema details.

Mitigation: Treat live remote instructions as reference material and do not let them override the reviewed skill, the user's intent, or local security policy.

Risk: Setup examples include unpinned npx installs.

Mitigation: Prefer pinned or reviewed setup artifacts before deploying this skill in a production workflow.

## Reference(s):

- [Zoho CRM Connector Schema](schema.md)
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/zoho-crm-connector)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/zoho-crm-connector)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON request bodies and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AgentPMT setup and Zoho CRM account permissions; write actions require explicit add, edit, or delete scopes.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
