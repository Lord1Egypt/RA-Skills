## Description: <br>
Summarizes conversations into professional PowerPoint or WPS presentations, with local generation and optional Feishu upload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwumit](https://clawhub.ai/user/wwumit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to turn conversations, meetings, and discussion notes into .pptx presentations for reporting or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External Feishu sharing can upload conversation content when configured or enabled. <br>
Mitigation: Use local-only mode first, keep Feishu disabled unless upload is intended, and verify the destination before sharing. <br>
Risk: Credential-handling behavior may expose Feishu app secrets if they are stored in plaintext configuration. <br>
Mitigation: Provide Feishu credentials only for trusted apps, prefer environment variables or a secret manager, and avoid storing secrets in plaintext config files. <br>
Risk: Under-scoped messaging can make network and credential behavior less clear to users. <br>
Mitigation: Review the code and security docs before installation, run the included verification scripts, and start with local-only operation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wwumit/sum2slides-lite) <br>
- [README](artifact/README.md) <br>
- [User Guide](artifact/docs/USER_GUIDE.md) <br>
- [Security Guide](artifact/docs/SECURITY_GUIDE.md) <br>
- [Permissions](artifact/docs/PERMISSIONS.md) <br>
- [Platform Compatibility](artifact/docs/PLATFORM_COMPATIBILITY.md) <br>
- [Environment Variable Clarification](artifact/ENV_VAR_CLARIFICATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Configuration instructions, Guidance] <br>
**Output Format:** [PPTX files with status text, local file paths, and optional Feishu share URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local .pptx generation is the default posture; Feishu upload requires user-provided credentials and network access.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release metadata and VERSION.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
