## Description: <br>
Creates production-quality AI skills from ideas or existing workflows through an interview, generation, testing, evaluation, and optimization pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wipal](https://clawhub.ai/user/wipal) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, team leads, prompt engineers, and non-coders use this skill to turn repeatable workflows into structured, testable agent skills for supported AI agent platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can fetch remote code and persistently modify agent configuration or bridge files. <br>
Mitigation: Review install.sh and installed file paths before use; prefer manual, workspace-scoped installation over curl|bash, global installation, or install-all. <br>
Risk: Broad bridge or rule files can cause the skill to activate across projects where it was not intended. <br>
Mitigation: Use the narrowest supported platform scope and review any generated bridge, rule, or instruction file before enabling it. <br>
Risk: Generated skills and bundled scripts may propose shell commands, package changes, or workflow automation with safety impact. <br>
Mitigation: Keep command execution approval enabled, run validation and security checks, and review generated scripts before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Generator listing](https://clawhub.ai/wipal/skill-generator) <br>
- [Publisher profile](https://clawhub.ai/user/wipal) <br>
- [Skill Generator on Unikorn](https://unikorn.vn/p/skillgenerator?ref=embed) <br>
- [Skill writing guide](resources/skill_writing_guide.md) <br>
- [Script integration guide](resources/script_integration.md) <br>
- [Evaluation guide](resources/eval_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and generated skill package files, with optional shell commands and JSON reports from bundled utilities] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate SKILL.md files, examples, resources, scripts, evaluation reports, package archives, and platform-specific export guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
