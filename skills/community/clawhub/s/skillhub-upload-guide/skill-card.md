## Description: <br>
Provides a Chinese-language guide for preparing separated release and runtime packages, uploading skills to SkillHub.cn through web or CLI workflows, and checking for credential and path exposure before publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawhub-master](https://clawhub.ai/user/clawhub-master) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this guide to prepare SkillHub.cn release packages, publish them through the web dashboard or CLI, and run a pre-publication checklist that reduces API key and local path leakage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The published guidance includes a real-looking IMA ClientID and API key, creating a credential exposure risk. <br>
Mitigation: Rotate or revoke the exposed credential, replace credential values with placeholders or environment-variable examples, and avoid running the IMA snippets unless the operator owns that account and intends to create or modify those notes. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/clawhub-master/skills/skillhub-upload-guide) <br>
- [Publisher profile](https://clawhub.ai/user/clawhub-master) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell, JavaScript, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language operational guidance with checklists and example commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
