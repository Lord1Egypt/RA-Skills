## Description: <br>
Create, edit, improve, or audit AgentSkills. Use when creating a new skill from scratch, restructuring an existing skill, auditing skill quality, or making a skill easier for weaker AI models and agent runtimes to follow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ciklopentan](https://clawhub.ai/user/ciklopentan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to create new AgentSkills, restructure existing skills, audit skill quality, and prepare skill packages for validation and release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify target skill folders and prepare packaging or publishing steps. <br>
Mitigation: Review the target directory, generated files, .clawhubignore contents, version metadata, and publish command before any public release. <br>
Risk: The skill runs bundled Python validators and packagers in the local workspace. <br>
Mitigation: Use it in a trusted workspace and review validator, packaging, and generated archive results before relying on them. <br>


## Reference(s): <br>
- [Authoring Guide](references/authoring-guide.md) <br>
- [Progressive Disclosure](references/progressive-disclosure.md) <br>
- [Workflows](references/workflows.md) <br>
- [Output Patterns](references/output-patterns.md) <br>
- [Weak Model Fallbacks](references/weak-model-fallbacks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses, code edits, shell commands, generated files, and validation or packaging status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify skill files, run bundled Python validators and packagers, and provide publish command details when requested.] <br>

## Skill Version(s): <br>
6.1.2 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
