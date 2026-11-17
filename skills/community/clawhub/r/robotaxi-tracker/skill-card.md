## Description:

Helps agents retrieve and compare current Robotaxi Tracker data for U.S. autonomous vehicle fleets, including Tesla and Waymo counts, city distribution, official fleet numbers, and tracker-collected metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pekky](https://clawhub.ai/user/pekky)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to answer current U.S. robotaxi fleet questions with Robotaxi Tracker data, including provider comparisons and city-level tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow makes live requests to Robotaxi Tracker and public Convex backend hosts.

Mitigation: Run it only in environments where those outbound requests are acceptable, and review returned data before relying on it.

Risk: The workflow uses fixed temporary paths that could collide on shared machines.

Mitigation: Use private mktemp-created directories before running the workflow in shared or multi-user environments.

## Reference(s):

- [Robotaxi Tracker](https://robotaxitracker.com/)
- [ClawHub Skill Page](https://clawhub.ai/pekky/skills/robotaxi-tracker)
- [Publisher Profile](https://clawhub.ai/user/pekky)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables and concise prose with optional shell command workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates official fleet counts from tracker-collected metrics and validates city rows, totals, and selected public data host when live data is available.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
