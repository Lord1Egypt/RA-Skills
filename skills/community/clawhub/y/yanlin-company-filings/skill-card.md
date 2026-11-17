## Description:

Collects Chinese-market company announcements from Sina Finance and exchange disclosure indexes, filters for material events, and labels likely impact, importance, sector, and direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoling7878-arch](https://clawhub.ai/user/caoling7878-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial analysts use this skill to fetch and triage Chinese company announcements for investment research workflows. It is intended as a screening aid that highlights material filings and likely direction, not as verified investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to public Sina Finance and exchange-related URLs, including some HTTP endpoints.

Mitigation: Install only in environments where those network requests are acceptable, and prefer confirming important announcements through official HTTPS exchange or company disclosure pages.

Risk: Filtered announcement output can be incomplete, weakly attributed, or unsuitable as investment advice.

Mitigation: Treat results as a screening aid and verify material events before making financial decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON filing output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces date-stamped filing summaries sorted by importance, with company, code, event, category, direction, sector, and data source fields when JSON output is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
