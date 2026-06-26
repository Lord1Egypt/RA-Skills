## Description: <br>
Catalyst Calendar tracks upcoming market-moving macro, crypto, regulatory, exchange, conference, and earnings events and pre-flags relevant assets 7-14 days before each event. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain a forward-looking trading catalyst calendar, add or scan high-impact events, and flag pre-positioning windows for affected assets. It supports human review of market catalysts and should not be used to automate trades without oversight. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect or stale catalyst entries could mislead trading analysis. <br>
Mitigation: Verify event sources and review proposed calendar additions before saving them. <br>
Risk: Downstream trading tools could overreact to pre-positioning signals. <br>
Mitigation: Keep trading decisions under human review and do not allow automated trade execution from these entries alone. <br>
Risk: The skill updates a local trading calendar file. <br>
Mitigation: Install only when an agent-maintained file under ~/.openclaw/workspace/trading/ is expected, and inspect changes to catalyst-calendar.json. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-catalyst-calendar) <br>
- [Publisher profile](https://clawhub.ai/user/Zero2Ai-hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell or cron-style commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates a local JSON catalyst calendar when the agent follows the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
