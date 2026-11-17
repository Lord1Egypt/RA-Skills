## Description:

Plan a day at a Six Flags theme park with live ride wait times, park hours, show schedules, and next-ride suggestions. Use when the user asks about Carowinds or any Six Flags / Cedar Fair park (Cedar Point, Canada's Wonderland, Magic Mountain, the Hurricane Harbor water parks, etc.) — current waits, what to ride next, what time the park opens/closes, or what shows are on. Backed by the sixflags-mcp server over the public themeparks.wiki API (no login).

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Theme-park visitors use this skill to check current ride waits, park hours, showtimes, and attraction information, then choose what to ride next across Six Flags and former Cedar Fair parks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supplied instructions describe use of a separately configured sixflags-mcp server, whose implementation was not included in this review.

Mitigation: Configure a trusted sixflags-mcp server before using the skill; the documented workflow requires no login or API key.

## Reference(s):

- [ClawHub release: sixflags-mcp](https://clawhub.ai/chrischall/skills/sixflags-mcp)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Ride wait and status summaries, park schedules, showtimes, attraction listings, and next-ride suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live waits and showtimes depend on park operating hours; the skill documents that off-hours rides may appear closed with no wait.]

## Skill Version(s):

2.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
