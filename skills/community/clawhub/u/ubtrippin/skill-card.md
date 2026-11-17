## Description:

Manages a user's UBTRIPPIN travel data, including trips, itinerary items, loyalty programs, family sharing, city guides, events, notifications, webhooks, and billing-related links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fistfulayen](https://clawhub.ai/user/fistfulayen)

### License/Terms of Use:


## Use Case:

External users and their agents use this skill to view and manage UBTRIPPIN travel plans, booking details, loyalty information, family sharing, city guides, notifications, webhooks, and account-related travel workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manage sensitive travel data, loyalty numbers, family sharing, collaborators, notifications, webhooks, and billing-related links.

Mitigation: Grant access only when the user accepts this scope, keep the API key in a protected secret store or environment variable, and avoid placing secrets in TOOLS.md or example scripts.

Risk: Delete operations, sharing changes, webhook setup, checkout actions, calendar-token regeneration, and email forwarding can have lasting account or privacy impact.

Mitigation: Require explicit user confirmation before these actions and summarize the affected trip, item, family member, collaborator, webhook, billing action, or email attachment before proceeding.

Risk: Forwarding booking emails and attachments may expose personal itinerary, ticket, and payment-adjacent information.

Mitigation: Use only the user's registered sender address, confirm which email and attachments will be forwarded, and verify the imported result after processing.

## Reference(s):

- [UBTRIPPIN API documentation](https://www.ubtrippin.xyz/api/v1/docs)
- [UBTRIPPIN website](https://www.ubtrippin.xyz)
- [ClawHub skill page](https://clawhub.ai/fistfulayen/skills/ubtrippin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with REST API examples, JSON request and response snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a UBTRIPPIN API key and registered sender email for authenticated operations.]

## Skill Version(s):

2.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
