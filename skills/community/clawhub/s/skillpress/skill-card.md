## Description:

SkillPress analyzes repeatable workflows from conversations or tasks and generates standard SKILL.md templates and script skeletons for reusable agent skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxr-666](https://clawhub.ai/user/lxr-666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use SkillPress to turn completed repeatable workflows into reusable agent skills by generating SKILL.md templates and starter script structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Path-like skill names can cause the helper script to write or read SKILL.md files outside the intended skills folder.

Mitigation: Use simple slug names containing only lowercase letters, numbers, and hyphens; avoid slashes, dots, '..', and absolute paths until strict slug validation and resolved-path containment checks are added.

Risk: The skill creates persistent local files when generating skill skeletons.

Mitigation: Run it in a controlled workspace and review generated files before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and Python-generated files with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent local skill files under the configured OpenClaw work directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
