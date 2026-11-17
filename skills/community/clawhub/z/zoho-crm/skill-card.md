## Description:

Helps agents read and manage Zoho CRM records, search contacts, and retrieve account, user, and module information through an authorized connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and developers use this skill to find and maintain leads, contacts, accounts, and deals in an authorized Zoho CRM account, with approval before changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad connection permissions could expose more CRM data than a task needs.

Mitigation: Authorize only the intended account and prefer read-only OAuth scopes where possible.

Risk: Record changes or deletions could alter or remove business data.

Mitigation: Verify the target and intended effect, then obtain explicit approval before each write or deletion.

Risk: Hosted functions, triggers, destinations, and watch commands can continue to act or forward events.

Mitigation: Approve persistent automation separately, limit its scope, and remove it when no longer needed.

Risk: Raw API keys can be exposed through logs or local processes.

Mitigation: Use managed authentication when possible; avoid raw API keys unless the CLI cannot be used.

## Reference(s):

- [Zoho CRM skill release](https://clawhub.ai/byungkyu/skills/zoho-crm)
- [Zoho CRM API v8 documentation](https://www.zoho.com/crm/developer/docs/api/v8/)
- [Maton documentation](https://docs.maton.ai)
- [Maton homepage](https://maton.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline commands and CRM data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize JSON responses from the connected CRM account.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
