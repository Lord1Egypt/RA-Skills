## Description: <br>
Automated report generation for self-reflection and system analysis across daily, weekly, and monthly reports from logs, databases, and system metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikikari](https://clawhub.ai/user/kikikari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate daily, weekly, monthly, and ad-hoc Markdown reports from local databases, logs, memory notes, and system metrics for monitoring, review, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may summarize sensitive logs, databases, memory notes, or system metrics. <br>
Mitigation: Restrict input paths, redact secrets and personal data, and protect the reports directory before enabling report generation. <br>
Risk: Scheduled reports may repeatedly process local operational data without manual review. <br>
Mitigation: Review any report-generation scripts before scheduling them and confirm retention and output settings match local policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kikikari/reports-creator) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with command examples and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces report files under a reports directory and may summarize local logs, databases, memory notes, and system metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
