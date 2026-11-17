## Description:

市内公交地铁路线查询，自动规划最优换乘方案，地铁优先展示，支持最快/少换乘/少步行三种策略，零配置即装即用。暑期城市出行导航。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask for same-city public transit routes between an origin and destination. It returns route options for bus and metro travel, with strategy choices for fastest travel, fewer transfers, or less walking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Route queries send origin, destination, and city details to the skill's cloud proxy and map provider.

Mitigation: Avoid highly sensitive home, workplace, or routine-location queries unless that data sharing is acceptable.

Risk: Transit times, fares, and route options may differ from current local operations.

Mitigation: Treat route details as estimates and check local transit or map apps for real-time service changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/transit-route-query)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with route summaries, step-by-step transit segments, estimated duration, walking distance, and fare where available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Route details are estimates and do not include real-time arrival information.]

## Skill Version(s):

1.0.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
