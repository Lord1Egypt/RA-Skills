## Description:

World Cup 2026 is a Chinese-localized viewing assistant that answers schedule, matchup-intensity, upset-odds, group, knockout, and score-prediction questions with chat-native Markdown tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External users and football fans use this skill to choose which 2026 World Cup matches to watch, inspect team schedules, find high-intensity or upset-potential games, and get transparent score predictions from local tournament data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Update requests for odds, rankings, or knockout teams can modify local JSON data and affect later answers.

Mitigation: Review pasted update data before permitting changes and preserve prior data when the release process requires auditability.

Risk: Predictions and upset-odds answers are simplified estimates based on local ranking, odds, rivalry, and Poisson assumptions.

Mitigation: Present probabilities as estimates, disclose model limitations when relevant, and refresh time-sensitive data before relying on it.

## Reference(s):

- [World Cup 2026 ClawHub release page](https://clawhub.ai/kyro-ma/skills/world-cup-2026)
- [README](artifact/README.md)
- [Intensity scoring model](artifact/assets/scoring.md)
- [Score prediction model](artifact/assets/prediction.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Analysis, Guidance]

**Output Format:** [Chat-native Markdown tables and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON schedule, team, odds, and rivalry data; default responses are capped to short ranked lists rather than full tournament dumps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
