## Description:

Guides agents through Trading 212 API authentication, environment selection, account and portfolio queries, instrument lookup, historical data retrieval, CSV exports, and order-related API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsvetelin-kulinski](https://clawhub.ai/user/tsvetelin-kulinski)

### License/Terms of Use:

MIT License

## Use Case:

External developers and Trading 212 account holders use this skill to configure API credentials, choose DEMO or LIVE environments, inspect account and portfolio data, search instruments, retrieve history, and prepare Trading 212 API requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide API calls that place or cancel real-money trades.

Mitigation: Use DEMO first and require explicit confirmation before any LIVE order placement or cancellation.

Risk: Credentials could be sent to the wrong destination if a custom base URL or precomputed authorization header is used carelessly.

Mitigation: Use only the official live.trading212.com or demo.trading212.com hosts and confirm the selected environment before API calls.

Risk: Shared temporary instrument metadata caches can become stale or be unsuitable for trade decisions.

Mitigation: Refresh and validate Trading 212 instrument data before trading, and do not rely on a shared /tmp cache for final decisions.

## Reference(s):

- [Trading212 API ClawHub skill page](https://clawhub.ai/tsvetelin-kulinski/skills/trading212-api)
- [Trading 212 demo API base URL](https://demo.trading212.com/api/v0)
- [Trading 212 live API base URL](https://live.trading212.com/api/v0)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API Calls, Code]

**Output Format:** [Markdown with inline bash, curl, JSON, and CSV examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit environment selection and confirmation before live order placement or cancellation.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
