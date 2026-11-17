## Description:

Monitors configured social channels daily to identify trending topics, viral content, and new content ideas within a user-selected niche, delivering structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryudi84](https://clawhub.ai/user/ryudi84)

### License/Terms of Use:


## Use Case:

Content creators, marketers, and agents use this skill to monitor configured social and feed sources, identify high-engagement topics and formats, and produce daily content ideas for a selected niche.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses configured sources and optional Twitter API credentials.

Mitigation: Review sources.json before installation and include only sources and credentials the agent is authorized to use.

Risk: Generated trend reports may be saved under data/ and shared through a configured notification channel.

Mitigation: Confirm that local report storage and the notification channel are appropriate for the derived trend summaries before enabling scheduled use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryudi84/skills/sovereign-content-scraper)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON report saved as data/trend-report-{date}.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily report includes trending topics, content ideas, viral formats, source evidence, suggested angles, hooks, key points, and calls to action.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
