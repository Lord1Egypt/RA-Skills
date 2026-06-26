## Description: <br>
Monitor cron jobs and background tasks with PulseMon. Check monitor status, create/update/delete monitors, view incidents, and manage alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ramongalego](https://clawhub.ai/user/ramongalego) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and SREs use this skill to manage PulseMon monitors for cron jobs and background tasks, inspect pings and incidents, and send monitor pings from an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The PulseMon API key lets an agent change monitor configuration. <br>
Mitigation: Install only if you are comfortable granting that access, and review update, pause, resume, and delete requests before approving them. <br>
Risk: Ping bodies may be included in PulseMon alert notifications. <br>
Mitigation: Do not put secrets, tokens, or sensitive job output in ping bodies. <br>


## Reference(s): <br>
- [PulseMon ClawHub release](https://clawhub.ai/ramongalego/pulsemon) <br>
- [PulseMon](https://pulsemon.dev) <br>
- [PulseMon API key settings](https://pulsemon.dev/dashboard/settings) <br>
- [PulseMon API base endpoint](https://pulsemon.dev/api/v1) <br>
- [PulseMon ping endpoint pattern](https://pulsemon.dev/api/ping/{slug}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request details and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated monitor management requires PULSEMON_API_KEY; ping calls use the public monitor slug endpoint.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
