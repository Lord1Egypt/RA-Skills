## Description:

Track movies and series with progress, watchlist, ratings, and proactive alerts for new releases and platform changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this agent skill to maintain a personal or family media tracker, including current progress, watchlists, completed titles, ratings, recommendations, and release reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist viewing history, preferences, family-member details, and child-specific reaction notes in local files.

Mitigation: Use aliases or age ranges for children, avoid recording unnecessary sensitive reactions, and periodically review or delete the local ~/shows files.

## Reference(s):

- [Discovery & Recommendations](artifact/discovery.md)
- [Family Viewing Mode](artifact/family.md)
- [Streaming Platforms](artifact/platforms.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown records and concise natural-language responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local media-tracking files under ~/shows/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
