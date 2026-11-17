## Description:

SXSW 2026 schedule lookup, event search, speaker info, and recommendations for the March 12-18 conference and festivals in Austin, TX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianleach](https://clawhub.ai/user/brianleach)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to answer SXSW 2026 schedule, speaker, venue, topic, and planning questions from a bundled schedule snapshot, with web search only when local data may be stale or incomplete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled schedule data may be stale for schedule changes, cancellations, or last-minute additions.

Mitigation: Use the disclosed web search fallback for time-sensitive queries and include direct schedule.sxsw.com URLs when referencing specific events.

Risk: The CLI examples invoke a TypeScript file with node, while packaging may require a TypeScript runner or compiled JavaScript entry point.

Mitigation: Confirm the runtime before deployment and use an appropriate TypeScript runner or compiled JavaScript entry point.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brianleach/skills/sxsw-skill)
- [SXSW 2026 schedule](https://schedule.sxsw.com/2026)
- [Publisher profile](https://clawhub.ai/user/brianleach)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown answers with event lists, times, venues, speakers, and direct schedule URLs; CLI output is plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a bundled local JSON schedule snapshot scraped on 2026-02-26 and may use web search for schedule changes or missing local results.]

## Skill Version(s):

1.0.1 (source: server release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
