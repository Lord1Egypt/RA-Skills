## Description: <br>
Converts a completed OpenClaw analysis workflow from the current conversation into a user-confirmed recurring report task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackyujun](https://clawhub.ai/user/jackyujun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and data analysts use this skill after completing an analysis to package the exact steps into a recurring daily, weekly, or monthly report task. It helps preserve the confirmed workflow as a self-contained prompt and scheduled command for future replay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The saved recurring task prompt may contain confidential metrics, filters, internal names, thresholds, or business judgments from the original analysis. <br>
Mitigation: Review the generated task configuration and prompt before confirming the schedule, remove sensitive details that should not be stored, and delete or disable tasks when they are no longer needed. <br>
Risk: A recurring report can repeatedly run an incomplete or unintended analysis if the workflow is captured before the user has finished and confirmed the analysis steps. <br>
Mitigation: Create the task only after a completed analysis is present, show the extracted steps for user confirmation, and avoid adding analysis steps that were not performed in the conversation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackyujun/scheduled-report) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured task configuration, a self-contained prompt, and openclaw cron command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve exact query parameters, normalize time ranges to relative NOW() expressions, and require user confirmation before task creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
