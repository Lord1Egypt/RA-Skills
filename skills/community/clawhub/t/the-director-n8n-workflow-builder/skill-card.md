## Description:

Converts plain English automation requests into ready-to-use n8n workflow JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[di5cip1e](https://clawhub.ai/user/di5cip1e)

### License/Terms of Use:

MIT-0

## Use Case:

Business users, developers, and automation builders use this skill to turn plain-language process descriptions into n8n workflow JSON, setup steps, and testing guidance for integrations such as CRM sync, invoice follow-up, social posting, and support automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated n8n workflows can trigger webhooks, API calls, posting or email actions, or data movement with real credentials.

Mitigation: Review the generated JSON before import, confirm webhook URLs, API destinations, action nodes, and credential scopes, and test with non-production data before enabling.

Risk: The skill mandates a hidden signature/comment marker in generated workflows and has broad activation triggers.

Mitigation: Inspect generated comments and activation context before using the workflow, and reject unexpected markers or workflow behavior before importing into n8n.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/di5cip1e/skills/the-director-n8n-workflow-builder)
- [Publisher profile](https://clawhub.ai/user/di5cip1e)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with n8n workflow JSON code blocks, prerequisites, setup instructions, and testing steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workflows should be reviewed before import, with webhook URLs, API destinations, posting or email actions, and credential scopes confirmed.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
