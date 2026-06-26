## Description: <br>
Tencent Maps location-service skill for POI search, nearby search, route planning, travel planning, and map or trajectory visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vajraBodhi](https://clawhub.ai/user/vajraBodhi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to search Tencent Maps places, inspect nearby points of interest, plan walking, driving, bicycling, electric-bike, transit, and travel routes, and generate links for map or trajectory visualization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task-related location and travel details may be sent to Tencent Maps. <br>
Mitigation: Use the skill only when sharing those details with Tencent Maps is acceptable. <br>
Risk: Generated links and API calls may include a Tencent Maps key. <br>
Mitigation: Use a temporary, tightly restricted key and avoid sharing generated links that contain the real key. <br>
Risk: Home or work routes, vehicle plate numbers, private trajectory URLs, or signed data links can reveal sensitive personal information. <br>
Mitigation: Avoid submitting those values unless they are necessary for the task. <br>


## Reference(s): <br>
- [Tencent Maps Web Service API Overview](https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview) <br>
- [Tencent Location Service](https://lbs.qq.com/) <br>
- [Tencent Maps Place Search API](https://lbs.qq.com/service/webService/webServiceGuide/webServiceSearch) <br>
- [Scene 1: Keyword Search](references/scene1-keyword-search.md) <br>
- [Scene 2: Nearby Search](references/scene2-nearby-search.md) <br>
- [Scene 3: POI Search](references/scene3-poi-search.md) <br>
- [Scene 4: Route Planning](references/scene4-route-planning.md) <br>
- [Scene 5: Travel Planning](references/scene5-travel-planner.md) <br>
- [Scene 7: Trail Map](references/scene7-trail-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with Tencent Maps URLs, inline shell commands, and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some workflows require node and the TMAP_LBS_CONFIG environment variable.] <br>

## Skill Version(s): <br>
1.1.32 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
