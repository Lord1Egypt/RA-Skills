## Description:

Tencent Maps location-service skill for POI search, nearby search, route planning, travel planning, map data visualization, and trail visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qfish](https://clawhub.ai/user/qfish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to answer location questions, search Tencent Maps points of interest, plan routes or travel itineraries, and generate map or trail visualization links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Tencent Maps URLs can expose a Tencent Maps API key and precise location or travel data.

Mitigation: Use a restricted temporary Tencent Maps API key, avoid entering sensitive home or work routes, private itinerary details, vehicle plate numbers, or secret-bearing trajectory URLs, and avoid sharing generated links that contain a key.

Risk: The security verdict is suspicious because location workflows may send precise user data to Tencent Maps.

Mitigation: Review before installing and prefer an updated release that keeps API keys server-side and warns users before sending location data to Tencent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qfish/skills/tmap-lbs-service)
- [Tencent Maps Web Service overview](https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview)
- [Tencent Maps service](https://lbs.qq.com/)
- [Tencent Maps place search API documentation](https://lbs.qq.com/service/webService/webServiceGuide/webServiceSearch)
- [Keyword search workflow](references/scene1-keyword-search.md)
- [Nearby search workflow](references/scene2-nearby-search.md)
- [POI search workflow](references/scene3-poi-search.md)
- [Route planning workflow](references/scene4-route-planning.md)
- [Travel planner workflow](references/scene5-travel-planner.md)
- [Trail map workflow](references/scene7-trail-map.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with Tencent Maps URLs, inline shell commands, and JSON-shaped API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and TMAP_LBS_CONFIG for API-backed Tencent Maps workflows.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
