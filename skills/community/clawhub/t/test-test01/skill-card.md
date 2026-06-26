## Description: <br>
从test页面获取数据导入到test01。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shandongwill](https://clawhub.ai/user/shandongwill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and automation developers use this skill to move tabular data from a PCS page into an EBP system by exporting Excel data and uploading it to the target application. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated scheduled imports can duplicate, overwrite, or move data into the wrong target if source and target URLs, selectors, or idempotency behavior are not verified. <br>
Mitigation: Review before installing or operationalizing, test in a non-production environment, verify source and target URLs, confirm duplicate-import prevention, and enable cron only after rollback and idempotency behavior are clear. <br>
Risk: Browser automation for internal systems may expose operational credentials or perform actions with broader permissions than intended. <br>
Mitigation: Use least-privilege credentials, require logs or audit records, and keep secrets out of skill files and command history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shandongwill/test-test01) <br>
- [Publisher profile](https://clawhub.ai/user/shandongwill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces automation instructions for Playwright-based page access, Excel export, upload, and optional cron scheduling.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
