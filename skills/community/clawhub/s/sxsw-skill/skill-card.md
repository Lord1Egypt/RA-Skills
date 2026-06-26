## Description: <br>
SXSW 2026 schedule lookup, event search, speaker info, and recommendations for the March 12-18 conference and festivals in Austin, TX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianleach](https://clawhub.ai/user/brianleach) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External SXSW attendees, conference planners, and agent users use this skill to search bundled SXSW 2026 events, speakers, venues, tracks, and dates, then generate concise schedule guidance and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live-update questions may rely on agent-initiated web search when bundled schedule data is incomplete or stale. <br>
Mitigation: Verify cancellations, last-minute changes, RSVP links, and important schedule decisions with official SXSW sources before acting. <br>
Risk: The bundled schedule data is a pre-scraped snapshot and can become stale as SXSW programming changes. <br>
Mitigation: Treat local results as a planning aid and refresh or cross-check against the official SXSW schedule for time-sensitive use. <br>
Risk: The CLI entry point is a TypeScript file, so environments that run plain Node without a TypeScript loader may not execute it directly. <br>
Mitigation: Install or provide the expected TypeScript execution path before relying on the CLI commands, or have the agent read the bundled JSON data directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brianleach/sxsw-skill) <br>
- [Publisher profile](https://clawhub.ai/user/brianleach) <br>
- [SXSW 2026 schedule source](https://schedule.sxsw.com/2026) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell command examples and event links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include schedule.sxsw.com event URLs, dates, times, venues, speaker details, and recommendation summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
