## Description:

Plan United States trips with region-specific routing, verified entry rules, transport logistics, and practical tourist safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External travelers and travel-planning agents use this skill to plan U.S. trips that account for entry requirements, regional routing, transport tradeoffs, seasonality, cost, accessibility, and tourist safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel rules, entry requirements, permits, prices, and safety conditions can change after the skill content was authored.

Mitigation: Verify official sources before booking, relying on entry guidance, using emergency information, or committing to time-sensitive reservations.

Risk: The skill stores trip preferences locally in ~/united-states/memory.md.

Mitigation: Avoid storing unnecessary sensitive personal, immigration, payment, or medical details; review or delete the local memory file when it is no longer needed.

Risk: The content is scoped to United States travel and may not generalize to other destinations.

Mitigation: Use this skill only for U.S. travel planning, and switch to destination-specific guidance for non-U.S. trips.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/united-states)
- [Clawic skill homepage](https://clawic.com/skills/united-states)
- [U.S. Visitor Visa](https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html)
- [CBP Visa Waiver Program](https://www.cbp.gov/travel/international-visitors/visa-waiver-program)
- [CBP ESTA overview](https://www.cbp.gov/travel/international-visitors/esta)
- [TSA REAL ID](https://www.tsa.gov/real-id)
- [NPS entrance passes](https://www.nps.gov/planyourvisit/passes.htm)
- [Recreation.gov](https://www.recreation.gov/)
- [FEMA Ready alerts](https://www.ready.gov/alerts)
- [AirNow air quality](https://www.airnow.gov/air-quality-and-health/)
- [Artifact source map](artifact/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with occasional shell command snippets and local memory updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initialize or update local trip context under ~/united-states/ when the user chooses to use persistent planning memory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
