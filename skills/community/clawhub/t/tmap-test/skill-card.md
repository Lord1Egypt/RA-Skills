## Description: <br>
Tencent Maps location services skill for POI search, route planning, travel planning, nearby search, trajectory visualization, and map data visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qfish](https://clawhub.ai/user/qfish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Tencent Maps locations, find nearby POIs, plan routes or trips, and generate map or trail visualization links from user-supplied places, coordinates, or trajectory data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map queries, route details, trajectory links, plate numbers, and API-key-bearing URLs can expose sensitive location or credential information. <br>
Mitigation: Use temporary referrer- or IP-restricted Tencent Maps API keys with quota limits, avoid sharing generated URLs, rotate keys after use, and avoid submitting sensitive home, work, route, trajectory, or plate-number data unless necessary. <br>


## Reference(s): <br>
- [Tencent Maps Web Service Overview](https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview) <br>
- [Tencent Location Services](https://lbs.qq.com/) <br>
- [Tencent Maps Place Search API](https://lbs.qq.com/service/webService/webServiceGuide/webServiceSearch) <br>
- [Keyword Search Scenario](references/scene1-keyword-search.md) <br>
- [Nearby Search Scenario](references/scene2-nearby-search.md) <br>
- [POI Search Scenario](references/scene3-poi-search.md) <br>
- [Route Planning Scenario](references/scene4-route-planning.md) <br>
- [Travel Planner Scenario](references/scene5-travel-planner.md) <br>
- [Trail Map Scenario](references/scene7-trail-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with Tencent Maps links, shell command examples, and JSON API result summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a Tencent Maps API key configured through TMAP_LBS_CONFIG for API-backed searches and route planning.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
