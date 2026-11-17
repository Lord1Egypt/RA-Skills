## Description:

Queries marketing data from 100+ platforms including Google Analytics, Meta Ads, Google Ads, and LinkedIn, using a required Supermetrics API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bartschneider](https://clawhub.ai/user/bartschneider)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to discover Supermetrics data sources, accounts, fields, and to query connected marketing-platform reporting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query Supermetrics-connected marketing accounts and reporting data.

Mitigation: Install and invoke it only for explicit Supermetrics or connected marketing-platform reporting tasks.

Risk: The Supermetrics API key and returned account/report data are sensitive.

Mitigation: Store the API key with appropriate access controls and avoid exposing returned data outside authorized workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bartschneider/skills/supermetrics-openclawd)
- [Supermetrics MCP API endpoint](https://mcp.supermetrics.com)

## Skill Output:

**Output Type(s):** [API calls, JSON, Guidance]

**Output Format:** [Python dictionaries containing success/data or success/error payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SUPERMETRICS_API_KEY and may return connected-account and marketing-report data.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
