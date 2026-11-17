## Description:

Search Resy availability and manage reservations, favorites, and Priority Notify from the shell using curl, with fpx for browser-based token setup when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Resy account holders can use this skill to search venues and reservation slots, review account details, and manage bookings, cancellations, favorites, and availability notifications from shell workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Booking with a saved payment method or cancelling a real reservation can change account state without a confirmation safeguard.

Mitigation: Get explicit approval of the reservation details, selected saved payment method, and any applicable fees before booking or cancelling.

Risk: The Resy account token and paired browser session can grant access to account data and actions.

Mitigation: Protect the token and revoke browser pairing when the setup is no longer needed.

## Reference(s):

- [Resy API request examples](artifact/references/resy-api.md)
- [ClawHub release page](https://clawhub.ai/chrischall/skills/resy-fpx)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance]

**Output Format:** [Markdown with curl examples, shell setup steps, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions and copyable commands for interacting with a Resy account.]

## Skill Version(s):

1.4.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
