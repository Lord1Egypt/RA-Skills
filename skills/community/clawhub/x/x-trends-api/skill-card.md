## Description:

Get trending topics on X (Twitter) using the X API for worldwide or location-specific trend checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryds](https://clawhub.ai/user/terryds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch X trend data for a WOEID location, limit result counts, and look up WOEID values for cities or countries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the configured bearer token to api.x.com when fetching trends.

Mitigation: Use a token scoped only for the X API access the skill needs and review token permissions before installation.

Risk: Trend queries reveal the WOEID locations requested to the X API.

Mitigation: Run the skill only for locations you are comfortable querying through api.x.com.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terryds/skills/x-trends-api)
- [X Developer Portal](https://developer.x.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; helper scripts emit JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and X_BEARER_TOKEN; trend output includes trend names and tweet counts when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
