## Description: <br>
从test页面获取数据导入到test01 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shandongwill](https://clawhub.ai/user/shandongwill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations users and automation maintainers can use this skill to transfer table data from a PCS page into an EBP system through an Excel export and upload workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The automation can import transferred data into another system if a user implements or runs the referenced script. <br>
Mitigation: Verify target URLs, inspect the generated Excel file before import, test outside production first, and use least-privilege accounts. <br>
Risk: Repeated scheduled runs may duplicate or overwrite business data if the import workflow is not idempotent. <br>
Mitigation: Enable cron only after confirming repeated imports are safe and monitored. <br>
Risk: Page structure or selector changes can cause the automation to capture or submit incorrect data. <br>
Mitigation: Review and update selectors when source or target pages change, then validate the workflow before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shandongwill/test-test1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides browser automation, Excel export, and Excel upload/import behavior.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
