## Description: <br>
火车票智能中转方案推荐助手。查火车票/高铁票/动车票/12306余票，智能拼接中转换乘方案，学习用户偏好（坐席策略、时间偏好、中转约束）。火车票查询/余票/车次/预订/中转换乘/坐席偏好。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangxchao](https://clawhub.ai/user/zhangxchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-assistant agents use this skill to query China Railway train availability, compare direct and transfer options, apply seat and time preferences, and present booking links from flyai search-train results. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local travel preferences and trip history, which may reveal sensitive travel plans. <br>
Mitigation: Use only when comfortable with local preference and history storage; clear assets/history.json and avoid saved defaults for sensitive trips. <br>
Risk: The skill depends on the external flyai CLI and may send train-search details and optional API credentials to that provider. <br>
Mitigation: Review the installed flyai CLI and API-key provider before use, and avoid configuring FLYAI_API_KEY unless the provider is acceptable. <br>
Risk: Booking recommendations can be stale or incorrect if search conditions change or API results are misunderstood. <br>
Mitigation: Re-run searches whenever date, route, time, seat, or transfer constraints change, and verify returned details before booking. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhangxchao/super-train) <br>
- [flyai search-train command reference](references/flyai-cli-reference.md) <br>
- [FlyAI Open Platform](https://flyai.open.fliggy.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses flyai search-train results and may update local preference and trip-history JSON files.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
