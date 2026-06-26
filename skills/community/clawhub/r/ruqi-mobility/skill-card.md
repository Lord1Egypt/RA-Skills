## Description: <br>
如祺出行打车助手。提供实时叫车、价格预估、订单跟踪、司机位置查询、路线规划等完整出行服务。触发词："打车"、"叫车"、"去[地点]"、"回家"、"上班"、"下班"、"查价格"、"路线规划"、"怎么走"、"取消订单"、"司机"、"查订单"。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruqi](https://clawhub.ai/user/ruqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill through an agent to request RuQi rides, estimate fares, confirm pickup and destination details, place orders, cancel orders, and track drivers or active ride status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores account tokens, phone numbers, and saved home or work locations in plaintext. <br>
Mitigation: Install only when comfortable with this data exposure, and delete or rotate saved tokens and addresses when they are no longer needed. <br>
Risk: Live trip details and screenshots may be sent to configured chat targets. <br>
Mitigation: Verify the RUQI_TARGET destination before use and avoid shared channels for ride updates. <br>


## Reference(s): <br>
- [RuQi Mobility homepage](https://www.ruqimobility.com) <br>
- [RuQi mini app download page](https://web.ruqimobility.com/ruqi/index.html#/download?to=service&pagePath=pages%2Findex%2Findex&toPlatform=miniApp&skipType=3) <br>
- [ClawHub skill page](https://clawhub.ai/ruqi/ruqi-mobility) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and openclaw; uses RuQi account, phone, token, location, order, driver, chat target, and screenshot data during ride workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
