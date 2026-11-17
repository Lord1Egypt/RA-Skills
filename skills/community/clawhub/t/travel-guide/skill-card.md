## Description:

Travel Guide is a bilingual travel-planning agent skill that helps users plan holiday and destination trips with recommendations, practical logistics, itinerary ideas, and pitfall-avoidance guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuqingsonga](https://clawhub.ai/user/zhuqingsonga)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning assistants use this skill to collect trip preferences, compare holiday or destination options, and produce practical travel guidance for China-focused and international trips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel details such as visa rules, safety conditions, weather, opening hours, prices, and booking availability can change after the static reference files were written.

Mitigation: Verify current information with authoritative travel, venue, carrier, and booking sources before making commitments.

Risk: Destination recommendations may not fit a user's budget, mobility needs, risk tolerance, or travel constraints if the initial preferences are incomplete.

Mitigation: Collect travel dates, party size, budget, transportation, lodging, interests, and constraints before presenting recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuqingsonga/skills/travel-guide)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Spring Festival holiday guide](references/holidays/china/春节.md)
- [National Day holiday guide](references/holidays/china/国庆.md)
- [Summer vacation guide](references/holidays/china/暑假.md)
- [Christmas holiday guide](references/holidays/western/christmas.md)
- [Sanya travel guide](references/destinations/china/三亚.md)
- [Beijing travel guide](references/destinations/china/北京.md)
- [Chengdu travel guide](references/destinations/china/成都.md)
- [Japan travel guide](references/destinations/international/japan.md)
- [Thailand travel guide](references/destinations/international/thailand.md)
- [France travel guide](references/destinations/international/france.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown travel-planning guidance with questions, recommendations, practical tips, and itinerary outlines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include destination comparisons, budget-aware recommendations, safety notes, and caveats about information that should be verified before booking.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
