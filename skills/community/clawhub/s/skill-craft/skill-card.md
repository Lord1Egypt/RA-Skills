## Description:

Create, optimize, or update AgentSkills with evidence-based design across trigger precision, context efficiency, structure, step decomposition, positive constraints, examples, verification, freedom calibration, and progressive loading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonardo-lb](https://clawhub.ai/user/leonardo-lb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create new AgentSkills, optimize existing skills, validate skill structure, and package skill folders for release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaging script can include files outside the intended skill folder through symlinks.

Mitigation: Use the packaging script only on trusted skill folders, inspect generated archives before sharing, and remove or reject symlinks until packaging verifies that every archived file resolves inside the skill directory.

## Reference(s):

- [Skill Craft release page](https://clawhub.ai/leonardo-lb/skills/skill-craft)
- [Evidence Database for Skill Optimization](references/evidence-database.md)
- [Skill Optimization Guide](references/skill-optimization.md)
- [Skill Taxonomy](references/skill-taxonomy.md)
- [State Machine Patterns](references/state-machine-patterns.md)
- [Source Code Agent](https://arxiv.org/abs/2508.02721)
- [Compiled AI](https://arxiv.org/abs/2604.05150)
- [LLM Output Drift](https://arxiv.org/abs/2511.07585)
- [Know When To Stop](https://aclanthology.org/2024.naacl-long.202/)
- [LangGraph](https://github.com/langchain-ai/langgraph)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with optional Python-generated files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce SKILL.md content, resource folder structure, validation feedback, and .skill archives when the bundled scripts are run.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata, released 2026-04-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
