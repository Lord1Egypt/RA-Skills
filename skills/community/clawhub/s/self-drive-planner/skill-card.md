## Description: <br>
零配置即装即用，提供3项自驾规划工具，支持路线规划与过路费估算、沿途设施搜索和天气查询，基于高德地图实时数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Drivers and travel-planning agents use this skill to plan self-drive trips, estimate distance, time, tolls and fuel or EV costs, find nearby facilities, and review weather-based driving advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel locations and nearby-place searches are sent through the publisher's Tencent SCF proxy for Gaode/Amap lookup. <br>
Mitigation: Use the skill only if that data flow is acceptable, and avoid entering highly sensitive travel plans unless the publisher's proxy and no-storage claim are trusted. <br>
Risk: Route, toll, cost, weather, and facility results can differ from real conditions. <br>
Mitigation: Confirm final navigation, weather, tolls, and stops in an authoritative map or navigation app before driving. <br>
Risk: The release evidence notes a confusing commission or booking disclosure. <br>
Mitigation: Treat booking links and commercial ordering as outside the route-planning result, and independently compare options before booking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/self-drive-planner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON strings containing route plans, cost estimates, POI results, weather data, and driving guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on the publisher's cloud proxy and upstream Gaode/Amap data; cost and travel-time values are estimates.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
