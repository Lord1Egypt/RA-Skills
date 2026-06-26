## Description: <br>
Create new skills, modify and improve existing skills, and measure skill performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[limoxt](https://clawhub.ai/user/limoxt) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and skill authors use this skill to draft, revise, evaluate, benchmark, validate, and package agent skills. It supports iterative skill creation workflows from initial intent capture through testing and release preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or modified skill instructions could introduce incorrect, misleading, or overly broad agent behavior. <br>
Mitigation: Review and scan generated or changed SKILL.md files before enabling or distributing them. <br>
Risk: Evaluation prompts, workspaces, or packaged folders could accidentally include sensitive information. <br>
Mitigation: Use a dedicated workspace and avoid placing secrets in eval prompts, skill folders, or packaged artifacts. <br>
Risk: Local evaluation or helper scripts may execute commands as part of skill testing and packaging workflows. <br>
Mitigation: Verify external local scripts before allowing an agent to run them. <br>


## Reference(s): <br>
- [Skill Creator on ClawHub](https://clawhub.ai/limoxt/rex-skill-creator) <br>
- [Output Patterns](references/output-patterns.md) <br>
- [Workflow Patterns](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, JSON evaluation files, shell commands, and generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify skill directories, evaluation artifacts, review HTML, packaged skill archives, and validation outputs when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
