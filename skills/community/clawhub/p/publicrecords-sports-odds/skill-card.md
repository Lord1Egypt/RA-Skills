## Description:

Retrieves live and pre-game odds from Kambi-powered sportsbooks and compares prices by game and outcome; it provides data, not betting advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geminigeorge22](https://clawhub.ai/user/geminigeorge22)

### License/Terms of Use:

MIT-0

## Use Case:

Sports fans and analysts can request current odds for a supported league or game and compare sportsbook prices, including the best price per outcome. The skill fetches odds data and does not provide betting advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marked the skill suspicious because its described odds task does not match the placeholder Actor request, and the recommended MCP connection exposes unrelated Actors. The review was partial.

Mitigation: Confirm the Actor target before installation, limit the MCP connection to the sports odds service and required helpers, and review the unresolved local references.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/geminigeorge22/skills/publicrecords-sports-odds)
- [Publisher profile](https://clawhub.ai/user/geminigeorge22)
- [Apify Sports Odds API Actor](https://apify.com/publicrecords/sports-odds-api)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Odds records returned as JSON dataset items, with concise text comparisons when summarized.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One record per game with sportsbook prices and best prices per outcome; may cover live and pre-game odds.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
