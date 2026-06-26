## Description: <br>
Guide for creating effective skills, for use when creating or updating a skill that extends an agent's capabilities with specialized knowledge, workflows, or tool integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[86293073](https://clawhub.ai/user/86293073) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent authors use this skill to plan, create, validate, and package reusable skill directories with SKILL.md, scripts, references, and assets. It helps structure procedural guidance for specialized agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or edited skill instructions can contain incorrect, incomplete, or misleading guidance. <br>
Mitigation: Review generated SKILL.md and bundled resources before packaging or publishing. <br>
Risk: Packaging the wrong folder can include secrets or unrelated private files. <br>
Mitigation: Use the skill only on intended skill workspaces and inspect the folder contents before creating a .skill package. <br>
Risk: File-writing scripts can modify the selected workspace. <br>
Mitigation: Run scripts only against the intended skill directory and review created or changed files before sharing them. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/86293073/skill-creator-0-1-0) <br>
- [Workflow Patterns](references/workflows.md) <br>
- [Output Patterns](references/output-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code blocks and generated skill files when used by an agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update SKILL.md, references, scripts, assets, and .skill packages in the target workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
