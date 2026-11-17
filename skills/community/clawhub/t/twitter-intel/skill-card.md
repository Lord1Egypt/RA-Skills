## Description:

Twitter keyword search, monitoring, and trend analysis via GraphQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to search Twitter/X keywords, monitor configured topics, and turn collected high-engagement tweets into structured trend reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on live Twitter/X browser session cookies, which can expose the account if the cookie file is leaked or committed.

Mitigation: Use a dedicated low-risk account, store the cookie file outside the project with restrictive permissions, never share or commit it, and revoke sessions if exposure is suspected.

Risk: The setup references unpinned external code and a pre-release dependency, increasing supply-chain and behavior-change risk.

Mitigation: Pin and review dependency versions before repeated use, and prefer an official OAuth/API flow for ongoing monitoring.

Risk: Unofficial GraphQL access may fail as query IDs, cookies, rate limits, or platform behavior change.

Mitigation: Monitor 403, 404, and rate-limit failures, pause automation when failures occur, and refresh credentials only through an intentional reviewed process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/twitter-intel)
- [Project homepage](https://canlah.ai)
- [rnet Twitter client](https://github.com/PHY041/rnet-twitter-client)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with Python, shell, and JSON configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include filtered tweet summaries, monitoring configuration, state-file guidance, and trend narratives.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
