## Description:

Plan Taiwan trips with city-specific food, rail, hot spring, and regional tips that avoid tourist filler and logistics mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers use this skill to plan Taiwan trips by matching cities, routes, food, transport, lodging, beaches, hiking, tea, nightlife, and family pacing to their itinerary. It helps the agent ask useful trip-planning questions and optionally keep Taiwan travel preferences in local memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain Taiwan trip preferences such as dates, pace, transport style, food restrictions, and travel history in local memory if the user opts in.

Mitigation: Ask before retaining preferences, keep saved details limited to Taiwan trip planning, and store them only under ~/taiwan/.

Risk: Travel guidance can become stale for weather, closures, prices, schedules, typhoon impacts, emergencies, and other live conditions.

Mitigation: Verify current sources before finalizing time-sensitive travel, transport, outdoor, beach, mountain, ferry, or emergency advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/taiwan)
- [Skill homepage](https://clawic.com/skills/taiwan)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown travel-planning guidance with optional local preference notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask follow-up questions and may use local memory under ~/taiwan/ when the user opts in.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
