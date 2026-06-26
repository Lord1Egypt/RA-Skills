## Description: <br>
Provides scheduled progress reports for long-running tasks, with concise chat summaries and detailed Markdown status reports saved locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheffly](https://clawhub.ai/user/cheffly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor long-running agent tasks such as model training, data processing, crawler jobs, or multi-stage analysis by receiving periodic status updates and a persisted Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Progress reports can persist task details locally, including sensitive operational context if users provide it. <br>
Mitigation: Avoid putting secrets or sensitive operational details into progress fields, and review the report location before enabling long-running reporting. <br>
Risk: Scheduled progress reporting can continue after the task ends if the scheduling mechanism is not cleaned up. <br>
Mitigation: Confirm any scheduled reporting is stopped or removed when the task completes. <br>


## Reference(s): <br>
- [Task Progress Report on ClawHub](https://clawhub.ai/cheffly/task-progress-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise chat status updates and Markdown report files, with optional shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When the helper script is used, reports are written under /root/.openclaw/workspace/reports/progress.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
