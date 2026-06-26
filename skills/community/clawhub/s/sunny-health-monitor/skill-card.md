## Description: <br>
Lightweight system health monitoring for macOS - monitor CPU, memory, disk usage, cron job status, and generate health reports with Discord notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor macOS system health, OpenClaw cron job status, and resource thresholds, then generate status reports and operational guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send local system metrics, OpenClaw cron status, and failed job names to a hardcoded Discord webhook by default. <br>
Mitigation: Replace or remove the embedded webhook before installation; set SYSTEM_HEALTH_WEBHOOK only to an approved destination and confirm the report contents are acceptable to share. <br>
Risk: Hardcoded /Users/xufan65 paths may fail on other machines or read and write an unexpected local profile if that path exists. <br>
Mitigation: Change the status and cron job paths to explicit local paths for the target environment before running the monitor. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunnyhot/sunny-health-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/sunnyhot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON status files, shell command examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can post health reports to Discord when a webhook is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
