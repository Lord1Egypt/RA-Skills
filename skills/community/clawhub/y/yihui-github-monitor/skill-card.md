## Description: <br>
Monitor multiple GitHub repositories with configurable alert policies for releases, PRs, and security, sending low-noise notifications via scheduled cron jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1yihui](https://clawhub.ai/user/1yihui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and teams use this skill to configure recurring monitoring for one or more GitHub repositories, route release, security, and PR changes by severity, and receive concise alerts or daily digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository monitoring can produce noisy or misdirected alerts if the repository list, policy mode, interval, or notification target is configured incorrectly. <br>
Mitigation: Review the repository list, cron interval, policy mode, notification target, and digest behavior before enabling recurring checks. <br>
Risk: Local monitoring state can cause missed or repeated alerts if it is shared with other workflows, reset unexpectedly, or not scoped to this skill. <br>
Mitigation: Keep the state file isolated to this skill and retain enough auditability to reset or review notification cursors when needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, markdown] <br>
**Output Format:** [Markdown impact summaries and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to concise impact-first summaries, with event-level details only on request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
