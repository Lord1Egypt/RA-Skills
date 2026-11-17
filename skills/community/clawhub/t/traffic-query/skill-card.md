## Description:

Query and organize China travel information for flights and trains, including schedules, prices, duration, stops, and summary tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liubroth](https://clawhub.ai/user/liubroth)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to query domestic China flight and train options, normalize messy booking or timetable results, and summarize schedules, prices, duration, stops, and source caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel result pages can be dynamic, incomplete, or affected by login state, region, inventory, and source-specific pricing.

Mitigation: Review the agent's summary against the opened or cited result page before relying on prices, availability, or completeness.

Risk: City-level routes and shared-code flight rows can cause duplicate or mismatched travel options.

Mitigation: Confirm exact airports or stations, route date, and duplicate shared-code rows when comparing options.

## Reference(s):

- [Traffic Query Sources](artifact/references/sources.md)
- [Traffic Query ClawHub Release](https://clawhub.ai/liubroth/skills/traffic-query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with compact travel option summaries and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries may include normalized flight or train fields, highlights such as earliest or cheapest options, and notes about incomplete or source-dependent data.]

## Skill Version(s):

1.0.1 (source: server release metadata and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
