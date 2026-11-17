## Description:

Plans multi-day road trip routes in mainland China using Amap APIs, generates personal-map QR codes for continuous routes, and outputs daily itinerary details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlydreams](https://clawhub.ai/user/onlydreams)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to design mainland China self-driving itineraries with daily driving limits, route continuity, supply-point checks, seasonal cautions, and Amap personal-map QR output.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: The skill sends route locations and trip details to Amap APIs and official live-information sources.

Mitigation: Use the skill only when Amap-based mainland China route planning is intended, avoid sensitive trip details, and use a scoped Amap API key.

Risk: The skill relies on the external personal-map dependency and an AMAP_API_KEY before route generation can work.

Mitigation: Verify that the installed dependency is the intended @lbs-amap personal-map package and confirm the API key is configured before making API calls.

Risk: Seasonal guidance and route API results may not reflect current road closures, weather warnings, attraction access, or holiday traffic rules.

Mitigation: Verify official traffic, weather, attraction, reservation, and holiday information for the actual departure dates before finalizing an itinerary.

## Reference(s):

- [Server-resolved source repository](https://github.com/Onlydreams/road-trip-planner)
- [Road Trip Planner release page](https://clawhub.ai/onlydreams/skills/road-trip-planner)
- [Amap personal-map dependency](https://clawhub.ai/lbs-amap/personal-map)
- [Amap SDK skills repository](https://github.com/amap-demo/amap-sdk-skills)
- [Amap Open Platform](https://lbs.amap.com/)
- [Seasonal Checklist](references/seasonal.md)
- [Examples](examples.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, API calls, Files, Guidance]

**Output Format:** [Markdown itinerary with tables, inline shell commands, QR image path, and fallback map link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a temporary QR image file and depends on Amap API responses and current official travel information.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
