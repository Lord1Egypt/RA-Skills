## Description: <br>
Provides a Chinese-language publishing guide for agents preparing and releasing SkillHub.cn skill packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawhub-master](https://clawhub.ai/user/clawhub-master) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill as a publishing checklist and command reference for preparing SkillHub.cn release packages while keeping runtime credentials separate from published files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release exposes real-looking SkillHub and IMA credentials and instructs agents to use them for authenticated publishing and remote note import operations. <br>
Mitigation: Treat the credentials as compromised, rotate them, and replace all secrets with placeholders or secure runtime references before use. <br>
Risk: The publishing and import workflow can upload local file content to external services. <br>
Mitigation: Require explicit user confirmation before publishing a package or uploading local file content, and review the package for secrets before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawhub-master/skills/skillhub-publish-guide) <br>
- [SkillHub registry](https://skill.xfyun.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes publishing steps, package layout guidance, credential handling checks, and verification commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
