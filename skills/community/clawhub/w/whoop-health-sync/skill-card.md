## Description: <br>
Syncs WHOOP recovery, sleep, strain, workout, and profile data into local Markdown files so an agent can produce health summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aikong-cmd](https://clawhub.ai/user/aikong-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users connect their own WHOOP developer app and let an agent sync wearable metrics into Markdown files for daily briefings, weekly summaries, and health-data questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release bundles a populated WHOOP OAuth token file that may expose access to personal health data. <br>
Mitigation: Delete data/tokens.json before use, revoke or rotate any exposed WHOOP tokens, and authorize only with credentials from your own WHOOP app. <br>
Risk: The skill uses long-lived offline access to sensitive WHOOP health metrics. <br>
Mitigation: Install only in trusted workspaces, keep client credentials private, and review generated health files before sharing them with any agent or service. <br>
Risk: Daily background sync can store sensitive health data in the OpenClaw workspace. <br>
Mitigation: Enable scheduled sync only when local health-data storage is acceptable, restrict filesystem access, and remove generated reports when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aikong-cmd/whoop-health-sync) <br>
- [WHOOP Developer Dashboard](https://developer-dashboard.whoop.com/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown health reports and command-line instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily files named health/whoop-YYYY-MM-DD.md and optional weekly summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
