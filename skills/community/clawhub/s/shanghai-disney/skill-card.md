## Description: <br>
零配置即装即用，提供7项游园工具，含排队预估和路线规划，基于高德地图与本地数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users planning visits to Shanghai Disney Resort use this skill to estimate attraction waits, plan routes, review shows, check dining options, and look up recent park hours. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Schedule lookup uses a cloud proxy with an automatically provided proxy token. <br>
Mitigation: Install only when that network path is acceptable, and avoid sending unnecessary personal details in schedule queries. <br>
Risk: Wait times, ticket prices, and schedules may differ from current park conditions. <br>
Mitigation: Verify important plans, prices, bookings, and same-day operating details in the official Shanghai Disney app or website. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/shanghai-disney) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-like Chinese text responses with structured recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some schedule lookups may use a cloud proxy; wait times, ticket prices, and schedules should be treated as estimates.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
