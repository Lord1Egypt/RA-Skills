## Description:

Collect upcoming metal concerts and festivals by country using concerts-metal.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patfitzner](https://clawhub.ai/user/patfitzner)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect upcoming metal shows, gigs, and festivals for a selected country and maintain a local event list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts concerts-metal.com and depends on that site's availability and listing accuracy.

Mitigation: Confirm important concerts with the venue or event organizer before relying on the collected listings.

Risk: The skill keeps a local cache of concert listings and country settings that may reveal event interests or history.

Mitigation: Review or clear generated data files when local event history is sensitive.

Risk: Concerts that disappear from the source are flagged as potentially cancelled and may need human confirmation.

Mitigation: Treat cancellation status as a prompt to verify the event through an authoritative source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patfitzner/skills/upcoming-metal-concerts)
- [concerts-metal.com broadcast listings](https://broadcast.concerts-metal.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands; generated concert records are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates skill-config.json and data/concerts.json; no API key is required.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
