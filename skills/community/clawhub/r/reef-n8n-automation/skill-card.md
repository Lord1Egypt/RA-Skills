## Description:

Build, customize, debug, and deliver n8n workflows using a template library for triggers, actions, error handling, and multi-step automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[staybased](https://clawhub.ai/user/staybased)

### License/Terms of Use:


## Use Case:

Developers and automation builders use this skill to assess client requirements, select n8n workflow templates, customize integrations, test workflows, and prepare delivery documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: n8n API keys or local credentials could be used against the wrong instance or template path.

Mitigation: Confirm the local n8n instance and template path are owned by the user, and keep N8N_API_KEY scoped to the intended local instance.

Risk: Delivered workflows could accidentally retain preconfigured or non-client credentials.

Mitigation: Verify every delivered workflow uses client-owned credentials and contains no hardcoded sensitive data before delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/staybased/skills/reef-n8n-automation)
- [Publisher profile](https://clawhub.ai/user/staybased)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with workflow JSON guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workflow architecture notes, n8n workflow JSON, credential checklists, testing steps, and delivery documentation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
