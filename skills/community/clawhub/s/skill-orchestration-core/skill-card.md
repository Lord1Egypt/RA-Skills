## Description: <br>
Skill Orchestration Core provides Python-based context management, workflow orchestration, and output quality validation for multi-skill projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fish1981bimmer](https://clawhub.ai/user/fish1981bimmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate staged agent-skill workflows, share project context, validate expected outputs, and bootstrap common project workflows from templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validation and auto-fix behavior can read or modify project files selected through workflow design data. <br>
Mitigation: Run it only in trusted, version-controlled worktrees and inspect diffs after validation or auto-fix commands. <br>
Risk: Untrusted DESIGN.md content could steer delegated skills or broad tool access. <br>
Mitigation: Review DESIGN.md before execution and avoid broad toolsets for workflows from untrusted sources. <br>
Risk: Design-controlled expected output paths may escape the intended project area if absolute paths or parent-directory traversal are allowed. <br>
Mitigation: Reject absolute paths and ../ segments in expected_outputs before running validation or repair commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fish1981bimmer/skill-orchestration-core) <br>
- [Publisher Profile](https://clawhub.ai/user/fish1981bimmer) <br>
- [Template Authoring and Recovery](references/template-authoring-and-recovery.md) <br>
- [Workflow Orchestrator Regex Pitfalls](references/workflow-orchestrator-regex-pitfalls.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python API examples, CLI commands, workflow templates, and validation reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or update project files when validation and auto-fix commands are run.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
