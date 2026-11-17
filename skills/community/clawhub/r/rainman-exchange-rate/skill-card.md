## Description:

Queries real-time exchange rates, historical rates, and rate trends using Frankfurter API data sourced from the European Central Bank.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deusyu](https://clawhub.ai/user/deusyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to convert currencies, query latest or historical rates, inspect rate trends, and list supported currency codes from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires outbound network access to Frankfurter for exchange-rate data.

Mitigation: Allow network access only to the documented Frankfurter API endpoint and treat network, timeout, and HTTP failures as retriable data-access failures.

Risk: The skill may trigger on broad currency terms and natural-language conversion requests.

Mitigation: Confirm source currency, target currency, amount, and date before running commands when the user's request is ambiguous.

Risk: Exchange-rate values may be unsuitable for time-sensitive financial decisions because the source data updates once per working day.

Mitigation: Tell users the data source and update cadence when rate freshness matters.

## Reference(s):

- [Command Map](references/command-map.md)
- [Frankfurter API](https://api.frankfurter.dev/v1)
- [ClawHub Skill Page](https://clawhub.ai/deusyu/skills/rainman-exchange-rate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command results depend on Frankfurter availability and European Central Bank working-day data updates.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
