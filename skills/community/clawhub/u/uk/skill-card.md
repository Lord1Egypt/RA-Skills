## Description:

Plan United Kingdom trips with nation-specific routing, ETA-aware entry rules, rail-road tradeoffs, and practical local logistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to plan UK trips across England, Scotland, Wales, and Northern Ireland with entry checks, regional routing, transport choices, budgets, seasonality, accessibility, and on-the-ground logistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps durable UK trip preferences and constraints in ~/uk/memory.md.

Mitigation: Review or delete ~/uk/memory.md if durable trip memory is not desired.

Risk: Entry, transport, weather, and emergency guidance can change after the release evidence was checked.

Mitigation: Confirm time-sensitive travel decisions against the official sources listed in artifact/sources.md before booking or traveling.

## Reference(s):

- [United Kingdom skill page](https://clawhub.ai/ivangdavila/skills/uk)
- [Skill homepage](https://clawic.com/skills/uk)
- [Official source map](artifact/sources.md)
- [UK ETA guidance](https://www.gov.uk/guidance/apply-for-an-electronic-travel-authorisation-eta)
- [Check if you need a UK visa](https://www.gov.uk/check-uk-visa)
- [National Rail journey planning and service info](https://www.nationalrail.co.uk/)
- [TfL transport accessibility](https://tfl.gov.uk/transport-accessibility/)
- [Met Office weather warnings and advice](https://www.metoffice.gov.uk/weather/warnings-and-advice)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown travel plans, checklists, decision trees, and local memory updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store trip preferences and planning constraints in ~/uk/memory.md.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
