## Description:

Research time-stamped public sportsbook markets alongside event context from DraftKings Sportsbook, ESPN, SofaScore, and Flashscore without placing wagers or accessing accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and reporters use this skill to compare public, time-stamped odds and markets while cross-checking schedules, participants, and game status. It is not for wagering decisions or account actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sports lookup queries are sent to Crawlora and require an API key.

Mitigation: Use a dedicated key and avoid including secrets, personal information, or non-public account data in queries.

Risk: Public odds snapshots can become stale or be unavailable in a viewer's jurisdiction and can be mistaken for wagering advice.

Mitigation: Record collection time and locale, verify material decisions with the licensed operator and local rules, and do not use snapshots as wagering advice.

## Reference(s):

- [Endpoint reference](artifact/reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/sports-betting-research)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Time-stamped public odds comparisons; sports lookup responses can be JSON.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
