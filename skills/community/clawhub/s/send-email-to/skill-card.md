## Description: <br>
发送邮件并支持中文附件（RFC 2231 编码），在用户请求发送邮件、报告或日报时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szrw1825](https://clawhub.ai/user/szrw1825) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or workflow operators use this skill to send generated daily financial market reports with Word and PPT attachments to a configured recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically email local financial report files and the release evidence reports exposed SMTP authorization material. <br>
Mitigation: Rotate or remove the exposed authorization code, verify the sender and recipient configuration, restrict the attachment directory, and require explicit confirmation before sending. <br>
Risk: The workflow is tied to a fixed daily financial-report email use case and configured recipient. <br>
Mitigation: Install only for this intended workflow and review the report date, attachment list, and recipient before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and plain-text email or execution logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send SMTP email with locally discovered Word and PPT attachments based on configured market-report files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
