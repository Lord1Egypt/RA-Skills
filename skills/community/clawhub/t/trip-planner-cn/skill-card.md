## Description: <br>
行程规划助手，支持往返/单程行程规划，涵盖航班、高铁、机场周边、时间约束筛选和详细时间线生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doushen-cloud](https://clawhub.ai/user/doushen-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to compare air, rail, and local ground-transport options for China-focused one-way or round-trip travel plans under specific time constraints. The skill helps produce filtered options, an optimal itinerary timeline, and practical reminders such as airport or station buffer time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trip planning may involve sensitive travel-pattern, home, or workplace details when external travel and map services are used. <br>
Mitigation: Avoid sending sensitive exact locations unless needed, and confirm before external lookups when a simple travel question does not require them. <br>
Risk: Travel schedules and parsed route data can be incomplete or misleading if lazy-loaded pages, connector responses, or arrival-airport checks are not verified. <br>
Mitigation: Load complete travel results, validate key flights or trains against source data before recommending them, and clearly label estimates or historical timetable references. <br>


## Reference(s): <br>
- [Trip Planner CN on ClawHub](https://clawhub.ai/doushen-cloud/trip-planner-cn) <br>
- [doushen-cloud publisher profile](https://clawhub.ai/user/doushen-cloud) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown itinerary recommendations with comparison tables, timelines, and notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference external travel or map lookup results and should mark estimates when exact data is unavailable.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
