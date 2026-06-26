## Description: <br>
瑜伽老师专用学员课时管理系统。使用SQLite本地存储学员信息、课程套餐（包年/包课时）和课时扣除日志，每次扣课后自动发送邮件记录。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yujintang](https://clawhub.ai/user/yujintang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Yoga teachers use this skill to manage student contact records, online and offline course packages, remaining class hours, lesson deductions, and email reports from a local SQLite-backed command-line or Python workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool stores student personal data locally and may include notes in deduction emails or full reports. <br>
Mitigation: Protect the skill directory and database from syncing or sharing, avoid highly sensitive notes, and review report contents before sending. <br>
Risk: The tool stores an SMTP password or app code in local configuration. <br>
Mitigation: Use an app-specific email password, restrict access to the configuration file, and confirm the configured email account before sending records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yujintang/yoga-manage-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local SQLite database and email configuration file when the provided Python tool is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
