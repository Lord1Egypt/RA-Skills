## Description:

Calls the Salesforce REST, Bulk, Composite, and Metadata APIs for SOQL and SOSL queries, record CRUD and upserts, OAuth setup, bulk loads, sync design, metadata work, Apex REST calls, report access, and Salesforce error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query, load, update, export, and synchronize Salesforce data while selecting the appropriate Salesforce API and accounting for limits, permissions, authentication, and destructive-operation safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act with the Salesforce authority available to its configured access token.

Mitigation: Use a least-privileged integration user and verify that SF_INSTANCE_URL and SF_LOGIN_HOST point to trusted Salesforce hosts before use.

Risk: Local memory writes can persist business context such as contacts, project notes, subscriptions, org context, schema notes, saved queries, and load history.

Mitigation: Review or disable automatic local memory writes when those details should not persist across sessions, and keep tokens, private keys, and secrets out of Clawic data files.

Risk: Salesforce writes, deletes, bulk loads, and metadata changes can affect production data at scale.

Mitigation: Require explicit confirmation for destructive or broad changes, rehearse large writes in a sandbox, and state record counts and API-limit impact before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/salesforce-api-integration)
- [Clawic skill homepage](https://clawic.com/skills/salesforce-api-integration)
- [Skill source overview](artifact/SKILL.md)
- [Authentication guidance](artifact/auth.md)
- [Bulk API guidance](artifact/bulk.md)
- [Salesforce limits guidance](artifact/limits.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks, API examples, configuration notes, and local file update guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Salesforce REST, Bulk, Composite, Metadata, and OAuth request examples; may also update declared local Clawic note files when durable context should persist.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
