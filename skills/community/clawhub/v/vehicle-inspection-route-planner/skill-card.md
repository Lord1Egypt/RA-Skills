## Description: <br>
规划上班沿途车辆年检最优路线。输入家庭地址、公司地址和检测站列表，调用高德地图API计算实时路况下的驾车路线，输出带时间轴的Top5出行方案（含逐段导航明细）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shengbinxu](https://clawhub.ai/user/shengbinxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Drivers and agents use this skill to compare vehicle inspection stops along a commute, using a home address, work address, departure time, inspection duration, and candidate station list. It produces ranked route plans with driving durations, distance, arrival times, and turn-by-turn details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided AMap API key and route inputs that may reveal sensitive location patterns. <br>
Mitigation: Provide the API key only at runtime, do not hard-code or persist credentials, and avoid retaining reports that expose private home or workplace addresses. <br>
Risk: Route duration and arrival estimates depend on real-time traffic and geocoding quality at query time. <br>
Mitigation: Re-run planning near the intended travel time, review station locations before driving, and verify inspection appointments, required materials, and traffic constraints independently. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shengbinxu/skills/vehicle-inspection-route-planner) <br>
- [高德开放平台 Web 服务 Key](https://console.amap.com/dev/key/app) <br>
- [交通安全综合服务管理平台](https://122.gov.cn/) <br>
- [交管12123 APP](https://122.gov.cn/#/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown route report with a ranked overview table, per-route timeline, and navigation details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided AMap Web Service API key, origin and destination addresses, departure time, inspection duration, city, station CSV, and requested Top N count.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
