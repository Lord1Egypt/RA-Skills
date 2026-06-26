## Description: <br>
Organizes screenshot-derived tasks or ideas into tasks, notes, priorities, missing information, archive guidance, and next actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to turn screenshot summaries, context, and deadlines into reviewable task plans. It is suited to inspiration capture, to-do cleanup, and meeting screenshot organization when the user provides the screenshot content or OCR output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshot summaries may include personal or sensitive information. <br>
Mitigation: Redact sensitive screenshots or text before use, and provide only inputs the skill is intended to read. <br>
Risk: Generated task plans may overstate or misread incomplete screenshot context. <br>
Mitigation: Review the draft and fill any missing information before acting on the task list. <br>
Risk: The optional Python helper writes output files when requested. <br>
Mitigation: Write outputs only to user-controlled locations and inspect generated files before sharing or using them downstream. <br>
Risk: The artifact includes a placeholder homepage and dormant audit code that may warrant review. <br>
Mitigation: Review the package source before deployment, while noting that server security evidence found no active malicious behavior in this version. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/screenshot-to-task) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance, Files] <br>
**Output Format:** [Structured Markdown or JSON generated from local input] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write output to a user-controlled file when run with the local Python helper; otherwise produces a reviewable draft directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
