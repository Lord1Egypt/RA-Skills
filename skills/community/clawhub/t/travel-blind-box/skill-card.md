## Description: <br>
真正的盲盒旅行规划器！用户只需提供当前位置、出发日期、天数和预算，自动推荐未去过的目的地并生成轻松行程。使用 flyai skill 查询实时信息，支持历史记录管理避免重复。主打新奇体验和随意放松。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haoxuanljj](https://clawhub.ai/user/haoxuanljj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to generate surprise travel plans from their current city, departure date, trip length, and budget. It helps an agent propose unfamiliar destinations, relaxed itineraries, budget splits, booking links, and updated Markdown trip documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated itineraries and booking summaries may include sensitive travel dates, hotel addresses, phone numbers, and confirmation numbers. <br>
Mitigation: Avoid entering full confirmation numbers unless needed, redact sensitive details before sharing, and review generated documents before sending them to others. <br>
Risk: The skill can store visited-city history in a local file, which may reveal travel patterns. <br>
Mitigation: Periodically review or delete the local history file and avoid sharing it with generated itinerary documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haoxuanljj/travel-blind-box) <br>
- [README.md](README.md) <br>
- [QUICKSTART.md](QUICKSTART.md) <br>
- [TESTING.md](TESTING.md) <br>
- [example_outputs/itinerary_example.md](example_outputs/itinerary_example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown itinerary documents, plain-text travel guidance, and optional JSON from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include travel dates, hotel addresses, booking links, booking confirmation numbers, and locally stored travel-history summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact package.json reports 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
