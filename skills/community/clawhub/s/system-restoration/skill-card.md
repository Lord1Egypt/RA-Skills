## Description: <br>
Restore Advantage HPE operational intelligence systems when systems are down, alerts are missing, schedules are broken, or data sources fail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephen550](https://clawhub.ai/user/stephen550) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations engineers and maintainers use this skill to investigate and restore Advantage HPE alerting, scheduling, Slack notification, LaunchD, cron, and data-source workflows after failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide users to re-enable persistent automations and change production scripts. <br>
Mitigation: Review proposed script, plist, cron, and service changes before execution, test manually first, and monitor logs and Slack posts after restoration. <br>
Risk: The skill references Slack token locations and production channel IDs. <br>
Mitigation: Confirm Slack token scope, channel IDs, and access controls before using any notification or posting workflow. <br>
Risk: The browser data-source helper can return mock operational records. <br>
Mitigation: Do not use the helper in live reporting until it fetches verified real data or fails closed instead of returning mock data. <br>


## Reference(s): <br>
- [System Restoration skill page](https://clawhub.ai/stephen550/system-restoration) <br>
- [Slack Channel IDs](references/channel-ids.md) <br>
- [LaunchD Service Templates](references/launchd-service-templates.md) <br>
- [System Restoration Troubleshooting Checklist](references/troubleshooting-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, plist snippets, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local LaunchD, cron, Slack, and data-source restoration actions for the described environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
