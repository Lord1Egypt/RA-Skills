## Description: <br>
Automates functional testing for web systems with agent-browser CLI and generates standardized Word (.docx) test reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superchao9](https://clawhub.ai/user/superchao9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and release reviewers use this skill to walk through web application modules, exercise CRUD and workflow paths, capture screenshots, and produce a structured functional test report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use login credentials while testing authenticated web systems. <br>
Mitigation: Use disposable low-privilege test accounts and avoid sharing credentials in generated reports. <br>
Risk: The skill can create, modify, delete, submit, or export application data during functional testing. <br>
Mitigation: Run it only on systems you are authorized to test, preferably staging or test environments, and confirm destructive or workflow-changing actions before execution. <br>
Risk: Screenshots and reports may capture sensitive application data. <br>
Mitigation: Review generated screenshots and Word reports, remove passwords and sensitive data, and share reports only with authorized recipients. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superchao9/web-test-reporter) <br>
- [Report format reference](references/report-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and a Python report-generation template for Word .docx output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces screenshot naming conventions, test execution notes, defect summaries, and a python-docx report template.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
