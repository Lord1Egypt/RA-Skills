## Description:

Plan Turkey trips with city-coast-Cappadocia routing, verified entry rules, domestic transport strategy, and practical seasonal safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel planners use this skill to design Turkey trips around entry requirements, route clusters, domestic transport, lodging, budget, seasonality, safety, and region-specific tradeoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store trip preferences and constraints locally in ~/turkey/memory.md.

Mitigation: Avoid saving highly sensitive personal details unless needed, and review or delete ~/turkey/memory.md when trip context should no longer be retained.

Risk: Travel rules, visa pathways, transport schedules, museum access, weather alerts, and safety conditions can change after the skill's source links were last checked.

Mitigation: Refresh official sources close to departure before relying on time-sensitive travel decisions.

## Reference(s):

- [Republic of Turkey MFA visa information](https://www.mfa.gov.tr/visa-information-for-foreigners.en.mfa)
- [Official e-Visa portal](https://www.evisa.gov.tr/en/)
- [GoTurkiye travel planning portal](https://goturkiye.com/)
- [Official museums portal](https://muze.gov.tr/)
- [TCDD Tasimacilik](https://www.tcddtasimacilik.gov.tr/)
- [Istanbul Airport transport](https://www.igairport.aero/en/transport)
- [AFAD disaster and emergency authority](https://www.afad.gov.tr/en/)
- [Turkish State Meteorological Service](https://www.mgm.gov.tr/eng/forecast-cities.aspx)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown travel-planning guidance with structured itinerary, logistics, and safety notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initialize and reuse a scoped local trip-memory file at ~/turkey/memory.md.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
