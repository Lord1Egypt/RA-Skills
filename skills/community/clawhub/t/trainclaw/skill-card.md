## Description: <br>
TrainClaw queries China Railway 12306 for tickets, route stops, and transfer plans without login, with filters for train type, time, and duration. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[AI4MSE](https://clawhub.ai/user/AI4MSE) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run explicit China rail ticket, route-stop, and transfer lookups through a Python CLI and return results to an agent or user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route, date, and station details may be sent to China Railway 12306 endpoints during lookups. <br>
Mitigation: Use only for explicit ticket, train-stop, or transfer queries, and avoid submitting sensitive travel details unless the user accepts the network lookup. <br>
Risk: Station data is cached locally and lookup results depend on 12306 availability and recommendation logic. <br>
Mitigation: Treat schedules, seats, prices, and transfer plans as lookup results to verify before travel decisions; refresh or clear cached station data if stale data is suspected. <br>
Risk: Broad trigger wording could run lookups when the user only mentions rail travel casually. <br>
Mitigation: Ask for confirmation before executing network calls unless the request clearly asks for ticket, stop, or transfer information. <br>


## Reference(s): <br>
- [ClawHub TrainClaw Release](https://clawhub.ai/AI4MSE/trainclaw) <br>
- [TrainClaw Skill Instructions](artifact/SKILL_EN.md) <br>
- [TrainClaw README](artifact/README_ENG.md) <br>
- [China Railway 12306](https://www.12306.cn/index/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, CSV, Guidance] <br>
**Output Format:** [Plain text, JSON, or CSV query results with shell-command invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Errors are written to stderr, data to stdout, and station data may be cached locally for repeated lookups.] <br>

## Skill Version(s): <br>
0.0.7 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
