## Description: <br>
Track and analyze cycling performance from Strava, including ride data, fitness trends, workout performance, and automatic monitoring of new rides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EricRosenberg](https://clawhub.ai/user/EricRosenberg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Cyclists and coaching workflows use this skill to fetch Strava virtual ride data, analyze power, heart-rate zones, personal records, training load, and recent fitness trends, and optionally monitor for new rides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Strava client credentials and OAuth tokens in ~/.config/strava/config.json. <br>
Mitigation: Use the skill only on trusted machines, keep the config file restricted to the local user, and revoke the Strava application if access is no longer needed. <br>
Risk: Optional monitoring can run repeatedly from cron and analyze new rides on a schedule. <br>
Mitigation: Review the cron entry before enabling automation, keep monitoring optional, and remove the entry when stopping use of the skill. <br>
Risk: Local cache and log files under ~/.cache/strava can contain activity details. <br>
Mitigation: Avoid shared machines for this skill or clear the cache and logs when the local activity history should not persist. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/EricRosenberg/strava-cycling-coach) <br>
- [Strava API Reference](artifact/references/api.md) <br>
- [Strava API Documentation](https://developers.strava.com/docs/reference/) <br>
- [Strava API Application Settings](https://www.strava.com/settings/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text or Markdown ride analysis, optional JSON summaries, and shell commands for setup and monitoring.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use Strava activity/profile data, local Strava configuration, local activity cache/log files, and an optional Telegram chat ID for notifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
