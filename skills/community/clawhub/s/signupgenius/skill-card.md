## Description:

Read sign-up sheets, slot reports, and groups on SignUpGenius — and add members to your groups. Triggers on phrases like "check SignUpGenius", "what am I signed up for", "what slots are left for [event]", "available slots", "list my SignUpGenius groups", "add [person] to my [group] group", or any request involving SignUpGenius sign-ups, RSVPs, volunteer slots, potlucks, carpools, classroom helpers, or PTA/HOA/Scout/team sign-ups. Works against your own signed-in account; supports Pro key for full slot reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals use this skill to review their SignUpGenius sign-ups, groups, RSVPs, and volunteer slots, and to make approved changes to their own account. It can also retrieve metadata and slot availability from public sign-up sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external npm package and browser bridge require separate trust and can access the signed-in SignUpGenius account.

Mitigation: Trust and preferably pin the external package before granting account access; review the bridge permissions.

Risk: Configuration may contain an account password or API key, and approved changes can affect sign-ups or send group invitations.

Mitigation: Protect credentials in configuration. Check the person, sheet, slot, and previewed identity before confirming a change; note that adding group members may send invitations.

Risk: Scripted or automated account access may conflict with SignUpGenius terms.

Mitigation: Keep use to the documented personal-account, personal-scale audience and follow the service's terms.

## Reference(s):

- [SignUpGenius](https://www.signupgenius.com)
- [signupgenius-mcp package](https://www.npmjs.com/package/signupgenius-mcp)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [ClawHub skill page](https://clawhub.ai/chrischall/skills/signupgenius)

## Skill Output:

**Output Type(s):** [Text, Structured data]

**Output Format:** [Natural-language summaries and structured tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides read results and previews for supported account changes before confirmation.]

## Skill Version(s):

2.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
