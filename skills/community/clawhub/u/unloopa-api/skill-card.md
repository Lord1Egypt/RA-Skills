## Description:

Unloopa Api lets an agent use the Unloopa REST API to find local business leads, generate websites, send outreach emails, and manage voice calling workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echris6](https://clawhub.ai/user/echris6)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to connect an agent to Unloopa for lead generation, generated website review, email outreach, and optional voice calling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send outreach emails or initiate voice calls to third parties.

Mitigation: Require explicit user confirmation for recipient lists, message content, outbound calls, campaign activation, and campaign triggering before using the API.

Risk: The skill can buy or release phone numbers through the connected Unloopa account.

Mitigation: Require explicit user confirmation before any paid phone-number purchase or number release, and check quota, plan, and credits first.

Risk: The API key gives an agent authority over lead generation, outreach, voice campaigns, and account-linked resources.

Mitigation: Install only after reviewing the requested authority, store UNLOOPA_API_KEY securely, and limit use to agents that are allowed to act on the Unloopa account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/echris6/skills/unloopa-api)
- [Unloopa API base URL](https://dashboard.unloopa.com/api/v1/)
- [Unloopa API key settings](https://dashboard.unloopa.com/settings)
- [Unloopa email setup](https://dashboard.unloopa.com/settings?tab=email)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST endpoint names, JSON request and response examples, and shell snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UNLOOPA_API_KEY and may guide actions that send outreach, place calls, activate campaigns, or purchase phone numbers.]

## Skill Version(s):

1.3.0 (source: server release metadata; artifact frontmatter reports 1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
