## Description: <br>
Triggers publishing for existing local skills when requested, without creating new skill files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhoulincom](https://clawhub.ai/user/zhoulincom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers who maintain local ClawHub skills use this skill to trigger single-skill or batch publishing for existing skills and receive publish results or troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can directly publish one or many local skills, including batch publishing when no skill name is specified. <br>
Mitigation: Before use, confirm the exact skill name, destination registry or account, changed files, version, and whether batch mode is intended. <br>
Risk: Ambiguous upload requests may trigger live publishing rather than a dry run. <br>
Mitigation: Avoid vague requests such as "模拟上传" unless live publishing is intended; require an explicit publish target when possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhoulincom/simulated-upload-helper) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown or plain text with shell commands and publish status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish a named skill or run batch publishing when no skill name is specified.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
