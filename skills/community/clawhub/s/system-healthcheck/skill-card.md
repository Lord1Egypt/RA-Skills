## Description: <br>
Three-tier system health monitoring (L1/L2/L3) with heartbeat mechanism, zero external dependencies, i18n support, and console output only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lim1202](https://clawhub.ai/user/lim1202) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor local OpenClaw workspaces and host health through L1/L2/L3 checks, heartbeat status, cron setup guidance, and console or JSON reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled monitoring can add cron jobs that run local checks repeatedly. <br>
Mitigation: Review and edit crontab entries and paths before enabling them. <br>
Risk: Daily audit checks local system state such as update status, process counts, and aggregate temp/cache directory sizes. <br>
Mitigation: Run it only where local system telemetry collection is acceptable and keep output logs scoped to the intended workspace. <br>
Risk: Health checks call local utilities such as systemctl, pgrep, lsof, ps, apt-get, and yum, so results vary by OS and permissions. <br>
Mitigation: Validate behavior on the target Linux or macOS host and treat warnings as operational signals rather than automatic remediation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lim1202/system-healthcheck) <br>
- [Publisher profile](https://clawhub.ai/user/lim1202) <br>
- [README](README.md) <br>
- [Installation guide](INSTALL.md) <br>
- [Changelog](CHANGELOG.md) <br>
- [Crontab example](templates/crontab_example.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Console text, JSON status objects, Markdown guidance, and cron/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes indicate pass/fail; quiet mode can suppress healthy output except HEARTBEAT_OK.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and CHANGELOG, released 2026-03-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
