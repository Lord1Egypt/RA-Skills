## Description:

Generates multilingual travel-guide itineraries as responsive HTML and companion exports, including daily plans, routes, lodging, food, budget guidance, and travel caveats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmmg55](https://clawhub.ai/user/gmmg55)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users planning leisure trips use this skill to turn a destination, trip length, origin, and preferences into a reviewable itinerary package. It is aimed at travel-guide creation rather than booking, visa handling, business travel, or payment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel preferences and route queries may be used for web research or optional Amap routing.

Mitigation: Avoid including sensitive personal details in trip prompts, and use the offline route estimator when privacy or Amap coverage is a concern.

Risk: AMAP_KEY is a sensitive credential when optional precise routing is enabled.

Mitigation: Provide it through a temporary environment variable or secrets manager, do not paste it into chat, and rotate it if exposure is suspected.

Risk: Generated travel details such as route times, opening hours, weather, and prices can be stale, estimated, or incomplete.

Mitigation: Review sources and confirm live details before booking or departure; keep estimated routes clearly labeled in generated outputs.

Risk: One dependency maintenance issue is noted in the security guidance.

Mitigation: Use Python 3.10+ where possible and update the requests dependency pin when compatible with the runtime.

## Reference(s):

- [Travel Guide Generator README](README.md)
- [Travel guide schema](references/guide-schema.json)
- [Daily itinerary HTML specification](references/daily-itinerary-spec.md)
- [HTML design specification](references/design-spec.md)
- [Amap Open Platform](https://lbs.amap.com/)
- [ClawHub skill page](https://clawhub.ai/gmmg55/skills/travel-guide-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, JSON, ICS calendar files, GeoJSON, Guidance]

**Output Format:** [Responsive HTML files, Markdown summaries, ICS, GeoJSON, normalized JSON, and conversational text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use optional AMAP_KEY for route lookups; falls back to labeled estimates when the API is unavailable.]

## Skill Version(s):

2.0.0 (source: server release evidence, artifact metadata, and README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
