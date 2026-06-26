## Description: <br>
Tencent Maps location services skill for POI search, nearby search, route planning, travel planning, and map or trail visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vajraBodhi](https://clawhub.ai/user/vajraBodhi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to turn map-related requests into Tencent Maps CLI commands, map links, POI results, route summaries, travel plans, and trail visualizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tencent Maps API keys may be exposed or over-scoped when configuring the CLI or sharing transcripts. <br>
Mitigation: Use a limited or temporary Tencent Maps API key, configure it through a secure environment or secret store where possible, and never print or share the key. <br>
Risk: Location, route, trail, or home and work coordinates can reveal sensitive personal movement patterns. <br>
Mitigation: Avoid sensitive coordinates and private GPS traces; use generalized or non-sensitive locations when possible. <br>
Risk: The trail visualization feature can use user-provided data URLs, including internal or credential-bearing links. <br>
Mitigation: Use public, non-sensitive JSON data URLs only and avoid signed URLs, internal links, or URLs carrying credentials. <br>


## Reference(s): <br>
- [Tencent Maps Web Service API Overview](https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview) <br>
- [Tencent Location Service](https://lbs.qq.com/) <br>
- [Nearby Search Scenario](references/scene1-nearby-search.md) <br>
- [POI Search Scenario](references/scene2-poi-search.md) <br>
- [Route Planning Scenario](references/scene3-route-planning.md) <br>
- [Travel Planning Scenario](references/scene4-travel-planner.md) <br>
- [Trail Visualization Scenario](references/scene5-trail-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands, Tencent Maps links, formatted text summaries, and optional JSON from raw CLI output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the tmap-lbs CLI and TMAP_WEBSERVICE_KEY for API-backed searches, route planning, and travel planning; trail visualization uses a user-provided JSON data URL.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
