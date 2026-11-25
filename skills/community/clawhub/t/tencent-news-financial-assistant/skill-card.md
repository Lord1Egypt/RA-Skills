## Description:

Queries current and historical stock prices, market changes, and related financial data through the Tencent News CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to query stock prices, price changes, historical trends, financial indicators, company information, and significant events. The agent presents the CLI's returned data and identifies mismatches between the requested and returned data.

### Deployment Geography for Use:

Global; documented test coverage includes A-share, Hong Kong, and U.S. equities, while other markets are unverified.

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious because it reports direct execution of remote installers, forced CLI updates, and credential-related actions beyond the stock-query purpose; parts of script analysis were partial.

Mitigation: Avoid installation unless the installer and CLI are verified through a trusted source; review requested local changes and update behavior, and keep API keys user-managed and private.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/tencent-adm/skills/tencent-news-financial-assistant)
- [CLI capability and verification notes](references/cli-integration.md)
- [CLI environment and credential guidance](references/cli-environment.md)
- [Installation guide](references/installation-guide.md)
- [Update guide](references/update-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown or JSON-formatted financial data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports fields returned by the CLI; does not provide investment advice.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
