## Description:

Use the Wego CLI to authenticate, resolve travel locations, look up visa-free destinations for a passport, public holidays in a market, published flight timetables and nearby airports, search and compare flights and hotels, inspect trips and room rates, refine existing searches, and generate Wego or provider checkout links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wego](https://clawhub.ai/user/wego)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and travel-support agents use this skill to translate natural-language travel requests into Wego CLI searches, reference lookups, comparisons, refinements, and checkout handoff links for flights and hotels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installer uses a direct curl-to-shell pattern for downloaded code.

Mitigation: Review the installer before approval and prefer a downloaded, versioned, checksum- or signature-verified package when available.

Risk: Authenticated Wego CLI use may send travel search details to Wego services.

Mitigation: Use the skill only when the user is comfortable sending the travel request to Wego, and avoid exposing credentials or local credential files.

Risk: The skill can store pricing preferences or send feedback from the user's machine.

Mitigation: Change local Wego configuration or send feedback only after explicit user approval.

Risk: Generated checkout links can be mistaken for completed reservations.

Mitigation: State that links are checkout handoffs and that no booking, reservation, payment, cancellation, or modification has occurred.

## Reference(s):

- [ClawHub Wego Skill Page](https://clawhub.ai/wego/skills/wego)
- [Wego CLI Installer](https://api.wego.com/install)
- [Wego API Rate Limits](https://docs.wego.com/api/rate-limits/)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance, Configuration]

**Output Format:** [Markdown with inline shell commands and concise human-readable travel comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JSON returned by the Wego CLI as evidence and may produce checkout handoff links, but does not complete bookings or payments.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
