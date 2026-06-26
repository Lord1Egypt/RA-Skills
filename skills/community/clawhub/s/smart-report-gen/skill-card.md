## Description: <br>
Generates daily, weekly, monthly, project, sprint, incident, and customer reports from local work records such as memory files, logs, Git commits, and user-provided notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wskflf](https://clawhub.ai/user/wskflf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, project leads, and delivery teams use this skill to turn local work history and selected notes into concise status reports for personal tracking, team updates, management reporting, customer updates, sprint summaries, or incident reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can gather local work records, memory files, logs, Git history, and project files that may contain sensitive information. <br>
Mitigation: Specify exact source files, repositories, and date ranges before use, and exclude sensitive repositories or memory logs. <br>
Risk: Generated reports may be prepared for external sharing, including Feishu card formatting, before the user has checked the content. <br>
Mitigation: Review the complete generated report and require explicit confirmation before anything is sent or formatted for Feishu. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wskflf/smart-report-gen) <br>
- [Additional report templates](artifact/references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, Feishu card content, or custom user-supplied report format] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate daily, weekly, monthly, project, sprint, incident, customer, English, or bilingual report variants.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
