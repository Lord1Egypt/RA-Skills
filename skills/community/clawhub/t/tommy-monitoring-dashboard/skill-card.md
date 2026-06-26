## Description: <br>
Zero-token real-time Discord monitoring dashboard for OpenClaw. Displays system health, cron jobs, sessions, and performance analytics via persistent Discord messages updated every 2 minutes with no LLM token cost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keylimesoda](https://clawhub.ai/user/keylimesoda) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw activity, cron jobs, sessions, system health, and performance trends through live Discord dashboard messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard can send local system and OpenClaw activity data to configured Discord destinations. <br>
Mitigation: Replace all hardcoded Discord user, channel, and message IDs; confirm the target destination and telemetry content before enabling scheduled updates. <br>
Risk: A direct Discord REST variant can read a local Discord bot token for API writes. <br>
Mitigation: Avoid the direct token-reading REST script unless that path is intentionally required, and keep Discord bot tokens out of repository artifacts. <br>
Risk: Continuous cron-based updates can keep publishing monitoring data until the job is disabled. <br>
Mitigation: Test updates manually first and confirm how to disable the OpenClaw cron job before enabling continuous monitoring. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/keylimesoda/tommy-monitoring-dashboard) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown dashboard content, shell commands, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Discord dashboard updates and local performance data; requires configured OpenClaw and Discord message destinations.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
