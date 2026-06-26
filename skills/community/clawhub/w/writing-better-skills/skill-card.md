## Description: <br>
Use when creating or improving a skill for an AI agent, especially when the skill needs strong trigger wording, project-local context, references, scripts, tests, self-healing rules, or a completion gate another agent could follow without guessing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zenchantlive](https://clawhub.ai/user/zenchantlive) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent-skill authors use this skill to create or improve reusable agent skills with clear trigger wording, project-local context, references, scripts, tests, self-healing rules, and completion gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project-local context files may contain incorrect, stale, or overly broad repository instructions. <br>
Mitigation: Review generated or updated project.skill.md content before relying on it, and keep commands, paths, constraints, and completion criteria explicit. <br>
Risk: Local context files may accidentally capture secrets or credential values. <br>
Mitigation: Do not place secrets or credential values in project.skill.md; record only non-sensitive environment variable names when needed. <br>
Risk: Validation scripts or suggested commands can modify local files while skill work is in progress. <br>
Mitigation: Review the proposed command and expected file changes before execution, then inspect the resulting diff before accepting the skill update. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zenchantlive/writing-better-skills) <br>
- [Project Skill Context Template](project.skill.template.md) <br>
- [Behavioral Validation Checklist](references/behavioral-validation-checklist.md) <br>
- [Completion Gate](references/completion-gate.md) <br>
- [Description Writing](references/description-writing.md) <br>
- [Output Patterns](references/output-patterns.md) <br>
- [Project Skill Context](references/project-skill-context.md) <br>
- [Script / Test Conventions](references/script-test-conventions.md) <br>
- [Self-Healing Rules](references/self-healing-rules.md) <br>
- [Skill Architecture Levels](references/skill-architecture-levels.md) <br>
- [Skill Testing](references/skill-testing.md) <br>
- [Workflow Patterns](references/workflows.md) <br>
- [Release Notes Generator Reference Skill](reference-skills/release-notes-generator/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline paths, commands, and optional generated project.skill.md content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project-local context files and propose validation commands while authoring skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, created 2026-03-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
