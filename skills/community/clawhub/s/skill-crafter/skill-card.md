## Description: <br>
Skill Crafter helps agents create, modify, validate, and register high-quality skills using a four-layer skill structure and four-phase workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to turn a requested workflow or domain practice into a reusable agent skill, including scoping, scaffolding, quality checks, and registration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skills may contain incorrect guidance or unsafe operational instructions if registered without review. <br>
Mitigation: Review the generated SKILL.md, references, and scripts before registration, then scan the skill before deployment. <br>
Risk: Generated helper scripts may propose repository cloning, dependency installation, writing outside the workspace, or embedding private conversation details. <br>
Mitigation: Inspect generated scripts and instructions for file-system scope, dependency changes, network use, and private data before use. <br>


## Reference(s): <br>
- [Skill Crafter on ClawHub](https://clawhub.ai/tuobadaidai/skill-crafter) <br>
- [Quality Checklist](references/checklist.md) <br>
- [Complete Example](references/example-complete.md) <br>
- [Four-Layer Structure](references/four-layers.md) <br>
- [Iteration Guide](references/iteration.md) <br>
- [Output Patterns](references/output-patterns.md) <br>
- [Phase Mapping](references/phase-mapping.md) <br>
- [Workflow Patterns](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create SKILL.md, reference files, and helper scripts for a new skill.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
