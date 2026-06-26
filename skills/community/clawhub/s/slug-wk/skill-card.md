## Description: <br>
Guide for creating effective skills, including new skill creation and updates to existing skills with specialized workflows, references, scripts, and other bundled resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangkang5](https://clawhub.ai/user/wangkang5) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and skill authors use this skill to design, initialize, validate, package, and iterate on agent skills. It provides guidance for concise skill instructions, progressive disclosure, bundled resources, and reusable workflow patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts create, validate, and package files in skill directories, so running them against the wrong folder can produce unintended files or packages. <br>
Mitigation: Run helper scripts only against the intended working folder and review generated or modified files before packaging. <br>
Risk: Packaged skill archives can include unrelated local files or secrets if they are present inside the selected skill directory. <br>
Mitigation: Remove secrets and unrelated local files from the skill directory before packaging or sharing a .skill archive. <br>


## Reference(s): <br>
- [Workflow Patterns](references/workflows.md) <br>
- [Output Patterns](references/output-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/wangkang5/slug-wk) <br>
- [Publisher profile](https://clawhub.ai/user/wangkang5) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional generated or packaged files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use bundled Python helper scripts to initialize, validate, or package skill directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
