## Description:

Use Tibber API data to fetch hourly spot prices, plan cheapest appliance or EV charging windows, detect consumption anomalies, and trigger smart-home actions from price thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmagnomuller](https://clawhub.ai/user/pmagnomuller)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Tibber electricity prices, identify low-cost appliance or EV charging windows, detect unusual hourly consumption, and prepare price-triggered smart-home actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local credential loading can expose sensitive Tibber access tokens when the skill is run from a shared or untrusted directory.

Mitigation: Prefer environment variables or a user-owned config file, keep tokens out of project files, and avoid running the skill from shared or untrusted directories.

Risk: Price-triggered control can run arbitrary on/off command strings when execution mode is enabled.

Mitigation: Keep control in dry-run until thresholds and command text are reviewed, and use only trusted, narrowly scoped smart-home commands.

Risk: The skill requests broad Tibber home and account fields while fetching price and consumption data.

Mitigation: Review API permissions and narrow the queried Tibber GraphQL fields before deployment where data minimization is required.

## Reference(s):

- [Tibber Developer Documentation](https://developer.tibber.com)
- [Tibber GraphQL API](https://api.tibber.com/v1-beta/gql)
- [ClawHub Skill Page](https://clawhub.ai/pmagnomuller/skills/tibber-energy)
- [ClawHub Publisher Profile](https://clawhub.ai/user/pmagnomuller)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and a Tibber personal access token.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
