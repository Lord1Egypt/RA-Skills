## Description:

Generates personalized travel plans by collecting trip details, querying AMAP REST APIs for routes, places, distances, restaurants, and hotels, and combining that data with weather lookup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bifang988](https://clawhub.ai/user/bifang988)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to build detailed AMAP-backed itineraries from group composition, origin, destination, travel dates, budget, and preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trip details such as origin, destination, dates, group composition, budget, and preferences may be shared with AMAP and a weather search provider.

Mitigation: Inform users before lookup, minimize submitted details where possible, and skip or remove the weather search step when third-party exposure should be reduced.

Risk: An AMAP API key could be exposed or over-permissioned if stored permanently or configured without restrictions.

Mitigation: Use a restricted AMAP Web Service key, configure IP allowlisting and only required service permissions, and avoid saving the key in shell startup files.

## Reference(s):

- [AMAP Open Platform](https://lbs.amap.com)
- [ClawHub Skill Page](https://clawhub.ai/bifang988/skills/travel-planner-amap)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown itinerary with inline shell and Python command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AMAP_KEY environment variable and user-provided trip details.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
