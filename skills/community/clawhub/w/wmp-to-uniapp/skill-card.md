## Description: <br>
Convert native WeChat Mini Program projects into uni-app + Vue3 + TypeScript cross-platform projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert native WeChat Mini Program source trees into runnable uni-app projects using Vue 3 and TypeScript. It supports project analysis, configuration migration, page and component conversion, utility migration, and final verification guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write a converted project to disk, so choosing an existing target directory may overwrite or mix generated files with existing work. <br>
Mitigation: Use a fresh output directory unless the user explicitly intends to modify an existing project. <br>
Risk: Generated code and migrated dependencies may require review before they are installed, built, or shipped. <br>
Mitigation: Review generated code and dependencies before running npm install, build commands, or deploying the converted project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/wmp-to-uniapp) <br>
- [WeChat Mini Program to uni-app mapping reference](references/mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, generated project files, configuration files, and verification checklist items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a new uni-app project directory from an inspected Mini Program source tree.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
