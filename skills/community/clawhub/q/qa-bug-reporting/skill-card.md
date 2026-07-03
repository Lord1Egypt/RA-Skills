## Description: <br>
Helps QA teams write or improve Chinese-language bug reports with clear reproduction steps, expected and actual results, attachments, root-cause hypotheses, and impact assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, testers, and product teams use this skill to turn observed defects into complete bug reports that developers can reproduce and triage. It is especially useful when a report was rejected as incomplete or when a team wants a consistent bug-reporting structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad report-format or attachment requests, producing QA bug-report guidance when the user intended a different report type. <br>
Mitigation: Use it for defect reporting workflows and review the generated report structure before filing it in an issue tracker. <br>
Risk: Bug evidence can include sensitive information in logs, screenshots, network captures, HAR files, or other attachments. <br>
Mitigation: Sanitize credentials, tokens, personal data, and internal-only details before adding attachments or sharing the report. <br>
Risk: The skill is written for Chinese-language QA workflows, which may make the output less usable for teams that require another language. <br>
Mitigation: Translate or adapt generated reports before using them in non-Chinese workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kokxi/skills/qa-bug-reporting) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown bug report template and checklist guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include severity, priority, reproduction steps, expected versus actual results, attachment guidance, root-cause hypotheses, and impact assessment.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
