## Description: <br>
Monitors websites for content changes, compares page snapshots with diffs, schedules periodic checks, and sends alerts through email or webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and site owners use this skill to monitor public web pages, compare stored snapshots, schedule recurring checks, and receive change notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package creates persistent local state containing monitored URLs, snapshots, and configuration. <br>
Mitigation: Use it for non-sensitive pages unless the local data directory is protected, and avoid storing secrets or sensitive webhook URLs. <br>
Risk: The scheduling feature can install cron jobs that keep checking URLs after setup. <br>
Mitigation: Inspect any cron entry before keeping it and remove stale entries when monitoring is no longer needed. <br>
Risk: The release contains duplicate root and nested skill artifacts with different behavior. <br>
Mitigation: Prefer the root script for the website monitor workflow or remove the stale nested skill and script before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain3/site-change-alert) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces stdout status messages, diffs, snapshot history, notification setup details, and local state files.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
