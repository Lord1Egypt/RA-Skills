## Description: <br>
Create, validate, and publish OpenClaw Skills through conversation, including guided and expert workflows for generating SKILL.md files, validating metadata, and preparing ClawHub releases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to create new OpenClaw skills, validate skill metadata and security patterns, apply safe fixes, and prepare publishing commands for ClawHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SKILL.md content or auto-fix changes may introduce incorrect metadata, dependencies, or publishing guidance. <br>
Mitigation: Review generated content and any auto-fix changes before accepting them, then run validation and security scanning before publishing. <br>
Risk: ClawHub login tokens can be exposed through shared terminals, logs, screenshots, or shell history. <br>
Mitigation: Use trusted authentication flows and avoid pasting real ClawHub tokens into shared or recorded environments. <br>
Risk: Publishing workflows depend on a trusted ClawHub CLI installation. <br>
Mitigation: Install the ClawHub CLI from a trusted source and verify the tool before using it for release operations. <br>


## Reference(s): <br>
- [Skill Studio on ClawHub](https://clawhub.ai/ToBeWin/skill-studio) <br>
- [Publishing to ClawHub Guide](references/publish-guide.md) <br>
- [Validation Rules Reference](references/validation-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose SKILL.md content, validation results, metadata fixes, dependency checks, and ClawHub publishing commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
