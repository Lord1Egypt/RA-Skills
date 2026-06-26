## Description: <br>
Tencent Maps location-services skill for POI search, nearby search, route planning, travel planning, trajectory visualization, and map data visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qfish](https://clawhub.ai/user/qfish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Tencent Maps points of interest, find nearby places, plan walking, driving, cycling, e-bike, transit, and travel routes, and generate map or trajectory visualization links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map searches, addresses, precise coordinates, route preferences, optional plate numbers, API keys, and generated links may be sent to Tencent services or exposed through chat, logs, or browser history. <br>
Mitigation: Use a temporary, referrer-restricted, quota-limited Tencent Maps key; avoid sharing generated links; and rotate any key that appears outside the intended configuration. <br>
Risk: Trajectory visualization can expose sensitive GPS traces or private signed data URLs. <br>
Mitigation: Use only non-sensitive trajectory data and avoid private, signed, or personally identifying GPS data URLs. <br>
Risk: Tencent Maps API responses can fail, be quota-limited, or return incomplete location and routing results. <br>
Mitigation: Check API status values, review generated routes and POI results before acting on them, and ask the user to verify important location decisions. <br>


## Reference(s): <br>
- [Tencent Maps Web Service API Overview](https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview) <br>
- [Tencent Location Services](https://lbs.qq.com/) <br>
- [Tencent Maps Place Search API Documentation](https://lbs.qq.com/service/webService/webServiceGuide/webServiceSearch) <br>
- [Scene 1: Keyword Search](references/scene1-keyword-search.md) <br>
- [Scene 2: Nearby Search](references/scene2-nearby-search.md) <br>
- [Scene 3: POI Search](references/scene3-poi-search.md) <br>
- [Scene 4: Route Planning](references/scene4-route-planning.md) <br>
- [Scene 5: Travel Planning](references/scene5-travel-planner.md) <br>
- [Scene 7: Trail Map](references/scene7-trail-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with URLs, shell command examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TMAP_LBS_CONFIG for Tencent Maps API-backed actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
