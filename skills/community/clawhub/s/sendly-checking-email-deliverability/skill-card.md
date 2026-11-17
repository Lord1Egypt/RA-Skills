## Description:

Helps users diagnose Sendly email delivery problems and address domain authentication, suppressions, and list quality with confirmation before changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Sendly users and administrators use this skill to investigate delivery failures, review domain authentication and suppressions, and validate addresses before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Domain setup or suppression changes may alter delivery or consent settings.

Mitigation: Confirm the exact domain or address before changes; remove a suppression only after the address owner requests mail again.

Risk: Address validation and list cleaning incur per-address charges.

Mitigation: State the address count and metered cost before requesting confirmation.

Risk: DNS changes may not be effective until verified or propagated.

Mitigation: Report the domain as fixed only after Sendly confirms verification or domain health.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Configuration instructions]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports domain status and diagnostic findings, DNS records to publish, suppression counts, and validation results; does not send email.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
