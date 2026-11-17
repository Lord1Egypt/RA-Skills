## Description:

Answers time and timezone questions with live data from the worldclock.pro MCP server, including city and country times, timezone conversion, meeting scheduling across zones, daylight saving transitions, UTC or GMT offsets, coordinate-based lookups, and city resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldclock.pro](https://clawhub.ai/user/worldclock.pro)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to answer current time questions, convert times across locations and timezones, check daylight saving transitions, and resolve locations or coordinates through worldclock.pro.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Time, location, coordinate, or meeting-conversion queries are sent to worldclock.pro for live results.

Mitigation: Avoid entering sensitive meeting details or private location information; send only the location and time data needed for the answer.

Risk: Live answers depend on the worldclock.pro service being reachable and current.

Mitigation: Use the documented worldclock.pro human pages when MCP is unavailable, and avoid answering from memory when live access is unavailable.

## Reference(s):

- [worldclock.pro homepage](https://worldclock.pro)
- [worldclock.pro MCP endpoint](https://worldclock.pro/mcp)
- [worldclock.pro agent page map](https://worldclock.pro/llms.txt)
- [ClawHub skill page](https://clawhub.ai/worldclock.pro/skills/world-clock-pro)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON-formatted time and timezone results, with optional curl fallback commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include worldclock.pro source_url attribution for returned time facts.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
