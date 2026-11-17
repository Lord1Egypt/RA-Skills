## Description:

Creates a customized learning-project skill with SKILL.md and references that guides a learner from planning through study, review, and completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[balancegsr](https://clawhub.ai/user/balancegsr)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and learners use this skill to turn a learning goal into an installable project skill that plans modules, guides learning sessions, records progress, supports reviews, and closes with a summary or cognitive framework.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and install new skill files and package them with shell commands.

Mitigation: Review before installing and use it only in workspaces where creating learning-project files and new skill directories is acceptable.

Risk: Unusual or adversarial topic names could affect generated file paths.

Mitigation: Prefer simple alphanumeric topic names and inspect generated paths before direct installation or ZIP packaging.

Risk: Direct installation can write multiple files into the current workspace.

Mitigation: Confirm the exact write targets before installation and review generated skill files before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/balancegsr/skills/skill-creator-learning)
- [Strategy extension notes](references/strategies/README.md)
- [Lite learning skill template](references/templates/skill/lite.md)
- [Full learning skill template](references/templates/skill/full.md)
- [Module review guide](references/templates/guides/review_guide.md)
- [Cognitive framework guide](references/templates/guides/framework_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files with inline code blocks, file paths, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an installable learning-project skill with supporting references and project files such as learning plans, notes, module summaries, project summaries, and feedback records.]

## Skill Version(s):

1.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
