## Description:

Plan Sweden trips with verified entry rules, region-specific routing, rail-ferry logistics, and practical seasonal safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to build Sweden itineraries that account for entry rules, regional routing, transport tradeoffs, seasonality, budget, safety, and local trip context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain Sweden trip preferences and constraints in ~/sweden/memory.md.

Mitigation: Review or delete ~/sweden/memory.md if prior travel preferences should not be reused.

Risk: Travel, entry, transport, and weather guidance can become stale or depend on a traveler's specific status and dates.

Mitigation: Use the skill's official source map and verify entry rules, transport schedules, seasonal conditions, and emergency guidance before booking or travel.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/sweden)
- [Skill Homepage](https://clawic.com/skills/sweden)
- [Official Source Map](artifact/sources.md)
- [Swedish Migration Agency Visitor Guidance](https://www.migrationsverket.se/English/Private-individuals/Visiting-Sweden.html)
- [Swedish Police Travel to and Stay in Sweden](https://polisen.se/en/laws-and-regulations/travel-to-and-stay-in-sweden/)
- [Swedish Customs Traveler Guidance](https://www.tullverket.se/en/private/travelling.4.7df61c5915510cfe9e7106be.html)
- [Visit Sweden Planning Portal](https://visitsweden.com/)
- [SMHI English Weather](https://www.smhi.se/en)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown travel guidance, itineraries, checklists, and occasional shell commands for local memory setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local trip memory in ~/sweden/memory.md when enough user-provided trip context exists.]

## Skill Version(s):

1.0.0 (source: server evidence release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
