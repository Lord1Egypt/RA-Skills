## Description:

Work with Salesflare CRM through its native OAuth MCP connection for accounts, contacts, opportunities, tasks, pipelines, users, tags, and account feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeroencorthout](https://clawhub.ai/user/jeroencorthout)

### License/Terms of Use:

MIT-0

## Use Case:

Salesflare users can ask an agent to review CRM records and, after explicit confirmation, create, update, or delete records through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating, changing, or deleting CRM records may affect live customer data.

Mitigation: Require explicit confirmation before any mutation, especially deletes and bulk changes; report affected record IDs.

Risk: Test records may remain in the CRM if cleanup is unavailable.

Mitigation: Check for cleanup tools before creating fixtures; otherwise obtain explicit approval to leave labeled fixtures.

## Reference(s):

- [Salesflare CRM skill on ClawHub](https://clawhub.ai/jeroencorthout/skills/salesflare)

## Skill Output:

**Output Type(s):** [Markdown, JSON]

**Output Format:** [Concise Markdown summary; raw JSON on request]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries include relevant record IDs and changed fields; large results are condensed.]

## Skill Version(s):

1.0.13 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
