## Description: <br>
Proactive self-monitoring of infrastructure, services, and health that tracks disk, memory, load, service health, cron job status, and recent errors, then suggests or performs remediation actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suryast](https://clawhub.ai/user/suryast) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and infrastructure maintainers use Self Monitor during heartbeats or scheduled checks to inspect system health, service status, cron activity, and recent errors and to produce a health report with recommended or automated remediation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic cleanup guidance can delete system logs or user cache files without clear approval or retention safeguards. <br>
Mitigation: Disable or edit auto-fix cleanup before scheduling the skill, require explicit confirmation before deletion, and review log-retention and troubleshooting requirements before touching /var/log. <br>
Risk: Automatic service restart guidance can disrupt running workloads if applied without operator review. <br>
Mitigation: Require explicit confirmation before restarting services and scope restart commands to known services with an approved recovery plan. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with shell command snippets and cron examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local system metrics, service status, and remediation guidance based on command output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact SKILL.md frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
