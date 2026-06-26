## Description: <br>
Handles sensitive content remediation after scanning by redacting detected keywords or PII and password-encrypting files, with optional Feishu and WeCom notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinkai25](https://clawhub.ai/user/qinkai25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security, compliance, document review, and data protection teams use this skill after sensitive-content scanning to redact sensitive values, encrypt files, choose output handling, and optionally send completion notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF redaction may leave sensitive text recoverable or otherwise present in the output. <br>
Mitigation: Independently inspect and test redacted PDFs before sharing them, and avoid relying on PDF redaction for regulated data until the implementation is reviewed. <br>
Risk: Encryption passwords may be sent through Feishu, WeCom, or email notification paths. <br>
Mitigation: Disable password-bearing notifications and share passwords only through a separate approved secret-sharing channel. <br>
Risk: Overwrite or disposal options can replace original files and make mistakes hard to reverse. <br>
Mitigation: Keep backups and prefer writing new redacted or encrypted output files unless overwrite behavior has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qinkai25/sensitive-content-disposal) <br>
- [Publisher profile](https://clawhub.ai/user/qinkai25) <br>
- [README](README.md) <br>
- [User guide](用户操作指南.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, configuration examples, and generated file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create redacted file copies, encrypted .enc files, and optional notification status.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata, artifact CHANGELOG.md, and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
