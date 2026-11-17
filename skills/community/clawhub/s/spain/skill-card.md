## Description:

Plans Spain travel with local-level picks for itineraries, restaurants, regional rules, timing, booking windows, logistics, and tourist-trap avoidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to plan Spain trips, compare regions and cities, build itineraries, choose restaurants and experiences, and prepare practical logistics. It advises only and does not book, pay, or transact on the user's behalf.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the release suspicious because the skill under-discloses local file access and may move legacy preference files while claiming it stays within one data folder.

Mitigation: Review local-file behavior before installing, confirm any legacy file movement with the user, and limit preference reads and writes to the documented Clawic data paths.

Risk: Stored travel preferences can reveal itinerary details, dietary needs, mobility needs, budget, and other personal travel context.

Mitigation: Store only preferences the user explicitly provides, keep them local, and avoid reading shared profile data without clear user consent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/spain)
- [Clawic Spain skill page](https://clawic.com/skills/spain)
- [Clawic skill library](https://clawic.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or plain text travel advice, itineraries, named recommendations, and local preference updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and persist user travel preferences under ~/Clawic/data/spain/ when the user reveals them.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
