## Description:

Helps WOL attendees check catering and event information and manage orders, registrations, and seats through the WOL API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onokje](https://clawhub.ai/user/onokje)

### License/Terms of Use:

MIT-0

## Use Case:

WOL attendees use this skill to check menus, orders, balances, event availability, registration status, and seats, and to request confirmed catering or registration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An exposed API token could allow access to the user's WOL account.

Mitigation: Use the provided token setup or WOL_API_TOKEN; never paste a token into chat.

Risk: An incorrect order, cancellation, registration, or seat choice could affect the user's account or incur a charge.

Mitigation: Review the preview and obtain explicit user confirmation before executing any change.

## Reference(s):

- [WOL API skill on ClawHub](https://clawhub.ai/onokje/skills/wol-api)
- [Wake-up On LAN](https://wollan.nl)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Plain text or Markdown, with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offers a preview and requests explicit user confirmation before orders or registration and seat changes.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
