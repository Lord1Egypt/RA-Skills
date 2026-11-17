## Description:

Track, aggregate, and report OpenClaw token usage and costs across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[space-cadet](https://clawhub.ai/user/space-cadet)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and developers can review token usage, model and session breakdowns, and approximate costs over selected time periods, including daily and weekly reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner flagged copying a whole protected agent database to a temporary location, beyond the usage information the reports need.

Mitigation: Review this snapshot behavior before use. If you proceed, limit access to the temporary copy and remove it when processing is complete.

## Reference(s):

- [Token Usage Tracker on ClawHub](https://clawhub.ai/space-cadet/skills/token-usage)
- [Project homepage](https://github.com/space-cadet/openclaw-token-usage)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Token usage summaries and cost reports as Markdown or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-turn processing volume; cached reads are reported separately and cost estimates are approximate.]

## Skill Version(s):

2.5.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
