## Description: <br>
零配置即装即用，查询任意两个地点之间的公交和地铁路线，自动规划最优换乘方案，地铁优先展示，支持最快、少换乘、少步行三种策略。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and transit users use this skill to ask for local bus and metro routes between two places, compare fastest, fewer-transfer, or less-walking strategies, and receive formatted transfer steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route searches share origin, destination, city, and strategy details with the publisher's proxy service and the underlying map provider. <br>
Mitigation: Avoid highly sensitive home, workplace, or personal itinerary details when that privacy tradeoff is unacceptable. <br>
Risk: Transit times, fares, and last-train details may differ from current local operations. <br>
Mitigation: Check official transit notices or a map app before relying on time-sensitive travel plans. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/transit-route-query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-formatted Chinese text with route options, transfer steps, walking distances, estimated time, and cost.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts origin, destination, city, and optional strategy; returns metro-prioritized and bus route options when available.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
