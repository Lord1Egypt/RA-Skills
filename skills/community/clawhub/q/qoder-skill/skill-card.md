## Description: <br>
Integrates Alibaba Cloud Qoder so agents can request code generation, refactoring, documentation, test generation, code review, and SPEC-driven development through Qoder commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frisky1985](https://clawhub.ai/user/frisky1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to route coding tasks to Qoder, including generating code, refactoring files, producing documentation, creating tests, analyzing codebases, and working from specifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Qoder can access selected project files and send prompts, code, paths, or directory context to an external AI service. <br>
Mitigation: Use it only in approved workspaces, avoid secrets or private business data unless authorized, and review the selected files and prompts before running Qoder. <br>
Risk: The integration requires API credentials and may rely on a local ~/.qoder configuration file. <br>
Mitigation: Use a scoped API key, protect local Qoder configuration files, and rotate credentials if exposure is suspected. <br>
Risk: Generated or refactored code may be incorrect, insecure, or unsuitable for the target project. <br>
Mitigation: Review, test, and scan all generated or modified files before committing or deploying them. <br>


## Reference(s): <br>
- [Qoder official documentation](https://help.aliyun.com/product/qoder) <br>
- [Qoder usage examples](references/examples.md) <br>
- [Qoder configuration reference](references/qoder_config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated or refactored code, documentation, tests, reports, and configuration-dependent outputs through Qoder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
