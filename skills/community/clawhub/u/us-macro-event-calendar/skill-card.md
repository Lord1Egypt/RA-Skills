## Description:

Use when the user asks when the next Fed (FOMC) rate decision, CPI, PPI or jobs report (nonfarm payrolls) is, or wants to check macro event risk before an options or stock trade. Free, no-auth calendar from the official Federal Reserve and BLS release schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a0971025732-netizen](https://clawhub.ai/user/a0971025732-netizen)

### License/Terms of Use:

MIT

## Use Case:

External users can check scheduled FOMC, CPI, PPI, and jobs report dates and times when planning around US economic events. The calendar provides schedule information, not forecasts or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Economic-event schedules can change, and the remote calendar service implementation was not verified.

Mitigation: Check the returned official source links for schedule changes.

Risk: A suggested paid follow-up may incur a charge.

Mitigation: Obtain the user's approval before running any paid follow-up.

## Reference(s):

- [Finch calendar service](https://finch-agent-catalog.finch-catalog-mcp.workers.dev/mcp)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON calendar data with event names, dates, Eastern and UTC times, reference periods, source links, and the next matching event.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Filters may select FOMC, CPI, PPI, or jobs events; results cover a requested day window and include the next matching event even if it falls outside that window.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
