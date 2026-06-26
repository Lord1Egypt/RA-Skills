## Description: <br>
Task Auditor audits auto-iterator task quality by scoring execution logs, iteration counts, report length, timestamps, and substantive content, then generates audit reports and low-score alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zenmejiang-commits](https://clawhub.ai/user/zenmejiang-commits) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers or operators who run auto-iterator workflows can use this skill to audit task completion quality, create Markdown audit records, and flag low-quality work for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The auditor writes persistent files under the OpenClaw workspace. <br>
Mitigation: Review the local file-writing behavior before installation and run it only in a controlled workspace where audit reports, alerts, and daily logs are expected. <br>
Risk: The task ID is used in file paths without validation. <br>
Mitigation: Use tightly controlled task IDs made from letters, numbers, dashes, or underscores, and add validation before accepting untrusted task IDs. <br>
Risk: The alert threshold and trigger behavior may create alerts more broadly than expected. <br>
Mitigation: Require opt-in for report or alert creation, narrow trigger phrases, and align the alert threshold with the documented pass criteria before autonomous use. <br>


## Reference(s): <br>
- [Task Auditor ClawHub release page](https://clawhub.ai/zenmejiang-commits/task-auditor) <br>
- [zenmejiang-commits ClawHub publisher profile](https://clawhub.ai/user/zenmejiang-commits) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown files and plain-text status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces audit reports under tasks/audits, alert files under memory, daily audit logs, and pass/fail score output.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, skill.json, skill.yaml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
