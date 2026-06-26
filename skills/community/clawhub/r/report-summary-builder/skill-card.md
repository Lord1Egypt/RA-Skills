## Description: <br>
基于已有日报自动汇总生成周报和月报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bounding-elk](https://clawhub.ai/user/bounding-elk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and team leads use this skill to turn existing daily Markdown work reports into weekly or monthly summaries. It aggregates completed work, progress, blockers, next plans, and source periods without inventing missing work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated summaries may be incomplete if expected daily report files are missing. <br>
Mitigation: Review generated summaries before sharing them and preserve the skill's required missing-data notice when daily records are incomplete. <br>
Risk: Optional scheduled report generation can create reports automatically at configured times. <br>
Mitigation: Enable the Cron examples only when scheduled automatic report creation is intended. <br>
Risk: The skill reads from and writes to fixed report paths. <br>
Mitigation: Install only when /data/reports/daily/ is the intended source for daily reports and the weekly and monthly output folders are appropriate. <br>


## Reference(s): <br>
- [Report Summary Builder on ClawHub](https://clawhub.ai/bounding-elk/report-summary-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown report files plus a concise user-facing summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads daily reports from /data/reports/daily/ and saves weekly or monthly reports to fixed report folders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
