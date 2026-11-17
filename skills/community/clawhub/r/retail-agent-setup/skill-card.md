## Description:

Guides retail businesses through a 12-step setup to configure a digital employee agent for store operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangwei-frank](https://clawhub.ai/user/fangwei-frank)

### License/Terms of Use:

MIT-0

## Use Case:

Retail business owners, store managers, and implementation staff use this skill to set up a store AI assistant, connect retail data, choose roles and channels, configure permissions, test readiness, and establish post-launch improvement loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live retail integrations may expose operational systems or credentials during setup.

Mitigation: Use sandbox or read-only API credentials where possible and avoid pasting raw secrets into chat.

Risk: Imported customer, staff, or sales data may include sensitive or personal information.

Mitigation: Avoid importing customer PII unless necessary and review uploaded data before adding it to the agent knowledge base.

Risk: Persistent memory and knowledge-base edits can preserve incorrect, unauthorized, or sensitive content.

Mitigation: Restrict knowledge edits to authenticated staff-only channels and review updates before live use.

Risk: Recurring digests, alerts, and reports can continue sending operational information after setup.

Mitigation: Create recurring jobs only with clear recipients, expiry, audit, and deletion controls.

## Reference(s):

- [Retail Agent Setup release page](https://clawhub.ai/fangwei-frank/skills/retail-agent-setup)
- [Step 01 - System Inventory](references/step-01-systems.md)
- [Step 02 - Data Infrastructure Assessment](references/step-02-data-infra.md)
- [Step 03 - Data Import & Auto-Structuring](references/step-03-data-import.md)
- [Step 04 - Role Selection](references/step-04-role-select.md)
- [Step 05 - Skills Configuration](references/step-05-skills-config.md)
- [Step 06 - Knowledge Base Validation](references/step-06-knowledge.md)
- [Step 07 - Digital Employee Persona](references/step-07-persona.md)
- [Step 08 - Channel Integration](references/step-08-channels.md)
- [Step 09 - Permissions & Escalation](references/step-09-permissions.md)
- [Step 10 - Pre-Launch Testing](references/step-10-test.md)
- [Step 11 - Launch & Handoff](references/step-11-handoff.md)
- [Step 12 - Continuous Improvement](references/step-12-iterate.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup artifacts such as system inventories, knowledge-base entries, role and persona configs, permission matrices, test reports, staff handoff materials, and recurring job definitions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
