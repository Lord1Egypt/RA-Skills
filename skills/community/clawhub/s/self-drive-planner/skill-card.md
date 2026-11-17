## Description:

自驾出行规划助手，基于高德地图实时数据，支持路线规划与过路费估算、沿途加油站/充电桩/服务区搜索和天气查询，零配置即装即用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan self-drive trips, compare route strategy, estimate toll and energy costs, find nearby travel facilities, and review weather-based driving advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive home, work, school, medical, waypoint, nearby-search, or weather-query locations may be sent to the proxy service and upstream map or weather services.

Mitigation: Review data-sharing expectations before use and avoid entering sensitive locations unless that disclosure is acceptable.

Risk: Route, toll, fuel, charging, facility, and weather details are estimates that may be outdated or differ from actual road conditions.

Mitigation: Confirm final navigation, costs, charging availability, and severe-weather decisions with authoritative mapping, weather, and service-provider sources before driving.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/travel-skills/skills/self-drive-planner)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON strings containing route, POI, weather, cost, and driving-advice fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are estimates and recommendations; route, weather, facility, toll, fuel, and charging information may differ from real-world conditions.]

## Skill Version(s):

1.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
