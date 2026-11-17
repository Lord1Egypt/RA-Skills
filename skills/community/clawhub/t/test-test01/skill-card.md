## Description:

从test页面获取数据导入到test01

This skill is ready for commercial/non-commercial use.

## Publisher:

[shandongwill](https://clawhub.ai/user/shandongwill)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or operations teams use this skill to automate transferring table data from a PCS page into an EBP system through an Excel import workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended imports over plaintext HTTP can expose or alter business data without sufficient review.

Mitigation: Use approved HTTPS endpoints or a trusted private network, restrict the source and destination pages, and require dry-run validation or confirmation before import.

Risk: Generated Excel files may contain sensitive data after transfer.

Mitigation: Store generated Excel files only in approved locations and clean them up after use.

Risk: Scheduled automation may continue running after page structure changes or failed imports.

Mitigation: Enable logging and rollback procedures before allowing unattended cron execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shandongwill/skills/test-test01)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide browser automation and Excel file generation when used by an agent.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
